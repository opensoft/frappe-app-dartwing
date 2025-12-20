# Feature Specification: Equipment DocType

**Feature Branch**: `007-equipment-doctype`
**Created**: 2025-12-14
**Status**: Draft
**Input**: User description: "Equipment DocType - asset management doctype for tracking equipment owned by organizations"

## Clarifications

### Session 2025-12-14

- Q: What happens when equipment's owning organization is deleted? → A: Block deletion - Organization cannot be deleted while equipment exists
- Q: What happens when the assigned person is removed from the organization? → A: Block removal - Prevent person removal from org while equipment is assigned

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Register New Equipment (Priority: P1)

An organization administrator needs to register a new piece of equipment in the system. They access the equipment management area, create a new equipment record with basic details (name, type, serial number), and assign it to their organization. The equipment appears in their organization's asset inventory.

**Why this priority**: This is the foundational capability - without being able to create equipment records, no other equipment management features can function. Every organization needs to track their assets.

**Independent Test**: Can be fully tested by creating an equipment record with required fields and verifying it appears in the organization's equipment list. Delivers immediate value by establishing the asset registry.

**Acceptance Scenarios**:

1. **Given** an authenticated user who is a member of an organization, **When** they create a new equipment record with name, type, and serial number, **Then** the equipment is saved and linked to their organization.
2. **Given** an authenticated user creating equipment, **When** they attempt to save without providing a name, **Then** the system prevents saving and displays a validation message.
3. **Given** an authenticated user creating equipment, **When** they enter a serial number that already exists in the system, **Then** the system prevents saving and displays a duplicate warning.

---

### User Story 2 - View Organization Equipment List (Priority: P1)

An organization member needs to view all equipment owned by their organization. They navigate to the equipment section and see a list of all equipment with key details (name, type, status, assigned person). They can only see equipment belonging to organizations they are members of.

**Why this priority**: Users need to discover and browse existing equipment. This is essential for day-to-day operations and prevents duplicate registrations.

**Independent Test**: Can be fully tested by querying equipment for an organization and verifying only authorized equipment appears. Delivers immediate operational value.

**Acceptance Scenarios**:

1. **Given** a user who is a member of Organization A, **When** they view the equipment list, **Then** they see only equipment belonging to Organization A.
2. **Given** a user who is a member of multiple organizations, **When** they view equipment, **Then** they can filter by organization to see relevant equipment.
3. **Given** a user who is not a member of any organization, **When** they attempt to view equipment, **Then** they see an empty list (no access to any equipment).

---

### User Story 3 - Assign Equipment to Person (Priority: P2)

An organization member with write access assigns a piece of equipment to a specific person within their organization. They select equipment, choose a person from the organization's members, and confirm the assignment.

**Why this priority**: Assignment tracking is a core asset management function but depends on equipment creation being complete. Most organizations need to know who is responsible for each asset.

**Independent Test**: Can be tested by assigning equipment to a person and verifying the assignment appears on both the equipment record and is queryable by person.

**Acceptance Scenarios**:

1. **Given** a user with write access viewing equipment details, **When** they select a person from the organization's members and assign the equipment, **Then** the equipment record shows the assigned person.
2. **Given** equipment already assigned to Person A, **When** a user reassigns it to Person B, **Then** the equipment shows Person B as the current assignee.
3. **Given** equipment that needs to be unassigned, **When** a user clears the assignment, **Then** the equipment shows no assigned person.

---

### User Story 4 - Track Equipment Location (Priority: P2)

An organization member records the current location of a piece of equipment by linking it to an address. This helps track where physical assets are located, especially for organizations with multiple sites.

**Why this priority**: Location tracking is important for asset management but is a secondary concern after knowing what assets exist and who is responsible for them.

**Independent Test**: Can be tested by setting an address on equipment and verifying the location is retrievable.

**Acceptance Scenarios**:

1. **Given** equipment with no location set, **When** a user links an address to the equipment, **Then** the equipment displays the address as its current location.
2. **Given** equipment at Location A, **When** the equipment is moved and the location is updated to Location B, **Then** the equipment shows Location B as current location.

---

### User Story 5 - Attach Documents to Equipment (Priority: P3)

An organization member attaches documents to an equipment record, such as manuals, warranty certificates, or purchase receipts. These documents are stored with the equipment record for easy reference.

**Why this priority**: Document attachment enhances equipment records but is not essential for basic asset tracking. Organizations can function without this initially.

**Independent Test**: Can be tested by uploading a document to equipment and verifying it can be retrieved and downloaded.

**Acceptance Scenarios**:

1. **Given** an equipment record, **When** a user attaches a document with a type label (e.g., "Manual"), **Then** the document appears in the equipment's document list with its type.
2. **Given** equipment with multiple documents, **When** a user views the equipment, **Then** all attached documents are listed and downloadable.
3. **Given** a document attached to equipment, **When** a user removes the document, **Then** the document no longer appears in the equipment's document list.

---

### User Story 6 - Schedule Equipment Maintenance (Priority: P3)

An organization member sets up recurring maintenance tasks for equipment, such as annual inspections or monthly servicing. The system tracks when each maintenance task is next due.

**Why this priority**: Maintenance scheduling is valuable for compliance and equipment longevity but requires the core equipment tracking to be in place first.

**Independent Test**: Can be tested by creating a maintenance schedule and verifying the next due date is calculated correctly.

**Acceptance Scenarios**:

1. **Given** an equipment record, **When** a user adds a maintenance task with frequency "Monthly" and sets the next due date, **Then** the task appears in the equipment's maintenance schedule.
2. **Given** equipment with multiple maintenance tasks, **When** a user views the equipment, **Then** all scheduled maintenance tasks are visible with their due dates.
3. **Given** a maintenance task, **When** a user removes the task, **Then** it no longer appears in the maintenance schedule.

---

### User Story 7 - Update Equipment Status (Priority: P2)

An organization member updates the status of equipment to reflect its current operational state (Active, In Repair, Retired). This helps organizations know which assets are available for use.

**Why this priority**: Status tracking is important for operational visibility and helps organizations manage their asset lifecycle.

**Independent Test**: Can be tested by changing equipment status and verifying the change is reflected in equipment lists and filters.

**Acceptance Scenarios**:

1. **Given** equipment with status "Active", **When** a user changes the status to "In Repair", **Then** the equipment displays the new status.
2. **Given** equipment with status "In Repair", **When** a user changes the status to "Retired", **Then** the equipment displays "Retired" status.
3. **Given** an equipment list, **When** a user filters by status "Active", **Then** only active equipment appears in the results.

---

### Edge Cases

- When equipment's owning organization is deleted: System MUST block deletion and display an error indicating equipment must be transferred or deleted first.
- When assigned person is removed from organization: System MUST block Org Member deactivation/deletion and display an error indicating equipment must be reassigned first.
- When user tries to create equipment without belonging to any organization: System MUST prevent creation and display an error message.
- Duplicate serial numbers: Serial numbers are globally unique across all organizations (enforced by FR-002).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow organization members to create equipment records with a name and owner organization.
- **FR-002**: System MUST enforce uniqueness of serial numbers across all equipment records.
- **FR-003**: System MUST restrict equipment visibility to members of the owning organization.
- **FR-004**: System MUST allow equipment to be assigned to a Person within the owning organization.
- **FR-005**: System MUST allow equipment to be linked to an Address for location tracking.
- **FR-006**: System MUST support equipment status values: Active, In Repair, and Retired.
- **FR-007**: System MUST allow multiple documents to be attached to equipment with type labels.
- **FR-008**: System MUST allow maintenance tasks to be scheduled with frequency (Daily, Weekly, Monthly, Quarterly, Yearly) and next due date.
- **FR-009**: System MUST filter equipment lists by the user's organization permissions (via User Permission on Organization). *(Implementation mechanism for FR-003)*
- **FR-010**: System MUST validate that assigned person is a member of the same organization as the equipment.
- **FR-011**: System MUST support equipment categorization by type (e.g., Vehicle, Electronics, Furniture, Machinery, Tools, Other).
- **FR-012**: System MUST prevent deletion of an Organization that has associated equipment records.
- **FR-013**: System MUST prevent deactivation or removal of an Org Member who has equipment assigned to them.

### Key Entities

- **Equipment**: The primary entity representing a physical asset. Contains name, serial number, status, type, and relationships to organization, person (assignee), and address (location). Has child tables for documents and maintenance schedules.
- **Equipment Document (Child)**: Attached documents with type classification (e.g., Manual, Warranty, Receipt, Inspection Report). Each document has a type label and file attachment.
- **Equipment Maintenance (Child)**: Recurring maintenance tasks with task description, frequency, and next due date. Tracks scheduled servicing requirements.
- **Organization**: Parent entity that owns equipment. Equipment inherits access permissions through the Organization link.
- **Person**: Entity that can be assigned equipment. Must be a member of the equipment's organization.
- **Address**: Entity representing physical locations. Equipment can reference an address for location tracking.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create and save a new equipment record within 1 minute including all required fields.
- **SC-002**: Equipment list loads and displays within 2 seconds for organizations with up to 1000 equipment items.
- **SC-003**: 95% of users can successfully find specific equipment using search/filter within 30 seconds.
- **SC-004**: Users can only view equipment from organizations they belong to (100% permission enforcement).
- **SC-005**: Equipment assignment to person completes in a single action with no additional steps required.
- **SC-006**: Document uploads complete successfully and files are retrievable 100% of the time.
- **SC-007**: Duplicate serial number attempts are blocked with clear user feedback in 100% of cases.

## Assumptions

- The Organization doctype already exists and has the hybrid architecture with bidirectional linking implemented.
- User Permission propagation (Feature 5) is implemented, so users have appropriate Organization permissions.
- The Person doctype (Feature 1) exists and can be linked to equipment.
- The Address doctype is available for location linking (standard Frappe Address or custom implementation).
- Equipment is owned at the Organization level (polymorphic), not at the concrete type level (Family, Company, etc.).
- All organization types (Family, Company, Nonprofit, Association) can own equipment.

## Dependencies

- **Feature 1 (Person DocType)**: Required for equipment assignment to persons.
- **Feature 5 (User Permission Propagation)**: Required for filtering equipment by organization access.
- **Organization DocType**: Must exist with polymorphic linking pattern.
- **Address DocType**: Required for location tracking (can use Frappe's standard Address).
