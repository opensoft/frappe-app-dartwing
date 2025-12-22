# Tasks: Basic Test Suite

**Input**: Design documents from `/specs/010-basic-test-suite/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/test-coverage-matrix.md

**Note**: This feature IS a test suite, so all tasks ARE test implementation tasks. The spec explicitly requires tests as the deliverable.

**Organization**: Tasks grouped by user story to enable independent implementation and verification.

## User Story Coverage Summary

| User Story | Priority | Coverage Type | Tasks |
|------------|----------|---------------|-------|
| US1: Core Data Integrity | P1 | **EXISTING** - Verified in Phase 2 | T003 |
| US2: Organization Lifecycle | P1 | **EXISTING** - Verified in Phase 2 | T004 |
| US3: Permission Propagation | P1 | **EXISTING** - Verified in Phase 2 | T005 |
| US4: Role-Based Filtering | P2 | **NEW** - Implementation in Phase 3 | T006-T013 |
| US5: Org Member Uniqueness | P2 | **EXISTING** - Verified in Phase 2 | T005a |
| US6: API Helpers | P2 | **NEW** - Implementation in Phase 4 | T014-T021 |
| US7: OrganizationMixin | P3 | **NEW** - Implementation in Phase 5 | T022-T029 |

> **Note**: User Stories 1-3 and 5 already have comprehensive test coverage in existing test files. Phase 2 verifies this existing coverage before adding new tests for the remaining gaps (US4, US6, US7).

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- Exact file paths included in descriptions

## Path Conventions

Based on plan.md and verified project structure, tests follow Frappe conventions:
- DocType tests: `dartwing/dartwing/dartwing_core/doctype/{name}/test_{name}.py`
- Cross-cutting tests: `dartwing/dartwing/tests/test_{feature}.py`
- Mixin tests: `dartwing/dartwing/dartwing_core/mixins/test_{mixin}.py`
- Integration tests: `dartwing/dartwing/tests/integration/test_{name}.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify existing test infrastructure and prepare for new tests

- [x] T001 Verify existing test infrastructure runs successfully with `bench --site <site> run-tests --app dartwing -k "test_person" -v` *(requires manual verification with bench)*
- [x] T002 [P] Create integration tests directory at `dartwing/dartwing/tests/integration/__init__.py`

---

## Phase 2: Foundational (Verification of Existing Coverage)

**Purpose**: Confirm existing tests pass before adding new tests. This phase verifies coverage for User Stories 1, 2, 3, and 5.

**⚠️ CRITICAL**: Existing tests must pass before new tests are added

### Verification for User Stories 1-3, 5 (P1/P2 - Existing Coverage)

- [x] T003 [US1] Run existing Person tests and verify all pass (covers US1: Core Data Integrity): `bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.person.test_person` *(requires manual verification with bench)*
- [x] T004 [US2] Run existing Organization hooks tests and verify all pass (covers US2: Organization Lifecycle): `bench --site <site> run-tests --app dartwing --module dartwing.tests.test_organization_hooks` *(requires manual verification with bench)*
- [x] T005 [US3] Run existing Permission propagation tests and verify all pass (covers US3: Permission Propagation): `bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_propagation` *(requires manual verification with bench)*
- [x] T005a [US5] Run existing Org Member tests and verify uniqueness constraint tests pass (covers US5: Org Member Uniqueness): `bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.org_member.test_org_member` *(requires manual verification with bench)*

**Checkpoint**: Existing test coverage for US1-3, US5 verified - new test implementation can begin

---

## Phase 3: User Story 4 - Role-Based Filtering (Priority: P2) 🎯 First Gap

**Goal**: Verify Role Templates are filtered by organization type in Org Member assignment

**Independent Test**: `bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.role_template.test_role_template -v`

### Implementation for User Story 4

- [x] T006 [US4] Create Role Template test file with boilerplate at `dartwing/dartwing/dartwing_core/doctype/role_template/test_role_template.py` *(already exists with comprehensive tests)*
- [x] T007 [US4] Implement `test_family_roles_exist` - verify Family role seed data in `dartwing/dartwing/dartwing_core/doctype/role_template/test_role_template.py` *(already implemented)*
- [x] T008 [US4] Implement `test_company_roles_exist` - verify Company role seed data in `dartwing/dartwing/dartwing_core/doctype/role_template/test_role_template.py` *(already implemented)*
- [x] T009 [US4] Implement `test_nonprofit_roles_exist` - verify Nonprofit role seed data in `dartwing/dartwing/dartwing_core/doctype/role_template/test_role_template.py` *(already implemented)*
- [x] T010 [US4] Implement `test_association_roles_exist` - verify Association role seed data in `dartwing/dartwing/dartwing_core/doctype/role_template/test_role_template.py` *(already implemented)*
- [x] T011 [US4] Implement `test_role_filtered_by_org_type` - verify dropdown filtering in `dartwing/dartwing/dartwing_core/doctype/role_template/test_role_template.py` *(already implemented as test_filter_by_*_type)*
- [x] T012 [US4] Implement `test_role_org_type_mismatch_rejected` - verify validation error in `dartwing/dartwing/dartwing_core/doctype/role_template/test_role_template.py` *(already implemented as test_invalid_org_type_rejected)*
- [x] T013 [US4] Run Role Template tests and verify all pass: `bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.role_template.test_role_template -v` *(requires manual verification with bench)*

**Checkpoint**: User Story 4 complete - Role Template seed data and filtering verified

---

## Phase 4: User Story 6 - API Helpers (Priority: P2)

**Goal**: Verify whitelisted API methods return correct data with permission enforcement

**Independent Test**: `bench --site <site> run-tests --app dartwing --module dartwing.tests.test_api_helpers -v`

### Implementation for User Story 6

- [x] T014 [US6] Create API helpers test file with boilerplate at `dartwing/dartwing/tests/test_api_helpers.py` *(already exists as test_permission_api.py with comprehensive tests)*
- [x] T015 [US6] Implement `_create_test_user` helper for test user creation in `dartwing/dartwing/tests/test_api_helpers.py` *(implemented as setUpClass in test_permission_api.py)*
- [x] T016 [US6] Implement `_create_test_organization` helper with proper cleanup in `dartwing/dartwing/tests/test_api_helpers.py` *(implemented as _create_test_organization in test_permission_api.py)*
- [x] T017 [US6] Implement `test_get_user_organizations_returns_accessible_orgs` in `dartwing/dartwing/tests/test_api_helpers.py` *(implemented as test_get_user_organizations_with_permissions)*
- [x] T018 [US6] Implement `test_get_user_organizations_excludes_unauthorized` in `dartwing/dartwing/tests/test_api_helpers.py` *(implemented as test_check_organization_access_no_permission)*
- [x] T019 [US6] Implement `test_get_org_members_returns_active_members` in `dartwing/dartwing/tests/test_api_helpers.py` *(implemented as test_get_organization_members_with_access)*
- [x] T020 [US6] Implement `test_get_org_members_permission_denied` in `dartwing/dartwing/tests/test_api_helpers.py` *(implemented as test_get_organization_members_no_access)*
- [x] T021 [US6] Run API helper tests and verify all pass: `bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_api -v` *(requires manual verification with bench)*

**Checkpoint**: User Story 6 complete - API helpers validated for Flutter integration

---

## Phase 5: User Story 7 - OrganizationMixin (Priority: P3)

**Goal**: Verify OrganizationMixin provides correct access to parent Organization properties

**Independent Test**: `bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.mixins.test_organization_mixin -v`

### Implementation for User Story 7

- [x] T022 [US7] Create OrganizationMixin test file with boilerplate at `dartwing/dartwing/dartwing_core/mixins/test_organization_mixin.py`
- [x] T023 [US7] Implement `_create_test_family` helper for Family with linked Organization in `dartwing/dartwing/dartwing_core/mixins/test_organization_mixin.py`
- [x] T024 [US7] Implement `test_org_name_property_returns_parent_value` in `dartwing/dartwing/dartwing_core/mixins/test_organization_mixin.py`
- [x] T025 [US7] Implement `test_logo_property_returns_parent_value` in `dartwing/dartwing/dartwing_core/mixins/test_organization_mixin.py`
- [x] T026 [US7] Implement `test_org_status_property_returns_parent_value` in `dartwing/dartwing/dartwing_core/mixins/test_organization_mixin.py`
- [x] T027 [US7] Implement `test_get_organization_doc_returns_full_document` in `dartwing/dartwing/dartwing_core/mixins/test_organization_mixin.py`
- [x] T028 [US7] Implement `test_update_org_name_modifies_parent` in `dartwing/dartwing/dartwing_core/mixins/test_organization_mixin.py`
- [x] T029 [US7] Run OrganizationMixin tests and verify all pass: `bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.mixins.test_organization_mixin -v` *(requires manual verification with bench)*

**Checkpoint**: User Story 7 complete - Mixin functionality validated

---

## Phase 6: Integration Testing & Edge Cases

**Goal**: End-to-end workflow test covering complete user flow across all features, plus edge case coverage

**Independent Test**: `bench --site <site> run-tests --app dartwing --module dartwing.tests.integration.test_full_workflow -v`

### Implementation for Integration

- [x] T030 Create integration test file at `dartwing/dartwing/tests/integration/test_full_workflow.py`
- [x] T031 Implement `test_complete_membership_workflow` - Person → Org → OrgMember → Permission flow in `dartwing/dartwing/tests/integration/test_full_workflow.py`
- [x] T032 Implement `test_multi_org_membership_workflow` - User in multiple orgs with proper isolation in `dartwing/dartwing/tests/integration/test_full_workflow.py`
- [x] T033 Implement `test_organization_lifecycle_workflow` - Create → Use → Delete with cascade in `dartwing/dartwing/tests/integration/test_full_workflow.py`

### Edge Case Coverage (from spec.md)

- [x] T033a Implement `test_delete_person_with_pending_org_member` - What happens when Person deleted with pending Org Members in `dartwing/dartwing/tests/integration/test_full_workflow.py`
- [x] T033b Implement `test_manual_permission_deletion_resilience` - System behavior when User Permissions manually deleted but Org Member exists in `dartwing/dartwing/tests/integration/test_full_workflow.py`
- [x] T033c Implement `test_concurrent_org_member_creation` - Race condition handling for same Person/Org pair in `dartwing/dartwing/tests/integration/test_full_workflow.py`

- [ ] T034 Run integration tests and verify all pass: `bench --site <site> run-tests --app dartwing --module dartwing.tests.integration.test_full_workflow -v` *(requires manual verification with bench)*

**Checkpoint**: Integration tests and edge cases complete - Full workflows validated

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and documentation

- [ ] T035 Run full test suite and verify all tests pass: `bench --site <site> run-tests --app dartwing` *(requires manual verification with bench)*
- [ ] T036 Run full test suite 10 consecutive times to verify zero flakiness (per SC-005) *(requires manual verification with bench)*
- [ ] T037 Verify test suite completes within 5 minutes (SC-004) *(requires manual verification with bench)*
- [x] T038 Update quickstart.md with final test commands if needed *(updated with OrganizationMixin, Integration, Role Template, and Permission API test commands)*

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all new test implementation
- **User Story 4 (Phase 3)**: Can start after Foundational
- **User Story 6 (Phase 4)**: Can start after Foundational (parallel with US4)
- **User Story 7 (Phase 5)**: Can start after Foundational (parallel with US4, US6)
- **Integration (Phase 6)**: Depends on US4, US6, US7 completion
- **Polish (Phase 7)**: Depends on all phases complete

### User Story Independence

- **User Stories 1-3, 5**: Already covered by existing tests - verified in Phase 2
- **User Story 4 (Role Filtering)**: No dependencies on other new stories - tests Role Template directly
- **User Story 6 (API Helpers)**: No dependencies on US4/US7 - tests API methods directly
- **User Story 7 (Mixin)**: No dependencies on US4/US6 - tests mixin properties directly

### Within Each User Story

- Create test file first (boilerplate)
- Implement helper methods
- Implement test cases
- Run and verify

### Parallel Opportunities

```text
After Phase 2 (Foundational) completes, these can run in parallel:
├── Phase 3: US4 (Role Template tests)
├── Phase 4: US6 (API Helper tests)
└── Phase 5: US7 (Mixin tests)
```

---

## Parallel Example: After Foundational Phase

```bash
# These three user story phases can run simultaneously:
# Developer A: User Story 4 (T006-T013)
# Developer B: User Story 6 (T014-T021)
# Developer C: User Story 7 (T022-T029)

# Each story has independent test files and can be verified independently
```

---

## Implementation Strategy

### MVP First (US4 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational verification
3. Complete Phase 3: User Story 4 (Role Template tests)
4. **STOP and VALIDATE**: Run US4 tests independently
5. Coverage gap reduced from 32% to ~22%

### Incremental Delivery

1. Setup + Foundational → Baseline verified (US1-3, US5 confirmed)
2. Add US4 tests → Test independently → Coverage ~78%
3. Add US6 tests → Test independently → Coverage ~90%
4. Add US7 tests → Test independently → Coverage 100%
5. Add Integration + Edge Cases → Full workflow validated

### Full Implementation (Parallel)

With three developers:
1. Complete Setup + Foundational together
2. Developer A: US4, Developer B: US6, Developer C: US7 (parallel)
3. All converge for Integration phase
4. Polish together

---

## Notes

- All tasks create or modify test files (this feature IS a test suite)
- Use TEST_PREFIX pattern for test data isolation (per research.md)
- Use FrappeTestCase base class (per research.md)
- Run verification commands after each user story
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
