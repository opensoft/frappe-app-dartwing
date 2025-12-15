# Code Review: Background Job Engine (Branch: 011-background-job-engine)

**Reviewer:** sonn45 (Senior Frappe/ERPNext Core Developer)
**Review Date:** December 15, 2025
**Branch:** `011-background-job-engine`
**Confidence Level:** 95%

---

## Feature Summary

**Background Job Engine** - A foundational platform feature providing guaranteed asynchronous task execution for long-running operations (OCR, fax sending, PDF generation, AI tasks). The implementation includes real-time progress tracking, intelligent retry with error classification, multi-tenant isolation, job dependencies, dead letter queue, and operational metrics.

**Files Reviewed:**
- DocTypes: Background Job, Job Type, Job Execution Log
- Python Modules: engine.py, executor.py, retry.py, progress.py, errors.py, scheduler.py, metrics.py
- API Layer: api/jobs.py
- Total Implementation: ~1,700 lines of code

---

## 1. Critical Issues & Blockers (Severity: HIGH)

### 1.1 SQL Injection Vulnerability in Metrics Module

**Location:** `background_jobs/metrics.py` lines 61-77, 84-100, 108-145, 167-190

**Issue:** Multiple SQL injection vulnerabilities exist due to f-string interpolation of user-controllable organization filters directly into SQL queries.

**Example:**
```python
org_filter = f"AND organization = '{filters['organization']}'"  # UNSAFE!
result = frappe.db.sql(f"""
    SELECT status, COUNT(*) as count
    FROM `tabBackground Job`
    WHERE 1=1 {org_filter}
    GROUP BY status
""", as_dict=True)
```

**Why This Is a Blocker:**
This is a **critical security vulnerability**. An attacker could craft a malicious organization name containing SQL injection payloads, potentially:
- Extracting sensitive data from other organizations
- Bypassing multi-tenant isolation
- Modifying or deleting database records
- Escalating privileges

**Fix:**
Use parameterized queries with placeholders instead of string interpolation:

```python
def _get_job_count_by_status(filters: dict) -> dict:
    """Get count of jobs by status."""
    conditions = ["1=1"]
    params = []

    if filters.get("organization"):
        if isinstance(filters["organization"], tuple):
            # Handle IN clause safely
            orgs = filters["organization"][1]
            placeholders = ", ".join(["%s"] * len(orgs))
            conditions.append(f"organization IN ({placeholders})")
            params.extend(orgs)
        else:
            conditions.append("organization = %s")
            params.append(filters["organization"])

    query = f"""
        SELECT status, COUNT(*) as count
        FROM `tabBackground Job`
        WHERE {" AND ".join(conditions)}
        GROUP BY status
    """

    result = frappe.db.sql(query, tuple(params), as_dict=True)
    return {row.status: row.count for row in result}
```

Apply this same fix to:
- `_get_queue_depth_by_priority()` (lines 81-103)
- `_get_processing_time()` (lines 106-161)
- `_get_failure_rate_by_type()` (lines 164-196)

---

### 1.2 Race Condition in Job Status Transitions

**Location:** `background_jobs/engine.py` lines 131-148 (`cancel_job`)

**Issue:** There's a time-of-check to time-of-use (TOCTOU) race condition between checking `job.can_cancel()` and actually updating the status. A job could transition from "Queued" to "Running" between the check and the update.

**Why This Is a Blocker:**
This can cause:
- Jobs marked as "Canceled" that are actually running (data corruption risk)
- Unexpected behavior when handlers check for cancellation
- Audit log inconsistencies

**Fix:**
Use a database-level conditional update with a WHERE clause that validates the current status:

```python
def cancel_job(job_id: str) -> "frappe.Document":
    """Cancel a pending or running job."""
    job = frappe.get_doc("Background Job", job_id)
    _validate_job_access(job, require_write=True)

    if not job.can_cancel():
        frappe.throw(_("Cannot cancel job in status: {0}").format(job.status))

    # Atomic status update with condition
    old_status = job.status
    affected_rows = frappe.db.sql("""
        UPDATE `tabBackground Job`
        SET status = 'Canceled',
            canceled_at = %s,
            canceled_by = %s
        WHERE name = %s
        AND status IN ('Pending', 'Queued', 'Running')
    """, (now_datetime(), frappe.session.user, job_id))

    if affected_rows == 0:
        job.reload()
        frappe.throw(
            _("Cannot cancel job - status changed to: {0}").format(job.status)
        )

    job.reload()  # Refresh to get updated values
    frappe.db.commit()

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status=old_status,
        to_status="Canceled",
    )

    return job
```

---

### 1.3 Missing Scheduler Hooks Configuration

**Location:** Missing from `dartwing_core/hooks.py`

**Issue:** The scheduler functions `process_retry_queue()` and `process_dependent_jobs()` are defined in `background_jobs/scheduler.py` but are not registered in `hooks.py`. This means:
- Failed jobs will never be retried automatically
- Dependent jobs will never be enqueued after parent completion
- The entire retry mechanism is non-functional

**Why This Is a Blocker:**
The Background Job Engine's core promise of "guaranteed execution" cannot be fulfilled without the scheduler. This is a **critical functional gap**.

**Fix:**
Add to `dartwing_core/hooks.py`:

```python
scheduler_events = {
    "cron": {
        # Process retry queue every minute
        "* * * * *": [
            "dartwing.dartwing_core.background_jobs.scheduler.process_retry_queue",
            "dartwing.dartwing_core.background_jobs.scheduler.process_dependent_jobs",
        ]
    }
}
```

**Important:** Frappe cron syntax uses 5 fields: `minute hour day month weekday`. The spec mentions "every minute" which is `* * * * *`.

---

### 1.4 Timeout Implementation Using SIGALRM Is Not Thread-Safe

**Location:** `background_jobs/executor.py` lines 148-175 (`_execute_with_timeout`)

**Issue:** The timeout mechanism uses `signal.SIGALRM`, which:
1. Only works in the main thread (will fail in Frappe's background workers which run in separate threads)
2. Is not portable to Windows
3. Can interfere with other signal handlers in the process

**Why This Is a Blocker:**
This code will raise an exception in production:
```
ValueError: signal only works in main thread of the main interpreter
```

When Frappe's RQ workers execute jobs in separate threads/processes, `signal.signal()` will fail, causing all jobs to crash immediately.

**Fix:**
Use a thread-safe timeout approach with `threading.Timer` or rely on Frappe's built-in timeout mechanism:

```python
import threading

def _execute_with_timeout(handler: Callable, context: JobContext, timeout_seconds: int) -> Any:
    """
    Execute handler with timeout using threading.

    Args:
        handler: Job handler function
        context: JobContext instance
        timeout_seconds: Maximum execution time

    Returns:
        Handler result

    Raises:
        JobTimeoutError: If execution exceeds timeout
    """
    result = [None]  # Mutable container to store result
    exception = [None]  # Mutable container to store exception

    def target():
        try:
            result[0] = handler(context)
        except Exception as e:
            exception[0] = e

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout=timeout_seconds)

    if thread.is_alive():
        # Thread is still running - timeout occurred
        # Note: We can't forcefully kill the thread, but we can mark it as timed out
        # The handler should check context.is_canceled() at checkpoints
        raise JobTimeoutError(f"Job exceeded {timeout_seconds}s timeout")

    if exception[0]:
        raise exception[0]

    return result[0]
```

**Alternative (Recommended):** Since Frappe's `frappe.enqueue()` already supports `timeout` parameter, rely on RQ's built-in timeout and remove the custom implementation:

```python
def execute_job(job_id: str):
    """Execute a background job."""
    # ... existing code ...

    # Simply execute handler - RQ handles timeout
    try:
        result = handler(context)
        _handle_success(job, result)
    except Exception as e:
        # RQ will raise rq.exceptions.JobTimeoutException for timeouts
        if type(e).__name__ == 'JobTimeoutException':
            _handle_timeout(job, JobTimeoutError(str(e)))
        else:
            _handle_failure(job, e)
```

---

### 1.5 Missing Organization Permission Check in `list_jobs`

**Location:** `background_jobs/engine.py` lines 225-243

**Issue:** When a non-admin user provides an `organization` parameter, the code calls `_validate_organization_access(organization)` to check permissions. **However**, this validation only checks if the user is a member of the organization—it does NOT verify that the user actually has permission to view Background Job records for that organization.

**Why This Is a Blocker:**
Frappe's permission system is designed to work through DocType permissions and User Permissions. Simply being an Org Member doesn't automatically grant read access to Background Jobs. A user could be a "Dartwing User" role member of Org A but lack the "read" permission on the Background Job doctype.

**Current Code (Vulnerable):**
```python
elif organization:
    _validate_organization_access(organization)  # Only checks Org Member
    filters["organization"] = organization
```

**Fix:**
Use Frappe's built-in permission checking:

```python
elif organization:
    # Check if user has permission to read Background Jobs for this org
    if not frappe.has_permission("Background Job", "read", user=frappe.session.user):
        frappe.throw(
            _("You don't have permission to view background jobs"),
            frappe.PermissionError
        )
    _validate_organization_access(organization)
    filters["organization"] = organization
```

**Better Approach:** Let Frappe's ORM handle permissions automatically by using `frappe.get_all()` which respects User Permissions:

```python
def list_jobs(
    organization: str = None,
    status: str = None,
    job_type: str = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """List jobs with filtering and pagination."""
    filters = {}

    # Add filters
    if organization:
        filters["organization"] = organization
    if status:
        filters["status"] = status
    if job_type:
        filters["job_type"] = job_type

    # frappe.get_all respects permissions automatically
    jobs = frappe.get_all(
        "Background Job",
        filters=filters,
        fields=["name", "job_type", "status", "progress", "created_at", "organization"],
        order_by="created_at desc",
        start=offset,
        page_length=limit,
        ignore_permissions=False,  # IMPORTANT: respect permissions
    )

    total = frappe.db.count("Background Job", filters)

    return {
        "jobs": [...],
        "total": total,
        "limit": limit,
        "offset": offset,
    }
```

---

### 1.6 Retry Logic Missing in `_retry_job` When Dependency Check Fails

**Location:** `background_jobs/executor.py` lines 92-130 (`_check_dependency`)

**Issue:** When a job's parent dependency is still in progress (not in a terminal state), the function returns `False` to block execution. However, there's **no mechanism to re-enqueue this job later**. The job remains in "Queued" status indefinitely, orphaned.

**Code:**
```python
def _check_dependency(job) -> bool:
    # ...
    if parent_status in ["Failed", "Dead Letter", "Canceled", "Timed Out"]:
        # Parent failed - fail this job too
        # ... marks as Dead Letter
        return False

    # Parent still in progress - re-queue this job
    # The scheduler will pick it up again later
    return False  # ← Job is not re-enqueued!
```

**Why This Is a Blocker:**
Jobs with dependencies will be silently dropped and never execute. The comment says "The scheduler will pick it up again later," but looking at `scheduler.py:process_dependent_jobs()`, it only finds jobs where `parent.status = 'Completed'`. It doesn't re-queue jobs waiting on in-progress parents.

**Fix:**
Modify `_check_dependency` to explicitly re-schedule the job:

```python
def _check_dependency(job) -> bool:
    """
    Check if job dependency is satisfied.

    Returns:
        True if job can proceed, False if blocked
    """
    if not job.depends_on:
        return True

    parent_status = frappe.db.get_value("Background Job", job.depends_on, "status")

    if parent_status == "Completed":
        return True

    if parent_status in ["Failed", "Dead Letter", "Canceled", "Timed Out"]:
        # Parent failed - fail this job too
        job.status = "Dead Letter"
        job.error_message = f"Parent job {job.depends_on} failed with status: {parent_status}"
        job.error_type = "Permanent"
        job.completed_at = now_datetime()
        job.save(ignore_permissions=True)
        frappe.db.commit()

        publish_job_status_changed(
            job_id=job.name,
            organization=job.organization,
            from_status="Queued",
            to_status="Dead Letter",
            error_message=job.error_message,
        )
        return False

    # Parent still in progress - delay this job and re-enqueue after a wait
    # Re-enqueue with a delay (e.g., 30 seconds)
    frappe.enqueue(
        "dartwing.dartwing_core.background_jobs.executor.execute_job",
        job_id=job.name,
        queue="default",
        timeout=job.timeout_seconds or 300,
        enqueue_after_commit=True,
        at_front=False,
        # Delay by 30 seconds
        is_async=True,
    )

    frappe.logger().info(
        f"Job {job.name} waiting for parent {job.depends_on} (status: {parent_status}), "
        f"re-queued for later"
    )

    return False
```

**Note:** Frappe's `frappe.enqueue()` doesn't natively support delayed execution. A better approach is to update `next_retry_at` field and let the scheduler handle it:

```python
# Parent still in progress - delay execution
job.next_retry_at = add_to_date(now_datetime(), seconds=30)
job.save(ignore_permissions=True)
frappe.db.commit()

frappe.logger().info(
    f"Job {job.name} waiting for parent {job.depends_on}, "
    f"will check again at {job.next_retry_at}"
)

return False
```

Then modify `process_dependent_jobs()` scheduler to check `next_retry_at`:

```python
def process_dependent_jobs():
    """Check dependent jobs that may be ready to run."""
    from dartwing.dartwing_core.background_jobs.engine import _enqueue_job

    now = now_datetime()

    jobs = frappe.db.sql("""
        SELECT bj.name, bj.depends_on
        FROM `tabBackground Job` bj
        INNER JOIN `tabBackground Job` parent ON bj.depends_on = parent.name
        WHERE bj.status = 'Queued'
        AND bj.depends_on IS NOT NULL
        AND (bj.next_retry_at IS NULL OR bj.next_retry_at <= %s)
        AND parent.status = 'Completed'
        LIMIT 100
    """, (now,), as_dict=True)

    for job_data in jobs:
        try:
            job = frappe.get_doc("Background Job", job_data.name)
            job.next_retry_at = None
            job.save(ignore_permissions=True)
            _enqueue_job(job)
        except Exception as e:
            frappe.log_error(
                f"Failed to enqueue dependent job {job_data.name}: {e}",
                "Background Job Scheduler",
            )

    if jobs:
        frappe.db.commit()
```

---

### 1.7 Missing Database Index on Critical Query Fields

**Location:** All DocType JSONs (Background Job, Job Execution Log)

**Issue:** The implementation performs frequent queries on fields that lack database indexes:
- `Background Job.status` - queried in scheduler, metrics, list_jobs
- `Background Job.next_retry_at` - queried in retry scheduler
- `Background Job.organization` - queried in permission checks, metrics
- `Background Job.job_hash` - queried for duplicate detection
- `Job Execution Log.background_job` - queried for history lookup

**Why This Is a Blocker:**
Without indexes, these queries will perform **full table scans** as the job count grows. At scale (10,000+ jobs), this will cause:
- Severe performance degradation (queries taking seconds instead of milliseconds)
- Lock contention on the Background Job table
- Scheduler tasks timing out
- API endpoints becoming unresponsive

**Fix:**
Add indexes to `Background Job` DocType JSON:

```json
{
  "doctype": "Background Job",
  // ... existing fields ...
  "fields": [
    // ... existing fields ...
  ],
  "indexes": [
    {
      "fields": ["status", "next_retry_at"],
      "name": "idx_status_next_retry"
    },
    {
      "fields": ["organization", "status"],
      "name": "idx_org_status"
    },
    {
      "fields": ["job_hash", "creation"],
      "name": "idx_hash_creation"
    },
    {
      "fields": ["depends_on", "status"],
      "name": "idx_depends_status"
    }
  ]
}
```

Add index to `Job Execution Log`:

```json
{
  "doctype": "Job Execution Log",
  // ... existing fields ...
  "indexes": [
    {
      "fields": ["background_job", "timestamp"],
      "name": "idx_job_timestamp"
    }
  ]
}
```

**Note:** Frappe DocType JSON supports the `"indexes"` key for composite indexes.

---

### 1.8 Missing Permission Validation in Socket.IO Events

**Location:** `background_jobs/progress.py` lines 96-163

**Issue:** The `publish_job_progress()` and `publish_job_status_changed()` functions broadcast events to rooms scoped by organization (`room=f"org:{organization}"`). However, there's **no validation** that the organization string is safe or that the emitting code has permission to broadcast to that room.

**Why This Is a Blocker:**
An attacker could:
1. Submit a job with a manipulated organization field (e.g., `"org:ORG-2025-99999"`)
2. Receive real-time updates about jobs from other organizations they don't have access to
3. Potentially trigger denial-of-service by flooding rooms with events

**Fix:**
Add validation in the broadcast functions:

```python
def publish_job_progress(
    job_id: str,
    organization: str,
    status: str,
    progress: int,
    progress_message: str = None,
):
    """Publish job progress update via Socket.IO."""
    # Validate organization exists and is not malicious
    if not frappe.db.exists("Organization", organization):
        frappe.logger().warning(
            f"Attempt to publish progress for invalid organization: {organization}"
        )
        return

    # Validate job belongs to this organization (prevent spoofing)
    job_org = frappe.db.get_value("Background Job", job_id, "organization")
    if job_org != organization:
        frappe.logger().error(
            f"Security violation: Job {job_id} belongs to {job_org}, "
            f"not {organization}"
        )
        return

    frappe.publish_realtime(
        event="job_progress",
        message={
            "job_id": job_id,
            "status": status,
            "progress": progress,
            "progress_message": progress_message,
            "updated_at": str(now_datetime()),
        },
        room=f"org:{organization}",
    )
```

Apply the same validation to `publish_job_status_changed()`.

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### 2.1 Improve Error Classification Heuristics

**Location:** `background_jobs/errors.py` lines 60-109 (`classify_error`)

**Current Behavior:**
The error classification uses a "fail-safe" approach where unknown errors default to retryable (`return True`). While this prevents permanent failures from being misclassified, it can cause:
- Infinite retry loops for errors that will never succeed
- Wasted worker capacity
- Delayed detection of code bugs

**Suggestion:**
Add logging and metrics for unknown error types to identify classification gaps:

```python
def classify_error(exception: Exception) -> bool:
    """Classify an exception as retryable or not."""
    # ... existing checks ...

    # Default: retry unknown errors (fail-safe)
    exception_type = type(exception).__name__
    frappe.logger().warning(
        f"Unknown error type encountered: {exception_type} - {str(exception)}. "
        f"Defaulting to retryable. Consider adding explicit classification."
    )

    # Track unknown error types in metrics
    if hasattr(frappe.local, "job_unknown_errors"):
        frappe.local.job_unknown_errors.add(exception_type)
    else:
        frappe.local.job_unknown_errors = {exception_type}

    return True
```

**Additional Suggestion:**
Add more Frappe-specific error patterns:

```python
# Database errors (usually transient - deadlock, connection lost)
transient_db_errors = {
    "QueryDeadlockError",
    "OperationalError",  # Connection errors
    "InterfaceError",
}
if exception_type in transient_db_errors:
    return True

# Frappe rate limiting
if exception_type == "RateLimitExceededError":
    return True
```

---

### 2.2 Add Exponential Backoff Cap

**Location:** `background_jobs/retry.py` lines 12-32 (`calculate_backoff`)

**Current Behavior:**
The exponential backoff grows unbounded: `delay = base_delay * (2 ** (attempt - 1))`. For attempt 5 with base_delay=60, this is 960 seconds (16 minutes). For attempt 10, it would be 30,720 seconds (8.5 hours).

**Issue:**
While the current implementation caps retries at 5 by default (via `max_retries`), if a Job Type is configured with `max_retries=10`, the delays become unreasonably long, delaying failure detection.

**Suggestion:**
Add a maximum backoff cap:

```python
def calculate_backoff(attempt: int, base_delay: int = 60, max_delay: int = 3600) -> int:
    """
    Calculate retry delay with exponential backoff, jitter, and cap.

    Args:
        attempt: Current retry attempt (1-based)
        base_delay: Base delay in seconds (default: 60)
        max_delay: Maximum delay cap in seconds (default: 3600 = 1 hour)

    Returns:
        Delay in seconds with ±20% jitter, capped at max_delay
    """
    delay = base_delay * (2 ** (attempt - 1))
    delay = min(delay, max_delay)  # Cap at max_delay
    jitter = delay * 0.2 * (random.random() * 2 - 1)  # ±20%
    return max(1, int(delay + jitter))
```

---

### 2.3 Improve Duplicate Detection Window Logic

**Location:** `background_jobs/engine.py` lines 376-391 (`_check_duplicate`)

**Current Behavior:**
Duplicate detection uses `creation >= cutoff`, which prevents submitting identical jobs within the window. However, it excludes completed and canceled jobs from the check.

**Issue:**
If a PDF generation job completes in 10 seconds, the user can immediately submit an identical job even if the deduplication window is 300 seconds. This could lead to:
- Unnecessary duplicate processing
- Resource waste
- User confusion (why did two identical jobs run?)

**Suggestion:**
Consider the use case. There are two valid interpretations:

1. **Prevent duplicate submissions regardless of completion** (stricter):
```python
existing = frappe.db.get_value(
    "Background Job",
    {
        "job_hash": job_hash,
        "creation": (">=", cutoff),
        # Remove status filter - check all jobs
    },
    ["name", "status"],
    as_dict=True,
)
```

2. **Allow re-submission after completion** (current behavior is correct)

**Recommendation:** Add a `deduplication_strategy` field to Job Type:
- `"strict"` - prevent duplicates even if completed
- `"loose"` - only prevent duplicates for non-terminal states (current)

---

### 2.4 Add Bulk Job Cleanup Scheduled Task

**Location:** Missing from `background_jobs/cleanup.py` or `scheduler.py`

**Current Behavior:**
Completed jobs are retained indefinitely. The spec (FR-012) states jobs should be "persisted for at least 30 days," but there's no cleanup mechanism.

**Issue:**
Over time, the `Background Job` and `Job Execution Log` tables will grow unbounded, causing:
- Performance degradation
- Disk space exhaustion
- Slow queries even with indexes

**Suggestion:**
Implement a cleanup scheduler (create `background_jobs/cleanup.py`):

```python
"""Cleanup for Background Job Engine."""

import frappe
from frappe.utils import now_datetime, add_to_date


def cleanup_old_jobs():
    """
    Scheduled task: Delete completed jobs older than retention period.

    Run daily to remove jobs in terminal states (Completed, Dead Letter, Canceled)
    older than 30 days.
    """
    retention_days = frappe.db.get_single_value("System Settings", "job_retention_days") or 30
    cutoff = add_to_date(now_datetime(), days=-retention_days)

    # Find old jobs in terminal states
    old_jobs = frappe.db.get_all(
        "Background Job",
        filters={
            "status": ("in", ["Completed", "Canceled"]),
            "completed_at": ("<", cutoff),
        },
        pluck="name",
        limit=1000,  # Process in batches
    )

    for job_name in old_jobs:
        try:
            # Delete job (cascades to Job Execution Log if configured)
            frappe.delete_doc("Background Job", job_name, force=True, ignore_permissions=True)
        except Exception as e:
            frappe.log_error(
                f"Failed to delete old job {job_name}: {e}",
                "Background Job Cleanup",
            )

    if old_jobs:
        frappe.db.commit()
        frappe.logger().info(f"Cleaned up {len(old_jobs)} old background jobs")


def cleanup_dead_letter_queue():
    """
    Scheduled task: Delete resolved DLQ entries older than retention period.

    Keep Dead Letter jobs longer (90 days) for forensic analysis.
    """
    retention_days = 90
    cutoff = add_to_date(now_datetime(), days=-retention_days)

    old_dlq_jobs = frappe.db.get_all(
        "Background Job",
        filters={
            "status": "Dead Letter",
            "completed_at": ("<", cutoff),
        },
        pluck="name",
        limit=500,  # Smaller batch for DLQ
    )

    for job_name in old_dlq_jobs:
        try:
            frappe.delete_doc("Background Job", job_name, force=True, ignore_permissions=True)
        except Exception as e:
            frappe.log_error(
                f"Failed to delete old DLQ job {job_name}: {e}",
                "Background Job Cleanup",
            )

    if old_dlq_jobs:
        frappe.db.commit()
        frappe.logger().info(f"Cleaned up {len(old_dlq_jobs)} old DLQ entries")
```

Add to `hooks.py`:

```python
scheduler_events = {
    "cron": {
        # ... existing scheduler tasks ...
        # Cleanup daily at 2am
        "0 2 * * *": [
            "dartwing.dartwing_core.background_jobs.cleanup.cleanup_old_jobs",
        ],
        # Cleanup DLQ weekly on Sundays at 3am
        "0 3 * * 0": [
            "dartwing.dartwing_core.background_jobs.cleanup.cleanup_dead_letter_queue",
        ]
    }
}
```

---

### 2.5 Improve Progress Update Performance

**Location:** `background_jobs/progress.py` lines 40-75 (`update_progress`)

**Current Behavior:**
Every call to `update_progress()` performs:
1. A database write (`frappe.db.set_value`)
2. A cancellation check (`frappe.db.get_value`)
3. A Socket.IO broadcast

For a job that calls `update_progress()` 100 times, this is 200 database queries + 100 broadcasts.

**Issue:**
High-frequency progress updates can:
- Create database write contention
- Slow down job execution
- Flood Socket.IO with events
- Impact other users' queries

**Suggestion:**
Implement progress update throttling:

```python
from dataclasses import dataclass, field
from typing import Any
import time

@dataclass
class JobContext:
    job_id: str
    job_type: str
    organization: str
    parameters: dict = field(default_factory=dict)
    timeout_seconds: int = 300
    _canceled: bool = field(default=False, repr=False)
    _last_progress_update: float = field(default=0.0, repr=False)  # Timestamp
    _last_progress_value: int = field(default=0, repr=False)

    def update_progress(self, percent: int, message: str = None, force: bool = False):
        """
        Update job progress with throttling.

        Args:
            percent: Progress percentage (0-100)
            message: Optional status message
            force: Skip throttling (useful for final 100% update)
        """
        # Check for cancellation at checkpoint
        if self.is_canceled():
            from dartwing.dartwing_core.background_jobs.errors import PermanentError
            raise PermanentError("Job was canceled")

        percent = max(0, min(100, percent))
        now = time.time()

        # Throttle: Only update if:
        # 1. force=True (e.g., final update)
        # 2. Progress increased by at least 5%
        # 3. At least 2 seconds elapsed since last update
        should_update = (
            force or
            abs(percent - self._last_progress_value) >= 5 or
            (now - self._last_progress_update) >= 2.0
        )

        if not should_update:
            return

        # Update database
        frappe.db.set_value(
            "Background Job",
            self.job_id,
            {"progress": percent, "progress_message": message},
            update_modified=False,
        )

        # Broadcast progress update
        publish_job_progress(
            job_id=self.job_id,
            organization=self.organization,
            status="Running",
            progress=percent,
            progress_message=message,
        )

        # Update throttle state
        self._last_progress_update = now
        self._last_progress_value = percent
```

**Usage in handlers:**
```python
def my_handler(context: JobContext):
    for i, item in enumerate(items):
        process(item)
        context.update_progress(int((i + 1) / len(items) * 100))

    # Force final update to ensure 100% is recorded
    context.update_progress(100, "Completed!", force=True)
```

---

### 2.6 Add Job Cancellation Checkpoint Validation

**Location:** `background_jobs/progress.py` lines 77-93 (`is_canceled`)

**Current Behavior:**
The `is_canceled()` check queries the database on every call. Long-running jobs that check frequently (e.g., in a tight loop processing 10,000 items) will perform 10,000 database queries.

**Suggestion:**
Add a local cache with TTL:

```python
@dataclass
class JobContext:
    # ... existing fields ...
    _canceled: bool = field(default=False, repr=False)
    _last_cancel_check: float = field(default=0.0, repr=False)
    _cancel_check_interval: int = field(default=5, repr=False)  # Check every 5 seconds

    def is_canceled(self) -> bool:
        """
        Check if job has been marked for cancellation.

        Returns:
            True if job should stop, False otherwise
        """
        # If already canceled, return immediately
        if self._canceled:
            return True

        now = time.time()

        # Only check database if interval elapsed
        if (now - self._last_cancel_check) < self._cancel_check_interval:
            return False

        # Check database for cancellation flag
        status = frappe.db.get_value("Background Job", self.job_id, "status")
        self._last_cancel_check = now

        if status == "Canceled":
            self._canceled = True
            return True

        return False
```

This reduces database queries from 10,000 to ~200 for a job that takes 1000 seconds (check every 5 seconds).

---

### 2.7 Improve Job Type Handler Validation

**Location:** `doctype/job_type/job_type.py` lines 19-35 (`validate_handler_method`)

**Current Behavior:**
The validation only checks that the handler path is a valid Python dotted path (e.g., `module.function`). It doesn't verify that the module exists or is importable.

**Issue:**
A Job Type can be created with `handler_method = "nonexistent.module.handler"`, and the error only occurs at **runtime** when a job is executed, causing:
- Confusing error messages for users
- Jobs going to Dead Letter queue for configuration errors
- Difficulty debugging

**Suggestion:**
Add runtime validation to check the handler is importable:

```python
def validate_handler_method(self):
    """Ensure handler method exists and is callable."""
    if not self.handler_method:
        return

    parts = self.handler_method.split(".")
    if len(parts) < 2:
        frappe.throw(
            _("Handler method must be a dotted Python path (e.g., module.function)")
        )

    # Check for valid identifier characters
    for part in parts:
        if not part.isidentifier():
            frappe.throw(
                _("Invalid handler method path: '{0}' is not a valid identifier").format(part)
            )

    # NEW: Validate handler is importable (only in dev/test mode to avoid import overhead)
    if frappe.conf.get("developer_mode"):
        try:
            module_path, func_name = self.handler_method.rsplit(".", 1)
            module = frappe.get_module(module_path)
            handler = getattr(module, func_name)

            if not callable(handler):
                frappe.throw(
                    _("Handler '{0}' is not callable").format(self.handler_method)
                )
        except ImportError as e:
            frappe.throw(
                _("Cannot import handler module '{0}': {1}").format(module_path, str(e))
            )
        except AttributeError:
            frappe.throw(
                _("Handler function '{0}' not found in module '{1}'").format(
                    func_name, module_path
                )
            )
```

---

### 2.8 Add Organization Suspension Check in Job Execution

**Location:** `background_jobs/executor.py` lines 29-65 (`execute_job`)

**Current Behavior:**
The `BackgroundJob.validate()` method checks if an organization is suspended during **creation**, but not during **execution**. If an organization is suspended between job submission and execution, the job will still run.

**Issue:**
This violates the business requirement stated in spec edge cases: "What happens to jobs when an organization is suspended? - Pending jobs for suspended organizations should be paused; running jobs should complete but results should be inaccessible until reactivation."

**Suggestion:**
Add suspension check in executor:

```python
def execute_job(job_id: str):
    """Execute a background job."""
    job = frappe.get_doc("Background Job", job_id)

    # Validate job can be executed
    if job.status not in ["Queued"]:
        frappe.log_error(
            f"Job {job_id} cannot be executed in status {job.status}",
            "Background Job Executor",
        )
        return

    # NEW: Check if organization is suspended
    org_status = frappe.db.get_value("Organization", job.organization, "status")
    if org_status == "Suspended":
        # Pause the job - keep in Queued status and re-check later
        job.next_retry_at = add_to_date(now_datetime(), hours=1)  # Check again in 1 hour
        job.save(ignore_permissions=True)
        frappe.db.commit()

        frappe.logger().info(
            f"Job {job_id} paused due to suspended organization {job.organization}"
        )
        return

    # Check dependency
    if not _check_dependency(job):
        return

    # ... rest of execution ...
```

---

### 2.9 Improve API Parameter Validation

**Location:** `api/jobs.py` lines 12-46 (`submit_job`)

**Current Behavior:**
The API accepts `parameters` as a dict but doesn't validate:
- Size limits (could submit gigabytes of JSON)
- Type safety (could submit non-serializable objects)
- Required parameter keys for specific job types

**Suggestion:**
Add parameter validation:

```python
@frappe.whitelist()
def submit_job(job_type: str, organization: str, parameters: dict = None, priority: str = "Normal", depends_on: str = None):
    """Submit a new background job for execution."""
    from dartwing.dartwing_core.background_jobs import submit_job as engine_submit_job

    # Validate parameters size
    if parameters:
        params_json = frappe.as_json(parameters)
        if len(params_json) > 1_000_000:  # 1MB limit
            frappe.throw(
                _("Job parameters too large (max: 1MB)"),
                frappe.ValidationError
            )

        # Ensure serializable
        try:
            frappe.parse_json(params_json)
        except Exception as e:
            frappe.throw(
                _("Job parameters must be JSON-serializable: {0}").format(str(e)),
                frappe.ValidationError
            )

    job = engine_submit_job(
        job_type=job_type,
        organization=organization,
        parameters=parameters,
        priority=priority,
        depends_on=depends_on,
    )

    return {
        "job_id": job.name,
        "status": job.status,
        "message": "Job submitted successfully",
    }
```

---

### 2.10 Add Dead Letter Queue Management UI Helpers

**Location:** Missing from API layer

**Current Behavior:**
The spec mentions a Dead Letter Queue for failed jobs, and admins can retry jobs via `retry_job()`, but there's no convenient way to:
- List all DLQ jobs
- Bulk retry DLQ jobs for a specific error type
- Mark DLQ jobs as "resolved" or "ignored"

**Suggestion:**
Add DLQ management endpoints to `api/jobs.py`:

```python
@frappe.whitelist()
def list_dead_letter_jobs(organization: str = None, limit: int = 50, offset: int = 0):
    """
    List jobs in dead letter queue.

    Args:
        organization: Filter by org (admin sees all if omitted)
        limit: Page size (default: 50)
        offset: Pagination offset

    Returns:
        dict: {jobs: [...], total, limit, offset}
    """
    # Admin only
    if not frappe.has_permission("Background Job", "write"):
        frappe.throw(_("Admin permission required"), frappe.PermissionError)

    filters = {"status": "Dead Letter"}
    if organization:
        filters["organization"] = organization

    jobs = frappe.get_all(
        "Background Job",
        filters=filters,
        fields=["name", "job_type", "organization", "error_message", "error_type", "failed_at", "retry_count"],
        order_by="completed_at desc",
        start=offset,
        page_length=limit,
    )

    total = frappe.db.count("Background Job", filters)

    return {
        "jobs": jobs,
        "total": total,
        "limit": limit,
        "offset": offset,
    }


@frappe.whitelist()
def bulk_retry_dead_letter(job_ids: list):
    """
    Retry multiple DLQ jobs at once.

    Args:
        job_ids: List of Background Job IDs

    Returns:
        dict: {retried: count, failed: count, errors: [...]}
    """
    from dartwing.dartwing_core.background_jobs.engine import retry_job as engine_retry_job

    # Admin only
    if not frappe.has_permission("Background Job", "write"):
        frappe.throw(_("Admin permission required"), frappe.PermissionError)

    retried = 0
    failed = 0
    errors = []

    for job_id in job_ids:
        try:
            engine_retry_job(job_id)
            retried += 1
        except Exception as e:
            failed += 1
            errors.append({"job_id": job_id, "error": str(e)})

    return {
        "retried": retried,
        "failed": failed,
        "errors": errors,
    }
```

---

## 3. General Feedback & Summary (Severity: LOW)

### 3.1 Code Quality Assessment

**Overall Quality: Good with Critical Gaps**

The Background Job Engine implementation demonstrates solid software engineering fundamentals:

**Strengths:**
- **Clean Architecture:** Clear separation of concerns with dedicated modules (engine, executor, retry, progress, metrics)
- **Well-Designed State Machine:** The status transition validation in `BackgroundJob` controller is excellent and prevents invalid state changes
- **Comprehensive Error Classification:** The `TransientError` / `PermanentError` distinction is a best practice for retry logic
- **Real-Time Updates:** Socket.IO integration for progress tracking shows modern UX thinking
- **Good Documentation:** Docstrings are thorough and follow Google style
- **Multi-Tenancy Awareness:** Organization-scoped isolation is implemented (though with security gaps noted above)

**Areas of Excellence:**
1. The `JobContext` dataclass pattern is elegant and provides a clean API for job handlers
2. The exponential backoff with jitter in `calculate_backoff()` follows industry best practices
3. The state transition logging in `Job Execution Log` provides excellent auditability
4. The metrics module provides good operational visibility

**Critical Gaps (Already Detailed in Section 1):**
While the architecture is sound, the implementation has several **critical security and correctness issues** that must be addressed before production use:
- SQL injection vulnerabilities (1.1)
- Race conditions (1.2)
- Missing scheduler hooks (1.3)
- Thread-unsafe timeout mechanism (1.4)
- Permission enforcement gaps (1.5, 1.8)
- Orphaned dependent jobs (1.6)
- Missing database indexes (1.7)

**Code Readability:** Excellent. Variable names are descriptive, functions are focused and short, and the code flow is easy to follow.

**Frappe Best Practices Adherence:** Mostly good, with some violations:
- ✅ Uses `frappe.whitelist()` for API endpoints
- ✅ Leverages `frappe.enqueue()` for background jobs
- ✅ Uses `frappe.publish_realtime()` for Socket.IO
- ✅ Follows Frappe DocType patterns
- ❌ Raw SQL instead of ORM in metrics module (OK for performance, but introduces SQL injection risk)
- ❌ Doesn't use Frappe's permission query conditions pattern (could simplify permission logic)

---

### 3.2 Positive Reinforcement

Several aspects of this implementation deserve recognition:

1. **Job Hash for Duplicate Detection:** The use of SHA-256 hash in `generate_job_hash()` (engine.py:315-328) is a clean solution for detecting duplicate submissions without complex queries. Well done.

2. **Audit Trail via Job Execution Log:** The automatic logging of all state transitions with timestamps and actors is **excellent** for compliance and debugging. The `_get_transition_message()` method (background_job.py:136-155) provides human-readable descriptions that will be invaluable for operators.

3. **Error Classification Design:** The `errors.py` module is well-thought-out. The heuristic-based classification (HTTP status codes, exception types) combined with explicit `TransientError` / `PermanentError` classes provides both convenience and control.

4. **Progress Throttling Awareness:** The comment in progress.py about throttling shows awareness of performance concerns, even though it's not yet implemented.

5. **Metrics for Operational Visibility:** The metrics module demonstrates understanding that monitoring is not an afterthought—it's essential infrastructure. The P95 calculation (metrics.py:137-156) shows sophistication.

6. **Job Dependencies:** The `depends_on` feature (FR-019) is implemented, which is a complex feature that many similar systems don't support initially. This shows forward-thinking design.

---

### 3.3 Future Technical Debt Items

These are not blockers but should be tracked for future improvement:

1. **Distributed Locking for Deduplication:** The current `job_hash` check has a race condition window between checking and inserting. With high concurrency, duplicate jobs could slip through. Consider using Redis distributed locks or database-level unique constraints.

2. **Job Result Storage:** Currently, `output_reference` is just a string field. For jobs that produce large outputs (e.g., generated files), consider integrating with Feature C-07 (Unified File Storage) to automatically upload results.

3. **Job Prioritization Within Queue:** The current implementation maps priority to Frappe queues (Critical→short, High→short, Normal→default, Low→long). This is coarse-grained. Consider implementing priority queue ordering within each queue.

4. **Progress Estimation:** The current progress tracking requires handlers to manually call `update_progress()`. Consider adding an automatic progress estimator based on historical execution times for the job type.

5. **Job Chaining DSL:** The `depends_on` field supports simple linear dependencies. For complex workflows (Job A completes → run Jobs B and C in parallel → run Job D when both complete), consider a workflow DSL or integration with a workflow engine.

6. **Job Metrics Instrumentation:** The metrics module provides query-based metrics. For real-time operational dashboards, consider instrumenting the executor with Prometheus metrics or StatsD integration.

7. **Job Templates:** Allow Job Types to define parameter schemas (JSON Schema) for validation. This would catch invalid parameters at submission time rather than execution time.

8. **Multi-Region Support:** The current design assumes all jobs execute in one region. For global deployments, consider adding region awareness and locality-based job routing.

---

### 3.4 Documentation Suggestions

The code has good docstrings, but consider adding:

1. **Handler Development Guide:** A markdown file (`docs/background_jobs_handler_guide.md`) with:
   - How to write a job handler
   - Using `JobContext` for progress updates
   - Error handling best practices
   - Testing handlers
   - Example handlers

2. **Operational Runbook:** A guide for operators (`docs/background_jobs_operations.md`):
   - Monitoring dashboard setup
   - How to investigate stuck jobs
   - DLQ management procedures
   - Scaling worker capacity
   - Troubleshooting common issues

3. **Architecture Decision Records (ADRs):** Document key design decisions:
   - Why exponential backoff with jitter?
   - Why separate Job Type from Background Job?
   - Why Socket.IO for progress vs polling?
   - Why default to retry unknown errors?

---

### 3.5 Testing Recommendations

While test files weren't part of this review, the spec mentions testing requirements. Based on the implementation, critical test scenarios should include:

1. **State Machine Tests:**
   - Invalid transitions are rejected
   - Valid transitions work
   - Terminal states prevent further transitions

2. **Error Classification Tests:**
   - Transient errors retry
   - Permanent errors go to DLQ
   - Unknown errors retry (fail-safe)

3. **Concurrency Tests:**
   - Race condition in `cancel_job()` (fixed in 1.2)
   - Duplicate detection under concurrent submission
   - Multiple workers executing different jobs

4. **Security Tests:**
   - SQL injection attempts in metrics queries
   - Permission enforcement (user can't access other org's jobs)
   - Socket.IO room isolation

5. **Integration Tests:**
   - End-to-end job submission → execution → completion
   - Retry flow (transient failure → backoff → success)
   - Job dependencies (parent completes → child executes)
   - Scheduler tasks (retry queue processing, dependent job enqueueing)

6. **Performance Tests:**
   - Metrics queries with 100,000+ jobs
   - Progress update frequency impact
   - Concurrent job submission

---

### 3.6 Alignment with Frappe Low-Code Philosophy

Frappe's strength is rapid low-code development through metadata-driven design. This implementation aligns well:

✅ **DocTypes as Configuration:** Job Type and Background Job use Frappe DocTypes, enabling:
- Automatic REST API generation
- Desk UI for management
- Role-based permissions
- Customization via Custom Fields

✅ **Hooks for Extensibility:** Using `scheduler_events` (once added to hooks.py) follows Frappe patterns.

✅ **Whitelisted Methods:** All API endpoints use `@frappe.whitelist()`, making them accessible from client scripts and integrations.

**Opportunity:** Consider exposing job handlers as Frappe "Server Scripts" to allow no-code job creation. Admins could write simple Python handlers in the UI without deploying code.

---

### 3.7 Comparison to Frappe Built-In Background Jobs

Frappe already has `frappe.enqueue()`. How does this implementation add value?

**Advantages of This Implementation:**
1. **Progress Tracking:** Built-in support for real-time progress updates
2. **Intelligent Retry:** Error classification and exponential backoff
3. **Observability:** Metrics, audit logs, DLQ
4. **Multi-Tenancy:** Organization-scoped isolation
5. **Job Dependencies:** Workflow support
6. **User-Facing:** Background Job DocType is accessible to users, not just developers

**Frappe's Built-In Jobs:**
- Lightweight, no overhead
- Good for internal system tasks
- No built-in retry or monitoring

**Recommendation:** This Background Job Engine should be positioned as the **user-facing job system** for long-running operations that users initiate (PDF generation, OCR, fax sending). Internal system tasks (cache warming, cleanup) should continue using `frappe.enqueue()` directly.

---

### 3.8 Summary Statement

**Overall Assessment:** This is a **solid foundation** with **critical security and correctness issues** that must be fixed before production deployment.

The architecture demonstrates:
- Understanding of distributed systems patterns (retry, backoff, idempotency)
- Awareness of multi-tenancy requirements
- Modern UX thinking (real-time updates)
- Operational maturity (metrics, audit logs)

However, the implementation has:
- **Critical security vulnerabilities** (SQL injection, permission gaps)
- **Functional blockers** (missing scheduler hooks, thread-unsafe timeout)
- **Performance risks** (missing indexes)

**Recommendation:** **HOLD merging** until the 8 critical issues in Section 1 are resolved. Once fixed, this will be production-ready and will serve as excellent infrastructure for Features C-04 (Offline-First), C-10 (Notifications), C-24 (Fax Engine), and C-25 (Scheduler).

**Estimated Effort to Fix Critical Issues:** 2-3 days for an experienced Frappe developer.

**Post-Fix Assessment:** Once critical issues are addressed, this implementation will be of **high quality** and aligned with Frappe best practices.

---

## Appendix: Files Reviewed

| File Path | Lines | Purpose |
|-----------|-------|---------|
| `dartwing_core/doctype/background_job/background_job.json` | 290 | Background Job DocType definition |
| `dartwing_core/doctype/background_job/background_job.py` | 164 | Background Job controller with state machine |
| `dartwing_core/doctype/job_type/job_type.json` | 136 | Job Type DocType definition |
| `dartwing_core/doctype/job_type/job_type.py` | 91 | Job Type controller |
| `dartwing_core/doctype/job_execution_log/job_execution_log.json` | 103 | Job Execution Log DocType |
| `dartwing_core/background_jobs/__init__.py` | 49 | Public API exports |
| `dartwing_core/background_jobs/engine.py` | 429 | Core job submission and management |
| `dartwing_core/background_jobs/executor.py` | 261 | Job execution with timeout handling |
| `dartwing_core/background_jobs/retry.py` | 129 | Retry policy and scheduler |
| `dartwing_core/background_jobs/progress.py` | 163 | Progress tracking and Socket.IO |
| `dartwing_core/background_jobs/errors.py` | 123 | Error classification |
| `dartwing_core/background_jobs/scheduler.py` | 62 | Scheduler task definitions |
| `dartwing_core/background_jobs/metrics.py` | 197 | Operational metrics |
| `dartwing_core/api/jobs.py` | 169 | REST API endpoints |
| **Total** | **~1,700** | **14 files** |

---

**End of Review**
