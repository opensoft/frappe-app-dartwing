# Feature Specification: Organization Bidirectional Hooks

**Feature Branch**: `004-org-bidirectional-hooks`
**Created**: 2025-12-13
**Status**: Draft
**Input**: User description: "Organization Bidirectional Hooks - Auto-create concrete types when Organization is created and maintain data integrity between Organization and its concrete type (Family, Company, Association, Nonprofit)"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Automatic Concrete Type Creation (Priority: P1)

An administrator creates a new Organization record by specifying an organization name and type. The system automatically creates the corresponding concrete type record (Family, Company, Association, or Nonprofit) and establishes the bidirectional link without requiring any additional manual steps.

**Why this priority**: This is the core functionality of the feature. Without automatic creation of concrete types, the hybrid Organization model cannot function, and administrators would need to manually create and link records, leading to data inconsistency and poor user experience.

**Independent Test**: Can be fully tested by creating an Organization with any org_type and verifying the corresponding concrete type record exists with proper linkage. Delivers immediate value by enabling the hybrid organization architecture to work automatically.

**Acceptance Scenarios**:

1. **Given** no Organizations exist, **When** an administrator creates an Organization with org_type "Family", **Then** a Family record is automatically created and linked to the Organization via the organization field
2. **Given** no Organizations exist, **When** an administrator creates an Organization with org_type "Company", **Then** a Company record is automatically created and linked to the Organization
3. **Given** no Organizations exist, **When** an administrator creates an Organization with org_type "Nonprofit", **Then** a Nonprofit record is automatically created and linked to the Organization
4. **Given** no Organizations exist, **When** an administrator creates an Organization with org_type "Association", **Then** an Association record is automatically created and linked to the Organization
5. **Given** an Organization is being created, **When** the concrete type is created, **Then** the Organization's linked_doctype and linked_name fields are populated with the concrete type's doctype name and record name

---

### User Story 2 - Organization Retrieval with Concrete Details (Priority: P1)

A system user or external application needs to retrieve an Organization's complete information, including both the shared identity fields (name, logo, status) and the type-specific fields from its concrete type. The system provides a convenient way to fetch this combined data in a single request.

**Why this priority**: This is essential for any application consuming Organization data. Without easy access to the concrete type details, every consumer would need to make multiple requests and manually join data, creating poor performance and complex integration code.

**Independent Test**: Can be fully tested by retrieving an existing Organization and verifying the response includes both Organization fields and nested concrete type fields. Delivers value by enabling single-request data access for all Organization consumers.

**Acceptance Scenarios**:

1. **Given** an Organization exists with a linked Family record, **When** a user requests the Organization with details, **Then** the response includes Organization fields and nested Family-specific fields
2. **Given** an Organization exists with a linked Company record, **When** a user requests the Organization with details, **Then** the response includes Organization fields and nested Company-specific fields (tax_id, entity_type, jurisdiction)
3. **Given** an Organization exists, **When** a user requests just the concrete type document, **Then** the system returns only the concrete type record without the parent Organization wrapper

---

### User Story 3 - Cascade Delete to Concrete Type (Priority: P2)

When an Organization is deleted, the system automatically deletes the associated concrete type record to prevent orphaned data. This maintains referential integrity without requiring manual cleanup.

**Why this priority**: Data integrity is important but secondary to core creation functionality. Orphaned records would cause data quality issues over time, but the system can function with some orphaned data temporarily.

**Independent Test**: Can be fully tested by deleting an Organization and verifying the linked concrete type record no longer exists. Delivers value by maintaining data integrity automatically.

**Acceptance Scenarios**:

1. **Given** an Organization with a linked Family record exists, **When** the Organization is deleted, **Then** the Family record is also deleted
2. **Given** an Organization with a linked Company record exists, **When** the Organization is deleted, **Then** the Company record is also deleted
3. **Given** an Organization is being deleted but the linked concrete type was already deleted, **When** the deletion is processed, **Then** the Organization deletion succeeds without error
4. **Given** multiple Organizations exist, **When** one Organization is deleted, **Then** other Organizations and their concrete types are unaffected

---

### User Story 4 - Organization Type Immutability (Priority: P2)

Once an Organization is created with a specific org_type, the type cannot be changed. This prevents data integrity issues that would arise from changing types (e.g., Family to Company) where the concrete type would have incompatible fields and relationships.

**Why this priority**: Immutability prevents a class of data corruption bugs. While important for long-term data integrity, the system can function initially even if this protection is weak.

**Independent Test**: Can be fully tested by attempting to change an Organization's org_type after creation and verifying the system rejects the change. Delivers value by preventing data corruption from invalid type changes.

**Acceptance Scenarios**:

1. **Given** an Organization exists with org_type "Family", **When** a user attempts to change org_type to "Company", **Then** the system rejects the change with a clear error message
2. **Given** an Organization exists, **When** a user modifies other fields (org_name, status, logo), **Then** those changes are saved successfully without affecting org_type

---

### Edge Cases

- What happens when the concrete doctype does not exist (e.g., Association module not installed)?
  - The org_type validation (FR-010) covers this case. Since ORG_TYPE_MAP only contains known-valid types, any org_type not in the map is rejected with ValidationError. If a mapped doctype is missing at runtime, the hook will fail and transaction rolls back (FR-011). Both scenarios result in clear error messages.
- What happens if concrete type creation fails partway through (e.g., database error)?
  - The Organization creation should be rolled back to maintain transactional integrity
- What happens when attempting to delete an Organization that is referenced by other records (Org Members, Tasks)?
  - Frappe's built-in LinkExistsError handling applies; deletion is blocked with a clear error message listing the dependent records. No custom implementation needed - this is standard Frappe behavior for Link fields.
- What happens when linked_doctype or linked_name fields become out of sync with actual data?
  - Out of scope for this feature. The hooks ensure consistency at creation and deletion time. Manual data corruption or direct database edits are not protected. A future reconciliation feature may address bulk data integrity checks.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically create the appropriate concrete type record (Family, Company, Association, or Nonprofit) when an Organization is created, based on the org_type field value
- **FR-002**: System MUST populate the Organization's linked_doctype field with the concrete type's doctype name (e.g., "Family", "Company")
- **FR-003**: System MUST populate the Organization's linked_name field with the created concrete type's record name/ID
- **FR-004**: System MUST populate the concrete type's organization field with the parent Organization's name/ID to establish the reverse link
- **FR-005**: System MUST delete the associated concrete type record when an Organization is deleted (cascade delete)
- **FR-006**: System MUST handle gracefully the case where the concrete type record no longer exists during cascade delete
- **FR-007**: System MUST prevent changes to the org_type field after Organization creation
- **FR-008**: System MUST provide a method to retrieve an Organization with its concrete type details in a single request
- **FR-009**: System MUST provide a method to retrieve just the concrete type document given an Organization identifier
- **FR-010**: System MUST validate that the org_type value is one of the supported types (Family, Company, Association, Nonprofit) before creating the Organization
- **FR-011**: System MUST ensure atomic creation - if concrete type creation fails, the Organization creation must also be rolled back
- **FR-012**: System MUST log all hook executions (create and delete) with Organization ID, concrete type, and outcome (success/failure) for audit and debugging purposes
- **FR-013**: System MUST execute hook operations (concrete type creation/deletion) with system privileges, bypassing the current user's permission checks

### Key Entities

- **Organization**: The thin reference shell that holds shared identity (org_name, org_type, logo, status) and acts as the polymorphic target for foreign keys. Contains linked_doctype and linked_name fields to reference its concrete type.
- **Concrete Types (Family, Company, Association, Nonprofit)**: Type-specific records that hold domain-specific data. Each contains an organization field linking back to its parent Organization.
- **Bidirectional Link**: The relationship maintained between Organization and its concrete type, consisting of Organization's linked_doctype/linked_name pointing to the concrete type, and the concrete type's organization field pointing back.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of newly created Organizations have a corresponding concrete type record created within the same transaction
- **SC-002**: 100% of Organization-to-concrete-type links are bidirectionally consistent (Organization.linked_name points to a concrete type whose organization field points back)
- **SC-003**: Organization with details retrieval completes in a single request without requiring client-side joins
- **SC-004**: Zero orphaned concrete type records exist after Organization deletions
- **SC-005**: All attempts to modify org_type on existing Organizations are rejected with appropriate error messages
- **SC-006**: System handles 100 concurrent Organization creations without data corruption or link inconsistencies
- **SC-007**: Organization retrieval with concrete type details completes within 500ms under normal load

## Clarifications

### Session 2025-12-13

- Q: Should the system log hook executions for audit and debugging? → A: Log all hook executions (create/delete) with Organization ID and outcome
- Q: Should hook operations enforce user permissions or execute with system privileges? → A: Execute with system privileges (bypass permission checks)
- Q: Should there be a response time target for retrieval methods? → A: Retrieval must complete within 500ms

## Assumptions

- The concrete type doctypes (Family, Company, Association, Nonprofit) already exist with an organization Link field pointing to Organization
- The Organization doctype already exists with linked_doctype and linked_name fields
- Frappe's document hooks (after_insert, on_trash) are the appropriate mechanism for implementing this behavior
- All four organization types will be supported at launch; no phased rollout is planned
