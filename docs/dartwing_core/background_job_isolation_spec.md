# Background Job Isolation Specification

**Objective:** Define queue strategy and isolation mechanisms to prevent noisy neighbor issues in multi-tenant background job processing.

## Goals

- Prevent one organization from starving others of job processing capacity
- Prioritize critical operations (fax, notifications) over bulk operations
- Provide visibility into job queue health and stuck jobs
- Enable graceful degradation under load

## Problem Statement

In a multi-tenant system, background jobs from one large organization can:

- Consume all worker capacity, blocking other orgs
- Cause timeouts for time-sensitive operations
- Hide failures in a sea of bulk operations
- Make it impossible to debug per-org issues

## Architecture

### Queue Hierarchy

```
┌─────────────────────────────────────────────────────────────────┐
│                    BACKGROUND JOB ISOLATION                      │
│                                                                  │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                    Job Submission                            ││
│  │                                                              ││
│  │  frappe.enqueue() → Route to appropriate queue              ││
│  └──────────────────────────┬──────────────────────────────────┘│
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐       │
│  │  Critical   │     │   Default   │     │    Bulk     │       │
│  │   Queue     │     │    Queue    │     │   Queue     │       │
│  │             │     │             │     │             │       │
│  │ • 4 workers │     │ • 8 workers │     │ • 2 workers │       │
│  │ • 60s timeout│    │ • 300s timeout│   │ • 600s timeout│     │
│  │ • No org limit│   │ • 500/org   │     │ • 100/org   │       │
│  │             │     │             │     │             │       │
│  │ Fax, Notif, │     │ Sync, CRUD, │     │ Import,     │       │
│  │ Auth        │     │ Webhooks    │     │ Reports,    │       │
│  │             │     │             │     │ Exports     │       │
│  └─────────────┘     └─────────────┘     └─────────────┘       │
│         │                   │                   │               │
│         └───────────────────┼───────────────────┘               │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                Dead Letter Queue (DLQ)                       ││
│  │                                                              ││
│  │  • Jobs that fail after max retries                         ││
│  │  • Retained for 7 days for debugging                        ││
│  │  • Alerts when depth > 50                                   ││
│  └─────────────────────────────────────────────────────────────┘│
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Queue Configuration

### Queue Definitions

```python
# dartwing_core/jobs/queue_config.py

QUEUE_CONFIG = {
    "critical": {
        "workers": 4,
        "timeout_seconds": 60,
        "max_jobs_per_org": None,  # No limit for critical
        "retry_count": 3,
        "retry_delay": [10, 30, 60],  # Seconds between retries
        "job_types": [
            "dartwing_fax.send_fax",
            "dartwing_core.notifications.send_notification",
            "dartwing_core.auth.sync_keycloak_session",
            "dartwing_core.integrations.refresh_token",
        ],
    },
    "default": {
        "workers": 8,
        "timeout_seconds": 300,
        "max_jobs_per_org": 500,
        "retry_count": 3,
        "retry_delay": [60, 300, 900],
        "job_types": [
            "dartwing_core.sync.process_delta",
            "dartwing_core.webhooks.dispatch",
            "dartwing_core.email.send",
        ],
    },
    "bulk": {
        "workers": 2,
        "timeout_seconds": 600,
        "max_jobs_per_org": 100,
        "rate_limit_per_minute": 50,
        "retry_count": 2,
        "retry_delay": [300, 900],
        "job_types": [
            "dartwing_core.imports.process_batch",
            "dartwing_core.reports.generate",
            "dartwing_core.exports.full_export",
        ],
    },
}


def get_queue_for_job(job_method: str) -> str:
    """Determine which queue a job should be routed to."""
    for queue_name, config in QUEUE_CONFIG.items():
        if job_method in config.get("job_types", []):
            return queue_name
    return "default"
```

### Dead Letter Queue Configuration

```python
DLQ_CONFIG = {
    "max_retries": 3,  # After this, job goes to DLQ
    "retry_delay_seconds": [60, 300, 900],  # Exponential backoff
    "dlq_retention_days": 7,
    "alert_threshold": 50,  # Alert when DLQ depth exceeds this
}
```

## Implementation

### Job Router Decorator

```python
# dartwing_core/jobs/router.py

import frappe
from frappe.utils import now_datetime
from dartwing_core.jobs.queue_config import QUEUE_CONFIG, get_queue_for_job


def enqueue_with_isolation(
    method: str,
    organization: str = None,
    **kwargs
):
    """
    Enqueue a job with org isolation and queue routing.

    Args:
        method: Dotted path to the job function
        organization: Organization name for isolation
        **kwargs: Arguments to pass to the job
    """
    queue_name = get_queue_for_job(method)
    config = QUEUE_CONFIG.get(queue_name, QUEUE_CONFIG["default"])

    # Check org job limit
    if organization and config.get("max_jobs_per_org"):
        current_count = get_org_job_count(organization, queue_name)
        if current_count >= config["max_jobs_per_org"]:
            frappe.logger().warning(
                f"Org {organization} hit job limit ({config['max_jobs_per_org']}) "
                f"on queue {queue_name}"
            )
            # Queue anyway but log - could optionally reject here
            frappe.publish_realtime(
                "job_limit_warning",
                {"organization": organization, "queue": queue_name},
                user=frappe.session.user
            )

    # Enqueue with metadata
    frappe.enqueue(
        method,
        queue=queue_name,
        timeout=config["timeout_seconds"],
        job_name=f"{method}:{organization or 'system'}:{now_datetime().timestamp()}",
        organization=organization,
        **kwargs
    )


def get_org_job_count(organization: str, queue_name: str) -> int:
    """Count pending/running jobs for an organization in a queue."""
    from frappe.utils.background_jobs import get_queue

    queue = get_queue(queue_name)
    count = 0

    # Count jobs in queue
    for job in queue.jobs:
        if hasattr(job, 'kwargs') and job.kwargs.get('organization') == organization:
            count += 1

    return count
```

### Retry Handler

```python
# dartwing_core/jobs/retry.py

import frappe
from frappe.utils import now_datetime
from dartwing_core.jobs.queue_config import DLQ_CONFIG


def handle_job_failure(job, exception):
    """
    Handle job failure with retry logic and DLQ routing.
    Called from job wrapper or RQ failure handler.
    """
    retry_count = getattr(job, 'retry_count', 0)
    max_retries = DLQ_CONFIG["max_retries"]

    if retry_count < max_retries:
        # Schedule retry with backoff
        delay = DLQ_CONFIG["retry_delay_seconds"][retry_count]

        frappe.logger().warning(
            f"Job {job.id} failed (attempt {retry_count + 1}/{max_retries}), "
            f"retrying in {delay}s: {exception}"
        )

        # Re-enqueue with incremented retry count
        frappe.enqueue(
            job.func_name,
            queue=job.origin,
            timeout=job.timeout,
            at_front=False,
            retry_count=retry_count + 1,
            **job.kwargs
        )
    else:
        # Move to DLQ
        move_to_dlq(job, exception)


def move_to_dlq(job, exception):
    """Move a failed job to the Dead Letter Queue for manual review."""
    frappe.get_doc({
        "doctype": "Background Job DLQ",
        "job_id": job.id,
        "job_method": job.func_name,
        "organization": job.kwargs.get("organization"),
        "queue": job.origin,
        "failure_reason": str(exception)[:2000],
        "job_data": frappe.as_json(job.kwargs),
        "failed_at": now_datetime(),
        "retry_count": getattr(job, 'retry_count', 0),
    }).insert(ignore_permissions=True)

    frappe.logger().error(
        f"Job {job.id} moved to DLQ after {DLQ_CONFIG['max_retries']} retries: {exception}"
    )

    # Check DLQ depth and alert if needed
    check_dlq_alerts()


def check_dlq_alerts():
    """Alert if DLQ depth exceeds threshold."""
    dlq_count = frappe.db.count("Background Job DLQ", {"status": "Pending"})

    if dlq_count >= DLQ_CONFIG["alert_threshold"]:
        frappe.publish_realtime(
            "dlq_alert",
            {"count": dlq_count, "threshold": DLQ_CONFIG["alert_threshold"]},
            user="Administrator"
        )
```

### DLQ Doctype

```json
{
    "doctype": "Background Job DLQ",
    "module": "Dartwing Core",
    "autoname": "hash",
    "fields": [
        {"fieldname": "job_id", "label": "Job ID", "fieldtype": "Data"},
        {"fieldname": "job_method", "label": "Job Method", "fieldtype": "Data"},
        {"fieldname": "organization", "label": "Organization", "fieldtype": "Link", "options": "Organization"},
        {"fieldname": "queue", "label": "Queue", "fieldtype": "Data"},
        {"fieldname": "failure_reason", "label": "Failure Reason", "fieldtype": "Long Text"},
        {"fieldname": "job_data", "label": "Job Data (JSON)", "fieldtype": "Code"},
        {"fieldname": "failed_at", "label": "Failed At", "fieldtype": "Datetime"},
        {"fieldname": "retry_count", "label": "Retry Count", "fieldtype": "Int"},
        {"fieldname": "status", "label": "Status", "fieldtype": "Select", "options": "Pending\nRetried\nResolved\nIgnored", "default": "Pending"},
        {"fieldname": "resolution_notes", "label": "Resolution Notes", "fieldtype": "Small Text"}
    ]
}
```

### Stuck Job Detection

```python
# dartwing_core/jobs/monitoring.py

import frappe
from frappe.utils import now_datetime, add_to_date


def detect_stuck_jobs():
    """
    Scheduled job: Run every 15 minutes.
    Detect and handle jobs that have been running too long.
    """
    from frappe.utils.background_jobs import get_queue

    for queue_name, config in QUEUE_CONFIG.items():
        timeout = config["timeout_seconds"]
        stuck_threshold = add_to_date(
            now_datetime(),
            seconds=-(timeout * 2)  # 2x timeout = definitely stuck
        )

        queue = get_queue(queue_name)

        for job in queue.started_job_registry.get_job_ids():
            job_obj = queue.fetch_job(job)
            if job_obj and job_obj.started_at < stuck_threshold:
                frappe.logger().error(
                    f"Stuck job detected: {job_obj.id} in queue {queue_name}, "
                    f"started at {job_obj.started_at}"
                )

                # Move to DLQ
                move_to_dlq(job_obj, Exception("Job exceeded timeout threshold"))

                # Kill the job
                job_obj.cancel()


def cleanup_old_dlq_entries():
    """
    Scheduled job: Run daily.
    Remove resolved DLQ entries older than retention period.
    """
    retention_days = DLQ_CONFIG["dlq_retention_days"]
    cutoff = add_to_date(now_datetime(), days=-retention_days)

    old_entries = frappe.get_all(
        "Background Job DLQ",
        filters={
            "status": ["in", ["Resolved", "Ignored"]],
            "failed_at": ["<", cutoff]
        },
        pluck="name"
    )

    for name in old_entries:
        frappe.delete_doc("Background Job DLQ", name, ignore_permissions=True)

    if old_entries:
        frappe.logger().info(f"Cleaned up {len(old_entries)} old DLQ entries")
```

## Permission Enforcement

Background jobs run without user session context. To enforce org-scoped permissions:

```python
# dartwing_core/jobs/permissions.py

import frappe
from contextlib import contextmanager


@contextmanager
def org_context(organization: str):
    """
    Context manager to run job code with org-scoped permissions.

    Usage:
        with org_context("ORG-2025-00001"):
            # Code here runs with org permissions applied
            docs = frappe.get_all("Task", filters={"organization": organization})
    """
    # Store original user
    original_user = frappe.session.user

    try:
        # Get org admin user for permission context
        admin_user = get_org_admin_user(organization)
        if admin_user:
            frappe.set_user(admin_user)

        # Add org to context for permission queries
        frappe.flags.current_organization = organization

        yield

    finally:
        # Restore original context
        frappe.set_user(original_user)
        frappe.flags.pop("current_organization", None)


def get_org_admin_user(organization: str) -> str:
    """Get a user with admin access to the organization."""
    admin = frappe.db.get_value(
        "Org Member",
        {"organization": organization, "role": "Admin", "status": "Active"},
        "person"
    )
    if admin:
        return frappe.db.get_value("Person", admin, "frappe_user")
    return None
```

## Hooks Configuration

```python
# dartwing_core/hooks.py

scheduler_events = {
    "cron": {
        # Stuck job detection every 15 minutes
        "*/15 * * * *": [
            "dartwing_core.jobs.monitoring.detect_stuck_jobs"
        ],
        # DLQ cleanup daily at 3am
        "0 3 * * *": [
            "dartwing_core.jobs.monitoring.cleanup_old_dlq_entries"
        ],
    }
}
```

## Observability

### Metrics

| Metric | Type | Labels | Description |
|--------|------|--------|-------------|
| `jobs_enqueued_total` | counter | `queue`, `method`, `org` | Jobs enqueued |
| `jobs_completed_total` | counter | `queue`, `method`, `org`, `status` | Jobs completed (success/failure) |
| `jobs_duration_seconds` | histogram | `queue`, `method` | Job execution duration |
| `queue_depth` | gauge | `queue` | Current jobs in queue |
| `dlq_depth` | gauge | - | Dead letter queue depth |
| `org_job_count` | gauge | `org`, `queue` | Jobs per org per queue |

### Alerts

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Queue backlog | `queue_depth > 1000` for 15m | Warning | Scale workers |
| DLQ growing | `dlq_depth > 50` | Warning | Investigate failures |
| Stuck jobs | Jobs running > 2x timeout | Critical | Auto-kill and DLQ |
| Org rate limit | Org hits job limit | Info | Log only |
| Worker crash | Worker process dies | Critical | Auto-restart |

## Test Matrix

| Scenario | Test Method | Expected Result |
|----------|-------------|-----------------|
| Queue routing | Enqueue fax job | Goes to critical queue |
| Org limit | Enqueue 501 jobs for one org | 501st logs warning |
| Retry success | Job fails once, succeeds on retry | Job completes after retry |
| DLQ routing | Job fails 3 times | Moves to DLQ |
| Stuck detection | Job runs for 2x timeout | Detected and killed |
| Permission isolation | Job accesses other org data | Permission denied |
| Worker scaling | High load on critical queue | Critical jobs still process |

---

*Specification version: 1.0*
*Last updated: November 2025*
