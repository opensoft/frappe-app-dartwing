# Tasks: Background Job Engine

**Input**: Design documents from `/specs/011-background-job-engine/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

**Tests**: Per Constitution Principle 6 ("Tests required for business logic"), test tasks are included for each user story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md structure (Frappe app module):
- **Doctypes**: `dartwing/dartwing_core/doctype/{doctype_name}/`
- **Background Jobs Package**: `dartwing/dartwing_core/background_jobs/`
- **API**: `dartwing/dartwing_core/api/`
- **Tests**: `dartwing/tests/unit/`, `dartwing/tests/integration/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and doctype scaffolding

- [x] T001 Create background_jobs package structure in dartwing/dartwing_core/background_jobs/__init__.py
- [x] T002 [P] Create Job Type doctype folder in dartwing/dartwing_core/doctype/job_type/
- [x] T003 [P] Create Background Job doctype folder in dartwing/dartwing_core/doctype/background_job/
- [x] T004 [P] Create Job Execution Log doctype folder in dartwing/dartwing_core/doctype/job_execution_log/
- [x] T005 Create API module file in dartwing/dartwing_core/api/jobs.py
- [x] T006 Update hooks.py to register new doctypes and scheduler events in dartwing/hooks.py
- [x] T007 [P] Create test directory structure in dartwing/tests/unit/ and dartwing/tests/integration/

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core doctypes and base infrastructure that MUST be complete before ANY user story

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T008 Implement Job Type doctype JSON schema with fields (type_name, display_name, handler_method, default_timeout, default_priority, max_retries, is_enabled, requires_permission, deduplication_window) in dartwing/dartwing_core/doctype/job_type/job_type.json
- [x] T009 Implement Job Type controller with validation in dartwing/dartwing_core/doctype/job_type/job_type.py
- [x] T010 Implement Background Job doctype JSON schema with all fields per data-model.md in dartwing/dartwing_core/doctype/background_job/background_job.json
- [x] T011 Implement Background Job controller with state machine validation in dartwing/dartwing_core/doctype/background_job/background_job.py
- [x] T012 Implement Job Execution Log doctype JSON schema in dartwing/dartwing_core/doctype/job_execution_log/job_execution_log.json
- [x] T013 Implement Job Execution Log controller in dartwing/dartwing_core/doctype/job_execution_log/job_execution_log.py
- [x] T014 Create error classification module with TransientError and PermanentError classes in dartwing/dartwing_core/background_jobs/errors.py
- [x] T015 Create base executor module with timeout handling and checkpoint support in dartwing/dartwing_core/background_jobs/executor.py
- [x] T016 Implement job dependency handling (depends_on field, wait for parent completion) in dartwing/dartwing_core/background_jobs/engine.py
- [x] T017 Create sample job handler for testing in dartwing/dartwing_core/background_jobs/samples.py
- [x] T018 Add Job Type fixture with sample_job in dartwing/dartwing_core/fixtures/job_type.json

**Checkpoint**: Foundation ready - all doctypes exist, dependencies work, and can be created via Frappe

---

## Phase 3: User Story 1 - Submit and Monitor a Background Job (Priority: P1) 🎯 MVP

**Goal**: Users can submit jobs, track progress in real-time, and access results when complete

**Independent Test**: Submit a sample job via API, verify it executes with progress updates visible, and access the output reference on completion

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T019 [P] [US1] Unit test for job submission and hash generation in dartwing/tests/unit/test_job_engine.py
- [x] T020 [P] [US1] Unit test for duplicate detection logic in dartwing/tests/unit/test_job_engine.py
- [x] T021 [P] [US1] Integration test for submit_job API endpoint in dartwing/tests/integration/test_job_submission.py
- [ ] T022 [P] [US1] Integration test for real-time progress updates via Socket.IO in dartwing/tests/integration/test_job_progress.py

### Implementation for User Story 1

- [x] T023 [US1] Implement job submission function with duplicate detection in dartwing/dartwing_core/background_jobs/engine.py
- [x] T024 [US1] Implement job hash generation for duplicate detection in dartwing/dartwing_core/background_jobs/engine.py
- [x] T025 [US1] Implement progress tracking module with Socket.IO publish in dartwing/dartwing_core/background_jobs/progress.py
- [x] T026 [US1] Implement job state transition logging (creates Job Execution Log entries) in dartwing/dartwing_core/background_jobs/engine.py
- [x] T027 [US1] Implement submit_job API endpoint with validation in dartwing/dartwing_core/api/jobs.py
- [x] T028 [US1] Implement get_job_status API endpoint in dartwing/dartwing_core/api/jobs.py
- [x] T029 [US1] Implement list_jobs API endpoint with filtering and pagination in dartwing/dartwing_core/api/jobs.py
- [x] T030 [US1] Add organization-scoping permission check to all job operations in dartwing/dartwing_core/background_jobs/engine.py
- [x] T031 [US1] Integrate job execution with Frappe background jobs (frappe.enqueue wrapper) in dartwing/dartwing_core/background_jobs/engine.py
- [x] T032 [US1] Add real-time Socket.IO events for job_progress and job_status_changed in dartwing/dartwing_core/background_jobs/progress.py

**Checkpoint**: User Story 1 complete - jobs can be submitted, monitored, and completed with real-time progress. **Validate**: Duplicate detection rejects identical jobs within 5-minute window (FR-017).

---

## Phase 4: User Story 2 - Automatic Retry on Failure (Priority: P1)

**Goal**: Failed jobs automatically retry with exponential backoff; transient vs permanent error classification

**Independent Test**: Submit a job that fails with a transient error, verify it retries automatically with backoff delays

### Tests for User Story 2

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T033 [P] [US2] Unit test for exponential backoff calculation with jitter in dartwing/tests/unit/test_retry_policy.py
- [x] T034 [P] [US2] Unit test for error classification (transient vs permanent) in dartwing/tests/unit/test_error_classification.py
- [x] T035 [P] [US2] Integration test for automatic retry on transient failure in dartwing/tests/integration/test_job_retry.py

### Implementation for User Story 2

- [x] T036 [US2] Implement retry policy with exponential backoff and jitter calculation in dartwing/dartwing_core/background_jobs/retry.py
- [x] T037 [US2] Implement error classification logic (transient vs permanent) in dartwing/dartwing_core/background_jobs/retry.py
- [x] T038 [US2] Implement retry scheduling (set next_retry_at on transient failure) in dartwing/dartwing_core/background_jobs/engine.py
- [x] T039 [US2] Implement dead letter queue handling (move to Dead Letter status on exhausted retries) in dartwing/dartwing_core/background_jobs/dead_letter.py
- [x] T040 [US2] Create scheduler job to process retry queue in dartwing/dartwing_core/background_jobs/scheduler.py
- [x] T041 [US2] Register retry scheduler in hooks.py scheduler_events in dartwing/hooks.py
- [x] T042 [US2] Update executor to catch and classify errors in dartwing/dartwing_core/background_jobs/executor.py
- [x] T043 [US2] Add retry_count and next_retry_at to job status API response in dartwing/dartwing_core/api/jobs.py

**Checkpoint**: User Story 2 complete - transient failures retry automatically, permanent failures go to dead letter

---

## Phase 5: User Story 3 - Cancel a Running Job (Priority: P2)

**Goal**: Users can cancel pending or running jobs they own

**Independent Test**: Submit a long-running job, cancel it mid-execution, verify status changes to Canceled

### Tests for User Story 3

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T044 [P] [US3] Unit test for cancellation permission validation in dartwing/tests/unit/test_job_cancellation.py
- [x] T045 [P] [US3] Integration test for cancel_job API endpoint in dartwing/tests/integration/test_job_cancellation.py

### Implementation for User Story 3

- [x] T046 [US3] Implement cancellation flag checking in executor checkpoint in dartwing/dartwing_core/background_jobs/executor.py
- [x] T047 [US3] Implement cancel_job function with permission validation in dartwing/dartwing_core/background_jobs/engine.py
- [x] T048 [US3] Implement cancel_job API endpoint in dartwing/dartwing_core/api/jobs.py
- [x] T049 [US3] Add canceled_at and canceled_by field updates on cancellation in dartwing/dartwing_core/background_jobs/engine.py
- [x] T050 [US3] Emit job_status_changed Socket.IO event on cancellation in dartwing/dartwing_core/background_jobs/progress.py

**Checkpoint**: User Story 3 complete - users can cancel their own jobs

---

## Phase 6: User Story 4 - View Job History and Results (Priority: P2)

**Goal**: Users can view job history with filtering, access results, and see error details for failed jobs

**Independent Test**: Run several jobs (success, failure), verify history API returns filtered results with correct details

### Tests for User Story 4

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T051 [P] [US4] Integration test for multi-tenant job isolation in dartwing/tests/integration/test_multi_tenant_isolation.py
- [ ] T052 [P] [US4] Integration test for job history filtering in dartwing/tests/integration/test_job_history.py

### Implementation for User Story 4

- [x] T053 [US4] Implement get_job_history API endpoint (returns Job Execution Log entries) in dartwing/dartwing_core/api/jobs.py
- [x] T054 [US4] Add output_reference field handling for completed jobs in dartwing/dartwing_core/background_jobs/engine.py
- [x] T055 [US4] Add error_message and error_type to failed job details in dartwing/dartwing_core/api/jobs.py
- [x] T056 [US4] Implement organization-scoped filtering in list_jobs for multi-tenant isolation in dartwing/dartwing_core/api/jobs.py
- [ ] T057 [US4] Add date range filtering to list_jobs API in dartwing/dartwing_core/api/jobs.py

**Checkpoint**: User Story 4 complete - full job history accessible with filtering

---

## Phase 7: User Story 5 - Administrator Monitors System Health (Priority: P3)

**Goal**: Admins can view operational metrics, manage dead letter queue, and monitor system health

**Independent Test**: Access metrics API as admin, verify queue depth, failure rates, and processing times are accurate

### Tests for User Story 5

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T058 [P] [US5] Unit test for metrics calculations in dartwing/tests/unit/test_job_metrics.py
- [ ] T059 [P] [US5] Integration test for admin-only retry_job endpoint in dartwing/tests/integration/test_admin_operations.py

### Implementation for User Story 5

- [x] T060 [US5] Implement metrics collection module in dartwing/dartwing_core/background_jobs/metrics.py
- [x] T061 [P] [US5] Implement job_count_by_status metric calculation in dartwing/dartwing_core/background_jobs/metrics.py
- [x] T062 [P] [US5] Implement queue_depth_by_priority metric calculation in dartwing/dartwing_core/background_jobs/metrics.py
- [x] T063 [P] [US5] Implement processing_time (average and p95) metric calculation in dartwing/dartwing_core/background_jobs/metrics.py
- [x] T064 [P] [US5] Implement failure_rate_by_type metric calculation in dartwing/dartwing_core/background_jobs/metrics.py
- [x] T065 [US5] Implement get_job_metrics API endpoint in dartwing/dartwing_core/api/jobs.py
- [x] T066 [US5] Implement retry_job API endpoint (admin only, re-queues dead letter jobs) in dartwing/dartwing_core/api/jobs.py
- [x] T067 [US5] Add admin permission check for cross-organization views in dartwing/dartwing_core/api/jobs.py

**Checkpoint**: User Story 5 complete - admins have full operational visibility

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T068 [P] Implement job timeout enforcement with SIGALRM in dartwing/dartwing_core/background_jobs/executor.py
- [x] T069 [P] Implement job priority queue ordering in dartwing/dartwing_core/background_jobs/scheduler.py
- [x] T070 [P] Add data retention cleanup job (delete jobs older than 30 days) in dartwing/dartwing_core/background_jobs/cleanup.py
- [x] T071 Register cleanup job in hooks.py scheduler_events (daily) in dartwing/hooks.py
- [ ] T072 Add comprehensive docstrings and type hints to all modules in dartwing/dartwing_core/background_jobs/
- [ ] T073 Run quickstart.md validation - test all code examples work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 and US2 are both P1 priority but US2 depends on US1 (retry needs job execution)
  - US3, US4, US5 can proceed after US1 is complete
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

```
Phase 2 (Foundational)
        │
        ▼
  ┌─────────────┐
  │    US1      │ (P1) - Submit & Monitor
  │   Core Job  │
  └──────┬──────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────────────────────────┐
│  US2  │ │  US3, US4, US5 can start  │
│ Retry │ │  after US1 complete       │
│ (P1)  │ │  (in parallel if staffed) │
└───────┘ └───────────────────────────┘
```

- **User Story 1 (P1)**: Starts after Phase 2 - Core job submission and monitoring
- **User Story 2 (P1)**: Starts after US1 - Retry logic needs job execution foundation
- **User Story 3 (P2)**: Can start after US1 - Cancellation is independent
- **User Story 4 (P2)**: Can start after US1 - History viewing is independent
- **User Story 5 (P3)**: Can start after US1 - Metrics can be collected once jobs exist

### Within Each User Story

- **Tests FIRST**: Write tests and ensure they FAIL before implementation
- Models/Doctypes before services
- Services before API endpoints
- Core implementation before integrations
- Story complete before moving to next priority

### Parallel Opportunities

- T002, T003, T004 can run in parallel (different doctype folders)
- Within Phase 2, T008/T010/T012 (JSON schemas) can run in parallel
- All test tasks within a user story marked [P] can run in parallel
- Once US1 is complete, US3, US4, US5 can be worked in parallel
- Within US5, T061-T064 (metric calculations) can run in parallel
- All tasks in Phase 8 marked [P] can run in parallel

---

## Parallel Example: Phase 2 Doctypes

```bash
# Launch all doctype JSON schema tasks together:
Task: "T008 - Implement Job Type doctype JSON schema"
Task: "T010 - Implement Background Job doctype JSON schema"
Task: "T012 - Implement Job Execution Log doctype JSON schema"
```

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 test tasks together:
Task: "T019 - Unit test for job submission"
Task: "T020 - Unit test for duplicate detection"
Task: "T021 - Integration test for submit_job API"
Task: "T022 - Integration test for real-time progress"
```

## Parallel Example: User Story 5 Metrics

```bash
# Launch all metric calculation tasks together:
Task: "T061 - Implement job_count_by_status metric"
Task: "T062 - Implement queue_depth_by_priority metric"
Task: "T063 - Implement processing_time metric"
Task: "T064 - Implement failure_rate_by_type metric"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Submit & Monitor)
4. Complete Phase 4: User Story 2 (Retry Logic)
5. **STOP and VALIDATE**: Test core job engine end-to-end
6. Deploy/demo if ready - this is a functional background job engine

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Submit & Monitor) → Test → Deploy (Basic MVP!)
3. Add US2 (Retry Logic) → Test → Deploy (Reliable MVP!)
4. Add US3 (Cancel Jobs) → Test → Deploy
5. Add US4 (Job History) → Test → Deploy
6. Add US5 (Admin Metrics) → Test → Deploy (Full Feature!)
7. Polish phase → Final release

### Task Count Summary

| Phase | Tasks | Test Tasks | Parallel Tasks |
|-------|-------|------------|----------------|
| Phase 1: Setup | 7 | 0 | 4 |
| Phase 2: Foundational | 11 | 0 | 0 |
| Phase 3: US1 Submit & Monitor | 14 | 4 | 4 |
| Phase 4: US2 Retry Logic | 11 | 3 | 3 |
| Phase 5: US3 Cancel Jobs | 7 | 2 | 2 |
| Phase 6: US4 Job History | 7 | 2 | 2 |
| Phase 7: US5 Admin Metrics | 12 | 2 | 6 |
| Phase 8: Polish | 6 | 0 | 3 |
| **Total** | **73** | **13** | **24** |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [USn] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- **Tests first**: Write tests before implementation (TDD approach per Constitution P6)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Frappe-specific: Run `bench migrate` after doctype changes
- Frappe-specific: Run `bench clear-cache` after hooks.py changes
