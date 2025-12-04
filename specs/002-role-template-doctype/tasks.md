# Tasks: Role Template DocType

**Input**: Design documents from `/specs/002-role-template-doctype/`
**Prerequisites**: plan.md (required), spec.md (required), research.md (optional), data-model.md (optional), contracts/ (optional)

**Tests**: Tests are included as the plan.md indicates "tests required for business logic" per code quality standards.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Frappe DocType**: `dartwing/dartwing_core/doctype/role_template/`
- **Fixtures**: `dartwing/fixtures/`
- **Tests**: `dartwing/dartwing_core/doctype/role_template/test_role_template.py`

---

## Phase 1: Setup

**Purpose**: Create DocType directory structure and initialize files

- [x] T001 Create DocType directory at dartwing/dartwing_core/doctype/role_template/
- [x] T002 [P] Create `__init__.py` in dartwing/dartwing_core/doctype/role_template/`__init__.py`
- [x] T003 [P] Create empty controller file at dartwing/dartwing_core/doctype/role_template/role_template.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Update Organization DocType to use "Association" instead of "Club" - MUST complete before Role Template can work correctly

**⚠️ CRITICAL**: Role filtering depends on matching org_type values between Organization and Role Template

- [x] T004 Update Organization DocType org_type options from "Club" to "Association" in dartwing/dartwing_core/doctype/organization/organization.json
- [x] T005 Create data migration script to update existing "Club" records to "Association" in dartwing/patches/v0_0/update_org_type_club_to_association.py
- [x] T006 Register migration patch in dartwing/patches.txt
- [ ] T007 Run migration and verify Organization records are updated via bench migrate (deferred: migration requires new DocType to exist before running; must complete before proceeding to user stories)

**Checkpoint**: Organization DocType migration pending—must run T007 after DocType creation, then Role Template implementation can proceed

---

## Phase 3: User Story 1 - System Administrator Seeds Role Data (Priority: P1) 🎯 MVP

**Goal**: Create Role Template DocType with all fields and seed data fixtures for 14 predefined roles across all organization types

**Independent Test**: Deploy system and verify all expected roles exist for each organization type via `frappe.get_all("Role Template")`

### Tests for User Story 1

- [x] T008 [P] [US1] Create test file with test_fixture_loads_all_roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py
- [x] T009 [P] [US1] Add test_family_roles_exist to verify 4 Family roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py
- [x] T010 [P] [US1] Add test_company_roles_exist to verify 4 Company roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py
- [x] T011 [P] [US1] Add test_nonprofit_roles_exist to verify 3 Nonprofit roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py
- [x] T012 [P] [US1] Add test_association_roles_exist to verify 3 Association roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py

### Implementation for User Story 1

- [x] T013 [US1] Create Role Template DocType JSON with all fields (role_name, applies_to_org_type, is_supervisor, default_hourly_rate) in dartwing/dartwing_core/doctype/role_template/role_template.json
- [x] T014 [US1] Configure permissions in role_template.json: System Manager (full CRUD), Dartwing User (read-only)
- [x] T015 [US1] Create seed data fixture with all 14 roles in dartwing/fixtures/role_template.json
- [x] T016 [US1] Add Role Template to fixtures list in dartwing/hooks.py
- [ ] T017 [US1] Run bench migrate to create DocType in database (requires database access)
- [ ] T018 [US1] Run bench --site [site] import-fixtures to load seed data (requires database access)
- [ ] T019 [US1] Verify all tests pass: bench --site [site] run-tests --module dartwing.dartwing_core.doctype.role_template (requires database access)

**Checkpoint**: Role Template DocType exists with 14 predefined roles. US1 is independently testable and deliverable as MVP.

---

## Phase 4: User Story 2 - Organization Admin Assigns Roles to Members (Priority: P1)

**Goal**: Enable filtering of Role Templates by organization type for use in Org Member forms (Note: Org Member is Feature 3, but filtering query is prepared here)

**Independent Test**: Query Role Templates filtered by org_type and verify only matching roles returned

### Tests for User Story 2

- [x] T020 [P] [US2] Add test_filter_by_family_type returns only Family roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py
- [x] T021 [P] [US2] Add test_filter_by_company_type returns only Company roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py
- [x] T022 [P] [US2] Add test_filter_by_nonprofit_type returns only Nonprofit roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py
- [x] T023 [P] [US2] Add test_filter_by_association_type returns only Association roles in dartwing/dartwing_core/doctype/role_template/test_role_template.py

### Implementation for User Story 2

- [x] T024 [US2] Verify applies_to_org_type field is indexed (in_standard_filter: 1) in role_template.json
- [x] T025 [US2] Add whitelisted API method get_roles_for_org_type() with @frappe.whitelist() decorator in dartwing/dartwing_core/doctype/role_template/role_template.py
- [ ] T026 [US2] Document role filtering pattern for Org Member (Feature 3) in specs/002-role-template-doctype/quickstart.md
- [ ] T027 [US2] Verify all US2 tests pass (requires database access)

**Checkpoint**: Role Templates can be filtered by org_type. Ready for Org Member (Feature 3) integration.

---

## Phase 5: User Story 3 - System Enforces Supervisor Hierarchy (Priority: P2)

**Goal**: Ensure supervisor flags are correctly set on all roles for future permission system use

**Independent Test**: Query roles and verify is_supervisor flag matches expected values per seed data

### Tests for User Story 3

- [x] T028 [P] [US3] Add test_supervisor_flags_family verifies Parent=1, Child=0, Guardian=1, Extended Family=0 in test_role_template.py
- [x] T029 [P] [US3] Add test_supervisor_flags_company verifies Owner=1, Manager=1, Employee=0, Contractor=0 in test_role_template.py
- [x] T030 [P] [US3] Add test_supervisor_flags_nonprofit verifies Board Member=1, Volunteer=0, Staff=0 in test_role_template.py
- [x] T031 [P] [US3] Add test_supervisor_flags_association verifies President=1, Member=0, Honorary=0 in test_role_template.py

### Implementation for User Story 3

- [x] T032 [US3] Verify is_supervisor field is in_list_view for easy identification in role_template.json
- [x] T033 [US3] Add helper method is_supervisor_role(role_name) in dartwing/dartwing_core/doctype/role_template/role_template.py
- [ ] T034 [US3] Document supervisor hierarchy usage for Feature 5 (permissions) in quickstart.md
- [ ] T035 [US3] Verify all US3 tests pass (requires database access)

**Checkpoint**: Supervisor flags correctly identify supervisory roles. Ready for permission system (Feature 5).

---

## Phase 6: User Story 4 - Company Roles Include Hourly Rate (Priority: P3)

**Goal**: Implement conditional hourly rate field that only displays for Company roles

**Independent Test**: View Company role and verify hourly_rate visible; view Family role and verify hourly_rate hidden

### Tests for User Story 4

- [x] T036 [P] [US4] Add test_hourly_rate_visible_for_company verifies field accessible on Company roles in test_role_template.py
- [x] T037 [P] [US4] Add test_hourly_rate_cleared_for_non_company verifies rate is 0/null for non-Company roles in test_role_template.py

### Implementation for User Story 4

- [x] T038 [US4] Add depends_on="eval:doc.applies_to_org_type=='Company'" to default_hourly_rate field in role_template.json
- [x] T039 [US4] Add section_break_company with depends_on for Company Settings section in role_template.json
- [x] T040 [US4] Add validate() method to clear hourly_rate when org_type is not Company in role_template.py
- [ ] T041 [US4] Verify all US4 tests pass (requires database access)

**Checkpoint**: Hourly rate field conditionally displays only for Company roles.

---

## Phase 7: Edge Cases & Deletion Prevention

**Purpose**: Implement validation rules and deletion prevention per FR-002, FR-008

### Tests

- [x] T042 [P] Add test_duplicate_role_name_rejected verifies uniqueness constraint in test_role_template.py
- [x] T043 [P] Add test_missing_org_type_rejected verifies org_type is required in test_role_template.py
- [x] T044 [P] Add test_deletion_prevented_when_linked (placeholder - will work when Org Member exists) in test_role_template.py
- [x] T044a [P] Add test_read_access_for_dartwing_user verifies FR-009 (read access for authenticated users) in test_role_template.py
- [x] T044b [P] Add test_create_restricted_to_system_manager verifies FR-010 (write restriction) in test_role_template.py

### Implementation

- [x] T045 Verify unique=1 on role_name field in role_template.json
- [x] T046 Verify reqd=1 on applies_to_org_type field in role_template.json
- [x] T047 Implement on_trash() hook to prevent deletion when linked to Org Member in role_template.py
- [x] T048 Add graceful fallback in on_trash() when Org Member DocType doesn't exist yet
- [ ] T049 Verify all edge case tests pass (requires database access)

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final validation, documentation, and cleanup

- [ ] T050 [P] Run full test suite: bench --site [site] run-tests --module dartwing.dartwing_core.doctype.role_template
- [ ] T051 [P] Verify API access via curl: GET /api/resource/Role%20Template
- [ ] T052 [P] Verify filtered API: GET /api/resource/Role%20Template?filters=[["applies_to_org_type","=","Family"]]
- [x] T053 Update quickstart.md with final verification steps
- [ ] T054 Run bench --site [site] build to ensure no errors
- [ ] T055 Verify fixtures are idempotent: run import-fixtures twice without error

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories (org_type must be "Association")
- **User Story 1 (Phase 3)**: Depends on Foundational - Creates DocType and seed data
- **User Story 2 (Phase 4)**: Can start after US1 - Adds filtering capability
- **User Story 3 (Phase 5)**: Can start after US1 - Validates supervisor flags
- **User Story 4 (Phase 6)**: Can start after US1 - Adds conditional hourly rate
- **Edge Cases (Phase 7)**: Depends on US1 base implementation
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: FOUNDATIONAL - all other stories depend on DocType existing
- **User Story 2 (P1)**: Depends on US1 (needs DocType with data)
- **User Story 3 (P2)**: Depends on US1 (needs seed data to verify)
- **User Story 4 (P3)**: Depends on US1 (needs DocType JSON)

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- DocType JSON before controller
- Controller before fixtures
- Fixtures before tests can pass

### Parallel Opportunities

**Phase 1 (Setup)**:

```
Task: T002 Create __init__.py
Task: T003 Create empty controller
```

**Phase 3 (US1 Tests)**:

```
Task: T008 test_fixture_loads_all_roles
Task: T009 test_family_roles_exist
Task: T010 test_company_roles_exist
Task: T011 test_nonprofit_roles_exist
Task: T012 test_association_roles_exist
```

**Phase 4-6 (US2-4)**: Can run in parallel after US1 completes

```
Developer A: User Story 2 (filtering)
Developer B: User Story 3 (supervisor flags)
Developer C: User Story 4 (hourly rate)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (org_type migration)
3. Complete Phase 3: User Story 1 (DocType + seed data)
4. **STOP and VALIDATE**: Verify 14 roles exist via Frappe console
5. Deploy/demo if ready - Role Templates are available!

### Incremental Delivery

1. Setup + Foundational → Ready for DocType creation
2. Add User Story 1 → DocType + Fixtures deployed (MVP!)
3. Add User Story 2 → Filtering ready for Org Member (Feature 3)
4. Add User Story 3 → Supervisor hierarchy documented
5. Add User Story 4 → Company-specific features complete
6. Edge Cases + Polish → Production ready

### Single Developer Timeline

1. Phase 1-2: Setup + Foundational (T001-T007)
2. Phase 3: US1 - Core DocType (T008-T019) ← MVP
3. Phase 4: US2 - Filtering (T020-T027)
4. Phase 5: US3 - Supervisor flags (T028-T035)
5. Phase 6: US4 - Hourly rate (T036-T041)
6. Phase 7-8: Edge cases + Polish (T042-T055)

---

## Task Summary

| Phase           | Story                | Tasks  | Parallel Tasks |
| --------------- | -------------------- | ------ | -------------- |
| 1. Setup        | -                    | 3      | 2              |
| 2. Foundational | -                    | 4      | 0              |
| 3. US1 (P1)     | Seeds Role Data      | 12     | 5              |
| 4. US2 (P1)     | Filter by Org Type   | 8      | 4              |
| 5. US3 (P2)     | Supervisor Hierarchy | 8      | 4              |
| 6. US4 (P3)     | Hourly Rate          | 6      | 2              |
| 7. Edge Cases   | -                    | 10     | 5              |
| 8. Polish       | -                    | 6      | 3              |
| **Total**       |                      | **57** | **25**         |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable after US1
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US1 is the MVP - all other stories add incremental value
