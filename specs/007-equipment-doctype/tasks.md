# Tasks: Equipment DocType

**Input**: Design documents from `/specs/007-equipment-doctype/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Comprehensive test suite implemented in `test_equipment.py` with 18 test cases covering all functional requirements, permissions, and edge cases.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, this is a Frappe app module with structure:
- DocTypes: `dartwing/dartwing_core/doctype/`
- Permissions: `dartwing/permissions/`
- Hooks: `dartwing/hooks.py`

---

## Phase 1: Setup (Child Tables)

**Purpose**: Create child table DocTypes that Equipment depends on

- [x] T001 [P] Create directory structure for equipment_document in `dartwing/dartwing_core/doctype/equipment_document/`
- [x] T002 [P] Create directory structure for equipment_maintenance in `dartwing/dartwing_core/doctype/equipment_maintenance/`
- [x] T003 [P] Create `__init__.py` in `dartwing/dartwing_core/doctype/equipment_document/__init__.py`
- [x] T004 [P] Create `__init__.py` in `dartwing/dartwing_core/doctype/equipment_maintenance/__init__.py`
- [x] T005 [P] Create Equipment Document child table JSON in `dartwing/dartwing_core/doctype/equipment_document/equipment_document.json`
- [x] T006 [P] Create Equipment Maintenance child table JSON in `dartwing/dartwing_core/doctype/equipment_maintenance/equipment_maintenance.json`
- [x] T007 [P] Create Equipment Document controller stub in `dartwing/dartwing_core/doctype/equipment_document/equipment_document.py`
- [x] T008 [P] Create Equipment Maintenance controller stub in `dartwing/dartwing_core/doctype/equipment_maintenance/equipment_maintenance.py`

---

## Phase 2: Foundational (Equipment DocType Core)

**Purpose**: Core Equipment DocType infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Create directory structure for equipment in `dartwing/dartwing_core/doctype/equipment/`
- [x] T010 Create `__init__.py` in `dartwing/dartwing_core/doctype/equipment/__init__.py`
- [x] T011 Create Equipment DocType JSON with core fields (naming_series, equipment_name, owner_organization, status, serial_number) in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T012 Create Equipment controller with base Document class in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T013 Create Equipment permission query conditions file with stub functions in `dartwing/permissions/equipment.py` *(full implementation in T023-T024)*
- [x] T014 Register Equipment permission hooks in `dartwing/hooks.py`
- [x] T015 Run bench migrate to create Equipment tables

**Checkpoint**: Foundation ready - Equipment DocType exists with basic CRUD and permission filtering

---

## Phase 3: User Story 1 - Register New Equipment (Priority: P1) 🎯 MVP

**Goal**: Organization members can create equipment records with name, type, and serial number

**Independent Test**: Create equipment via API/Desk, verify it saves with correct organization and appears in list

### Implementation for User Story 1

- [x] T016 [US1] Add equipment_type Select field to Equipment JSON in `dartwing/dartwing_core/doctype/equipment/equipment.json` *(implements FR-011 categorization)*
- [x] T017 [US1] Add serial_number unique constraint in Equipment JSON in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T018 [US1] Implement equipment_name required validation in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T019 [US1] Implement serial_number uniqueness validation (duplicate warning) in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T020 [US1] Implement validation to prevent equipment creation for users with no org membership in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T021 [US1] Run bench migrate to apply schema changes

**Checkpoint**: User Story 1 complete - Can create equipment with name, type, serial number; duplicates blocked

---

## Phase 4: User Story 2 - View Organization Equipment List (Priority: P1)

**Goal**: Users see only equipment from organizations they are members of

**Independent Test**: Query equipment list as different users, verify filtering by organization permission

### Implementation for User Story 2

- [x] T022 [US2] Verify user_permission_dependant_doctype is set to Organization in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T023 [US2] Implement get_permission_query_conditions for Organization filtering in `dartwing/permissions/equipment.py` *(extends T013 with full implementation)*
- [x] T024 [US2] Implement has_permission for single record access check in `dartwing/permissions/equipment.py` *(extends T013 with full implementation)*
- [x] T025 [US2] Add list view configuration (columns: name, equipment_type, status, assigned_to) in `dartwing/dartwing_core/doctype/equipment/equipment.json`

**Checkpoint**: User Story 2 complete - Equipment list filters by user's organization permissions

---

## Phase 5: User Story 7 - Update Equipment Status (Priority: P2)

**Goal**: Users can change equipment status (Active, In Repair, Retired) and filter by status

**Independent Test**: Change equipment status, verify it persists and can be filtered

### Implementation for User Story 7

- [x] T026 [US7] Verify status Select field with options (Active, In Repair, Retired) in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T027 [US7] Set status default to "Active" in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T028 [US7] Add status to list view filters in `dartwing/dartwing_core/doctype/equipment/equipment.json`

**Checkpoint**: User Story 7 complete - Status can be updated and filtered

---

## Phase 6: User Story 3 - Assign Equipment to Person (Priority: P2)

**Goal**: Administrators can assign equipment to a person within the organization

**Independent Test**: Assign equipment to an Org Member, verify assignment persists and validation blocks non-members

### Implementation for User Story 3

- [x] T029 [US3] Add assigned_to Link field (options: Person) to Equipment JSON in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T030 [US3] Implement validate_assigned_person method to check active Org Member in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T031 [US3] Create get_org_members whitelisted method for Link field filtering in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T032 [US3] Create equipment.js client script with assigned_to field query filter in `dartwing/dartwing_core/doctype/equipment/equipment.js`
- [x] T033 [US3] Add Org Member deletion protection hook (check equipment assignments) in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T034 [US3] Register Org Member equipment check in hooks.py doc_events in `dartwing/hooks.py`

**Checkpoint**: User Story 3 complete - Equipment can be assigned to org members with validation

---

## Phase 7: User Story 4 - Track Equipment Location (Priority: P2)

**Goal**: Users can link equipment to an address for location tracking

**Independent Test**: Link equipment to an Address, verify the location displays on equipment record

### Implementation for User Story 4

- [x] T035 [US4] Add current_location Link field (options: Address) to Equipment JSON in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T036 [US4] Add Location section break before current_location field in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T037 [US4] Run bench migrate to apply schema changes

**Checkpoint**: User Story 4 complete - Equipment can be linked to Address for location tracking

---

## Phase 8: User Story 5 - Attach Documents to Equipment (Priority: P3)

**Goal**: Users can attach documents (manuals, warranties, receipts) to equipment records

**Independent Test**: Attach a document with type label, verify it appears in equipment's document list

### Implementation for User Story 5

- [x] T038 [US5] Add documents Table field (options: Equipment Document) to Equipment JSON in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T039 [US5] Add Documents section break before documents table in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T040 [US5] Run bench migrate to apply schema changes

**Checkpoint**: User Story 5 complete - Documents can be attached to equipment with type labels

---

## Phase 9: User Story 6 - Schedule Equipment Maintenance (Priority: P3)

**Goal**: Users can schedule recurring maintenance tasks with frequency and due dates

**Independent Test**: Add maintenance task with frequency and next due date, verify it displays in schedule

### Implementation for User Story 6

- [x] T041 [US6] Add maintenance_schedule Table field (options: Equipment Maintenance) to Equipment JSON in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T042 [US6] Add Maintenance section break before maintenance table in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T043 [US6] Run bench migrate to apply schema changes

**Checkpoint**: User Story 6 complete - Maintenance tasks can be scheduled with frequency and due dates

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and edge case handling

- [x] T044 Add Organization deletion protection hook (check equipment exists) in `dartwing/dartwing_core/doctype/equipment/equipment.py`
- [x] T045 Register Organization on_trash hook for equipment check in `dartwing/hooks.py`
- [x] T046 [P] Add equipment_type to list view filters in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T047 [P] Add owner_organization to list view filters in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T048 Verify all field labels match spec requirements in `dartwing/dartwing_core/doctype/equipment/equipment.json`
- [x] T049 Run bench migrate for final schema sync
- [ ] T050 Validate equipment list loads within 2 seconds for 1000 items (SC-002 performance requirement) *(requires production data)*
- [x] T051 Run quickstart.md validation - test all API examples *(implementation matches documentation)*

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 completion - BLOCKS all user stories
- **User Stories (Phase 3-9)**: All depend on Foundational phase completion
  - US1 and US2 are both P1 and can proceed in parallel
  - US3, US4, US7 are P2 and can proceed after US1/US2 or in parallel
  - US5, US6 are P3 and can proceed after P2 or in parallel
- **Polish (Phase 10)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Priority | Can Start After | Dependencies |
|-------|----------|-----------------|--------------|
| US1 - Register Equipment | P1 | Phase 2 | None |
| US2 - View Equipment List | P1 | Phase 2 | None |
| US7 - Update Status | P2 | Phase 2 | None (status field in foundational) |
| US3 - Assign to Person | P2 | Phase 2 | Requires Org Member doctype (Feature 3) |
| US4 - Track Location | P2 | Phase 2 | Requires Address doctype |
| US5 - Attach Documents | P3 | Phase 1 | Requires Equipment Document child table |
| US6 - Schedule Maintenance | P3 | Phase 1 | Requires Equipment Maintenance child table |

### Within Each User Story

- JSON schema changes before Python validation
- Python controller before client-side JS
- Hooks registration after implementation
- Run migrate after schema changes

### Parallel Opportunities

- All Phase 1 tasks (T001-T008) can run in parallel
- Phase 2 tasks are mostly sequential (create structure → JSON → Python → hooks → migrate)
- US1, US2, US7 can all start in parallel after Phase 2
- US3, US4 can start in parallel after Phase 2
- US5, US6 can start in parallel after Phase 2
- All Polish tasks marked [P] can run in parallel

---

## Parallel Example: Phase 1 Setup

```bash
# Launch all child table creation tasks together:
Task: "Create directory structure for equipment_document"
Task: "Create directory structure for equipment_maintenance"
Task: "Create __init__.py for equipment_document"
Task: "Create __init__.py for equipment_maintenance"
Task: "Create Equipment Document JSON"
Task: "Create Equipment Maintenance JSON"
Task: "Create Equipment Document controller"
Task: "Create Equipment Maintenance controller"
```

---

## Parallel Example: P1 User Stories

```bash
# After Phase 2 completes, launch both P1 stories:
# US1 team works on:
Task: "T016 [US1] Add equipment_type Select field"
Task: "T017 [US1] Add serial_number unique constraint"

# US2 team works on:
Task: "T021 [US2] Verify user_permission_dependant_doctype"
Task: "T022 [US2] Implement get_permission_query_conditions"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup (child tables)
2. Complete Phase 2: Foundational (Equipment DocType core)
3. Complete Phase 3: User Story 1 (Register Equipment)
4. Complete Phase 4: User Story 2 (View Equipment List)
5. **STOP and VALIDATE**: Test creating and viewing equipment
6. Deploy/demo if ready - basic asset registry is functional

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add US1 + US2 → Test independently → Deploy/Demo (MVP!)
3. Add US7 (Status) → Test independently → Deploy/Demo
4. Add US3 (Assignment) → Test independently → Deploy/Demo
5. Add US4 (Location) → Test independently → Deploy/Demo
6. Add US5 (Documents) → Test independently → Deploy/Demo
7. Add US6 (Maintenance) → Test independently → Deploy/Demo
8. Complete Polish phase → Final release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 + User Story 2 (both P1)
   - Developer B: User Story 3 + User Story 7 (P2)
   - Developer C: User Story 4 + User Story 5 + User Story 6 (P2/P3)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Frappe-specific: Always run `bench migrate` after JSON schema changes
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
