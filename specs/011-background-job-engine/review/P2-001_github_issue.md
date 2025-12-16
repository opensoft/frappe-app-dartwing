# GitHub Issue: Background Job Engine - Implement RQ Job Cancellation (P2-001)

**Copy the content below to create the issue manually at your repo's /issues/new page**

---

## Title
```
Background Job Engine: Implement RQ Job Cancellation (P2-001)
```

## Body

### Summary

The `cancel_job()` function in the Background Job Engine updates the database status to "Canceled" but does **not** actually cancel the RQ worker job. Jobs may continue executing even after cancellation is requested.

### Current Behavior

When a user cancels a job:
1. ✅ Database record updated to `status = "Canceled"`
2. ✅ `canceled_at` and `canceled_by` fields populated
3. ✅ Socket.IO event broadcast to notify clients
4. ❌ RQ job continues running until it checks `is_canceled()` (cooperative cancellation)

### Why This Was Deferred

The Background Job DocType lacks an `rq_job_id` field to track the RQ job ID. Without this field, we cannot look up and cancel the RQ job.

**Architectural Decision:** For MVP, cooperative cancellation via `JobContext.is_canceled()` polling is acceptable. Jobs that frequently call `update_progress()` will detect cancellation at those checkpoints.

**Reference:** `specs/011-background-job-engine/review/FIX_PLAN.md` (Task 9, P2-001)

### Proposed Implementation

#### Step 1: Add `rq_job_id` Field
```json
// background_job.json
{
    "fieldname": "rq_job_id",
    "fieldtype": "Data",
    "label": "RQ Job ID",
    "read_only": 1,
    "hidden": 1,
    "description": "Redis Queue job identifier for cancellation"
}
```

#### Step 2: Capture RQ Job ID on Enqueue
```python
# engine.py - _enqueue_job()
rq_job = frappe.enqueue(
    "dartwing.dartwing_core.background_jobs.executor.execute_job",
    background_job_id=job.name,
    queue=queue,
    timeout=job.timeout_seconds or 300,
    is_async=True,
    enqueue_after_commit=True,
)
job.db_set("rq_job_id", rq_job.id, update_modified=False)
```

#### Step 3: Cancel RQ Job on Cancellation
```python
# engine.py - cancel_job()
if job.rq_job_id:
    try:
        from frappe.utils.background_jobs import get_queue
        queue_map = {"Critical": "short", "High": "short", "Normal": "default", "Low": "long"}
        queue = get_queue(queue_map.get(job.priority, "default"))
        rq_job = queue.fetch_job(job.rq_job_id)
        if rq_job and rq_job.get_status() in ["queued", "deferred"]:
            rq_job.cancel()
    except Exception:
        pass  # RQ job may have already started or completed
```

### Acceptance Criteria

- [ ] `rq_job_id` field added to Background Job DocType
- [ ] RQ job ID captured when job is enqueued
- [ ] `cancel_job()` attempts to cancel RQ job if not yet started
- [ ] Jobs already running continue to use cooperative cancellation (no change)
- [ ] Unit tests cover:
  - Canceling a queued job removes it from RQ
  - Canceling a running job marks DB as canceled (cooperative)
  - Canceling a completed job is a no-op

### Priority

P2 - Medium (reliability improvement, not blocking)

---

*Created from MASTER_REVIEW.md code review consolidation*
*Branch: `011-background-job-engine`*

## Labels
- enhancement
- background-jobs
- technical-debt
