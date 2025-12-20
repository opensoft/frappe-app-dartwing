# Feature Specification: OrganizationMixin Base Class

**Feature Branch**: `008-organization-mixin`
**Created**: 2025-12-14
**Status**: Draft
**Input**: OrganizationMixin base class - shared functionality for concrete organization types (Family, Company, Association, Nonprofit)

## Clarifications

### Session 2025-12-14

- Q: When the `organization` field links to an Organization record that no longer exists (orphaned concrete type), what should the mixin properties return? → A: Return None silently (consistent with FR-007 for non-existent links)
- Q: When a concrete type record has an empty or null `organization` field, what should the mixin properties return? → A: Return None silently (same as orphaned Organization behavior)
- Q: When `update_org_name()` is called but the user lacks write permission on the Organization, what should happen? → A: Let the underlying permission system raise its standard permission error
- Q: When the Organization's `logo` field is empty/null, what should `concrete_type.logo` return? → A: Return None (consistent with other empty/missing values)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Access Parent Organization Data from Concrete Type (Priority: P1)

As a developer working with concrete organization types (Family, Company, Association, Nonprofit), I need to easily access common parent Organization data (name, logo, status) without writing repetitive code or making multiple database queries.

**Why this priority**: This is the core value proposition of the mixin - reducing code duplication and providing a consistent API for accessing Organization data from any concrete type. Every developer interaction with concrete types will benefit from this.

**Independent Test**: Can be fully tested by creating a Family record and verifying that `family.org_name`, `family.logo`, and `family.org_status` return the correct values from the parent Organization.

**Acceptance Scenarios**:

1. **Given** a Family record exists with a linked Organization, **When** a developer accesses `family.org_name`, **Then** the Organization's `org_name` value is returned without an additional explicit database query in the calling code.

2. **Given** a Company record exists with a linked Organization that has a logo, **When** a developer accesses `company.logo`, **Then** the Organization's logo attachment URL is returned.

3. **Given** a Nonprofit record exists with a linked Organization with status "Active", **When** a developer accesses `nonprofit.org_status`, **Then** the value "Active" is returned.

4. **Given** a concrete type record exists, **When** a developer accesses `record.get_organization_doc()`, **Then** a full Organization document object is returned.

---

### User Story 2 - Update Organization Name from Concrete Type (Priority: P2)

As a developer implementing organization management features, I need to update the Organization's display name directly from the concrete type without manually fetching and saving the parent Organization document.

**Why this priority**: While read operations are more common, updating the Organization name is a frequent administrative task. Providing a clean method simplifies UI development and ensures consistency.

**Independent Test**: Can be fully tested by calling `family.update_org_name("New Name")` and verifying the parent Organization's `org_name` field is updated in the database.

**Acceptance Scenarios**:

1. **Given** a Family record exists with Organization name "Smith Family", **When** `family.update_org_name("Johnson Family")` is called, **Then** the parent Organization's `org_name` becomes "Johnson Family".

2. **Given** a Company record exists, **When** `company.update_org_name("")` is called with an empty string, **Then** an appropriate validation error is raised.

---

### User Story 3 - Consistent API Across All Concrete Types (Priority: P1)

As a developer building features that work with multiple organization types, I need the same methods and properties available on Family and Company so I can write generic code that handles any organization type.

**Why this priority**: The polymorphic Organization pattern only delivers value if developers can interact with concrete types consistently. This enables building generic UI components and business logic.

**Independent Test**: Can be fully tested by verifying that `org_name`, `logo`, `org_status`, `get_organization_doc()`, and `update_org_name()` are available and work identically on Family and Company document types. (Association and Nonprofit are out of scope for this feature - they will inherit the mixin when those doctypes are created.)

**Acceptance Scenarios**:

1. **Given** a function that accepts any concrete type record, **When** it calls `record.org_name`, **Then** the Organization name is returned regardless of whether the record is Family or Company.

2. **Given** code iterating over Family and Company records, **When** each record's `org_status` is accessed, **Then** all return valid status values without type-specific handling.

---

### Edge Cases

- **Orphaned concrete type (deleted Organization)**: When the linked Organization record has been deleted but the concrete type still exists, all mixin properties (`org_name`, `logo`, `org_status`) return None silently. The `get_organization_doc()` method returns None. The `update_org_name()` method raises an error since there is no target to update.
- **Empty/null organization field**: When a concrete type record has an empty or null `organization` field, all mixin properties return None silently. The `update_org_name()` method raises an error since there is no target to update.
- **Permission denied on update**: When `update_org_name()` is called but the user lacks write permission on the Organization, the underlying permission system raises its standard permission error. The mixin does not catch or transform this error.
- **Empty logo field**: When the Organization's `logo` field is empty or null, the `logo` property returns None (consistent with other empty/missing value behavior).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a reusable mixin class that can be inherited by all concrete organization type controllers (Family, Company, Association, Nonprofit).

- **FR-002**: The mixin MUST provide read-only properties `org_name`, `logo`, and `org_status` that retrieve values from the linked Organization record.

- **FR-003**: The mixin MUST provide a `get_organization_doc()` method that returns the full parent Organization document object.

- **FR-004**: The mixin MUST provide an `update_org_name(new_name: str)` method that updates the `org_name` field on the linked Organization record.

- **FR-005**: Family controller MUST inherit from the OrganizationMixin to gain shared functionality.

- **FR-006**: Company controller MUST inherit from the OrganizationMixin to gain shared functionality.

- **FR-007**: All mixin properties MUST gracefully handle the case where the linked Organization does not exist (return None rather than raising an exception).

- **FR-008**: The `update_org_name()` method MUST validate that the new name is not empty before updating.

- **FR-009**: The mixin MUST NOT introduce additional database queries beyond what is necessary (use efficient single-field fetches for properties).

### Key Entities

- **OrganizationMixin**: A Python mixin class providing shared functionality for accessing and manipulating the parent Organization from concrete type documents.
- **Organization**: The parent polymorphic identity record linked via the `organization` field on concrete types.
- **Concrete Types**: Family, Company, Association, Nonprofit - the organization type-specific doctypes that inherit from the mixin.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All concrete type controllers (Family, Company) that exist can access `org_name`, `logo`, and `org_status` properties without additional code changes beyond inheriting the mixin.

- **SC-002**: Developers can update Organization name from any concrete type using a single method call without manually managing the parent document.

- **SC-003**: Code duplication for Organization access patterns is eliminated - no repeated database query code across concrete type controllers.

- **SC-004**: The mixin works identically across Family, Company, and any future concrete types (Association, Nonprofit) with zero type-specific handling required in consuming code.

- **SC-005**: Property access on concrete types returns correct Organization data with no additional latency beyond a single database query (properties use cached single-query fetch).

## Assumptions

- The `organization` field exists on all concrete type doctypes and is a required Link field to the Organization doctype.
- Concrete type controllers (Family, Company) already exist or will be created as standard Frappe Document subclasses.
- Python's multiple inheritance mechanism supports mixing Document with OrganizationMixin without conflicts.
- The Organization doctype has fields `org_name`, `logo`, and `status` as defined in the architecture document.
- Frappe's `frappe.db.get_value()` and `frappe.db.set_value()` functions are available for efficient single-field operations.

## Dependencies

- **Feature 004**: Organization Bidirectional Hooks - ensures the Organization ↔ Concrete Type relationship is properly maintained.
- **Feature 006**: Company DocType - the Company controller needs to exist to inherit from the mixin.
- Existing Family doctype and controller implementation.

## Out of Scope

- Creating the Association or Nonprofit concrete type doctypes (those are separate features).
- Implementing permission checks within the mixin methods (permissions are handled by Frappe's standard permission system).
- Caching or optimization beyond using efficient database queries.
- Any UI components - this is purely a backend code quality improvement.
- Modifying the Organization doctype structure.
