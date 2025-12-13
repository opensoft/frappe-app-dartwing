# Tasks: Org Member DocType

**Input**: Design documents from `/specs/003-org-member-doctype/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, the Frappe project structure is:

- DocType: `dartwing/dartwing_core/doctype/org_member/`
- Hooks: `dartwing/hooks.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Create DocType directory structure and initial files

- [x] T001 Create org_member directory at dartwing/dartwing_core/doctype/org_member/
- [x] T002 Create `__init__.py` at dartwing/dartwing_core/doctype/org_member/__init__.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core DocType definition that MUST be complete before ANY user story validation can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Create org_member.json DocType definition with all fields per data-model.md at dartwing/dartwing_core/doctype/org_member/org_member.json
- [x] T004 Create org_member.py controller skeleton with OrgMember class at dartwing/dartwing_core/doctype/org_member/org_member.py
- [x] T005 Add doc_events hook for Person on_trash in dartwing/hooks.py

**Checkpoint**: Foundation ready - DocType exists and can be migrated

---

## Phase 3: User Story 1 - Add Member to Organization (Priority: P1) 🎯 MVP

**Goal**: Enable administrators to add new members to organizations with role assignment

**Independent Test**: Create Organization, Person, Role Template, then create Org Member linking them. Verify status defaults to Active and start_date to today.

### Implementation for User Story 1

- [x] T006 [US1] Implement validate_unique_membership() in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-002: unique person+org constraint)
- [x] T007 [US1] Implement validate_role_for_org_type() in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-003: role compatibility check)
- [x] T008 [US1] Implement before_insert() with start_date and status defaults in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-004, FR-005)
- [x] T009 [US1] Implement add_member_to_organization() whitelist method with reactivation logic in dartwing/dartwing_core/doctype/org_member/org_member.py (handles both new and reactivation per acceptance scenario 4)
- [x] T010 [US1] Create test_org_member.py with User Story 1 tests at dartwing/dartwing_core/doctype/org_member/test_org_member.py

**Checkpoint**: User Story 1 complete - Can add members with role validation and duplicate prevention

---

## Phase 4: User Story 2 - View Organization Members (Priority: P1)

**Goal**: Enable users to view all members of an organization with their details

**Independent Test**: Create multiple Org Members for an Organization, call get_members_for_organization(), verify all members returned with correct fields.

### Implementation for User Story 2

- [x] T011 [US2] Implement get_members_for_organization() whitelist method in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-013)
- [x] T012 [US2] Implement get_organizations_for_person() whitelist method in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-014)
- [x] T013 [US2] Add User Story 2 tests to dartwing/dartwing_core/doctype/org_member/test_org_member.py

**Checkpoint**: User Story 2 complete - Can list members for organization and organizations for person

---

## Phase 5: User Story 3 - Manage Member Status (Priority: P2)

**Goal**: Enable administrators to change member status (Active/Inactive/Pending) with end_date tracking

**Independent Test**: Create Org Member, change status to Inactive with end_date, verify persistence. Reactivate and verify start_date updates.

### Implementation for User Story 3

- [x] T014 [US3] Implement validate_end_date() in dartwing/dartwing_core/doctype/org_member/org_member.py (V-005: end_date >= start_date)
- [x] T015 [US3] Implement deactivate_member() whitelist method in dartwing/dartwing_core/doctype/org_member/org_member.py (sets status to Inactive with end_date)
- [x] T016 [US3] Add User Story 3 tests to dartwing/dartwing_core/doctype/org_member/test_org_member.py

**Checkpoint**: User Story 3 complete - Can manage member status with proper date tracking

---

## Phase 6: User Story 4 - Change Member Role (Priority: P2)

**Goal**: Enable administrators to change a member's assigned role within valid roles for the org type

**Independent Test**: Create Org Member with one role, change to different valid role, verify update. Try invalid role and verify rejection.

### Implementation for User Story 4

- [x] T017 [US4] Implement change_member_role() whitelist method in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-008)
- [x] T018 [US4] Add User Story 4 tests to dartwing/dartwing_core/doctype/org_member/test_org_member.py

**Checkpoint**: User Story 4 complete - Can change member roles with org type validation

---

## Phase 7: User Story 5 - Remove Member from Organization (Priority: P3)

**Goal**: Enable administrators to remove members with last-supervisor protection

**Independent Test**: Create Org Member and deactivate. Create org with single supervisor and verify removal blocked.

### Implementation for User Story 5

- [x] T019 [US5] Implement check_last_supervisor() helper in dartwing/dartwing_core/doctype/org_member/org_member.py (queries org for supervisor count)
- [x] T020 [US5] Implement validate_not_last_supervisor() in validate() method in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-015)
- [x] T021 [US5] Implement check_is_last_supervisor() whitelist method in dartwing/dartwing_core/doctype/org_member/org_member.py (API for checking)
- [x] T022 [US5] Add User Story 5 tests to dartwing/dartwing_core/doctype/org_member/test_org_member.py

**Checkpoint**: User Story 5 complete - Can remove members with supervisor protection

---

## Phase 8: Edge Cases & Cascade Handling

**Purpose**: Handle deletion cascades and edge cases across doctypes

- [x] T023 Implement handle_person_deletion() for soft-cascade in dartwing/dartwing_core/doctype/org_member/org_member.py (FR-010)
- [x] T024 Add edge case tests for Person deletion cascade in dartwing/dartwing_core/doctype/org_member/test_org_member.py
- [x] T025 Add edge case tests for Organization deletion cascade in dartwing/dartwing_core/doctype/org_member/test_org_member.py (FR-012: verify Frappe's standard Link cascade deletes Org Members when Organization is deleted)
- [x] T026 Add edge case tests for Role Template deletion prevention (verify existing hook works) in dartwing/dartwing_core/doctype/org_member/test_org_member.py

**Checkpoint**: All edge cases handled - cascade behaviors work correctly

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: Final validation and cleanup

- [ ] T027 Run all tests via `bench --site alpha.localhost run-tests --module dartwing.dartwing_core.doctype.org_member`
  - Note: `alpha.localhost` is the default dev container site. If using a different site, check `sites/` directory for your site name.
- [ ] T028 Validate quickstart.md examples work correctly
- [x] T029 [P] Run ruff check on all new Python files
- [x] T030 [P] Verify DocType permissions match data-model.md specification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 and US2 can proceed in parallel (both P1)
  - US3 and US4 can proceed in parallel (both P2)
  - US5 (P3) can start after Foundational
- **Edge Cases (Phase 8)**: Depends on US5 completion (needs supervisor validation)
- **Polish (Phase 9)**: Depends on all phases complete

### User Story Dependencies

- **User Story 1 (P1)**: Foundation only - no other story dependencies
- **User Story 2 (P1)**: Foundation only - no other story dependencies
- **User Story 3 (P2)**: Foundation only - uses reactivation from US1 but testable independently
- **User Story 4 (P2)**: Foundation only - no other story dependencies
- **User Story 5 (P3)**: Foundation only - builds on status concepts but testable independently

### Within Each User Story

- Validation methods before whitelist methods
- Core implementation before tests
- Each story adds tests to the same test file (cumulative)

### Parallel Opportunities

- T001 and T002 can run in parallel (different files)
- T011 and T012 can run in parallel (different methods, same file but independent)
- T029 and T030 can run in parallel (different validation tasks)
- User Stories 1 & 2 can run in parallel (both P1, no dependencies)
- User Stories 3 & 4 can run in parallel (both P2, no dependencies)

---

## Parallel Example: User Story 1 & 2

```bash
# After Phase 2 (Foundational) completes, launch US1 and US2 in parallel:

# Developer A - User Story 1:
Task: T006 "Implement validate_unique_membership() in org_member.py"
Task: T007 "Implement validate_role_for_org_type() in org_member.py"
Task: T008 "Implement before_insert() with defaults in org_member.py"
Task: T009 "Implement add_member_to_organization() whitelist in org_member.py"
Task: T010 "Create test_org_member.py with US1 tests"

# Developer B - User Story 2 (can start immediately after T004):
Task: T011 "Implement get_members_for_organization() whitelist in org_member.py"
Task: T012 "Implement get_organizations_for_person() whitelist in org_member.py"
Task: T013 "Add US2 tests to test_org_member.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add Member)
4. **STOP and VALIDATE**: Run bench migrate, test member creation
5. Deploy if ready - basic membership functionality works

### Incremental Delivery

1. Setup + Foundational → DocType exists
2. Add User Story 1 → Can add members → MVP!
3. Add User Story 2 → Can view members → List functionality
4. Add User Story 3 → Can manage status → Lifecycle management
5. Add User Story 4 → Can change roles → Role flexibility
6. Add User Story 5 → Last supervisor protection → Complete safety
7. Edge Cases + Polish → Production ready

### Single Developer Strategy

1. Complete Setup + Foundational sequentially
2. Complete US1, test thoroughly
3. Complete US2, test thoroughly
4. Complete US3 & US4 (can be interleaved since both P2)
5. Complete US5
6. Complete Edge Cases & Polish

---

## Notes

- [P] tasks = different files or independent operations, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- All tests go in a single test file (test_org_member.py) organized by user story sections
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- The existing Role Template on_trash hook already handles FR-011 (prevent deletion of in-use roles)
