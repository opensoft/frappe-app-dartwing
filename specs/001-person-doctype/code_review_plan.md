# Code Review Fix Plan — Person API, Auto-Creation, and Sync Reliability

## Scope and Goals

- Close the gaps identified in the review: insecure Person APIs, disabled auto user creation, broken retry/backoff, and minor-consent interaction causing failed sync updates.
- Add missing automated tests to lock in behavior for user sync, deletion guards, and merge flows.

## Assumptions / Constraints

- Frappe job queue supports `enqueue_in`/`enqueue_at` for delayed retries.
- Org Member DocType may not exist in all sites; logic/tests should guard with existence checks.
- Settings DocType is the expected place for the `auto_create_user_on_keycloak_signup` flag (per spec); if adding a custom field is out of scope, provide a safe default/fallback.

## Work Plan (status)

1. Secure Person API endpoints (`dartwing/api/person.py`) — **Implemented**

   - `check_permission` on Person for read/write, guardian/role gate on consent capture (with configurable roles via Settings.consent_capture_roles), merged-target guard, and permission-denial tests in place. `ignore_permissions=True` is retained only for the internal consent/merge operations with justification comments. System Manager role always allowed as security fallback.

2. Enable auto user creation flag — **Implemented**

   - `auto_create_user_on_keycloak_signup` added to `dartwing_core/doctype/settings/settings.json`; flag read in `is_auto_creation_enabled()`.

3. Fix retry/backoff for user sync (`dartwing/utils/person_sync.py`) — **Implemented**

   - Backoff via `enqueue_in`, per-attempt job IDs, status/error updates; tests cover backoff and retry vs non-retry paths.

4. Resolve minor-consent/save interaction (`dartwing_core/doctype/person/person.py`) — **Implemented**

   - Sync field updates allowed for minors without consent; consent capture restrictions preserved; test added.

5. Add missing tests (`dartwing_core/doctype/person/test_person.py`) — **Implemented**
   - User sync success/pending/failure/backoff tests, deletion guard tests (DocType guarded), merge tests (including no Org Member) in place.

## Ordering / Execution Notes

- All items completed per plan.
