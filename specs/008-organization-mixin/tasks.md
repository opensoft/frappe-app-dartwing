# Tasks: OrganizationMixin Base Class

**Input**: Design documents from `/specs/008-organization-mixin/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, quickstart.md

**Tests**: Unit tests included as specified in plan.md ("Tests required per spec")

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Frappe app**: `dartwing/dartwing_core/`, `dartwing/dartwing_company/`
- **Tests**: `dartwing/dartwing_core/tests/`

## Requirement Coverage

**Pre-existing (already implemented in OrganizationMixin):**
- FR-001: Reusable mixin class - ✅ EXISTS (verified by T001)
- FR-002: Read-only properties (org_name, logo, org_status) - ✅ EXISTS (validated by T012-T014)
- FR-003: get_organization_doc() method - ✅ EXISTS (validated by T015)
- FR-007: Graceful None handling - ✅ EXISTS (validated by T018-T019)
- FR-009: Efficient queries with caching - ✅ EXISTS (no task needed)
- FR-006: Company inherits mixin - ✅ EXISTS (verified by T003, T009-T010)

**New implementation (this feature):**
- FR-004: update_org_name() method - 🔨 NEW (implemented by T007)
- FR-005: Family inherits mixin - 🔨 NEW (implemented by T004-T006)
- FR-008: Validate empty name - 🔨 NEW (implemented in T007, validated by T017)

---

## Phase 1: Setup

**Purpose**: No setup required - enhancing existing codebase

- [x] T001 Verify OrganizationMixin exists at dartwing/dartwing_core/mixins/organization_mixin.py
- [x] T002 Verify Family doctype exists at dartwing/dartwing_core/doctype/family/family.py
- [x] T003 Verify Company already inherits OrganizationMixin at dartwing/dartwing_company/doctype/company/company.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: No foundational work required - mixin infrastructure already exists

**⚠️ CRITICAL**: The OrganizationMixin already exists with caching infrastructure. User story implementation can begin immediately.

**Checkpoint**: Foundation ready - user story implementation can begin

---

## Phase 3: User Story 1 - Access Parent Organization Data (Priority: P1) 🎯 MVP

**Goal**: Enable Family to access parent Organization data (org_name, logo, org_status) via the mixin

**Independent Test**: Create a Family record with linked Organization, verify `family.org_name`, `family.logo`, `family.org_status` return correct values

### Implementation for User Story 1

- [x] T004 [US1] Add OrganizationMixin import to dartwing/dartwing_core/doctype/family/family.py
- [x] T005 [US1] Update Family class to inherit from OrganizationMixin in dartwing/dartwing_core/doctype/family/family.py (change to `class Family(Document, OrganizationMixin):`)
- [x] T006 [US1] Verify Family's existing validate() method still works correctly after mixin inheritance

**Checkpoint**: Family can now access org_name, logo, org_status properties from parent Organization

---

## Phase 4: User Story 2 - Update Organization Name (Priority: P2)

**Goal**: Add `update_org_name()` method to OrganizationMixin so concrete types can update their Organization's name directly

**Independent Test**: Call `family.update_org_name("New Name")`, verify Organization's org_name is updated in database

### Implementation for User Story 2

- [x] T007 [US2] Add `update_org_name(new_name: str)` method to OrganizationMixin in dartwing/dartwing_core/mixins/organization_mixin.py with:
  - Validation: Raise error if new_name is empty or whitespace-only using `frappe.throw(_("Organization name cannot be empty"))`
  - Validation: Raise error if self.organization is None using `frappe.throw(_("Cannot update organization name: No organization linked"))`
  - Update: Use `frappe.db.set_value("Organization", self.organization, "org_name", new_name)`
  - Cache: Call `self._clear_organization_cache()` after update
- [x] T008 [US2] Import `_` from frappe for translation support in dartwing/dartwing_core/mixins/organization_mixin.py (if not already imported)

**Checkpoint**: Concrete types can now update Organization name via single method call

---

## Phase 5: User Story 3 - Consistent API Across All Concrete Types (Priority: P1)

**Goal**: Verify the same mixin API works identically on both Family and Company

**Independent Test**: Call org_name, logo, org_status, get_organization_doc(), update_org_name() on both Family and Company instances, verify identical behavior

### Implementation for User Story 3

- [x] T009 [US3] Verify Company still has working mixin properties (org_name, logo, org_status) after update_org_name() was added
- [x] T010 [US3] Verify Company can use new update_org_name() method successfully

**Checkpoint**: Family and Company have identical mixin API

---

## Phase 6: Unit Tests

**Purpose**: Verify all mixin functionality with automated tests

### Test Implementation

- [x] T011 [P] Create test file dartwing/dartwing_core/tests/test_organization_mixin.py with test class structure
- [x] T012 [P] Add test: `test_org_name_returns_organization_name` - verify org_name property returns correct value
- [x] T013 [P] Add test: `test_logo_returns_organization_logo` - verify logo property returns correct value (and None when empty)
- [x] T014 [P] Add test: `test_org_status_returns_organization_status` - verify org_status property returns correct value
- [x] T015 [P] Add test: `test_get_organization_doc_returns_document` - verify get_organization_doc() returns full Organization document
- [x] T016 [P] Add test: `test_update_org_name_updates_organization` - verify update_org_name() changes org_name in database
- [x] T017 [P] Add test: `test_update_org_name_empty_raises_error` - verify update_org_name("") raises ValidationError
- [x] T018 [P] Add test: `test_properties_return_none_when_organization_null` - verify all properties return None when organization field is None
- [x] T019 [P] Add test: `test_properties_return_none_when_organization_deleted` - verify all properties return None when linked Organization is deleted
- [x] T020 [P] Add test: `test_update_org_name_raises_when_no_organization` - verify update_org_name() raises error when organization field is None

**Checkpoint**: All mixin functionality covered by tests

---

## Phase 7: Polish & Verification

**Purpose**: Final verification and documentation

- [x] T021 Run all tests to verify no regressions: `cd dartwing && pytest dartwing_core/tests/test_organization_mixin.py -v`
- [x] T022 Verify Company functionality unchanged (regression test)
- [x] T023 Run quickstart.md examples manually to validate documentation accuracy

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - verification only
- **Foundational (Phase 2)**: N/A - skipped (infrastructure exists)
- **User Story 1 (Phase 3)**: Can start immediately
- **User Story 2 (Phase 4)**: Can start in parallel with US1 (different file)
- **User Story 3 (Phase 5)**: Depends on US1 and US2 completion
- **Tests (Phase 6)**: Depends on US1 and US2 completion
- **Polish (Phase 7)**: Depends on all phases

### User Story Dependencies

- **User Story 1 (P1)**: No dependencies - Family inheritance is self-contained
- **User Story 2 (P2)**: No dependencies - Mixin enhancement is self-contained
- **User Story 3 (P1)**: Depends on US1 (Family must inherit mixin) and US2 (update_org_name must exist)

### Within Each User Story

- US1: Import → Inheritance → Verification (sequential)
- US2: Method implementation → Import check (mostly single task)
- US3: Company verification (sequential after US1/US2)

### Parallel Opportunities

**Between User Stories:**
- US1 and US2 can run in parallel (different files)
  - US1 modifies: `family.py`
  - US2 modifies: `organization_mixin.py`

**Within Tests Phase:**
- All test tasks (T011-T020) marked [P] can run in parallel after test file is created

---

## Parallel Example: User Stories 1 & 2

```bash
# These can run in parallel (different files):
Task: "[US1] Update Family class to inherit from OrganizationMixin in family.py"
Task: "[US2] Add update_org_name() method to OrganizationMixin in organization_mixin.py"
```

---

## Parallel Example: Test Creation

```bash
# All test methods can be written in parallel after T011:
Task: "Add test: test_org_name_returns_organization_name"
Task: "Add test: test_logo_returns_organization_logo"
Task: "Add test: test_org_status_returns_organization_status"
Task: "Add test: test_get_organization_doc_returns_document"
Task: "Add test: test_update_org_name_updates_organization"
# ... etc
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup verification
2. Complete Phase 3: User Story 1 (Family inherits mixin)
3. **STOP and VALIDATE**: Test Family.org_name, Family.logo, Family.org_status work
4. Family can now access Organization data - immediate developer value

### Full Implementation

1. Phase 1: Setup verification (3 tasks)
2. Phase 3: US1 - Family inheritance (3 tasks)
3. Phase 4: US2 - Add update_org_name() (2 tasks) - **can parallel with US1**
4. Phase 5: US3 - Verify consistency (2 tasks)
5. Phase 6: Unit tests (10 tasks)
6. Phase 7: Polish (3 tasks)

### Recommended Execution Order

1. Start US1 (T004-T006) and US2 (T007-T008) in parallel
2. Once both complete, run US3 (T009-T010)
3. Create test file (T011), then run all test tasks in parallel (T012-T020)
4. Final verification (T021-T023)

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Existing OrganizationMixin already has org_name, logo, org_status, get_organization_doc() - no changes needed to these
- Company already inherits from mixin - only verification needed
- Family is the only concrete type needing inheritance change
- update_org_name() is the only new method to implement
