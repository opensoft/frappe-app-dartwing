# Research: Background Job Engine

**Feature**: 011-background-job-engine
**Date**: 2025-12-15

## Overview

This document captures research findings and technical decisions for the Background Job Engine implementation. All items marked as "NEEDS CLARIFICATION" in the technical context have been resolved.

---

## 1. Frappe Background Jobs Integration

### Decision
Extend Frappe's built-in `frappe.background_jobs` module rather than replace it with a custom solution.

### Rationale
- Frappe 15.x already provides Redis/RQ-based background job infrastructure
- Built-in support for job queuing, worker management, and basic retry
- Integration with Frappe's authentication and permission system
- Documented API: `frappe.enqueue()`, `frappe.enqueue_doc()`

### Alternatives Considered
| Alternative | Rejected Because |
|-------------|------------------|
| Celery | Additional infrastructure complexity; Frappe already has RQ |
| Custom queue from scratch | Unnecessary duplication; Frappe's queue is production-tested |
| Dramatiq | Less mature integration with Frappe ecosystem |

### Implementation Approach
1. Create wrapper layer around `frappe.enqueue()` that adds:
   - Progress tracking callbacks
   - Error classification logic
   - Organization scoping
   - Audit logging
2. Store job metadata in custom `Background Job` doctype (not just Redis)
3. Use Frappe's existing worker infrastructure

---

## 2. Progress Tracking via Socket.IO

### Decision
Use Frappe's built-in Socket.IO integration for real-time progress updates.

### Rationale
- Frappe 15.x includes Socket.IO server (`frappe.realtime`)
- Existing pattern: `frappe.publish_realtime(event, message, room)`
- Room-based scoping supports organization isolation
- Flutter client can connect via `socket_io_client` package

### Implementation Approach
```python
# Progress update pattern
frappe.publish_realtime(
    event="job_progress",
    message={
        "job_id": job.name,
        "progress": 45,
        "status": "Processing page 5 of 11...",
        "step": "ocr_extraction"
    },
    room=f"org:{job.organization}"
)
```

### Room Naming Convention
- `org:{organization_name}` - Organization-scoped job updates
- `job:{job_id}` - Single job detail view
- `admin:jobs` - System-wide admin monitoring

---

## 3. Error Classification Strategy

### Decision
Classify errors into two categories: transient (retryable) and permanent (fail immediately).

### Rationale
- Prevents wasting retries on unrecoverable errors
- Improves user experience by failing fast on validation errors
- Standard pattern in distributed systems (AWS SQS, Azure Service Bus)

### Error Classification Rules

| Error Type | Category | Retry? | Examples |
|------------|----------|--------|----------|
| Network timeout | Transient | Yes | Connection refused, DNS failure |
| Service unavailable | Transient | Yes | HTTP 503, rate limited (429) |
| Resource exhaustion | Transient | Yes | Out of memory (temporary), disk full |
| Validation failure | Permanent | No | Invalid input, schema mismatch |
| Permission denied | Permanent | No | User lacks access, org suspended |
| Not found | Permanent | No | Resource deleted during execution |
| Authentication failure | Permanent | No | Token expired, invalid credentials |

### Implementation Approach
```python
class JobError(Exception):
    """Base class for job errors with retry classification."""
    is_retryable = True

class TransientError(JobError):
    """Errors that may succeed on retry."""
    is_retryable = True

class PermanentError(JobError):
    """Errors that will never succeed - fail immediately."""
    is_retryable = False

# Error classifier function
def classify_error(exception: Exception) -> bool:
    """Returns True if error is retryable."""
    if isinstance(exception, PermanentError):
        return False
    if isinstance(exception, (ConnectionError, TimeoutError)):
        return True
    if hasattr(exception, 'http_status'):
        return exception.http_status in (429, 500, 502, 503, 504)
    return True  # Default to retryable for unknown errors
```

---

## 4. Retry Policy with Exponential Backoff

### Decision
Implement exponential backoff with jitter, configurable per job type.

### Rationale
- Exponential backoff prevents thundering herd on service recovery
- Jitter spreads retry attempts to avoid synchronized retries
- Per-job-type configuration allows tuning for different workloads

### Default Retry Schedule
| Attempt | Base Delay | With Jitter (±20%) |
|---------|------------|-------------------|
| 1 | 1 min | 48s - 72s |
| 2 | 2 min | 96s - 144s |
| 3 | 4 min | 192s - 288s |
| 4 | 8 min | 384s - 576s |
| 5 | 16 min | 768s - 1152s |

### Implementation Approach
```python
import random

def calculate_backoff(attempt: int, base_delay: int = 60) -> int:
    """Calculate retry delay with exponential backoff and jitter."""
    delay = base_delay * (2 ** (attempt - 1))
    jitter = delay * 0.2 * (random.random() * 2 - 1)  # ±20%
    return int(delay + jitter)
```

---

## 5. Multi-Tenant Job Isolation

### Decision
Scope all jobs to Organization using Frappe's User Permission system.

### Rationale
- Consistent with existing Dartwing permission model (C-01, C-17)
- Leverages Frappe's built-in row-level security
- Automatically filters list views for non-admin users

### Implementation Approach
1. `Background Job` doctype has required `organization` Link field
2. Use `user_permission_dependant_doctype: "Organization"` in doctype JSON
3. Permission query hook filters jobs by user's organizations
4. Admin role bypasses organization filter for system-wide view

---

## 6. Dead Letter Queue Implementation

### Decision
Implement dead letter queue as a status on Background Job doctype, not a separate queue.

### Rationale
- Simpler architecture - single doctype for all job states
- Frappe's list filters provide dead letter view (`status = "Failed"`)
- Maintains full job context for debugging
- Admin can retry directly from job record

### Implementation Approach
```python
# Job states include "Dead Letter" as terminal failed state
JOB_STATES = [
    "Pending",      # Created, not yet queued
    "Queued",       # In Redis queue
    "Running",      # Currently executing
    "Completed",    # Success
    "Failed",       # Transient failure, will retry
    "Dead Letter",  # Exhausted retries, needs manual review
    "Canceled",     # User canceled
    "Timed Out"     # Execution exceeded timeout
]
```

---

## 7. Job Dependencies

### Decision
Implement simple parent-child dependency using `depends_on` Link field.

### Rationale
- Covers 90% of use cases (sequential workflows)
- Avoids complexity of full DAG scheduling
- Easy to understand and debug

### Implementation Approach
```python
# Background Job doctype includes:
{
    "fieldname": "depends_on",
    "fieldtype": "Link",
    "options": "Background Job",
    "label": "Depends On (Parent Job)"
}

# Scheduler only picks jobs where:
# - depends_on is null, OR
# - depends_on job status is "Completed"
```

### Limitations (Documented)
- No parallel fan-out/fan-in
- No complex DAG support
- Future enhancement if needed

---

## 8. Operational Metrics

### Decision
Expose metrics via Frappe whitelisted API, consumable by any monitoring system.

### Rationale
- No additional infrastructure (Prometheus, StatsD) required initially
- Frappe's API provides authentication and rate limiting
- Can be polled by external monitoring tools
- Future: Add Prometheus endpoint if needed

### Metrics Exposed
| Metric | Type | Description |
|--------|------|-------------|
| `job_count_by_status` | Gauge | Current jobs in each status |
| `queue_depth_by_priority` | Gauge | Jobs waiting per priority level |
| `job_duration_avg` | Gauge | Average processing time (last hour) |
| `job_duration_p95` | Gauge | 95th percentile processing time |
| `failure_rate_by_type` | Gauge | Failure percentage per job type |

### API Endpoint
```python
@frappe.whitelist()
def get_job_metrics(organization: str = None) -> dict:
    """Returns operational metrics, optionally scoped to organization."""
    # System Manager sees all, others see their org only
```

---

## 9. Duplicate Job Prevention

### Decision
Use content-based hashing to detect duplicate submissions within a configurable window.

### Rationale
- Prevents accidental double-clicks creating duplicate work
- Hash based on: job_type + organization + JSON-serialized parameters
- Configurable window allows tuning per use case

### Implementation Approach
```python
import hashlib
import json

def generate_job_hash(job_type: str, organization: str, params: dict) -> str:
    """Generate unique hash for duplicate detection."""
    content = f"{job_type}:{organization}:{json.dumps(params, sort_keys=True)}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]

# Check for existing job with same hash in last N minutes
existing = frappe.get_all(
    "Background Job",
    filters={
        "job_hash": job_hash,
        "creation": (">", now_minus_window),
        "status": ("not in", ["Completed", "Failed", "Dead Letter", "Canceled"])
    }
)
```

---

## 10. Job Timeout Handling

### Decision
Implement timeout at the job execution level with graceful termination.

### Rationale
- Prevents runaway jobs from consuming resources indefinitely
- Graceful termination allows cleanup (close connections, release locks)
- Timeout jobs can retry if configured

### Implementation Approach
```python
import signal

def execute_with_timeout(job_func, timeout_seconds: int):
    """Execute job function with timeout."""
    def timeout_handler(signum, frame):
        raise TimeoutError(f"Job exceeded {timeout_seconds}s timeout")

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    try:
        return job_func()
    finally:
        signal.alarm(0)  # Cancel alarm
```

### Default Timeouts
| Job Category | Default Timeout |
|--------------|-----------------|
| Standard | 5 minutes |
| Bulk operations | 30 minutes |
| Quick tasks | 1 minute |

---

## Summary

All technical decisions have been made. No "NEEDS CLARIFICATION" items remain. Ready for Phase 1: Design & Contracts.
