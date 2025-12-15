# Code Review: Background Job Engine (011-background-job-engine)

**Reviewer:** opus45 (Senior Frappe/ERPNext Core Developer)
**Date:** 2025-12-15
**Branch:** `011-background-job-engine`
**Module:** `dartwing_core`

---

## Feature Summary

**Feature:** Background Job Engine (Feature 11 / C-16)

**Purpose:** Implements a guaranteed asynchronous task execution system with:
- Real-time progress tracking via Socket.IO
- Intelligent retry with transient vs permanent error classification
- Multi-tenant job isolation scoped to Organization
- Dead letter queue for failed job review
- Operational metrics for monitoring

**Understanding Confidence:** 95%

The implementation closely follows the `background_job_isolation_spec.md` specification and addresses the core requirements for async processing foundation that will support offline sync, notifications, fax, and scheduled tasks.

---

## 1. Critical Issues & Blockers (Severity: HIGH)

### 1.1 SQL Injection Vulnerability in Metrics Module

**Location:** [metrics.py:59-76](dartwing/dartwing_core/background_jobs/metrics.py#L59-L76) (and similar patterns at lines 81-103, 106-131, 164-196)

**Issue:** The metrics functions use f-string interpolation to build SQL queries with organization names, which creates a SQL injection vulnerability:

```python
# Current vulnerable code
org_filter = f"AND organization = '{filters['organization']}'"
```

**Why Critical:** An attacker with API access could craft a malicious organization parameter to extract data from other tenants or perform destructive operations.

**Fix:**
```python
def _get_job_count_by_status(filters: dict) -> dict:
    """Get count of jobs by status."""
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

Apply this parameterized query pattern to all four metric functions.

---

### 1.2 Signal-Based Timeout Not Portable

**Location:** [executor.py:148-176](dartwing/dartwing_core/background_jobs/executor.py#L148-L176)

**Issue:** The `_execute_with_timeout` function uses `signal.SIGALRM` which:
1. **Only works on Unix** - Will crash on Windows
2. **Only works in main thread** - RQ workers may run handlers in non-main threads
3. **Can corrupt state** - Signal handlers can interrupt at any point, potentially leaving DB transactions incomplete

```python
# Current problematic code
def _execute_with_timeout(handler, context, timeout_seconds):
    def timeout_handler(signum, frame):
        raise JobTimeoutError(f"Job exceeded {timeout_seconds}s timeout")

    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout_seconds)
    # ...
```

**Why Critical:** This will cause hard-to-debug failures in production, especially if running on Windows or with certain RQ configurations.

**Fix:** Use a thread-based timeout or rely on Frappe's built-in timeout mechanism:

```python
import threading
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

def _execute_with_timeout(handler: Callable, context: JobContext, timeout_seconds: int) -> Any:
    """
    Execute handler with timeout using thread pool.
    """
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(handler, context)
        try:
            return future.result(timeout=timeout_seconds)
        except FuturesTimeoutError:
            raise JobTimeoutError(f"Job exceeded {timeout_seconds}s timeout")
```

**Alternative:** Since Frappe's `enqueue()` already accepts a `timeout` parameter (line 426 of engine.py), consider relying on that and removing the redundant timeout handling, or document that this is a secondary safeguard.

---

### 1.3 Missing Database Indexes for Performance

**Location:** [background_job.json](dartwing/dartwing_core/doctype/background_job/background_job.json)

**Issue:** The Background Job DocType lacks indexes on frequently queried fields that will cause performance degradation at scale:

1. `job_hash` - Used for duplicate detection queries
2. `next_retry_at` - Used by retry scheduler every minute
3. `(status, next_retry_at)` - Compound index for retry queue
4. `(status, modified)` - Used by cleanup job

**Why Critical:** Without indexes, the retry scheduler running every minute will perform full table scans. At 10,000+ jobs, this will cause noticeable delays.

**Fix:** Add index definitions to the DocType JSON:

```json
{
    "fields": [...],
    "indexes": [
        {
            "fields": ["job_hash"]
        },
        {
            "fields": ["status", "next_retry_at"]
        },
        {
            "fields": ["status", "modified"]
        }
    ]
}
```

---

### 1.4 Race Condition in Duplicate Detection

**Location:** [engine.py:53-62](dartwing/dartwing_core/background_jobs/engine.py#L53-L62)

**Issue:** The duplicate check and job insertion are not atomic, creating a race condition:

```python
# Check for duplicates
existing = _check_duplicate(job_hash, ...)
if existing:
    frappe.throw(...)

# Gap here where another request could insert the same job

# Create job document
job = frappe.new_doc("Background Job")
job.insert(ignore_permissions=True)
```

**Why Critical:** Under high concurrency, two identical job submissions could both pass the duplicate check before either inserts.

**Fix:** Add a unique constraint on `(job_hash, status)` for non-terminal states, or use a database-level lock:

```python
def submit_job(...):
    # ... validation ...

    job_hash = generate_job_hash(job_type, organization, parameters or {})

    # Use database-level duplicate check with insert
    try:
        job = frappe.new_doc("Background Job")
        job.job_hash = job_hash
        # ... set other fields ...
        job.insert(ignore_permissions=True)
    except frappe.DuplicateEntryError:
        existing = frappe.db.get_value(
            "Background Job",
            {"job_hash": job_hash, "status": ("not in", ["Completed", "Dead Letter", "Canceled"])},
            ["name", "status"],
            as_dict=True
        )
        if existing:
            frappe.throw(_("Duplicate job detected..."), exc=frappe.DuplicateEntryError)
```

---

### 1.5 Incorrect Field Reference in Organization Access Check

**Location:** [engine.py:338-341](dartwing/dartwing_core/background_jobs/engine.py#L338-L341)

**Issue:** The `_validate_organization_access` function queries `Org Member` with a `user` field, but based on the Org Member DocType in the architecture docs, the field is `person` (which links to Person, which links to User):

```python
# Current incorrect code
is_member = frappe.db.exists(
    "Org Member",
    {"organization": organization, "user": frappe.session.user, "status": "Active"},
)
```

**Why Critical:** This validation will always fail for non-System Manager users, blocking all job submissions.

**Fix:**
```python
def _validate_organization_access(organization: str):
    """Validate user has access to organization."""
    if "System Manager" in frappe.get_roles():
        return

    # Find Person linked to current user, then check Org Member
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

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### 2.1 Duplicate Key in hooks.py

**Location:** [hooks.py:125-127](dartwing/hooks.py#L125-L127)

**Issue:** The `permission_query_conditions` and `has_permission` dicts have duplicate `"Company"` keys:

```python
permission_query_conditions = {
    # ...
    "Company": "dartwing.dartwing_company.permissions.get_permission_query_conditions_company",
    "Company": "dartwing.permissions.company.get_permission_query_conditions",  # Overwrites above
}
```

**Fix:** Remove the duplicate entry - keep only one Company permission handler.

---

### 2.2 list_jobs Also Has Incorrect User Field

**Location:** [engine.py:229-231](dartwing/dartwing_core/background_jobs/engine.py#L229-L231)

**Issue:** Same problem as 1.5 - queries `Org Member` with `user` field:

```python
orgs = frappe.get_all(
    "Org Member",
    filters={"user": frappe.session.user, "status": "Active"},
    pluck="organization",
)
```

**Fix:** Query by `person` after looking up the Person from the current user.

---

### 2.3 Add Rate Limiting for Job Submission

**Issue:** No rate limiting on job submissions per organization could allow one organization to flood the queue.

**Suggestion:** Add configurable per-org limits (referenced in background_job_isolation_spec.md but not implemented):

```python
def _check_org_job_limit(organization: str, queue_name: str = "default"):
    """Check if organization has exceeded job submission limits."""
    pending_count = frappe.db.count(
        "Background Job",
        {"organization": organization, "status": ("in", ["Pending", "Queued", "Running"])}
    )

    # Configurable limit per organization
    max_concurrent = frappe.db.get_value("Organization", organization, "max_concurrent_jobs") or 500

    if pending_count >= max_concurrent:
        frappe.msgprint(
            _("Organization {0} has reached the maximum concurrent job limit ({1})").format(
                organization, max_concurrent
            ),
            indicator="orange"
        )
```

---

### 2.4 Cleanup Job Should Use Batched Commits

**Location:** [cleanup.py:35-47](dartwing/dartwing_core/background_jobs/cleanup.py#L35-L47)

**Issue:** The cleanup loop commits all deletions at once at the end. For 1000 jobs, this could be a long-running transaction.

**Suggestion:** Commit in batches:

```python
def cleanup_old_jobs(retention_days: int = 30, batch_size: int = 100):
    # ...
    deleted_count = 0
    for i, job_id in enumerate(jobs):
        try:
            frappe.delete_doc("Background Job", job_id, force=True, delete_permanently=True)
            deleted_count += 1

            # Commit every batch_size deletions
            if (i + 1) % batch_size == 0:
                frappe.db.commit()
        except Exception as e:
            frappe.log_error(...)

    if deleted_count % batch_size != 0:
        frappe.db.commit()

    return deleted_count
```

---

### 2.5 Consider Using Frappe's Query Builder

**Issue:** Multiple places use raw SQL strings. While parameterized queries fix injection, using Frappe's query builder is more maintainable.

**Example for metrics.py:**
```python
def _get_job_count_by_status(filters: dict) -> dict:
    query = (
        frappe.qb.from_("Background Job")
        .select("status", frappe.qb.fn.Count("*").as_("count"))
        .groupby("status")
    )

    if filters.get("organization"):
        if isinstance(filters["organization"], tuple):
            query = query.where(frappe.qb.Field("organization").isin(filters["organization"][1]))
        else:
            query = query.where(frappe.qb.Field("organization") == filters["organization"])

    result = query.run(as_dict=True)
    return {row["status"]: row["count"] for row in result}
```

---

### 2.6 Add Validation for handler_method Path Existence

**Location:** [job_type.py:19-35](dartwing/dartwing_core/doctype/job_type/job_type.py#L19-L35)

**Issue:** The validation only checks syntax, not whether the module/function exists.

**Suggestion:** Add import check on save:

```python
def validate_handler_method(self):
    # ... existing syntax validation ...

    # Verify the handler can be imported
    try:
        module_path, func_name = self.handler_method.rsplit(".", 1)
        module = frappe.get_module(module_path)
        if not hasattr(module, func_name):
            frappe.throw(
                _("Handler function '{0}' not found in module '{1}'").format(func_name, module_path)
            )
    except ImportError as e:
        frappe.throw(_("Cannot import handler module: {0}").format(str(e)))
```

---

### 2.7 Progress Update Should Commit Changes

**Location:** [progress.py:61-66](dartwing/dartwing_core/background_jobs/progress.py#L61-L66)

**Issue:** `update_progress` uses `frappe.db.set_value` but doesn't commit. If the job crashes, the last progress update may be lost.

**Suggestion:** Consider periodic commits during long-running jobs, or document that progress is eventually consistent.

---

### 2.8 Job Execution Log Should Link to Organization

**Location:** [job_execution_log.json](dartwing/dartwing_core/doctype/job_execution_log/job_execution_log.json)

**Issue:** The log only links to Background Job, not Organization. Querying logs by organization requires a join.

**Suggestion:** Add `organization` field for direct filtering:

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

## 3. General Feedback & Summary (Severity: LOW)

### Overall Assessment

The Background Job Engine implementation is **well-architected and follows Frappe best practices** in most areas. The separation of concerns (engine, executor, retry, progress, metrics, cleanup) demonstrates solid software design. The state machine in `BackgroundJob` is correctly defined with proper transition validation, and the error classification system (transient vs permanent) is thoughtfully designed.

### Strengths

1. **Excellent State Machine Design:** The `VALID_TRANSITIONS` constant and `validate_status_transition` method provide clear, maintainable status flow control.

2. **Good Use of Frappe Patterns:** Proper use of DocTypes, fixtures, hooks, scheduler events, and `@frappe.whitelist()` decorators.

3. **Comprehensive Test Coverage Structure:** Unit tests for hash generation, error classification, and backoff; integration tests for submission, retry, cancellation, and multi-tenant isolation.

4. **Real-time Progress via Socket.IO:** The `JobContext.update_progress()` pattern with Socket.IO broadcasting is well-designed for Flutter client integration.

5. **Clean API Surface:** The `__init__.py` exports provide a clear public API (`submit_job`, `get_job_status`, `cancel_job`, `TransientError`, `PermanentError`, `JobContext`).

6. **Audit Trail:** The `Job Execution Log` DocType provides good visibility into job lifecycle.

### Areas for Future Technical Debt

1. **Add More Comprehensive Metrics Tests:** The current `test_job_metrics.py` only tests the empty metrics structure. Add tests for actual metric calculations with sample data.

2. **Add API Documentation:** Consider adding OpenAPI/Swagger documentation for the `/api/method/dartwing.dartwing_core.api.jobs.*` endpoints.

3. **Add Monitoring Alerts:** The `background_job_isolation_spec.md` mentions alerts for queue backlog and DLQ growth - implement these proactively.

4. **Consider Adding Job Priority Preemption:** Currently, Critical priority jobs still wait in queue. Consider implementing preemption for truly urgent jobs.

5. **Add Client-Side TypeScript Types:** For Flutter/Dart integration, consider generating type definitions for job parameters.

6. **Performance Testing:** Add load tests to validate the system under high job submission rates.

### Alignment with Frappe Low-Code Philosophy

The implementation appropriately leverages Frappe's **DocType/Metadata-as-Data** principle:
- Job Types are configurable DocTypes (not hardcoded handlers)
- Background Jobs are persistent documents with full audit trail
- Permissions use Frappe's standard `permission_query_conditions` and `has_permission` hooks

The **only deviation** from pure low-code is the Python-based handler functions, which is appropriate given that background jobs inherently require procedural execution logic.

---

## Summary Table

| Severity | Count | Action Required |
|----------|-------|-----------------|
| HIGH | 5 | Must fix before merge |
| MEDIUM | 8 | Should fix for quality |
| LOW | 6 | Future improvements |

**Recommendation:** Address HIGH severity issues before merging to ensure security, correctness, and production stability. The MEDIUM issues can be addressed in a follow-up PR but should be tracked.
