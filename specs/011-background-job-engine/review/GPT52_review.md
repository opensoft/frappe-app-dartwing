# GPT52 Code Review — `011-background-job-engine` (`dartwing_core`)

## Context I used (docs + standards)

- Standards: `bench/apps/dartwing/.specify/memory/constitution.md` (note: requested `.frappe/memory/constitution.md` is not present in-repo).
- Feature intent: Phase 2 **Feature 11: Background Job Engine** in `bench/apps/dartwing/docs/dartwing_core/wip/dartwing_core_features_priority_phase2.md`.
- PRD reference: `bench/apps/dartwing/docs/dartwing_core/dartwing_core_prd.md` §5.10 (C-16).
- Related architecture guidance: `bench/apps/dartwing/docs/dartwing_core/background_job_isolation_spec.md`, `bench/apps/dartwing/docs/dartwing_core/observability_spec.md`.

The branch introduces:
- New DocTypes: `Background Job`, `Job Type`, `Job Execution Log`
- Engine modules under `dartwing/dartwing_core/background_jobs/`
- Whitelisted API endpoints: `dartwing/dartwing_core/api/jobs.py`
- Scheduler hooks + tests + fixtures

---

## 1. Critical Issues & Blockers (Severity: HIGH)

### 1.1 Org access checks are incorrect (will block real users) and bypass the project’s permission model

**Where**
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/engine.py:331` → `engine._validate_organization_access()`
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/engine.py:225` → `engine.list_jobs()`
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/metrics.py:23` → `metrics.get_metrics()`
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/dead_letter.py:27` → `dead_letter.get_dead_letter_jobs()`

**What / Why it’s a blocker**
- The code queries `Org Member` using a `user` field (e.g., `filters={"user": frappe.session.user, ...}`) but `Org Member` does not have a `user` field in this repo (it links to `Person` + `Organization`).
- Result: non-`System Manager` users will be incorrectly denied access to submit/list/metric/dead-letter endpoints, making the feature unusable outside admin contexts.
- It also diverges from the existing “row-level security via `User Permission`” approach already implemented across the app (see `bench/apps/dartwing/dartwing/permissions/*`).

**Concrete fix (preferred pattern)**
- Replace org access checks with the existing `User Permission` approach (lowest-risk and consistent with the codebase):
  - Use `dartwing.permissions.family.get_user_organizations(user)` (or a new shared helper in `dartwing.permissions`) to resolve the user’s org list.
  - Use `dartwing.permissions.api.check_organization_access(organization)` (or `frappe.has_permission("Organization", "read", organization)`) as the canonical “can user touch this org?” gate.
- Remove direct `Org Member` membership queries from background job engine modules.

**Concrete fix (even better long-term)**
- Add proper doctype-level permission enforcement:
  - Add `permission_query_conditions` + `has_permission` hooks for `Background Job` and `Job Execution Log`.
  - Then remove most manual access filtering from `list_jobs()`/`get_job_history()` and rely on standard Frappe behavior.

---

### 1.2 SQL injection risk in metrics (unsafe SQL string construction)

**Where**
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/metrics.py:57` through `metrics.py:196`

**What / Why it’s a blocker**
- `org_filter` is assembled via f-strings with values interpolated directly into SQL:
  - `metrics.py:63-66`, `metrics.py:87-91`, `metrics.py:112-116`, `metrics.py:170-174`
- Even if org names “normally” originate from the DB, this is still unsafe (org names can contain quotes; and this is a reusable metrics module that may be called with user-provided org input).
- This is a classic injection / query corruption vector and must be fixed before merge.

**Concrete fix**
- Use parameterized queries (placeholders) or Query Builder (`frappe.qb`) for all metrics queries.
- If you must build an `IN (...)` list, use placeholders:
  - Build `placeholders = ", ".join(["%s"] * len(orgs))`
  - Append params tuple and pass to `frappe.db.sql(query, params)`
- Avoid `f"AND organization = '{...}'"` patterns entirely.

---

### 1.3 Cancellation semantics are incorrect (canceled jobs become “Dead Letter”)

**Where**
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/progress.py:51-56` (`JobContext.update_progress`)
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/executor.py:225-255` (`_handle_failure`)
- Sample handlers also raise `PermanentError` on cancellation: `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/samples.py:29-38`, `samples.py:76-78`

**What / Why it’s a blocker**
- A cancel request sets the `Background Job.status = "Canceled"` (`engine.cancel_job()`), but when the running handler checks cancellation and raises `PermanentError`, the executor treats it as a permanent failure and sets status to `Dead Letter` (`executor.py:236-238`).
- This destroys the meaning of “Canceled”, breaks UI expectations, and could trigger incorrect operational workflows (e.g., admins bulk-retrying “dead letter” jobs that were actually user-canceled).

**Concrete fix**
- Introduce a dedicated cancellation exception (e.g., `JobCanceledError`) and handle it explicitly:
  - In `progress.py`, raise `JobCanceledError` instead of `PermanentError`.
  - In `executor.py`, catch that error (or detect `job.status == "Canceled"` after reload) and finalize as `Canceled` without moving to `Failed/Dead Letter` and without retry scheduling.
- Ensure state transitions in `Background Job` reflect this intended path (Running → Canceled is already allowed).

---

### 1.4 Dependency failure path violates the state machine (Queued → Dead Letter not allowed)

**Where**
- Dependency handling: `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/executor.py:110-126`
- State machine: `bench/apps/dartwing/dartwing/dartwing_core/doctype/background_job/background_job.py:14-26`

**What / Why it’s a blocker**
- When a parent dependency fails, `_check_dependency()` sets child status to `Dead Letter` while the child is still `Queued`.
- But the state machine does not allow `Queued → Dead Letter` (`background_job.py:18-19`), so `job.save()` will raise a validation error and leave the job stuck/undefined.

**Concrete fix (minimal)**
- Allow `Queued → Dead Letter` in `VALID_TRANSITIONS` for dependency-aborted jobs.

**Concrete fix (better model)**
- Introduce a distinct “Waiting/Blocked” status (or keep as `Pending`) for dependency-waiting jobs:
  - Don’t enqueue the job until dependency is satisfied.
  - This prevents wasting worker capacity and reduces queue spam (see next issue).

---

### 1.5 Retry/manual retry can race the DB commit and/or enqueue duplicates (job can silently “not run”)

**Where**
- Manual retry: `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/engine.py:183-192` + `_enqueue_job` at `engine.py:394-428`
- Automatic retry: `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/retry.py:111-128`
- Dependent-job scheduler: `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/scheduler.py:23-55`

**What / Why it’s a blocker**
- `frappe.enqueue()` runs immediately by default. If you enqueue before the transaction is committed, the worker can pick up the job and read stale DB state (e.g., still `Failed`), causing `executor.execute_job()` to exit early because it only runs `Queued` jobs (`executor.py:40-46`).
- In `engine.retry_job()` you set `status = "Queued"` and `save()`, then call `_enqueue_job()` which does not commit if status is already `"Queued"` (`engine.py:398-410`), so there is no guaranteed commit before enqueue.
- In scheduler `process_dependent_jobs()`, you select jobs where `status='Queued'` and parent is complete, and enqueue them every minute. Because the status stays `Queued`, you can enqueue the same job repeatedly; the extra worker runs just log and exit (`executor.py:41-46`), but they still burn worker time and queue capacity.

**Concrete fix**
- Use Frappe’s built-in enqueue safety features:
  - In `_enqueue_job()`, call `frappe.enqueue(..., enqueue_after_commit=True, job_id=job.name, deduplicate=True)`
  - Optionally namespace job ids: `job_id=f"background-job:{job.name}"`
- For dependency-waiting jobs:
  - Avoid putting them in `Queued` until they are actually eligible to execute (use `Pending`/`Waiting`).
  - Or, if you keep them `Queued`, store a separate “enqueued marker” (e.g., `enqueued_at` / `rq_job_id`) and skip re-enqueue if already enqueued.

---

### 1.6 Configuration values of `0` don’t work (max retries / dedup window become “defaults”)

**Where**
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/engine.py:55`, `engine.py:73-75`
- `bench/apps/dartwing/dartwing/dartwing_core/doctype/background_job/background_job.py:103-110`

**What / Why it’s a blocker**
- `or` / truthiness checks treat `0` as falsy:
  - `job_type_doc.max_retries or 5` forces retries even when configured as 0.
  - `job_type_doc.deduplication_window or 300` forces dedup even when configured as 0.
  - `if not self.max_retries:` will override 0 with defaults.
- This breaks “metadata-as-data” expectations: admins can’t configure “no retries” / “no deduplication”.

**Concrete fix**
- Use explicit `is None` checks:
  - `window = 300 if job_type_doc.deduplication_window is None else job_type_doc.deduplication_window`
  - Same for retries/timeouts/priority defaults in both engine and doctype controller.

---

### 1.7 `input_parameters` is a JSON field, but the engine stores a JSON string (risk of double-encoding)

**Where**
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/engine.py:71`
- Parameter usage: `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/executor.py:78`

**What / Why it’s a blocker**
- `Background Job.input_parameters` is defined as `fieldtype: "JSON"` in the DocType JSON, but `engine.submit_job()` stores `json.dumps(parameters)`.
- Depending on Frappe’s JSON field handling, this can lead to double-encoding and inconsistent handler inputs (handler receives a string instead of dict).

**Concrete fix**
- Store dicts directly (or `{}`) into the JSON field and let Frappe serialize.
- In the executor, normalize robustly:
  - `params = frappe.parse_json(job.input_parameters) or {}`
  - (and ensure `job.input_parameters` is stored consistently as JSON, not JSON-of-JSON).

---

### 1.8 `get_job_history()` is inconsistent with DocType permissions (will error for non-admin)

**Where**
- `bench/apps/dartwing/dartwing/dartwing_core/background_jobs/engine.py:277-309`
- `bench/apps/dartwing/dartwing/dartwing_core/doctype/job_execution_log/job_execution_log.json` (permissions are admin-only)

**What / Why it’s a blocker**
- `engine.get_job_history()` validates job access, then calls `frappe.get_all("Job Execution Log", ...)` with default permission enforcement.
- For non-admin roles, this will raise permission errors (despite them being allowed to see the job’s status via other endpoints).

**Concrete fix**
- Decide the intended product behavior and implement consistently:
  - If org members should see history: grant read permission appropriately and add permission query conditions for row-level scoping.
  - If history is admin-only: remove/lock down the endpoint and keep it aligned.

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### 2.1 Align “org scoping” with existing Dartwing permission helpers

- Centralize user-org resolution and access checks using `dartwing.permissions` so this feature matches the rest of the stack and doesn’t fork the security model.
- This will also reduce repeated logic across `engine.py`, `metrics.py`, and `dead_letter.py`.

### 2.2 Use `job_id`/`deduplicate` on `frappe.enqueue` to prevent queue spam

- `_enqueue_job()` should use `job_id` and `deduplicate=True` (supported by Frappe) so repeated scheduling doesn’t flood Redis/RQ with duplicates.
- Consider storing the RQ `job_id` (or `enqueued_at`) on the `Background Job` doctype for operational visibility/debugging.

### 2.3 Prefer built-in `creation/modified` timestamps unless there’s a strong reason for `created_at`

- Several queries use `created_at` (custom) while others use `creation` (system). Mixing increases cognitive load and can lead to subtle reporting bugs.
- If you keep `created_at`, standardize all time-based filters to use it consistently and ensure it’s always set (including migrations/fixtures).

### 2.4 Improve concurrency guarantees for retry/dependency schedulers

- Guard against multiple scheduler workers enqueuing the same work:
  - Update rows atomically (e.g., “claim jobs to enqueue” via an update query) before enqueueing.
  - Or rely on `deduplicate=True` + `job_id` consistently.

### 2.5 Data model/indexing for expected query patterns

- Add DB indexes for:
  - `organization`, `status`, `priority`, `job_type`, `next_retry_at`, `depends_on`, `job_hash`
- This will matter quickly once you have retries + UI polling + metrics dashboards.

### 2.6 Status and priority values as constants / enums

- Consolidate status/priority strings in a single module to reduce typos and keep transitions consistent across engine/executor/scheduler.

---

## 3. General Feedback & Summary (Severity: LOW)

The overall structure is a strong start: you modeled the job engine using DocTypes (`Job Type` as metadata-as-data, `Background Job` as durable state) and separated execution concerns cleanly (`engine` vs `executor` vs `retry` vs `scheduler`). The state machine + execution log are good foundations for auditability and a future UI. The main work needed before merge is to align access control with the existing `User Permission`-based security model, fix the SQL injection risk in metrics, and correct cancellation/dependency state handling so job lifecycle semantics are reliable.

**Future technical debt to track**
- Tighten the contract between `Background Job` and the underlying RQ job (store/monitor job_id, worker failures, hard timeouts).
- Add explicit permission query conditions for `Background Job`/`Job Execution Log` so Desk + API behave consistently.
- Expand tests to cover non-admin users with org-scoped permissions (the happy path right now mostly exercises admin behavior).

**Questions to confirm before finalizing behavior**
- Should *all* org members be able to view/cancel org-scoped jobs, or only the submitting user (owner) + admins?
- Do you want dependency-waiting jobs to be visible as “Queued”, or should they have a distinct “Waiting/Blocked” status for UI clarity?

