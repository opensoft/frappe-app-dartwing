# Tasks: Organization Bidirectional Hooks

**Input**: Design documents from `/specs/004-org-bidirectional-hooks/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are included as specified in plan.md (Constitution Check: "Will include tests for business logic")

**Organization**: Tasks are grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions (Frappe App)

Based on actual project structure:
- **Source**: `dartwing/dartwing/dartwing_core/`
- **Tests**: `dartwing/dartwing/tests/` or `tests/`
- **Doctype**: `dartwing/dartwing/dartwing_core/doctype/organization/`
- **Hooks Registration**: `dartwing/dartwing/hooks.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify existing structure and prepare for hook implementation

- [x] T001 Verify Organization doctype exists with linked_doctype and linked_name fields in dartwing/dartwing/dartwing_core/doctype/organization/organization.json
- [x] T002 Verify concrete type doctypes exist (Family, Company, Association, Nonprofit) with organization Link field

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Define ORG_TYPE_MAP constant mapping org_type values to doctype names in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T005 [P] Configure logger for dartwing_core.hooks in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T006 Register Organization doc_events in hooks.py (using doctype controller methods after_insert/on_trash)
- [x] T007 [P] Create test fixtures for Organization and concrete types in tests/test_organization_hooks.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Automatic Concrete Type Creation (Priority: P1) 🎯 MVP

**Goal**: Auto-create concrete type records when Organization is created with proper bidirectional linking

**Independent Test**: Create Organization with any org_type and verify concrete type exists with proper linkage

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [x] T008 [P] [US1] Test Organization with org_type Family creates Family record in tests/test_organization_hooks.py
- [x] T009 [P] [US1] Test Organization with org_type Company creates Company record in tests/test_organization_hooks.py
- [x] T010 [P] [US1] Test Organization with org_type Nonprofit creates Nonprofit record in tests/test_organization_hooks.py
- [x] T011 [P] [US1] Test Organization with org_type Association creates Association record in tests/test_organization_hooks.py
- [x] T012 [P] [US1] Test linked_doctype and linked_name are populated correctly in tests/test_organization_hooks.py
- [x] T013 [P] [US1] Test concrete type's organization field points back to Organization in tests/test_organization_hooks.py
- [x] T014 [P] [US1] Test invalid org_type is rejected with ValidationError in tests/test_organization_hooks.py
- [x] T015 [P] [US1] Test atomic rollback if concrete type creation fails in tests/test_organization_hooks.py

### Implementation for User Story 1

- [x] T016 [US1] Implement create_concrete_type hook function in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T017 [US1] Add org_type validation in Organization.validate() method in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T018 [US1] Implement ignore_permissions flag for concrete type creation in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T019 [US1] Implement db_set for linked_doctype and linked_name fields in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T020 [US1] Add audit logging for successful concrete type creation in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T021 [US1] Add error logging for failed concrete type creation in dartwing/dartwing/dartwing_core/doctype/organization/organization.py

**Checkpoint**: User Story 1 complete - Organizations auto-create their concrete types

---

## Phase 4: User Story 2 - Organization Retrieval with Concrete Details (Priority: P1)

**Goal**: Provide API methods to retrieve Organization with nested concrete type data in single request

**Independent Test**: Retrieve existing Organization and verify response includes both Organization and concrete type fields

### Tests for User Story 2

- [x] T022 [P] [US2] Test get_concrete_doc returns concrete type document in tests/test_organization_hooks.py
- [x] T023 [P] [US2] Test get_concrete_doc returns None when no linked concrete type in tests/test_organization_hooks.py
- [x] T024 [P] [US2] Test get_organization_with_details returns merged data in tests/test_organization_hooks.py
- [x] T025 [P] [US2] Test get_organization_with_details includes concrete_type nested object in tests/test_organization_hooks.py
- [x] T026 [P] [US2] Test retrieval completes within 500ms in tests/test_organization_hooks.py

### Implementation for User Story 2

- [x] T027 [US2] Implement get_concrete_doc whitelisted method in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T028 [US2] Implement get_organization_with_details whitelisted method in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T029 [US2] Add permission checks for retrieval methods in dartwing/dartwing/dartwing_core/doctype/organization/organization.py (uses Frappe's built-in permission checking via frappe.get_doc)

**Checkpoint**: User Story 2 complete - API consumers can retrieve Organization with details

---

## Phase 5: User Story 3 - Cascade Delete to Concrete Type (Priority: P2)

**Goal**: Automatically delete concrete type when Organization is deleted to maintain data integrity

**Independent Test**: Delete Organization and verify linked concrete type no longer exists

### Tests for User Story 3

- [x] T030 [P] [US3] Test deleting Organization cascades to delete Family record in tests/test_organization_hooks.py
- [x] T031 [P] [US3] Test deleting Organization cascades to delete Company record in tests/test_organization_hooks.py
- [x] T032 [P] [US3] Test deletion succeeds when concrete type already missing in tests/test_organization_hooks.py
- [x] T033 [P] [US3] Test other Organizations unaffected by single deletion in tests/test_organization_hooks.py

### Implementation for User Story 3

- [x] T034 [US3] Implement delete_concrete_type hook function in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T035 [US3] Add existence check before cascade delete in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T036 [US3] Implement ignore_permissions=True for cascade delete (force=True omitted for data integrity) in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T037 [US3] Add audit logging for cascade delete operations in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T038 [US3] Add warning log when concrete type not found during delete in dartwing/dartwing/dartwing_core/doctype/organization/organization.py

**Checkpoint**: User Story 3 complete - Organization deletions maintain data integrity

---

## Phase 6: User Story 4 - Organization Type Immutability (Priority: P2)

**Goal**: Prevent org_type changes after creation to avoid data corruption

**Independent Test**: Attempt to change org_type on existing Organization and verify rejection

### Tests for User Story 4

- [x] T039 [P] [US4] Test changing org_type raises ValidationError in tests/test_organization_hooks.py
- [x] T040 [P] [US4] Test modifying other fields (org_name, status) succeeds in tests/test_organization_hooks.py
- [x] T041 [P] [US4] Test error message is clear and user-friendly in tests/test_organization_hooks.py

### Implementation for User Story 4

- [x] T042 [US4] Add org_type immutability validation in Organization.validate() in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T043 [US4] Verify set_only_once attribute on org_type field in dartwing/dartwing/dartwing_core/doctype/organization/organization.json

**Checkpoint**: User Story 4 complete - org_type is immutable after creation

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T044 [P] Add docstrings to all public functions in dartwing/dartwing/dartwing_core/doctype/organization/organization.py
- [x] T045 [P] Review and ensure consistent error messages across all validation failures
- [x] T046 Run full test suite to verify all user stories work together (22 tests passed)
- [x] T047 Validate quickstart.md scenarios work end-to-end (updated import paths)
- [x] T048 [P] Review log output format matches contracts/api.md audit log format (verified)
- [x] T049 [P] Add concurrency stress test for SC-006 (100 concurrent Organization creations) in dartwing/tests/test_organization_hooks.py

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-6)**: All depend on Foundational phase completion
  - US1 and US2 can proceed in parallel (both P1 priority)
  - US3 and US4 can proceed in parallel after US1 (both P2 priority)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational - Requires US1 complete for test data (Organizations must exist)
- **User Story 3 (P2)**: Can start after US1 - Uses creation hooks for test setup
- **User Story 4 (P2)**: Can start after US1 - Uses creation hooks for test setup

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Hook functions before validation logic
- Core implementation before logging
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- All tests within a user story marked [P] can run in parallel
- US1 and US2 can proceed in parallel (both P1)
- US3 and US4 can proceed in parallel (both P2)

---

## Parallel Example: User Story 1 Tests

```bash
# Launch all US1 tests together (they test different org_types):
Task: "Test Organization with org_type Family creates Family record"
Task: "Test Organization with org_type Company creates Company record"
Task: "Test Organization with org_type Nonprofit creates Nonprofit record"
Task: "Test Organization with org_type Association creates Association record"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Automatic Creation)
4. **STOP and VALIDATE**: Test creating Organizations of all types
5. Deploy/demo core functionality

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add User Story 1 → Test → Deploy (Organizations auto-create concrete types)
3. Add User Story 2 → Test → Deploy (API retrieval methods available)
4. Add User Story 3 → Test → Deploy (Cascade delete works)
5. Add User Story 4 → Test → Deploy (Type immutability enforced)

### Parallel Team Strategy

With two developers:
1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (creation hooks)
   - Developer B: Prepare US2 test scaffolding
3. After US1:
   - Developer A: User Story 3 (cascade delete)
   - Developer B: User Story 2 (retrieval APIs)
4. Final:
   - Developer A: User Story 4 (immutability)
   - Developer B: Polish phase

---

## Notes

- [P] tasks = different files or independent test cases
- [Story] label maps task to specific user story for traceability
- Each user story is independently testable
- All hook operations use ignore_permissions=True per spec clarification
- All hook executions logged per spec clarification
- 500ms retrieval target per spec clarification
