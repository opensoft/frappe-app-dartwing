# Feature Specification: Company DocType

**Feature Branch**: `006-company-doctype`
**Created**: 2025-12-13
**Status**: Draft
**Input**: User description: "Company DocType - Create concrete Company organization type with tax ID, entity type, jurisdiction, officers, and partners fields"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create a Company Organization (Priority: P1)

A business owner or administrator needs to register their company in the system by creating an Organization with type "Company". When they do so, the system automatically creates a linked Company record where they can store business-specific information like tax identification, legal entity type, and formation jurisdiction.

**Why this priority**: This is the foundational capability that enables all B2B use cases. Without the ability to create Company organizations, users cannot track business entities, manage employees, or use any company-specific features.

**Independent Test**: Can be fully tested by creating an Organization with org_type="Company" and verifying a linked Company record is auto-created with proper bidirectional references.

**Acceptance Scenarios**:

1. **Given** a user with permission to create organizations, **When** they create an Organization with org_type set to "Company", **Then** the system automatically creates a linked Company record with the organization reference field populated and updates the Organization's linked_doctype to "Company" and linked_name to the new Company's identifier.

2. **Given** an existing Organization with org_type="Company", **When** a user views the Organization details, **Then** they can navigate to the linked Company record and see all company-specific fields.

3. **Given** a user attempts to create an Organization with org_type="Company", **When** they provide a valid organization name, **Then** the Company record is created with status fields properly initialized.

---

### User Story 2 - Record Legal Entity Information (Priority: P1)

A company administrator needs to document their company's legal entity details including the official legal name, tax identification number (EIN/Tax ID), entity type (LLC, C-Corp, S-Corp, etc.), and jurisdiction of formation. This information is essential for compliance, financial reporting, and official business documentation.

**Why this priority**: Legal entity information is fundamental to company operations and is required for tax compliance, contracts, and regulatory filings. Users cannot properly manage a business entity without recording these core details.

**Independent Test**: Can be tested by editing a Company record's legal fields and verifying they are properly saved and retrievable, with appropriate validation on entity type selections.

**Acceptance Scenarios**:

1. **Given** an existing Company record, **When** a user enters the legal entity name, tax ID, entity type, and jurisdiction, **Then** all fields are saved and displayed correctly upon retrieval.

2. **Given** a Company record being edited, **When** a user selects an entity type from the available options (C-Corp, S-Corp, LLC, Limited Partnership (LP), General Partnership, LLP, WFOE (China), Benefit Corporation, Cooperative), **Then** the selection is saved and the appropriate conditional fields become visible based on entity type.

3. **Given** a Company record, **When** a user enters a formation date and jurisdiction (country and state/province), **Then** the information is persisted and visible in the company profile.

---

### User Story 3 - Manage Company Officers and Directors (Priority: P2)

A company administrator needs to maintain a list of officers and directors for their company, including their titles (CEO, CFO, President, Director, etc.) and the dates they held those positions. This is required for corporate governance, legal filings, and organizational transparency.

**Why this priority**: While not required for basic company creation, officer and director tracking is essential for corporate compliance, especially for corporations that must maintain records of their board and executive officers.

**Independent Test**: Can be tested by adding, editing, and removing officer entries from a Company record and verifying the child table properly stores person references, titles, and date ranges.

**Acceptance Scenarios**:

1. **Given** an existing Company record, **When** a user adds an officer entry with a linked Person, title, and start date, **Then** the officer appears in the company's officers list.

2. **Given** a Company with existing officers, **When** a user sets an end date for an officer, **Then** the officer record reflects their tenure period while remaining in the historical record.

3. **Given** a Company record, **When** a user attempts to add an officer without specifying a Person reference or title, **Then** the system prevents the save and indicates the required fields.

---

### User Story 4 - Track LLC/Partnership Ownership (Priority: P2)

For LLCs and partnerships, the company administrator needs to record the members or partners, their ownership percentages, capital contributions, and voting rights. This information is specific to entity types that have member/partner structures rather than shareholders.

**Why this priority**: Ownership tracking is critical for LLCs and partnerships but only applicable to certain entity types. It enables proper profit distribution calculations and voting power determination.

**Independent Test**: Can be tested by selecting an LLC or Partnership entity type and adding member/partner entries with ownership details, then verifying the data is properly stored and displayed.

**Acceptance Scenarios**:

1. **Given** a Company with entity type "LLC" or "Partnership" variant, **When** a user views the company form, **Then** the ownership/members/partners section is visible.

2. **Given** a Company with entity type "C-Corp", **When** a user views the company form, **Then** the ownership/members/partners section is hidden (as corporations use shareholders, not members).

3. **Given** an LLC Company record, **When** a user adds a member with ownership percentage, capital contribution, and voting rights percentage, **Then** all values are saved and displayed correctly.

4. **Given** a Company with multiple members, **When** the total ownership percentages exceed 100%, **Then** the system displays a warning to alert the user of the discrepancy.

---

### User Story 5 - Manage Company Addresses (Priority: P3)

A company administrator needs to record different types of addresses for the company: registered address (legal address for service of process), physical/principal address (where business operations occur), and optionally a registered agent's information for legal correspondence.

**Why this priority**: Address management is important for compliance but is secondary to basic entity creation and legal entity information. Companies can function with minimal address data initially.

**Independent Test**: Can be tested by linking Address records to the Company's registered and physical address fields and verifying the references are properly stored.

**Acceptance Scenarios**:

1. **Given** an existing Company record, **When** a user links an Address to the registered address field, **Then** the address reference is saved and the linked address details are accessible.

2. **Given** a Company record, **When** a user specifies both a registered address and a physical address, **Then** both address references are maintained independently.

3. **Given** a Company record, **When** a user links a Person as the registered agent, **Then** the Person reference is saved and associated with the company.

---

### Edge Cases

- What happens when an Organization with org_type="Company" is deleted? The linked Company record must be cascade-deleted to maintain data integrity.
- How does the system handle a Company record being accessed directly (not through Organization)? The Company's organization reference field should provide navigation back to the parent Organization.
- What happens when ownership percentages don't sum to 100%? The system should display a warning but not prevent saving, as partial ownership records may be entered incrementally.
- How does the system handle entity type changes? Entity type should be changeable (unlike org_type on Organization which is immutable), but changing it should display a warning about conditional fields that may become hidden.
- What happens if a Person linked as an officer or member is deleted? The deletion should be prevented with an appropriate error message indicating the Person is still linked to Company records.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically create a Company record when an Organization is created with org_type set to "Company"
- **FR-002**: System MUST maintain bidirectional linking between Organization and Company (Organization stores linked_doctype="Company" and linked_name, Company stores organization reference)
- **FR-003**: System MUST cascade delete the Company record when the parent Organization is deleted
- **FR-004**: System MUST provide fields for legal entity information: legal_name, tax_id, entity_type, jurisdiction_country, jurisdiction_state, and formation_date
- **FR-005**: System MUST support entity types: C-Corp, S-Corp, LLC, Limited Partnership (LP), General Partnership, LLP, WFOE (China), Benefit Corporation, Cooperative
- **FR-006**: System MUST display the ownership/members/partners section only for applicable entity types (LLC, Limited Partnership, LLP, General Partnership)
- **FR-007**: System MUST allow tracking of officers and directors with Person reference, title, start date, and optional end date
- **FR-008**: System MUST allow tracking of members/partners with Person reference, ownership percentage, capital contribution, and voting rights percentage
- **FR-009**: System MUST support linking Address records for registered address and physical/principal address
- **FR-010**: System MUST support linking a Person as registered agent
- **FR-011**: System MUST inherit the OrganizationMixin to provide access to parent Organization's org_name, logo, and status
- **FR-012**: System MUST respect user permissions inherited through the Organization's User Permission system (users can only access Companies for Organizations they have permission to view)
- **FR-013**: System MUST provide a naming series for Company records (format: CO-.#####)
- **FR-014**: System MUST require the organization field and make it read-only (set automatically by hooks)

### Key Entities

- **Company**: The concrete organization type representing a business entity. Linked 1:1 to an Organization record where org_type="Company". Contains legal entity details, addresses, and references to child tables for officers and ownership.

- **Organization Officer (Child Table)**: Records individuals serving as officers or directors of the company. References a Person, includes title and date range of service. Shared child table also used by Nonprofit for board members.

- **Organization Member Partner (Child Table)**: Records members (for LLCs) or partners (for partnerships) with their ownership stake. References a Person, includes ownership percentage, capital contribution amount, and voting rights percentage. Only applicable to certain entity types.

- **Organization (Reference)**: The parent polymorphic identity shell that all Companies link back to. Provides the org_name, logo, and status that apply across all organization types.

- **Address (Reference)**: Standard address records that can be linked as registered address or physical address.

- **Person (Reference)**: Individual identity records linked as registered agent, officers, or members/partners.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a Company organization and have the linked Company record auto-created in under 5 seconds
- **SC-002**: 100% of Company records maintain valid bidirectional links to their parent Organization (no orphaned records)
- **SC-003**: Users can complete basic legal entity information entry (name, tax ID, entity type, jurisdiction) in under 2 minutes
- **SC-004**: Users can add officers and members/partners to a Company record with all required fields validated
- **SC-005**: Conditional field visibility (ownership section for LLCs/partnerships) functions correctly for all entity type selections
- **SC-006**: Company records are only accessible to users with proper Organization permissions (verified through permission tests)
- **SC-007**: Deleting an Organization with org_type="Company" successfully cascade-deletes the linked Company record with no orphaned data
- **SC-008**: The Company DocType integrates seamlessly with the existing Organization infrastructure and passes all integration tests
