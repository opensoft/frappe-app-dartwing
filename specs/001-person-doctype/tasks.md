# Tasks: Person DocType

**Input**: Design documents from `/specs/001-person-doctype/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests ARE included as the spec mentions "Basic tests for duplicate email rejection" in acceptance criteria.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

```text
dartwing/
├── dartwing_core/
│   └── doctype/
│       ├── person/
│       │   ├── __init__.py
│       │   ├── person.json
│       │   ├── person.py
│       │   └── test_person.py
│       └── person_merge_log/
│           ├── __init__.py
│           ├── person_merge_log.json
│           └── person_merge_log.py
├── api/
│   └── person.py
├── utils/
│   └── person_sync.py
└── tests/
    └── test_person_api.py
```

---

## Phase 1: Setup (Project Infrastructure)

**Purpose**: Create directory structure and initialize module files

- [ ] T001 Create Person DocType directory structure at `dartwing/dartwing_core/doctype/person/`
- [ ] T002 [P] Create Person Merge Log DocType directory structure at `dartwing/dartwing_core/doctype/person_merge_log/`
- [ ] T003 [P] Create `__init__.py` files for both doctype directories
- [ ] T004 Add `phonenumbers` dependency to `pyproject.toml` for mobile validation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core DocType definitions that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 Create Person Merge Log child table JSON structure in `dartwing/dartwing_core/doctype/person_merge_log/person_merge_log.json` with `istable: 1` property
- [ ] T006 Define Person Merge Log fields in `dartwing/dartwing_core/doctype/person_merge_log/person_merge_log.json` as specified in data-model.md: source_person (Link:Person), target_person (Link:Person), merged_at (Datetime), merged_by (Link:User), notes (Small Text)
- [ ] T007 Create Person DocType JSON definition in `dartwing/dartwing_core/doctype/person/person.json` using all field specifications as defined in `data-model.md`, including: primary_email (unique), keycloak_user_id, frappe_user (Link:User), first_name, last_name, full_name, mobile_no, personal_org (Link:Organization), is_minor, consent_captured, consent_timestamp, source (Select), status (Select), user_sync_status (Select), sync_error_message, last_sync_at, merge_logs (Table:Person Merge Log).
- [ ] T008 Create base Person controller in `dartwing/dartwing_core/doctype/person/person.py` with Document class skeleton and autoname property
- [ ] T009 Run `bench --site {site} migrate` to create database tables and verify schema matches data-model.md

**Checkpoint**: Foundation ready - Person DocType exists with all fields, user story implementation can now begin

---

## Phase 3: User Story 1 - Create Person Record (Priority: P1) 🎯 MVP

**Goal**: Enable creation of Person records with uniqueness enforcement on primary_email, keycloak_user_id, and frappe_user

**Independent Test**: Create a Person via API/UI, verify uniqueness constraints reject duplicates within 1 second

### Tests for User Story 1

- [ ] T010 [P] [US1] Write test for duplicate email rejection in `dartwing/dartwing_core/doctype/person/test_person.py` - verify DuplicateEntryError thrown when creating Person with existing primary_email
- [ ] T011 [P] [US1] Write test for nullable unique keycloak_user_id in `dartwing/dartwing_core/doctype/person/test_person.py` - verify multiple NULLs allowed but duplicate non-null values rejected
- [ ] T012 [P] [US1] Write test for mobile validation in `dartwing/dartwing_core/doctype/person/test_person.py` - verify E.164 format validation and normalization
- [ ] T012a [P] [US1] Write test for personal_org Link validation in `dartwing/dartwing_core/doctype/person/test_person.py` - verify Link to Organization works and invalid org names rejected (FR-009)

### Implementation for User Story 1

- [ ] T013 [US1] Implement `validate()` method in `dartwing/dartwing_core/doctype/person/person.py` with uniqueness checks for keycloak_user_id and frappe_user using validate hook pattern from research.md
- [ ] T014 [US1] Implement `_validate_and_normalize_mobile_no()` method in `dartwing/dartwing_core/doctype/person/person.py` using phonenumbers library to parse and normalize to E.164 format
- [ ] T015 [US1] Implement `before_save()` method in `dartwing/dartwing_core/doctype/person/person.py` to compute full_name from first_name + last_name
- [ ] T016 [US1] Implement `_enforce_minor_consent_policy()` method in `dartwing/dartwing_core/doctype/person/person.py` to block writes on minors without consent, with exception for consent capture operation per research.md. During the consent capture operation, ONLY consent fields and system metadata fields (such as 'modified' and 'modified_by') may be modified; all other fields must remain unchanged.
- [ ] T017 [US1] Add permissions to `person.json` for System Manager and Dartwing User roles
- [ ] T017a [US1] Create `capture_consent` API endpoint in `dartwing/api/person.py` per contracts/person-api.yaml to capture consent for minors (FR-013)

**Checkpoint**: User Story 1 complete - Person CRUD works with all uniqueness constraints enforced

---

## Phase 4: User Story 2 - Link Person to Frappe User (Priority: P1)

**Goal**: Auto-create Frappe User when keycloak_user_id is set, with resilient background retry on failure

**Independent Test**: Create Person with keycloak_user_id, verify Frappe User is created or sync status shows pending/failed with queued retry

### Tests for User Story 2

- [ ] T018 [P] [US2] Write test for successful User auto-creation in `dartwing/dartwing_core/doctype/person/test_person.py` - verify frappe_user link and user_sync_status="synced" when auto-creation succeeds
- [ ] T019 [P] [US2] Write test for sync failure handling in `dartwing/dartwing_core/doctype/person/test_person.py` - verify Person saved with user_sync_status="pending" when User creation fails

### Implementation for User Story 2

- [ ] T020 [US2] Create `dartwing/utils/person_sync.py` with `queue_user_sync(person_name, attempt)` function using frappe.enqueue() with job_id deduplication per research.md
- [ ] T021 [US2] Implement `sync_frappe_user(person_name, attempt)` in `dartwing/utils/person_sync.py` with exponential backoff retry logic (max 5 retries, 2s base delay)
- [ ] T022 [US2] Implement `create_frappe_user(person)` helper in `dartwing/utils/person_sync.py` to create User with "Dartwing User" role and link to Person
- [ ] T023 [US2] Add `after_insert()` hook in `dartwing/dartwing_core/doctype/person/person.py` to trigger User auto-creation when keycloak_user_id is set and auto-creation enabled
- [ ] T024 [US2] Create `get_sync_status` API endpoint in `dartwing/api/person.py` with @frappe.whitelist() decorator per contracts/person-api.yaml
- [ ] T025 [US2] Create `retry_sync` API endpoint in `dartwing/api/person.py` to manually trigger sync retry for pending/failed Persons

**Checkpoint**: User Story 2 complete - Person→User linkage works with resilient background sync

---

## Phase 5: User Story 3 - Prevent Deletion of Linked Person (Priority: P2)

**Goal**: Block deletion of Person records linked to Org Member, suggest deactivation or merge instead

**Independent Test**: Create Person, link to Org Member (if exists), attempt delete, verify LinkExistsError thrown

### Tests for User Story 3

- [ ] T026 [P] [US3] Write test for deletion blocking in `dartwing/dartwing_core/doctype/person/test_person.py` - verify LinkExistsError when deleting Person linked to Org Member
- [ ] T027 [P] [US3] Write test for successful deletion in `dartwing/dartwing_core/doctype/person/test_person.py` - verify Person without Org Member links can be deleted

### Implementation for User Story 3

- [ ] T028 [US3] Implement `before_delete()` hook in `dartwing/dartwing_core/doctype/person/person.py` to check for Org Member links and throw LinkExistsError with helpful message per research.md
- [ ] T029 [US3] Add status transition logic in `dartwing/dartwing_core/doctype/person/person.py` to allow Active→Inactive→Active but prevent changes from Merged status

**Checkpoint**: User Story 3 complete - Referential integrity protected, deactivation workflow available

---

## Phase 6: User Story 4 - Merge Duplicate Persons (Priority: P3)

**Goal**: Enable merging duplicate Person records with full audit trail via Person Merge Log child table

**Independent Test**: Create two Persons, execute merge, verify Org Member links transferred, merge log entry created, source status set to Merged

### Tests for User Story 4

- [ ] T030 [P] [US4] Write test for merge operation in `dartwing/dartwing_core/doctype/person/test_person.py` - verify source Person status="Merged", merge log entry created on target
- [ ] T031 [P] [US4] Write test for merge with Org Members in `dartwing/dartwing_core/doctype/person/test_person.py` - verify Org Member links transferred to target Person

### Implementation for User Story 4

- [ ] T032 [US4] Create `merge_persons` API endpoint in `dartwing/api/person.py` with @frappe.whitelist() decorator per contracts/person-api.yaml
- [ ] T033 [US4] Implement merge logic in `dartwing/api/person.py`: transfer Org Member links, append merge_log entry, set source status to "Merged"
- [ ] T034 [US4] Add query filter helpers to exclude Merged status Persons from standard list queries in `dartwing/dartwing_core/doctype/person/person.py`

**Checkpoint**: User Story 4 complete - Duplicate resolution with full audit trail

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: API completion, integration tests, documentation validation

- [ ] T035 _(Moved to T017a in US1)_
- [ ] T036 [P] Create integration tests in `dartwing/tests/test_person_api.py` covering full CRUD cycle via REST API
- [ ] T037 Run quickstart.md validation - execute all code examples and verify expected outputs
- [ ] T038 Update `dartwing/hooks.py` to register Person DocType fixtures if needed
- [ ] T039 Verify "Dartwing User" role exists in fixtures or create in `dartwing/fixtures/role.json`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational - Core CRUD functionality
- **User Story 2 (Phase 4)**: Depends on Foundational - Can run in parallel with US1
- **User Story 3 (Phase 5)**: Depends on Foundational - Can run in parallel with US1/US2
- **User Story 4 (Phase 6)**: Depends on Foundational - Can run in parallel with US1/US2/US3
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

```
Setup (Phase 1)
    │
    ▼
Foundational (Phase 2) ─────────────────────────────┐
    │                                                │
    ├───────────────┬───────────────┬───────────────┤
    │               │               │               │
    ▼               ▼               ▼               ▼
  US1 (P1)       US2 (P1)       US3 (P2)       US4 (P3)
  Phase 3        Phase 4        Phase 5        Phase 6
    │               │               │               │
    └───────────────┴───────────────┴───────────────┘
                            │
                            ▼
                    Polish (Phase 7)
```

- **User Story 1 (P1)**: No dependencies on other stories - MVP standalone
- **User Story 2 (P1)**: No dependencies on other stories - independent User sync
- **User Story 3 (P2)**: No dependencies on other stories - independent deletion protection
- **User Story 4 (P3)**: No dependencies on other stories - independent merge functionality

### Within Each User Story

- Tests written FIRST, must FAIL before implementation
- Validation logic before API endpoints
- Core implementation before integration points
- Story complete before moving to Polish phase

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- T005 and T006 (child table) can run parallel with T007 and T008 (parent)
- All test tasks within a story marked [P] can run in parallel
- **All four user stories can be developed in parallel** after Foundational phase completes
- Polish tasks marked [P] can run in parallel

---

## Parallel Example: Foundational Phase

```bash
# Launch child table and parent DocType creation in parallel:
Task: "T005 - Create Person Merge Log child table JSON"
Task: "T006 - Create Person Merge Log controller"
# These can run parallel with:
Task: "T007 - Create Person DocType JSON"
Task: "T008 - Create base Person controller"
```

## Parallel Example: User Story Tests

```bash
# Launch all tests for User Story 1 together:
Task: "T010 - Test for duplicate email rejection"
Task: "T011 - Test for nullable unique keycloak_user_id"
Task: "T012 - Test for mobile validation"
```

## Parallel Example: Multiple User Stories

```bash
# After Foundational (Phase 2) completes, all stories can start:
Developer A: User Story 1 (T010-T017)
Developer B: User Story 2 (T018-T025)
Developer C: User Story 3 (T026-T029)
Developer D: User Story 4 (T030-T034)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009)
3. Complete Phase 3: User Story 1 (T010-T017)
4. **STOP and VALIDATE**: Test Person CRUD independently
5. Deploy/demo if ready - basic Person management works

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → User linkage with sync → Deploy/Demo
4. Add User Story 3 → Referential integrity → Deploy/Demo
5. Add User Story 4 → Merge functionality → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (P1 - MVP)
   - Developer B: User Story 2 (P1 - User sync)
   - Developer C: User Story 3 (P2 - Deletion protection)
   - Developer D: User Story 4 (P3 - Merge)
3. Stories complete and integrate independently
4. All join for Polish phase

---

## Notes

- [P] tasks = different files, no dependencies within phase
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Run `bench --site {site} migrate` after JSON changes
- Reference research.md for implementation patterns
- Reference contracts/person-api.yaml for API signatures
