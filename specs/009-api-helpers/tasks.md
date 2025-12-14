# Tasks: API Helpers (Whitelisted Methods)

**Input**: Design documents from `/specs/009-api-helpers/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Tests are included based on Constitution requirement (Code Quality Standards: "Tests required for business logic").

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

This project uses Frappe app structure:

- **App root**: `dartwing/` (Python module)
- **Core module**: `dartwing/dartwing_core/`
- **Tests**: `dartwing/tests/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and API module structure

- [x] T001 Create API module directory at dartwing/dartwing_core/api/
- [x] T002 Create **init**.py in dartwing/dartwing_core/api/**init**.py
- [x] T003 [P] Create test file at dartwing/tests/test_organization_api.py with test class skeleton

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T004 Verify Person, Organization, Org Member, Role Template doctypes exist (dependency check)
- [x] T005 Verify User Permission propagation is functional (Feature #5 dependency check)
- [x] T006 [P] Create organization_api.py skeleton with imports in dartwing/dartwing_core/api/organization_api.py
- [x] T007 [P] Define logger instance in organization_api.py following existing pattern from organization.py

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Retrieve User's Organizations (Priority: P1) 🎯 MVP

**Goal**: Mobile app users can see all organizations they belong to via a single API call

**Independent Test**: Authenticate a user with multiple organization memberships, call `get_user_organizations`, verify exact organizations returned

### Tests for User Story 1

- [x] T008 [P] [US1] Write test_get_user_organizations_returns_all_memberships in dartwing/tests/test_organization_api.py
- [x] T009 [P] [US1] Write test_get_user_organizations_empty_for_no_memberships in dartwing/tests/test_organization_api.py
- [x] T010 [P] [US1] Write test_get_user_organizations_requires_authentication in dartwing/tests/test_organization_api.py

### Implementation for User Story 1

- [x] T011 [US1] Implement get_user_organizations() with @frappe.whitelist() in dartwing/dartwing_core/api/organization_api.py
- [x] T012 [US1] Add logic to derive current user's Person from frappe.session.user in get_user_organizations
- [x] T013 [US1] Add query to get Org Member records for current user's Person in get_user_organizations
- [x] T014 [US1] Add Organization join to include org_name, org_type, logo, status fields in get_user_organizations
- [x] T015 [US1] Add Role Template join to include role name and is_supervisor flag in get_user_organizations
- [x] T016 [US1] Format response as {data: [...], total_count: N} in get_user_organizations
- [x] T017 [US1] Add INFO-level audit logging for successful calls in get_user_organizations
- [x] T018 [US1] Run tests for User Story 1 and verify all pass

**Checkpoint**: User Story 1 fully functional - app home screen can display organization list

---

## Phase 4: User Story 2 - View Organization with Concrete Type Details (Priority: P1)

**Goal**: Users can view full organization details including type-specific data in one API call

**Independent Test**: Fetch a Company organization, verify both Organization fields and Company-specific fields (tax_id) are returned together

### Tests for User Story 2

- [x] T019 [P] [US2] Write test_get_organization_with_details_returns_concrete_type in dartwing/tests/test_organization_api.py
- [x] T020 [P] [US2] Write test_get_organization_with_details_permission_denied in dartwing/tests/test_organization_api.py
- [x] T021 [P] [US2] Write test_get_organization_with_details_not_found in dartwing/tests/test_organization_api.py

### Implementation for User Story 2

- [x] T022 [US2] Add explicit permission check using frappe.has_permission("Organization", "read", organization) with PermissionError at start of get_organization_with_details in dartwing/dartwing_core/doctype/organization/organization.py
- [x] T023 [US2] Verify existing response format matches data-model.md spec (nested concrete_type object)
- [x] T024 [US2] Ensure null concrete_type returned with warning log when link is broken
- [x] T025 [US2] Run tests for User Story 2 and verify all pass

**Checkpoint**: User Story 2 complete - organization detail screens can load in single request

---

## Phase 5: User Story 3 - Retrieve Concrete Type Document Directly (Priority: P2)

**Goal**: Developers can retrieve just the concrete type document for focused data retrieval

**Independent Test**: Call get_concrete_doc with an Organization ID, verify only concrete type fields returned (no Organization wrapper)

### Tests for User Story 3

- [x] T026 [P] [US3] Write test_get_concrete_doc_returns_family_fields in dartwing/tests/test_organization_api.py
- [x] T027 [P] [US3] Write test_get_concrete_doc_returns_null_when_unlinked in dartwing/tests/test_organization_api.py
- [x] T028 [P] [US3] Write test_get_concrete_doc_permission_check in dartwing/tests/test_organization_api.py

### Implementation for User Story 3

- [x] T029 [US3] Add explicit permission check using frappe.has_permission("Organization", "read", organization) with PermissionError at start of get_concrete_doc in dartwing/dartwing_core/doctype/organization/organization.py
- [x] T030 [US3] Verify existing response format matches data-model.md spec (direct document dict)
- [x] T031 [US3] Run tests for User Story 3 and verify all pass

**Checkpoint**: User Story 3 complete - type-specific screens can load efficiently

---

## Phase 6: User Story 4 - List Organization Members (Priority: P2)

**Goal**: Organization administrators can view paginated member lists with role and status information

**Independent Test**: Create Organization with 5 members, call get_org_members, verify all 5 returned with correct role info

### Tests for User Story 4

- [x] T032 [P] [US4] Write test_get_org_members_returns_all_members in dartwing/tests/test_organization_api.py
- [x] T033 [P] [US4] Write test_get_org_members_pagination in dartwing/tests/test_organization_api.py
- [x] T034 [P] [US4] Write test_get_org_members_status_filter in dartwing/tests/test_organization_api.py
- [x] T035 [P] [US4] Write test_get_org_members_permission_denied in dartwing/tests/test_organization_api.py

### Implementation for User Story 4

- [x] T036 [US4] Implement get_org_members() with @frappe.whitelist() in dartwing/dartwing_core/api/organization_api.py
- [x] T037 [US4] Add organization, limit, offset, status parameters with defaults (limit=20, offset=0)
- [x] T038 [US4] Add explicit permission check: frappe.has_permission("Organization", "read", organization)
- [x] T039 [US4] Add limit capping: min(int(limit), 100) to prevent abuse
- [x] T040 [US4] Add offset validation: max(int(offset), 0) to prevent negative offset
- [x] T041 [US4] Add status filter to query when provided (Active/Inactive/Pending)
- [x] T042 [US4] Query Org Member with frappe.get_all using limit_page_length and limit_start
- [x] T043 [US4] Add total_count via frappe.db.count for pagination UI
- [x] T044 [US4] Join Person to include member_name and person_email in results
- [x] T045 [US4] Join Role Template to include is_supervisor flag in results
- [x] T046 [US4] Format response as {data: [...], total_count: N, limit: N, offset: N}
- [x] T047 [US4] Add INFO-level audit logging for successful calls
- [x] T048 [US4] Run tests for User Story 4 and verify all pass

**Checkpoint**: User Story 4 complete - member management screens can load with pagination

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T049 [P] Add docstrings to all four API methods following Frappe conventions
- [x] T050 [P] Verify all methods handle edge case: organization not found (DoesNotExistError)
- [x] T051 [P] Verify all methods handle edge case: unauthenticated request (AuthenticationError)
- [x] T052 [P] Verify all methods handle edge case: session expires mid-request returns AuthenticationError
- [x] T053 [P] Verify response format consistency across all 4 API methods per data-model.md and FR-008
- [x] T054 Run full test suite: bench --site [site] run-tests --app dartwing --module tests.test_organization_api
- [x] T055 Validate quickstart.md examples work against actual implementation
- [x] T056 [P] Update contracts/organization-api.yaml if any response changes were made
- [x] T057 [P] Performance validation: verify SC-001 (<1s for 50 orgs), SC-005 (<500ms standard ops) via manual testing or load test

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - No dependencies on other stories

**Note**: US2 and US3 modify the same file (organization.py) - if worked in parallel, coordinate merges

### Within Each User Story

- Tests MUST be written and FAIL before implementation
- Permission checks before business logic
- Core implementation before response formatting
- Logging after core logic works
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks can run in parallel
- All Foundational tasks marked [P] can run in parallel
- Once Foundational completes, all 4 user stories can start in parallel
- All tests for a user story marked [P] can run in parallel
- US1 and US4 work on different files than US2 and US3

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Write test_get_user_organizations_returns_all_memberships in dartwing/tests/test_organization_api.py"
Task: "Write test_get_user_organizations_empty_for_no_memberships in dartwing/tests/test_organization_api.py"
Task: "Write test_get_user_organizations_requires_authentication in dartwing/tests/test_organization_api.py"
```

## Parallel Example: User Story 4

```bash
# Launch all tests for User Story 4 together:
Task: "Write test_get_org_members_returns_all_members in dartwing/tests/test_organization_api.py"
Task: "Write test_get_org_members_pagination in dartwing/tests/test_organization_api.py"
Task: "Write test_get_org_members_status_filter in dartwing/tests/test_organization_api.py"
Task: "Write test_get_org_members_permission_denied in dartwing/tests/test_organization_api.py"
```

---

## Implementation Strategy

### MVP First (User Stories 1 + 2 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (get_user_organizations)
4. Complete Phase 4: User Story 2 (get_organization_with_details)
5. **STOP and VALIDATE**: Test both stories independently
6. Deploy/demonstrate if ready - Flutter team can start building home screen and org details

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Flutter can build org selector (MVP!)
3. Add User Story 2 → Test independently → Flutter can build org details screen
4. Add User Story 3 → Test independently → Flutter can build type-specific editors
5. Add User Story 4 → Test independently → Flutter can build member management
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (organization_api.py)
   - Developer B: User Story 2 (organization.py modifications)
3. After P1 stories complete:
   - Developer A: User Story 4 (organization_api.py)
   - Developer B: User Story 3 (organization.py modifications)
4. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US2/US3 share organization.py - coordinate if working in parallel
- Existing methods in organization.py already have logging - just add permission checks
