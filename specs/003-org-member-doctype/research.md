# Research: Org Member DocType

**Feature**: 003-org-member-doctype
**Date**: 2025-12-12

## Research Summary

This document captures research findings for implementing the Org Member DocType that links Person to Organization with Role assignment.

---

## 1. Existing DocType Integration

### Role Template Analysis

**Decision**: Use existing `is_supervisor` field for admin-level role detection

**Rationale**: The Role Template DocType already has an `is_supervisor` boolean field that indicates roles with supervisory/admin privileges. This is used across all org types:
- Family: Parent (1), Guardian (1), Child (0), Extended Family (0)
- Company: Owner (1), Manager (1), Employee (0), Contractor (0)
- Nonprofit: Board Member (1), Volunteer (0), Staff (0)
- Association: President (1), Member (0), Honorary (0)

**Alternatives Considered**:
- Adding new `is_admin` field: Rejected as it duplicates existing functionality
- Using role name pattern matching: Rejected as fragile and not maintainable

**Source**: `dartwing/dartwing_core/doctype/role_template/role_template.json` lines 38-44

### Organization Analysis

**Decision**: Link to Organization via standard Frappe Link field

**Rationale**: Organization DocType uses naming_series `ORG-.YYYY.-` and has immutable `org_type` field (set_only_once: 1). This ensures role compatibility validation only needs to check at membership creation/role change time.

**Key Fields**:
- `name`: Auto-generated ID (e.g., ORG-2025-00001)
- `org_type`: Select field (Family/Company/Association/Nonprofit) - immutable
- `org_name`: Display name

**Source**: `dartwing/dartwing_core/doctype/organization/organization.json`

### Person Analysis

**Decision**: Link to Person via standard Frappe Link field with soft-cascade handling

**Rationale**: Person DocType uses naming_series `PERSON-.YYYY.-` and has unique constraint on `primary_email`. Soft-cascade on deletion preserves membership history per spec clarification.

**Key Fields**:
- `name`: Auto-generated ID (e.g., PERSON-2025-00001)
- `primary_email`: Unique identifier
- `full_name`: Computed display name

**Source**: `dartwing/dartwing_core/doctype/person/person.json`

---

## 2. Frappe Best Practices for DocType Links

### Unique Constraint Implementation

**Decision**: Use Frappe's `unique_together` or custom validate method

**Rationale**: Frappe doesn't have native `unique_together` in JSON definition. Implement via:
1. Custom `validate()` method checking for existing (person, organization) pair
2. Consider MySQL unique index via custom SQL migration (optional optimization)

**Pattern**: Similar to how Role Template ensures unique `role_name` via `unique: 1` field property.

### Cascade Deletion Patterns

**Decision**: Use `doc_events` hook for Person soft-cascade, standard Link behavior for Organization cascade

**Rationale**:
- **Person deletion → Soft-cascade**: Add `doc_events` in hooks.py to intercept Person `on_trash` and set Org Member status to "Inactive"
- **Organization deletion → Hard cascade**: Standard Frappe Link behavior with `ignore_linked_doctypes` or explicit cleanup in Organization's `on_trash`

**Pattern Reference**: `role_template.py:on_trash()` shows deletion prevention pattern; we need inverse (cascade instead of prevent).

---

## 3. API Design Patterns

### Whitelist Methods

**Decision**: Follow existing `role_template.py` pattern for API methods

**Rationale**: Role Template exposes `get_roles_for_org_type()` and `is_supervisor_role()` as whitelisted methods. Org Member should expose:
- `get_members_for_organization(organization: str)` - List active members
- `get_organizations_for_person(person: str)` - List person's memberships
- `add_member_to_organization(...)` - Create/reactivate membership
- `check_can_deactivate_member(member: str)` - Validate last-supervisor rule

**Source**: `dartwing/dartwing_core/doctype/role_template/role_template.py` lines 56-128

---

## 4. Testing Patterns

### Test Structure

**Decision**: Follow `test_role_template.py` pattern with user story sections

**Rationale**: Existing tests use clear section headers:
```python
# =========================================================================
# User Story 1: System Administrator Seeds Role Data (T008-T012)
# =========================================================================
```

Tests inherit from `frappe.tests.IntegrationTestCase` and use standard assertions.

**Source**: `dartwing/dartwing_core/doctype/role_template/test_role_template.py`

---

## 5. Permissions Model

### DocType Permissions

**Decision**: Mirror Role Template permission structure

**Rationale**:
- System Manager: Full CRUD
- Dartwing User: Read only (membership management via API methods with additional validation)
- Future: Add org-scoped permissions when permission system (Feature 5) is implemented

**Source**: `role_template.json` permissions section

---

## 6. Field Design Decisions

### Status Field

**Decision**: Use Select field with options "Active\nInactive\nPending"

**Rationale**: Matches spec FR-006. Default to "Active" per FR-005.

### Date Fields

**Decision**: Use Date fieldtype (not Datetime) for start_date and end_date

**Rationale**: Membership dates are typically day-granularity. Datetime adds unnecessary precision.

### Naming Strategy

**Decision**: Use hash naming (autoname not specified) to avoid conflicts

**Rationale**: Unlike Role Template (named by role_name) or Person (naming_series), Org Member has no natural unique identifier. Using Frappe's default hash naming ensures uniqueness without business key constraints.

---

## Unresolved Items

None - all NEEDS CLARIFICATION items resolved through spec clarification session and codebase research.
