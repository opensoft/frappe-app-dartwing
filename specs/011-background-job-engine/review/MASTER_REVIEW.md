# MASTER CODE REVIEW: Background Job Engine (011-background-job-engine)

**Consolidated By:** Director of Engineering
**Date:** 2025-12-15
**Branch:** `011-background-job-engine`
**Module:** `dartwing_core`

---

## Executive Summary

This document synthesizes findings from **4 independent code reviews** into a single, prioritized action plan. The Background Job Engine implementation demonstrates solid architectural foundations but contains **critical security and reliability issues** that must be addressed before production deployment.

### Review Sources

| Reviewer | Focus Areas | Critical Issues Found |
|----------|-------------|----------------------|
| GPT52 | Architecture, State Machine, Permissions | 8 HIGH |
| gemi30 | Thread Safety, Transactions, Serialization | 4 HIGH |
| sonn45 | Security, Race Conditions, Hooks Integration | 8 HIGH |
| opus45 | SQL Injection, Indexes, API Validation | 5 HIGH |

### Consensus Summary

- **Unanimous Agreement (4/4):** SQL injection vulnerability in metrics.py
- **Strong Consensus (3/4):** SIGALRM timeout not portable, missing database indexes, race conditions
- **Majority Agreement (2/4):** Incorrect `user` field in Org Member queries, state machine violations, transaction timing issues

---

## Master Action Plan

### Priority Legend

| Priority | Definition | Timeline |
|----------|------------|----------|
| **P1** | Security vulnerability or data corruption risk - MUST fix before merge | Immediate |
| **P2** | Reliability/correctness issue - Should fix before production | Before release |
| **P3** | Quality/maintainability improvement - Can address in follow-up PR | Post-merge |

---

## P1: Critical Security & Correctness Issues

### P1-001: SQL Injection Vulnerability in Metrics Module

**Consensus:** 4/4 reviewers (UNANIMOUS)
**Files:** [metrics.py:59-76, 81-103, 106-131, 164-196](dartwing/dartwing_core/background_jobs/metrics.py)

**Issue:** All metric functions use f-string interpolation with user-controlled organization parameter, enabling SQL injection attacks that could extract cross-tenant data or perform destructive operations.

**Vulnerable Pattern:**
```python
org_filter = f"AND organization = '{filters['organization']}'"
```

**Required Fix:** Use parameterized queries or Frappe's Query Builder:

```python
def _get_job_count_by_status(filters: dict) -> dict:
    """Get count of jobs by status with parameterized queries."""
    conditions = ["1=1"]
    values = {}

    if filters.get("organization"):
        if isinstance(filters["organization"], tuple):
            conditions.append("organization IN %(orgs)s")
            values["orgs"] = filters["organization"][1]
        else:
            conditions.append("organization = %(org)s")
            values["org"] = filters["organization"]

    result = frappe.db.sql(
        f"""
        SELECT status, COUNT(*) as count
        FROM `tabBackground Job`
        WHERE {" AND ".join(conditions)}
        GROUP BY status
        """,
        values,
        as_dict=True,
    )
    return {row.status: row.count for row in result}
```

**Apply to:** `_get_job_count_by_status`, `_get_average_execution_time`, `_get_failure_rate`, `_get_queue_depth`

---

### P1-002: Signal-Based Timeout Not Portable

**Consensus:** 3/4 reviewers (gemi30, sonn45, opus45)
**File:** [executor.py:148-176](dartwing/dartwing_core/background_jobs/executor.py#L148-L176)

**Issue:** `signal.SIGALRM` has multiple critical limitations:
1. Only works on Unix (Windows crashes)
2. Only works in main thread (RQ workers may use non-main threads)
3. Can corrupt state by interrupting mid-transaction

**Current Code:**
```python
def _execute_with_timeout(handler, context, timeout_seconds):
    def timeout_handler(signum, frame):
        raise JobTimeoutError(f"Job exceeded {timeout_seconds}s timeout")

    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    # ...
```

**Required Fix:** Use thread-based timeout:

```python
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

def _execute_with_timeout(handler: Callable, context: JobContext, timeout_seconds: int) -> Any:
    """Execute handler with portable thread-based timeout."""
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(handler, context)
        try:
            return future.result(timeout=timeout_seconds)
        except FuturesTimeoutError:
            raise JobTimeoutError(f"Job exceeded {timeout_seconds}s timeout")
```

**Alternative Consideration:** Since Frappe's `enqueue()` already accepts a `timeout` parameter, consider whether the custom timeout is redundant or serves as a secondary safeguard.

---

### P1-003: Incorrect Field Reference in Organization Access Checks

**Consensus:** 2/4 reviewers (GPT52, opus45)
**Files:**
- [engine.py:338-341](dartwing/dartwing_core/background_jobs/engine.py#L338-L341) (`_validate_organization_access`)
- [engine.py:229-231](dartwing/dartwing_core/background_jobs/engine.py#L229-L231) (`list_jobs`)

**Issue:** Per the architecture docs, `Org Member` links to `Person` (not `User`), and `Person` links to `User` via `frappe_user` field. The current code queries a non-existent `user` field, causing all non-System Manager access checks to fail.

**Current Broken Code:**
```python
is_member = frappe.db.exists(
    "Org Member",
    {"organization": organization, "user": frappe.session.user, "status": "Active"},
)
```

**Required Fix:**
```python
def _validate_organization_access(organization: str):
    """Validate user has access to organization via Person -> Org Member."""
    if "System Manager" in frappe.get_roles():
        return

    # Find Person linked to current user
    person = frappe.db.get_value("Person", {"frappe_user": frappe.session.user}, "name")
    if not person:
        frappe.throw(
            _("You don't have access to organization {0}").format(organization),
            frappe.PermissionError,
        )

    is_member = frappe.db.exists(
        "Org Member",
        {"organization": organization, "person": person, "status": "Active"},
    )
    if not is_member:
        frappe.throw(
            _("You don't have access to organization {0}").format(organization),
            frappe.PermissionError,
        )
```

**Same fix needed for `list_jobs`:**
```python
def list_jobs(filters=None, ...):
    # ...
    if "System Manager" not in frappe.get_roles():
        person = frappe.db.get_value("Person", {"frappe_user": frappe.session.user}, "name")
        if person:
            orgs = frappe.get_all(
                "Org Member",
                filters={"person": person, "status": "Active"},
                pluck="organization",
            )
        else:
            orgs = []
        # ...
```

---

### P1-004: Missing Database Indexes for Performance

**Consensus:** 3/4 reviewers (GPT52, sonn45, opus45)
**File:** [background_job.json](dartwing/dartwing_core/doctype/background_job/background_job.json)

**Issue:** Critical query paths lack indexes:
- `job_hash` - Duplicate detection (every submission)
- `next_retry_at` - Retry scheduler (runs every minute)
- `(status, next_retry_at)` - Retry queue queries
- `(status, modified)` - Cleanup job queries
- `organization` - Multi-tenant filtering

At 10,000+ jobs, the retry scheduler will cause full table scans every minute.

**Required Fix:** Add to DocType JSON:
```json
{
    "fields": [...],
    "indexes": [
        {"fields": ["job_hash"]},
        {"fields": ["status", "next_retry_at"]},
        {"fields": ["status", "modified"]},
        {"fields": ["organization", "status"]}
    ]
}
```

---

### P1-005: Race Condition in Duplicate Detection

**Consensus:** 3/4 reviewers (GPT52, sonn45, opus45)
**File:** [engine.py:53-62](dartwing/dartwing_core/background_jobs/engine.py#L53-L62)

**Issue:** The duplicate check and job insertion are not atomic:
```python
existing = _check_duplicate(job_hash, ...)  # Check
if existing:
    frappe.throw(...)
# GAP - another request could insert here
job = frappe.new_doc("Background Job")
job.insert()  # Insert
```

Under high concurrency, two identical submissions can both pass the check.

**Required Fix Options:**

**Option A (Recommended):** Database-level unique constraint + exception handling:
```python
def submit_job(...):
    job_hash = generate_job_hash(job_type, organization, parameters or {})

    try:
        job = frappe.new_doc("Background Job")
        job.job_hash = job_hash
        # ... set fields ...
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
```

**Option B:** Use `SELECT ... FOR UPDATE` lock:
```python
frappe.db.sql(
    "SELECT name FROM `tabBackground Job` WHERE job_hash = %s FOR UPDATE",
    (job_hash,)
)
```

---

### P1-006: Race Condition in Job Cancellation

**Consensus:** 2/4 reviewers (GPT52, sonn45)
**File:** [engine.py:cancel_job](dartwing/dartwing_core/background_jobs/engine.py)

**Issue:** Cancellation lacks proper synchronization - job could transition from `Queued` to `Running` between status check and update.

**Required Fix:**
```python
def cancel_job(job_id: str) -> "BackgroundJob":
    """Cancel a job with proper locking."""
    # Lock the row
    frappe.db.sql(
        "SELECT name FROM `tabBackground Job` WHERE name = %s FOR UPDATE",
        (job_id,)
    )

    job = frappe.get_doc("Background Job", job_id)

    if not job.can_cancel():
        frappe.throw(_("Cannot cancel job in status {0}").format(job.status))

    job.status = "Canceled"
    job.canceled_at = now_datetime()
    job.canceled_by = frappe.session.user
    job.save(ignore_permissions=True)

    # Also cancel in RQ if already queued
    if job.rq_job_id:
        try:
            from frappe.utils.background_jobs import get_queue
            rq_job = get_queue(job.queue_name).fetch_job(job.rq_job_id)
            if rq_job:
                rq_job.cancel()
        except Exception:
            pass  # RQ job may have already started

    return job
```

---

### P1-007: Missing Scheduler Hooks in hooks.py

**Consensus:** 1/4 reviewers (sonn45) - **CRITICAL SINGLE-POINT FINDING**
**File:** [hooks.py](dartwing/hooks.py)

**Issue:** The retry scheduler and cleanup job are defined but `scheduler_events` may not be properly registered in hooks.py, meaning jobs will never retry or be cleaned up.

**Verification Required:** Confirm hooks.py contains:
```python
scheduler_events = {
    "cron": {
        "*/1 * * * *": [
            "dartwing.dartwing_core.background_jobs.scheduler.process_retry_queue"
        ],
        "0 2 * * *": [
            "dartwing.dartwing_core.background_jobs.scheduler.cleanup_old_jobs"
        ]
    }
}
```

---

### P1-008: State Machine Violations in Cleanup

**Consensus:** 2/4 reviewers (GPT52, sonn45)
**File:** [cleanup.py](dartwing/dartwing_core/background_jobs/cleanup.py)

**Issue:** Cleanup may directly set status without using proper transition methods, bypassing audit logging.

**Required Fix:** Use the documented `transition_to` method or equivalent:
```python
def cleanup_old_jobs(...):
    for job_id in jobs:
        job = frappe.get_doc("Background Job", job_id)
        # Use proper transition
        job.transition_to("Archived")  # or delete properly
        job.save()
```

---

## P2: Reliability & Correctness Issues

### P2-001: cancel_job Doesn't Actually Cancel RQ Jobs

**Consensus:** 2/4 reviewers (GPT52, sonn45)
**File:** [engine.py:cancel_job](dartwing/dartwing_core/background_jobs/engine.py)

**Issue:** Marking a job as `Canceled` in the database doesn't stop RQ from executing it if already queued.

**Fix:** See P1-006 above (combined fix).

---

### P2-002: Transaction Timing Issues

**Consensus:** 2/4 reviewers (gemi30, sonn45)
**File:** [engine.py:submit_job](dartwing/dartwing_core/background_jobs/engine.py)

**Issue:** The job is committed to database and then immediately enqueued to RQ. If the RQ enqueue fails, the job record shows `Queued` but no RQ job exists.

**Reviewer Conflict:**
- gemi30: Suggests `enqueue_after_commit` to ensure DB commit happens first
- sonn45: Notes same issue but different fix approach

**Resolution:** Use Frappe's `enqueue_after_commit` pattern:
```python
def submit_job(...):
    job.insert(ignore_permissions=True)
    frappe.db.commit()  # Ensure job is persisted

    frappe.enqueue(
        "dartwing.dartwing_core.background_jobs.executor.execute_job",
        job_id=job.name,
        queue=queue_name,
        timeout=job.timeout_seconds,
        enqueue_after_commit=True  # This is key
    )
```

---

### P2-003: Duplicate Key in hooks.py

**Consensus:** 2/4 reviewers (opus45, sonn45)
**File:** [hooks.py:125-127](dartwing/hooks.py#L125-L127)

**Issue:** Python dict with duplicate `"Company"` keys - second entry overwrites first silently.

```python
permission_query_conditions = {
    "Company": "dartwing.dartwing_company.permissions...",  # Overwritten
    "Company": "dartwing.permissions.company...",          # This one wins
}
```

**Fix:** Remove the duplicate entry.

---

### P2-004: Config `0` Values Treated as Falsy

**Consensus:** 1/4 reviewers (GPT52)
**File:** [engine.py](dartwing/dartwing_core/background_jobs/engine.py)

**Issue:** Code like `timeout = timeout or job_type.default_timeout` treats `0` as falsy, ignoring explicit zero values.

**Fix:** Use explicit None checks:
```python
timeout = timeout if timeout is not None else job_type.default_timeout
```

---

### P2-005: Cleanup Job Should Use Batched Commits

**Consensus:** 2/4 reviewers (opus45, sonn45)
**File:** [cleanup.py:35-47](dartwing/dartwing_core/background_jobs/cleanup.py#L35-L47)

**Issue:** Deleting 1000+ jobs in a single transaction can cause lock timeouts and long-running transactions.

**Fix:**
```python
def cleanup_old_jobs(retention_days: int = 30, batch_size: int = 100):
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
```

---

### P2-006: Progress Update Should Commit Changes

**Consensus:** 1/4 reviewers (opus45)
**File:** [progress.py:61-66](dartwing/dartwing_core/background_jobs/progress.py#L61-L66)

**Issue:** `update_progress` uses `frappe.db.set_value` but doesn't commit. If job crashes, last progress update is lost.

**Fix:** Either commit periodically or document that progress is eventually consistent.

---

### P2-007: Job Execution Log Should Link to Organization

**Consensus:** 1/4 reviewers (opus45)
**File:** [job_execution_log.json](dartwing/dartwing_core/doctype/job_execution_log/job_execution_log.json)

**Issue:** Log only links to Background Job, not Organization. Querying logs by org requires a join.

**Fix:** Add `organization` field with `fetch_from`:
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

---

### P2-008: Socket.IO Permission Validation

**Consensus:** 1/4 reviewers (sonn45)
**File:** [progress.py](dartwing/dartwing_core/background_jobs/progress.py)

**Issue:** Socket.IO events are broadcast without validating whether the receiving user has permission to view that job/organization.

**Fix:** Add organization-scoped room names:
```python
def _broadcast_progress(job_id: str, organization: str, progress_data: dict):
    # Room scoped to organization
    room = f"job_progress:{organization}"
    frappe.publish_realtime(
        "job_progress",
        {"job_id": job_id, **progress_data},
        room=room
    )
```

---

## P3: Quality & Maintainability Improvements

### P3-001: Add Handler Method Import Validation

**Consensus:** 1/4 reviewers (opus45)
**File:** [job_type.py:19-35](dartwing/dartwing_core/doctype/job_type/job_type.py#L19-L35)

**Suggestion:** Validate handler_method path exists at save time, not just syntax.

---

### P3-002: Consider Using Frappe's Query Builder

**Consensus:** 1/4 reviewers (opus45)

**Suggestion:** Replace raw SQL with `frappe.qb` for better maintainability.

---

### P3-003: Add Rate Limiting for Job Submission

**Consensus:** 2/4 reviewers (opus45, sonn45)

**Suggestion:** Implement per-organization job limits to prevent queue flooding.

---

### P3-004: Add More Comprehensive Metrics Tests

**Consensus:** 1/4 reviewers (opus45)

**Suggestion:** Current metrics tests only verify empty structure. Add tests with sample data.

---

### P3-005: Add API Documentation

**Consensus:** 1/4 reviewers (opus45)

**Suggestion:** Add OpenAPI/Swagger documentation for job API endpoints.

---

### P3-006: Add Performance/Load Testing

**Consensus:** 2/4 reviewers (opus45, sonn45)

**Suggestion:** Add load tests to validate system under high job submission rates.

---

## Conflict Resolution Log

| Issue | Conflicting Views | Resolution |
|-------|-------------------|------------|
| **Timeout Implementation** | gemi30: Remove SIGALRM entirely; opus45: Use ThreadPoolExecutor; sonn45: Check threading.current_thread() | **Resolution:** Use ThreadPoolExecutor (most portable, cleanest). Consider making optional if Frappe's native timeout suffices. |
| **Transaction Commit Timing** | gemi30: Use enqueue_after_commit; sonn45: Wrap in try/finally | **Resolution:** Use `enqueue_after_commit=True` parameter (Frappe-native pattern). |
| **Job Type Not Found** | gemi30 flagged as HIGH; other reviewers did not mention | **Resolution:** Likely false positive - Job Type lookup is standard Frappe pattern. Verify test coverage exists. |
| **Duplicate Detection Fix** | opus45: Unique constraint + catch DuplicateEntryError; sonn45: FOR UPDATE lock | **Resolution:** Use unique constraint approach (Option A) as it's more performant and doesn't require explicit locks. |

---

## Test Coverage Assessment

Based on the test files reviewed:

| Test File | Coverage Area | Status |
|-----------|---------------|--------|
| `test_job_submission.py` | Submit, defaults, hash, duplicates, dependencies | ✅ Good |
| `test_job_cancellation.py` | Cancel flow, permissions, logging | ✅ Good |
| `test_job_retry.py` | Retry scheduling, backoff, dead letter | ✅ Good |
| `test_job_engine.py` | Hash generation, error classification, backoff math | ✅ Good |
| `test_job_metrics.py` | Metrics structure | ⚠️ Needs sample data tests |
| `test_multi_tenant.py` | (Referenced in review) | ⚠️ Verify exists |

**Gaps Identified:**
1. No tests for concurrent duplicate submission (race condition)
2. No tests for cancellation during execution
3. No tests for SIGALRM/timeout behavior
4. Limited metrics calculation tests

---

## Implementation Order

For developer efficiency, address issues in this order:

### Phase 1: Security (Day 1)
1. P1-001: SQL Injection in metrics.py
2. P1-003: Incorrect `user` field in org access

### Phase 2: Reliability (Day 2)
3. P1-002: SIGALRM timeout replacement
4. P1-005: Race condition in duplicate detection
5. P1-006: Race condition in cancellation
6. P2-002: Transaction commit timing

### Phase 3: Performance (Day 3)
7. P1-004: Add database indexes
8. P2-005: Batched cleanup commits

### Phase 4: Verification (Day 4)
9. P1-007: Verify scheduler hooks
10. P1-008: State machine audit
11. P2-003: Fix duplicate hook key

### Phase 5: Polish (Post-Merge)
12. All P3 items

---

## Final Recommendation

**HOLD MERGE** until P1 items 001-006 are addressed. These represent:
- Active security vulnerability (SQL injection)
- Production stability risks (SIGALRM, race conditions)
- Functional breakage (incorrect field references)

The implementation architecture is sound and follows Frappe patterns well. Once the critical issues are resolved, this feature will provide a solid foundation for the offline sync, notifications, and fax modules.

---

*Generated by synthesis of reviews from: GPT52, gemi30, sonn45, opus45*
