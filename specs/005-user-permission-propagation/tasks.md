# Tasks: User Permission Propagation

**Input**: Design documents from `/specs/005-user-permission-propagation/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in spec. Tests NOT included (can be added via separate request).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frappe App**: `dartwing/` at repository root
- **Permissions Module**: `dartwing/permissions/`
- **Utilities**: `dartwing/utils/`
- **Hooks**: `dartwing/hooks.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create module structure and base infrastructure

- [x] T001 Create permissions module directory structure at dartwing/permissions/
- [x] T002 [P] Create dartwing/permissions/__init__.py with module exports
- [x] T003 [P] Create dartwing/utils/ directory if not exists
- [x] T004 [P] Create dartwing/utils/permission_logger.py with log_permission_event function per research.md

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

**Dependencies**: See spec.md "Dependencies" section. This feature assumes Feature 3's unique constraint on Org Member (person + organization) exists. The permission helpers are idempotent (safe to re-run), but correct behavior depends on no duplicate Org Members existing—otherwise permission removal may leave orphaned memberships without access.

- [x] T005 Create dartwing/permissions/helpers.py with _create_permission and _delete_permission utility functions
- [x] T006 Add doc_events hook registration for Org Member in dartwing/hooks.py (after_insert, on_trash, on_update)
- [x] T007 Implement create_user_permissions function in dartwing/permissions/helpers.py - creates permissions for BOTH Organization AND concrete type (FR-001, FR-002, FR-007)
- [x] T008 Implement remove_user_permissions function in dartwing/permissions/helpers.py - removes permissions for BOTH Organization AND concrete type (FR-003)
- [x] T009 Implement handle_status_change function in dartwing/permissions/helpers.py (FR-009)

**Checkpoint**: Foundation ready - permission propagation hooks are in place

---

## Phase 3: User Story 1 - Single Organization Member Access (Priority: P1)

**Goal**: Users joining an organization automatically receive permissions and can only see that organization's data

**Independent Test**: Create a Person with Frappe User, add as Org Member to one Organization, verify they can only see that Organization's data in list views

### Implementation for User Story 1

- [x] T010 [P] [US1] Create dartwing/permissions/organization.py with get_permission_query_conditions function including System Manager bypass (FR-004, FR-006, FR-010)
- [x] T011 [P] [US1] Add has_permission function to dartwing/permissions/organization.py including System Manager bypass (FR-005, FR-006, FR-011)
- [x] T012 [US1] Register permission_query_conditions hook for Organization in dartwing/hooks.py
- [x] T013 [US1] Register has_permission hook for Organization in dartwing/hooks.py
- [x] T014 [US1] Add audit logging calls to create_user_permissions in dartwing/permissions/helpers.py (FR-012)
- [x] T015 [US1] Add audit logging calls to remove_user_permissions in dartwing/permissions/helpers.py (FR-012)

**Checkpoint**: User Story 1 complete - single org users see only their org's Organization records

---

## Phase 4: User Story 2 - Multi-Organization Access (Priority: P1)

**Goal**: Users belonging to multiple organizations can access data from all their organizations

**Independent Test**: Add a Person as Org Member to two different Organizations, verify they can see both in list views, but not a third organization

### Implementation for User Story 2

- [x] T016 [US2] Verify get_permission_query_conditions handles multiple User Permissions (IN clause) in dartwing/permissions/organization.py
- [x] T017 [US2] Verify has_permission checks all User Permissions for multi-org users in dartwing/permissions/organization.py
- [x] T018 [US2] Implement get_user_organizations API endpoint in dartwing/permissions/api.py per contracts/permissions-api.yaml
- [x] T019 [US2] Implement check_organization_access API endpoint in dartwing/permissions/api.py per contracts/permissions-api.yaml

**Checkpoint**: User Story 2 complete - multi-org users see combined data from all their organizations

---

## Phase 5: User Story 3 - Concrete Type Permission Inheritance (Priority: P2)

**Goal**: Users with Organization permission automatically get access to concrete type records (Family, Company, etc.)

**Independent Test**: Create Org Member for a Company org type, verify user can access both Organization and linked Company record

### Implementation for User Story 3

- [x] T020 [P] [US3] Create dartwing/permissions/family.py with get_permission_query_conditions and has_permission functions (include System Manager bypass per FR-006)
- [x] T021 [P] [US3] Create dartwing/permissions/company.py with get_permission_query_conditions and has_permission functions (include System Manager bypass per FR-006)
- [x] T022 [P] [US3] Create dartwing/permissions/association.py with get_permission_query_conditions and has_permission functions (include System Manager bypass per FR-006)
- [x] T023 [P] [US3] Create dartwing/permissions/nonprofit.py with get_permission_query_conditions and has_permission functions (include System Manager bypass per FR-006)
- [x] T024 [US3] Register permission_query_conditions hooks for Family, Company, Association, Nonprofit in dartwing/hooks.py
- [x] T025 [US3] Register has_permission hooks for Family, Company, Association, Nonprofit in dartwing/hooks.py
- [x] T026 [US3] Verify create_user_permissions creates concrete type permission (implemented in T007) via manual test
- [x] T027 [US3] Verify remove_user_permissions removes concrete type permission (implemented in T008) via manual test

**Checkpoint**: User Story 3 complete - concrete type permissions work automatically

---

## Phase 6: User Story 4 - Permission Removal on Membership End (Priority: P2)

**Goal**: Permissions are revoked when Org Member is deleted or status changes to Inactive

**Independent Test**: Create Org Member, verify permissions exist, delete Org Member, verify permissions removed

### Implementation for User Story 4

- [x] T028 [US4] Verify on_trash hook removes all User Permissions in dartwing/permissions/helpers.py (FR-003)
- [x] T029 [US4] Verify handle_status_change removes permissions when status becomes Inactive in dartwing/permissions/helpers.py (FR-009)
- [x] T030 [US4] Verify handle_status_change re-creates permissions when status becomes Active from Inactive in dartwing/permissions/helpers.py
- [x] T031 [US4] Add skip logging for remove when no User exists in dartwing/permissions/helpers.py (FR-012)

**Checkpoint**: User Story 4 complete - permission revocation works on delete and status change

---

## Phase 7: User Story 5 - System Administrator Override (Priority: P3)

**Goal**: System Managers can access all organizations regardless of membership

**Independent Test**: Login as System Manager without Org Member records, verify access to any Organization

**Note on Dartwing Admin**: Per clarification, "Dartwing Admin" role users access orgs via their Org Member records with supervisor/admin roles. This requires NO special code - the standard permission system handles it. Dartwing Admin is NOT a global bypass like System Manager.

### Implementation for User Story 5

- [x] T032 [US5] Verify System Manager bypass works in get_permission_query_conditions (implemented in T010) via manual test
- [x] T033 [US5] Verify System Manager bypass works in has_permission (implemented in T011) via manual test
- [x] T034 [P] [US5] Verify System Manager bypass works in all concrete type permission files (implemented in T020-T023) via manual test
- [x] T035 [US5] Implement get_organization_members API endpoint in dartwing/permissions/api.py per contracts/permissions-api.yaml
- [x] T036 [US5] Implement get_permission_audit_log API endpoint (admin only) in dartwing/permissions/api.py per contracts/permissions-api.yaml

**Checkpoint**: User Story 5 complete - System Managers have unrestricted access

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T037 [P] Add docstrings and type hints to all functions in dartwing/permissions/
- [x] T038 [P] Update dartwing/permissions/__init__.py with all public exports
- [x] T039 Validate hooks.py has all required registrations per research.md
- [x] T040 Run quickstart.md validation steps manually (requires running Frappe site)
- [x] T041 Clear Frappe cache and verify permission hooks are active (requires running Frappe site)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 and US2 are both P1 priority
  - US3 and US4 are both P2 priority
  - US5 is P3 priority
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Builds on US1's organization.py but no blocking dependency
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on US1/US2
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Validates foundational hooks work correctly
- **User Story 5 (P3)**: Can start after US1/US3 complete (verification tasks only - bypass implemented in US1/US3)

### Within Each User Story

- Permission query functions before hooks registration
- Hooks registration before integration
- Core implementation before API endpoints
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- T020-T023 (concrete type permission files) can all run in parallel
- T010-T011 (organization.py functions) can run in parallel
- After Phase 2, US1/US2/US3/US4 can start in parallel (if team capacity allows)

---

## Parallel Example: User Story 3

```bash
# Launch all concrete type permission files together:
Task: "Create dartwing/permissions/family.py with get_permission_query_conditions and has_permission functions"
Task: "Create dartwing/permissions/company.py with get_permission_query_conditions and has_permission functions"
Task: "Create dartwing/permissions/association.py with get_permission_query_conditions and has_permission functions"
Task: "Create dartwing/permissions/nonprofit.py with get_permission_query_conditions and has_permission functions"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test single-org permission isolation
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → MVP!
3. Add User Story 2 → Test multi-org → Enhanced MVP
4. Add User Story 3 → Test concrete types → Full type support
5. Add User Story 4 → Test revocation → Complete lifecycle
6. Add User Story 5 → Test admin bypass → Full feature

### Recommended Order for Solo Developer

1. Phase 1: Setup (T001-T004)
2. Phase 2: Foundational (T005-T009)
3. Phase 3: US1 (T010-T015) - Validates basic flow
4. Phase 5: US3 (T020-T027) - Adds concrete types
5. Phase 4: US2 (T016-T019) - Enhances multi-org
6. Phase 6: US4 (T028-T031) - Completes lifecycle
7. Phase 7: US5 (T032-T036) - Admin features
8. Phase 8: Polish (T037-T041)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Frappe cache clear required after hooks.py changes
- Test with `bench --site [site] console` for quick validation
