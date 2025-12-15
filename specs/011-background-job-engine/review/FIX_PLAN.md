# Master Fix Plan: Background Job Engine (011-background-job-engine)

**Created By:** Director of Engineering / Lead Developer
**Date:** 2025-12-15
**Branch:** `011-background-job-engine`
**Module:** `dartwing_core`

---

## Overview

This document provides a detailed implementation plan for all issues identified in MASTER_REVIEW.md, organized by priority (P1 → P2 → P3) with specific file changes, code fixes, and compliance notes.

**Execution Rule:** Execute P1 fixes first. Wait for approval before proceeding to P2 or P3.

---

## P1: Critical Security & Correctness Issues (8 Tasks)

### Task 1: Fix SQL Injection in Metrics Module

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-001 |
| **Consensus** | 4/4 Unanimous |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/metrics.py` |

**Problem:** Lines 59-66, 83-90, 108-115, 166-173 use f-string interpolation with user-controlled `organization` parameter.

**Plan:** Replace all f-string SQL construction with parameterized queries using `%(param)s` syntax for all four functions:
- `_get_job_count_by_status()`
- `_get_queue_depth_by_priority()`
- `_get_processing_time()`
- `_get_failure_rate_by_type()`

**Compliance Note:** Aligns with PRD C-01 "Complete data isolation between Organizations (no data leakage)" and Architecture Section 8 Security Architecture.

---

### Task 2: Replace Signal-Based Timeout with Thread-Safe Implementation

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-002 |
| **Consensus** | 3/4 (gemi30, sonn45, opus45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/executor.py` |

**Problem:** Lines 148-176 use `signal.SIGALRM` which only works on Unix main thread and can corrupt state.

**Plan:** Replace `_execute_with_timeout()` with `concurrent.futures.ThreadPoolExecutor`:
```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

def _execute_with_timeout(handler: Callable, context: JobContext, timeout_seconds: int) -> Any:
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(handler, context)
        try:
            return future.result(timeout=timeout_seconds)
        except FuturesTimeoutError:
            raise JobTimeoutError(f"Job exceeded {timeout_seconds}s timeout")
```

**Compliance Note:** PRD specifies "iOS, Android, Web, Desktop" support - signal.SIGALRM prevents Windows compatibility. Architecture specifies "Offline-First Mobile Apps" requiring portable background job execution.

---

### Task 3: Fix Incorrect Field Reference in Organization Access Checks

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-003 |
| **Consensus** | 2/4 (GPT52, opus45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py`, `dartwing/dartwing_core/background_jobs/metrics.py` |

**Problem:** Lines 338-341 query `Org Member` with `user` field, but Architecture docs define chain: `User → Person.frappe_user → Org Member.person → Organization`.

**Locations to fix:**
1. `_validate_organization_access()` at line 338
2. `list_jobs()` at line 229
3. `get_metrics()` at line 29 in metrics.py

**Plan:** Query Person first by `frappe_user`, then check Org Member by `person`:
```python
def _validate_organization_access(organization: str):
    if "System Manager" in frappe.get_roles():
        return

    person = frappe.db.get_value("Person", {"frappe_user": frappe.session.user}, "name")
    if not person:
        frappe.throw(_("You don't have access to organization {0}").format(organization), frappe.PermissionError)

    is_member = frappe.db.exists(
        "Org Member",
        {"organization": organization, "person": person, "status": "Active"},
    )
    if not is_member:
        frappe.throw(_("You don't have access to organization {0}").format(organization), frappe.PermissionError)
```

**Compliance Note:** Architecture Section 3.8 defines `Org Member` with `person` Link field (not `user`). Architecture Section 8.2.1 shows permission flow: `User → Org Member → Organization`.

---

### Task 4: Add Database Indexes for Performance

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-004 |
| **Consensus** | 3/4 (GPT52, sonn45, opus45) |
| **Files Affected** | `dartwing/dartwing_core/doctype/background_job/background_job.json` |

**Problem:** Critical query paths lack indexes. Current JSON has no `indexes` array.

**Plan:** Add indexes array to DocType JSON:
```json
"indexes": [
    {"fields": ["job_hash"]},
    {"fields": ["status", "next_retry_at"]},
    {"fields": ["status", "modified"]},
    {"fields": ["organization", "status"]}
]
```

**Compliance Note:** PRD Target Metric "API response time (simple queries) < 200ms" requires indexed queries. The retry scheduler runs every minute per hooks.py line 200.

---

### Task 5: Fix Race Condition in Duplicate Detection

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-005 |
| **Consensus** | 3/4 (GPT52, sonn45, opus45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Problem:** Lines 54-77 have gap between duplicate check and insert where concurrent requests can both pass.

**Plan:** Use try/except with DuplicateEntryError fallback:
```python
def submit_job(...):
    job_hash = generate_job_hash(job_type, organization, parameters or {})

    job = frappe.new_doc("Background Job")
    job.job_hash = job_hash
    # ... set all fields ...

    try:
        job.insert(ignore_permissions=True)
    except frappe.DuplicateEntryError:
        existing = frappe.db.get_value(
            "Background Job",
            {"job_hash": job_hash, "status": ("not in", ["Completed", "Dead Letter", "Canceled"])},
            ["name", "status"],
            as_dict=True
        )
        if existing:
            frappe.throw(_("Duplicate job: {0}").format(existing.name), exc=frappe.DuplicateEntryError)

    _enqueue_job(job)
    return job
```

**Note:** This requires the `job_hash` index from Task 4 to have a unique constraint for non-terminal statuses, OR we rely on the index + retry logic.

**Compliance Note:** PRD C-16 requires "guaranteed execution" - race conditions can cause duplicate job execution violating this.

---

### Task 6: Fix Race Condition in Job Cancellation

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-006 |
| **Consensus** | 2/4 (GPT52, sonn45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Problem:** `cancel_job()` at line 117 lacks locking - job can transition to Running between check and update.

**Plan:** Add `SELECT ... FOR UPDATE` locking:
```python
def cancel_job(job_id: str) -> "frappe.Document":
    # Lock the row to prevent concurrent modification
    frappe.db.sql(
        "SELECT name FROM `tabBackground Job` WHERE name = %s FOR UPDATE",
        (job_id,)
    )

    job = frappe.get_doc("Background Job", job_id)
    _validate_job_access(job, require_write=True)

    if not job.can_cancel():
        frappe.throw(_("Cannot cancel job in status: {0}").format(job.status))

    # ... rest of cancellation logic ...
```

**Compliance Note:** Background Job Isolation Spec requires proper job state management. Race conditions violate the state machine contract.

---

### Task 7: Verify Scheduler Hooks (Already Present - Mark as Verified)

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-007 |
| **Consensus** | 1/4 (sonn45) - Single-point finding |
| **Files Affected** | `dartwing/hooks.py` |

**Finding:** Scheduler events ARE correctly registered at lines 197-208:
```python
scheduler_events = {
    "cron": {
        "* * * * *": [
            "dartwing.dartwing_core.background_jobs.scheduler.process_retry_queue",
            "dartwing.dartwing_core.background_jobs.scheduler.process_dependent_jobs",
        ],
    },
    "daily": [
        "dartwing.dartwing_core.background_jobs.cleanup.daily_cleanup",
    ],
}
```

**Plan:** No change needed. Mark as VERIFIED - scheduler hooks are present.

**Compliance Note:** This aligns with Background Job Isolation Spec which requires scheduled retry processing.

---

### Task 8: Audit State Machine in Cleanup (Already Compliant)

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P1-008 |
| **Consensus** | 2/4 (GPT52, sonn45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/cleanup.py` |

**Finding:** cleanup.py uses `frappe.delete_doc()` which is appropriate for terminal-state jobs (Completed, Dead Letter, Canceled). No state transitions occur - jobs are permanently deleted.

**Plan:** No change needed. Mark as VERIFIED - cleanup properly deletes terminal-state jobs without state machine violations.

**Note:** The cleanup does need batched commits (see P2-005), but the state machine is correct.

---

## P2: Reliability & Correctness Issues (8 Tasks)

### Task 9: Cancel RQ Jobs on Cancellation

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-001 |
| **Consensus** | 2/4 (GPT52, sonn45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Problem:** `cancel_job()` marks DB record but doesn't cancel RQ job.

**Plan:** Add RQ job cancellation after DB update (combined with P1-006 fix):
```python
# After setting job.status = "Canceled"
if hasattr(job, 'rq_job_id') and job.rq_job_id:
    try:
        from frappe.utils.background_jobs import get_queue
        queue_map = {"Critical": "short", "High": "short", "Normal": "default", "Low": "long"}
        queue = get_queue(queue_map.get(job.priority, "default"))
        rq_job = queue.fetch_job(job.rq_job_id)
        if rq_job:
            rq_job.cancel()
    except Exception:
        pass  # RQ job may have already started
```

**Note:** Background Job DocType doesn't have `rq_job_id` field - may need to add it, OR skip this enhancement if we rely on job checking its own status.

**Compliance Note:** PRD C-16 requires "guaranteed execution" - stale RQ jobs violate predictable behavior.

---

### Task 10: Use enqueue_after_commit for Transaction Safety

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-002 |
| **Consensus** | 2/4 (gemi30, sonn45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Problem:** `_enqueue_job()` at line 394 enqueues immediately after insert, risking orphaned RQ jobs if enqueue fails before commit.

**Plan:** Add `enqueue_after_commit=True` to frappe.enqueue call at line 422:
```python
frappe.enqueue(
    "dartwing.dartwing_core.background_jobs.executor.execute_job",
    job_id=job.name,
    queue=queue,
    timeout=job.timeout_seconds or 300,
    is_async=True,
    enqueue_after_commit=True,  # Add this parameter
)
```

**Compliance Note:** Frappe best practice for transaction-safe background job queuing.

---

### Task 11: Fix Duplicate Key in hooks.py

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-003 |
| **Consensus** | 2/4 (opus45, sonn45) |
| **Files Affected** | `dartwing/hooks.py` |

**Problem:** Lines 125-126 and 134-135 have duplicate `"Company"` keys - Python dict silently overwrites.

**Current code:**
```python
permission_query_conditions = {
    "Company": "dartwing.dartwing_company.permissions.get_permission_query_conditions_company",
    "Company": "dartwing.permissions.company.get_permission_query_conditions",  # overwrites
}
```

**Plan:** Remove the duplicate entry, keeping the correct one based on codebase convention. Likely keep the `dartwing.permissions.company` version for consistency with other doctypes.

**Compliance Note:** Architecture Section 8.2.2 requires proper permission hooks for all concrete types.

---

### Task 12: Fix Config 0 Values Treated as Falsy

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-004 |
| **Consensus** | 1/4 (GPT52) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/engine.py` |

**Problem:** Line 70 uses `or` which treats `0` as falsy:
```python
job.priority = priority or job_type_doc.default_priority or "Normal"
```

**Plan:** Use explicit None checks:
```python
job.priority = priority if priority is not None else (job_type_doc.default_priority or "Normal")
job.timeout_seconds = job_type_doc.default_timeout if job_type_doc.default_timeout is not None else 300
job.max_retries = job_type_doc.max_retries if job_type_doc.max_retries is not None else 5
```

**Compliance Note:** Background Job Isolation Spec defines configurable timeouts per queue - `0` may be intentional for "no timeout".

---

### Task 13: Add Batched Commits to Cleanup Job

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-005 |
| **Consensus** | 2/4 (opus45, sonn45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/cleanup.py` |

**Problem:** Lines 35-47 delete in loop but only commit once at end. Long transactions risk lock timeouts.

**Plan:** Add batch commits:
```python
def cleanup_old_jobs(retention_days: int = 30, batch_size: int = 100):
    # ... existing query ...

    deleted_count = 0
    for i, job_id in enumerate(jobs):
        try:
            frappe.delete_doc("Background Job", job_id, force=True, delete_permanently=True)
            deleted_count += 1

            if (i + 1) % batch_size == 0:
                frappe.db.commit()
        except Exception as e:
            frappe.log_error(...)

    if deleted_count % batch_size != 0:
        frappe.db.commit()

    return deleted_count
```

**Compliance Note:** PRD Target Metric requires <200ms API response - long cleanup transactions can block other queries.

---

### Task 14: Progress Update Commit Strategy (Document Only)

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-006 |
| **Consensus** | 1/4 (opus45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/progress.py` |

**Problem:** `update_progress` doesn't commit, so progress may be lost on crash.

**Plan:** Document that progress is "eventually consistent" rather than adding commits (which would slow job execution). Add docstring clarification:
```python
def update_progress(...):
    """
    Update job progress. Note: Progress updates are buffered and may not
    survive job crashes. Use checkpoints for critical state.
    """
```

**Compliance Note:** PRD C-16 requires "progress UI" but doesn't mandate persistence guarantees for progress data.

---

### Task 15: Add Organization Field to Job Execution Log

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-007 |
| **Consensus** | 1/4 (opus45) |
| **Files Affected** | `dartwing/dartwing_core/doctype/job_execution_log/job_execution_log.json` |

**Problem:** Log links to Background Job but not Organization directly, requiring joins for org-filtered queries.

**Plan:** Add organization field with fetch_from:
```json
{
    "fieldname": "organization",
    "fieldtype": "Link",
    "label": "Organization",
    "options": "Organization",
    "fetch_from": "background_job.organization",
    "read_only": 1
}
```

**Compliance Note:** PRD C-01 requires "complete data isolation" - direct org field enables efficient permission filtering.

---

### Task 16: Socket.IO Room Scoping for Permission Validation

| Attribute | Value |
|-----------|-------|
| **Issue ID** | P2-008 |
| **Consensus** | 1/4 (sonn45) |
| **Files Affected** | `dartwing/dartwing_core/background_jobs/progress.py` |

**Problem:** Socket.IO events broadcast without org-scoped room names.

**Plan:** Use organization-scoped rooms:
```python
def _broadcast_progress(job_id: str, organization: str, progress_data: dict):
    room = f"job_progress:{organization}"
    frappe.publish_realtime(
        "job_progress",
        {"job_id": job_id, **progress_data},
        room=room
    )
```

**Compliance Note:** Architecture Section 2.2 specifies "Socket.IO channels scoped to `sync:<doctype>:<org>`".

---

## P3: Quality & Maintainability Improvements (6 Tasks)

| Task | Issue ID | Description | Priority |
|------|----------|-------------|----------|
| 17 | P3-001 | Add handler method import validation in job_type.py | Post-merge |
| 18 | P3-002 | Consider using Frappe Query Builder for metrics.py | Post-merge |
| 19 | P3-003 | Add rate limiting for job submission | Post-merge |
| 20 | P3-004 | Add comprehensive metrics tests | Post-merge |
| 21 | P3-005 | Add API documentation (OpenAPI) | Post-merge |
| 22 | P3-006 | Add performance/load testing | Post-merge |

**Note:** P3 items are deferred to follow-up PRs per MASTER_REVIEW.md guidance.

---

## Summary of High-Impact Decisions

### P1 Critical Fixes Requiring Architectural Changes

| Task | Change Type | Impact |
|------|-------------|--------|
| Task 1 (SQL Injection) | Security fix | All metric queries rewritten |
| Task 2 (SIGALRM) | Platform compatibility | Executor timeout mechanism replaced |
| Task 3 (User field) | Data model alignment | Permission checks rewritten to use Person |
| Task 4 (Indexes) | Schema change | Database migration required |
| Task 5 (Race condition) | Concurrency fix | Submit flow restructured |
| Task 6 (Cancel race) | Concurrency fix | Cancel flow adds locking |

### Judgment Calls / Deviations from MASTER_REVIEW.md

| Issue | MASTER_REVIEW Recommendation | My Decision | Rationale |
|-------|------------------------------|-------------|-----------|
| P1-007 (Scheduler hooks) | "Verification Required" | **VERIFIED - No change needed** | Hooks exist at lines 197-208 |
| P1-008 (State machine) | "Use transition_to method" | **VERIFIED - No change needed** | Cleanup deletes, doesn't transition |
| P2-001 (RQ cancel) | "Cancel RQ job" | **Conditional** | Background Job DocType lacks `rq_job_id` field - skip unless field added |
| P2-006 (Progress commit) | "Commit periodically" | **Document only** | Commits in progress loop would slow execution |

---

## Execution Order

For P1 execution, proceed in this order to minimize conflicts:

1. **Task 4** - Add indexes (schema change, no code conflicts)
2. **Task 1** - Fix SQL injection in metrics.py
3. **Task 3** - Fix user field in engine.py + metrics.py
4. **Task 2** - Replace SIGALRM in executor.py
5. **Task 5** - Fix duplicate detection race in engine.py
6. **Task 6** - Fix cancel race in engine.py
7. **Task 7** - Mark as verified (no change)
8. **Task 8** - Mark as verified (no change)

---

**I have completed the Master Fix Plan. Please review and approve this plan for execution. I will wait for your 'APPROVE' command before moving to Phase 3: Implementation.**
