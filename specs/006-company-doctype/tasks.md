# Tasks: Company DocType

**Input**: Design documents from `/specs/006-company-doctype/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

Based on plan.md, this is a Frappe DocType module with paths:
- **Core module**: `dartwing/dartwing_core/`
- **Company module**: `dartwing/dartwing_company/` (NEW)
- **Tests**: `dartwing/dartwing_company/doctype/company/test_company.py`

---

## Phase 1: Setup (Module Infrastructure)

**Purpose**: Create dartwing_company module structure and shared child tables

- [x] T001 Create dartwing_company module directory structure in dartwing/dartwing_company/
- [x] T002 [P] Create dartwing_company/__init__.py with module docstring
- [x] T003 [P] Create dartwing_company/doctype/__init__.py
- [x] T004 Register "Dartwing Company" in dartwing/modules.txt

---

## Phase 2: Foundational (Shared Child Tables)

**Purpose**: Create child tables in dartwing_core that MUST exist before Company DocType can reference them

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T005 Create organization_officer directory in dartwing/dartwing_core/doctype/organization_officer/
- [x] T006 [P] Create organization_officer/__init__.py
- [x] T007 [P] Create organization_officer.json with fields: person (Link->Person, reqd), title (Data, reqd), start_date (Date), end_date (Date) in dartwing/dartwing_core/doctype/organization_officer/organization_officer.json
- [x] T008 [P] Create organization_officer.py with date validation (end_date >= start_date) in dartwing/dartwing_core/doctype/organization_officer/organization_officer.py
- [x] T009 Create organization_member_partner directory in dartwing/dartwing_core/doctype/organization_member_partner/
- [x] T010 [P] Create organization_member_partner/__init__.py
- [x] T011 [P] Create organization_member_partner.json with fields: person (Link->Person, reqd), ownership_percent (Percent), capital_contribution (Currency), voting_rights (Percent) in dartwing/dartwing_core/doctype/organization_member_partner/organization_member_partner.json
- [x] T012 [P] Create organization_member_partner.py (empty controller) in dartwing/dartwing_core/doctype/organization_member_partner/organization_member_partner.py
- [x] T013 Create OrganizationMixin class in dartwing/dartwing_core/mixins/organization_mixin.py with org_name, logo, org_status properties
- [ ] T014 Run `bench migrate` to create child table database tables

**Checkpoint**: Foundation ready - child tables and mixin exist, user story implementation can begin

---

## Phase 3: User Story 1 - Create Company Organization (Priority: P1) MVP

**Goal**: Enable automatic creation of Company record when Organization with org_type="Company" is created

**Independent Test**: Create Organization with org_type="Company" and verify linked Company record is auto-created with proper bidirectional references

### Implementation for User Story 1

- [x] T015 Create company directory in dartwing/dartwing_company/doctype/company/
- [x] T016 [P] [US1] Create company/__init__.py
- [x] T017 [US1] Create company.json with naming_series (CO-.#####), organization (Link->Organization, reqd, read_only) in dartwing/dartwing_company/doctype/company/company.json
- [x] T018 [US1] Create company.py controller inheriting OrganizationMixin in dartwing/dartwing_company/doctype/company/company.py
- [x] T019 [US1] Update Organization.py to remove "if != Family" guard and add Company creation logic with legal_name mapping in dartwing/dartwing_core/doctype/organization/organization.py
- [x] T020 [US1] Add cascade delete logic for Company in Organization.on_trash() method in dartwing/dartwing_core/doctype/organization/organization.py
- [ ] T021 [US1] Run `bench migrate` to create Company table
- [ ] T022 [US1] Test: Create Organization with org_type="Company" and verify Company auto-creation

**Checkpoint**: User Story 1 complete - Companies are auto-created from Organizations

---

## Phase 4: User Story 2 - Record Legal Entity Information (Priority: P1)

**Goal**: Enable company administrators to record legal entity details (name, tax ID, entity type, jurisdiction)

**Independent Test**: Edit Company record's legal fields and verify they save/retrieve correctly

### Implementation for User Story 2

- [x] T023 [US2] Add legal_name (Data) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T024 [P] [US2] Add tax_id (Data) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T025 [P] [US2] Add entity_type (Select) field with options: C-Corp, S-Corp, LLC, Limited Partnership (LP), General Partnership, LLP, WFOE (China), Benefit Corporation, Cooperative in dartwing/dartwing_company/doctype/company/company.json
- [x] T026 [P] [US2] Add jurisdiction_country (Link->Country) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T027 [P] [US2] Add jurisdiction_state (Data) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T028 [P] [US2] Add formation_date (Date) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T029 [US2] Add section breaks for legal information grouping in company.json in dartwing/dartwing_company/doctype/company/company.json
- [ ] T030 [US2] Run `bench migrate` to apply schema changes
- [ ] T031 [US2] Test: Edit Company legal fields and verify persistence

**Checkpoint**: User Story 2 complete - Legal entity information can be recorded

---

## Phase 5: User Story 3 - Manage Officers and Directors (Priority: P2)

**Goal**: Enable tracking of company officers and directors with Person reference, title, and date range

**Independent Test**: Add, edit, and remove officer entries and verify child table operations

### Implementation for User Story 3

- [x] T032 [US3] Add officers section break to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T033 [US3] Add officers (Table->Organization Officer) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [ ] T034 [US3] Run `bench migrate` to apply schema changes
- [ ] T035 [US3] Test: Add officer with Person, title, start_date and verify child table storage

**Checkpoint**: User Story 3 complete - Officers can be tracked

---

## Phase 6: User Story 4 - Track LLC/Partnership Ownership (Priority: P2)

**Goal**: Enable recording of members/partners with ownership percentage, capital contribution, voting rights for LLCs and partnerships

**Independent Test**: Select LLC entity type, add member entries with ownership details, verify conditional visibility and data storage

### Implementation for User Story 4

- [x] T036 [US4] Add section_ownership with depends_on condition for LLC/LP/LLP/GP entity types in dartwing/dartwing_company/doctype/company/company.json
- [x] T037 [US4] Add members_partners (Table->Organization Member Partner) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T038 [US4] Add ownership percentage validation warning in company.py validate() method in dartwing/dartwing_company/doctype/company/company.py
- [ ] T039 [US4] Run `bench migrate` to apply schema changes
- [ ] T040 [US4] Test: Set entity_type to LLC, verify ownership section visible, add member and verify storage
- [ ] T041 [US4] Test: Set entity_type to C-Corp, verify ownership section hidden

**Checkpoint**: User Story 4 complete - LLC/Partnership ownership tracking works

---

## Phase 7: User Story 5 - Manage Company Addresses (Priority: P3)

**Goal**: Enable linking of Address records for registered and physical addresses, plus registered agent Person reference

**Independent Test**: Link Address records to Company and verify references are stored

### Implementation for User Story 5

- [x] T042 [US5] Add section_addresses section break to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T043 [P] [US5] Add registered_address (Link->Address) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T044 [P] [US5] Add physical_address (Link->Address) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T045 [P] [US5] Add registered_agent (Link->Person) field to company.json in dartwing/dartwing_company/doctype/company/company.json
- [ ] T046 [US5] Run `bench migrate` to apply schema changes
- [ ] T047 [US5] Test: Link Address and Person to Company address fields

**Checkpoint**: User Story 5 complete - Address management functional

---

## Phase 8: Permissions, Security & Edge Cases

**Purpose**: Implement permission inheritance from Organization and handle edge cases

- [x] T048 Add permissions array to company.json (System Manager full, Dartwing User read/write) in dartwing/dartwing_company/doctype/company/company.json
- [x] T049 Add user_permission_dependant_doctype="Organization" to company.json in dartwing/dartwing_company/doctype/company/company.json
- [x] T050 Create permissions.py with get_permission_query_conditions_company() function in dartwing/dartwing_company/permissions.py
- [x] T051 Register permission hook in dartwing/hooks.py for Company permission_query_conditions
- [ ] T052 Test: Verify user without Organization permission cannot access Company
- [x] T053 Add on_delete validation for Person to prevent deletion when linked as officer/member in dartwing/dartwing_core/doctype/person/person.py
- [x] T054 Add entity_type change warning in company.js client script in dartwing/dartwing_company/doctype/company/company.js

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: API helpers, code cleanup, documentation

- [x] T055 [P] Create api.py with get_company_with_org_details() whitelist method in dartwing/dartwing_company/api.py
- [x] T056 [P] Add get_user_companies() whitelist method to api.py in dartwing/dartwing_company/api.py
- [x] T057 [P] Add validate_ownership() whitelist method to api.py in dartwing/dartwing_company/api.py
- [x] T058 Create test_company.py with unit tests covering: auto-creation, bidirectional link, ownership warning in dartwing/dartwing_company/doctype/company/test_company.py
- [x] T059 Create test_company_integration.py with integration tests for cascade delete (SC-007) in dartwing/tests/integration/test_company_integration.py
- [x] T060 Add in_list_view and in_standard_filter flags to key fields in company.json
- [ ] T061 [P] Generate OpenAPI 3.0 schema for Company endpoints in specs/006-company-doctype/contracts/openapi.yaml
- [x] T062 [P] Add audit logging for Company create/update/delete operations in dartwing/dartwing_company/doctype/company/company.py
- [ ] T063 Run quickstart.md validation steps to verify all functionality
- [ ] T064 Run ruff check . to verify code quality

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - creates Company DocType
- **User Story 2 (Phase 4)**: Depends on US1 (Company must exist) - adds legal fields
- **User Story 3 (Phase 5)**: Depends on Foundational (Organization Officer exists) and US1 (Company exists)
- **User Story 4 (Phase 6)**: Depends on Foundational (Organization Member Partner exists), US1, and US2 (entity_type field)
- **User Story 5 (Phase 7)**: Depends on US1 (Company exists)
- **Permissions & Edge Cases (Phase 8)**: Depends on US1 (Company exists) - includes Person deletion handling and entity_type warnings
- **Polish (Phase 9)**: Depends on all user stories being complete

### User Story Dependencies

```
                    ┌─────────────────────┐
                    │   Setup (Phase 1)   │
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │ Foundational (Ph 2) │
                    │ (Child Tables/Mixin)│
                    └──────────┬──────────┘
                               │
                    ┌──────────▼──────────┐
                    │  US1: Create Org    │ ◄── MVP
                    │    (Phase 3)        │
                    └──────────┬──────────┘
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
┌─────────▼─────────┐ ┌────────▼────────┐ ┌────────▼────────┐
│  US2: Legal Info  │ │  US3: Officers  │ │  US5: Addresses │
│    (Phase 4)      │ │    (Phase 5)    │ │    (Phase 7)    │
└─────────┬─────────┘ └─────────────────┘ └─────────────────┘
          │
┌─────────▼─────────┐
│ US4: Ownership    │
│    (Phase 6)      │
└───────────────────┘
```

### Parallel Opportunities

**Phase 2 (Foundational)**: After T005/T009 directories created:
- T006, T007, T008 can run in parallel (Organization Officer)
- T010, T011, T012 can run in parallel (Organization Member Partner)

**Phase 4 (US2)**: After company.json exists:
- T024, T025, T026, T027, T028 can all run in parallel (different fields)

**Phase 7 (US5)**: After section break added:
- T043, T044, T045 can run in parallel (different fields)

**Phase 9 (Polish)**: All API helpers can run in parallel:
- T055, T056, T057 can run in parallel

---

## Parallel Example: Phase 2 Foundational

```bash
# After T005 creates organization_officer directory:
# Launch these in parallel:
Task: "Create organization_officer/__init__.py"
Task: "Create organization_officer.json with fields..."
Task: "Create organization_officer.py with date validation..."

# After T009 creates organization_member_partner directory:
# Launch these in parallel:
Task: "Create organization_member_partner/__init__.py"
Task: "Create organization_member_partner.json with fields..."
Task: "Create organization_member_partner.py..."
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (child tables + mixin)
3. Complete Phase 3: User Story 1 (Company auto-creation)
4. **STOP and VALIDATE**: Create Organization with org_type="Company", verify Company created
5. Deploy/demo if ready - basic Company functionality works

### Incremental Delivery

1. Setup + Foundational → Child tables ready
2. Add US1 → Companies auto-create → **MVP!**
3. Add US2 → Legal entity info → Enhanced MVP
4. Add US3 + US4 → Officers and ownership → Full compliance features
5. Add US5 → Addresses → Complete feature set
6. Add Permissions + Polish → Production ready

### Sequential Order (Single Developer)

T001 → T002 → T003 → T004 (Setup)
→ T005 → T006-T008 → T009 → T010-T013 → T014 (Foundational)
→ T015 → T016-T022 (US1 MVP)
→ T023-T031 (US2)
→ T032-T035 (US3)
→ T036-T041 (US4)
→ T042-T047 (US5)
→ T048-T054 (Permissions & Edge Cases)
→ T055-T064 (Polish)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Run `bench migrate` after creating/updating JSON files
- Commit after each task or logical group
- US1 is the MVP - stop there if needed
- US3 (Officers) and US5 (Addresses) can run in parallel after US1
- US4 (Ownership) requires US2 (entity_type field) first
