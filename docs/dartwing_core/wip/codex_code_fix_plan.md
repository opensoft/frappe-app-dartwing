# Codex Code Fix Plan — Person API, Auto-Creation, and Sync Reliability

## Scope and Goals
- Close the gaps identified in the review: insecure Person APIs, disabled auto user creation, broken retry/backoff, and minor-consent interaction causing failed sync updates.
- Add missing automated tests to lock in behavior for user sync, deletion guards, and merge flows.

## Assumptions / Constraints
- Frappe job queue supports `enqueue_in`/`enqueue_at` for delayed retries.
- Org Member DocType may not exist in all sites; logic/tests should guard with existence checks.
- Settings DocType is the expected place for the `auto_create_user_on_keycloak_signup` flag (per spec); if adding a custom field is out of scope, provide a safe default/fallback.

## Work Plan
1) Secure Person API endpoints (`dartwing/api/person.py`)
   - Add permission/role checks (e.g., System Manager or explicit roles) for all mutating endpoints: `capture_consent`, `retry_sync`, `merge_persons`; ensure read endpoints (`get_sync_status`) respect doc permissions or explicit allowlist.
   - Remove/limit `ignore_permissions=True` where not strictly required; use server-side flags only for controlled internals (e.g., merge log append).
   - Validate actor constraints for consent capture (disallow self-consent, require guardian role) and merges (disallow merging to/from Merged, require permission on both docs).
   - Verification: unit/integration tests for permission denials and success paths; manual bench call if needed.

2) Enable auto user creation flag
   - Add `auto_create_user_on_keycloak_signup` field to `dartwing_core/doctype/settings/settings.json` (Data/Check with default False) per spec, or provide a fallback config read with a sensible default.
   - Ensure `_trigger_user_auto_creation` uses this flag and communicates clearly when disabled.
   - Verification: unit test toggling the flag; confirm no log spam when field is present.

3) Fix retry/backoff for user sync (`dartwing/utils/person_sync.py`)
   - Apply delay (`enqueue_in` using computed backoff) and unique job IDs per attempt/person to avoid dedup collisions.
   - Include attempt in `job_id` and persist attempt count if useful for observability.
   - Ensure status transitions: pending → synced/failed, and sync_error_message updated consistently.
   - Verification: tests simulating retryable vs non-retryable exceptions; assert enqueue args/backoff.

4) Resolve minor-consent/save interaction (`dartwing_core/doctype/person/person.py`)
   - Allow the system sync path to update `frappe_user`, `user_sync_status`, and `last_sync_at` for minors without treating it as a prohibited user edit (e.g., a flag on doc or context check).
   - Keep the strict guard for user-facing writes; ensure consent capture still only alters allowed fields.
   - Verification: unit test where a minor without consent gets auto-sync status updates without raising `PermissionError`.

5) Add missing tests (`dartwing_core/doctype/person/test_person.py`)
   - Implement user sync success/pending tests with fakes/mocks for enqueue and user creation.
   - Add deletion blocking test that skips or adapts if Org Member DocType absent.
   - Add merge tests covering status change, merge log entry, and Org Member transfer when available.
   - Verification: bench test module; ensure new tests pass and guard against regressions.

## Ordering / Execution Notes
- Start with the Settings flag so auto-creation can be exercised in tests.
- Update consent guard and retry/backoff before tightening API permissions, so system flows remain stable.
- Finish with API permission hardening and the new tests to validate end-to-end behavior.
