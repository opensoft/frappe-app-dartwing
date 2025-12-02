# Feature Specification: Person DocType

**Feature Branch**: `001-person-doctype`
**Created**: 2025-12-01
**Status**: Draft
**Input**: Person DocType - the foundational identity layer for all user interactions in Dartwing

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Create Person Record (Priority: P1)

A system administrator or automated process creates a new Person record to establish identity for a user in the system. This is the foundation for all user-related functionality.

**Why this priority**: Person is the identity layer - every user interaction requires it. Org Member links Person to Organization. Cannot implement permissions without Person → User linkage.

**Independent Test**: Can be fully tested by creating a Person record through the UI or API and verifying all required fields are captured correctly and uniqueness constraints are enforced.

**Acceptance Scenarios**:

1. **Given** no Person exists with email "john@example.com", **When** an administrator creates a Person with primary_email "john@example.com" and required fields (first_name, last_name), **Then** the Person record is created successfully with status "Active" and source captured.
2. **Given** a Person already exists with email "john@example.com", **When** an administrator attempts to create another Person with the same email, **Then** the system rejects the creation with a duplicate email error.
3. **Given** a Person is being created for a minor, **When** the is_minor flag is set to true, **Then** the system records the consent_captured flag and consent_timestamp when consent is provided.

---

### User Story 2 - Link Person to Frappe User (Priority: P1)

A Person record is linked to a Frappe User account to enable system access and permissions.

**Why this priority**: This linkage is required for authentication and authorization - users cannot access the system without it.

**Independent Test**: Can be tested by creating a Person and verifying the frappe_user link is established correctly, either manually or via Keycloak integration.

**Acceptance Scenarios**:

1. **Given** a Person exists without a frappe_user link, **When** a Keycloak user ID is set and auto-creation is enabled, **Then** a Frappe User is automatically created and linked to the Person with user_sync_status set to "synced".
2. **Given** a Person is being created with keycloak_user_id, **When** Frappe User auto-creation fails (e.g., Keycloak unavailable), **Then** the Person record is saved with user_sync_status "pending" and a background retry job is queued.
3. **Given** a Person exists with a frappe_user link, **When** another Person attempts to link to the same Frappe User, **Then** the system rejects the operation due to uniqueness constraint.
4. **Given** a Person exists with keycloak_user_id, **When** a Frappe User is created for them, **Then** the User receives the default "Dartwing User" role.

---

### User Story 3 - Prevent Deletion of Linked Person (Priority: P2)

When a Person is linked to one or more Org Members, the system prevents accidental deletion to maintain data integrity.

**Why this priority**: Referential integrity is critical for audit trails and organizational relationships, but comes after core creation functionality.

**Independent Test**: Can be tested by attempting to delete a Person who has Org Member links and verifying the deletion is blocked.

**Acceptance Scenarios**:

1. **Given** a Person is linked to at least one Org Member, **When** an administrator attempts to delete the Person, **Then** the system prevents deletion and suggests deactivation or merge instead.
2. **Given** a Person has no Org Member links, **When** an administrator deletes the Person, **Then** the Person record is removed successfully.
3. **Given** a Person needs to be removed but has Org Member links, **When** an administrator changes the Person status to "Inactive", **Then** the Person is effectively disabled without breaking referential integrity.

---

### User Story 4 - Merge Duplicate Persons (Priority: P3)

When duplicate Person records are detected (e.g., same email or Keycloak ID), the system supports merging them to maintain a single source of truth.

**Why this priority**: Data quality is important but is a corrective action rather than primary functionality.

**Independent Test**: Can be tested by creating two Person records with overlapping identifiers and executing a merge operation.

**Acceptance Scenarios**:

1. **Given** two Person records exist with the same email address (one created as stub during invitation), **When** a merge operation is initiated, **Then** all Org Member links are transferred to the surviving Person, a Merge Log entry is created (capturing source Person, target Person, timestamp, and actor), and the duplicate is soft-deleted with status set to "Merged".
2. **Given** a Person has status "Merged", **When** the system queries active Persons, **Then** merged Persons are excluded from results.

---

### Edge Cases

- What happens when a Person's primary_email needs to change? The system must verify the new email is unique before allowing the update.
- How does the system handle a Person created via import who later signs up via Keycloak? The keycloak_user_id is set on the existing Person record without creating a duplicate.
- What happens when consent_captured is false for a minor? The system MUST block all write operations (updates, status changes) on the Person record until consent is captured.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST enforce uniqueness on primary_email across all Person records.
- **FR-002**: System MUST enforce uniqueness on keycloak_user_id when set (null values are allowed, but non-null values must be unique).
- **FR-003**: System MUST enforce uniqueness on frappe_user link when set (null values are allowed, but non-null values must be unique).
- **FR-004**: System MUST capture source of Person creation (signup, invite, or import).
- **FR-005**: System MUST track Person status (Active, Inactive, or Merged).
- **FR-006**: System MUST prevent deletion of Person records that are linked to Org Member records.
- **FR-007**: System MUST capture consent information (consent_captured flag and consent_timestamp) for compliance purposes.
- **FR-008**: System MUST allow marking a Person as a minor via is_minor flag.
- **FR-013**: System MUST block all write operations (updates, status changes) on a Person record where is_minor is true and consent_captured is false.
- **FR-009**: System MUST support linking a Person to a personal Organization via personal_org field.
- **FR-010**: System MUST validate mobile_no format when provided (country-aware validation).
- **FR-011**: System MUST auto-create a Frappe User with default "Dartwing User" role when keycloak_user_id is present, no frappe_user exists, and auto-creation is enabled by site configuration.
- **FR-014**: System MUST save Person record even if Frappe User auto-creation fails, marking user_sync_status as "pending" and queuing a background job for retry.
- **FR-012**: System MUST reject Person creation or update if primary_email already exists on another Person record.

### Key Entities

- **Person**: The core identity entity representing an individual in the system. Contains personal information (name, email, mobile), identity links (keycloak_user_id, frappe_user), privacy/consent tracking, organizational relationship (personal_org), and user_sync_status (Select: synced/pending/failed) for tracking Frappe User creation state. Primary key is the auto-generated name field; primary_email, keycloak_user_id, and frappe_user serve as unique identifiers.
- **Organization**: Referenced entity that a Person can be linked to via personal_org (their personal/family organization).
- **Org Member**: Dependent entity that links a Person to an Organization (not part of this feature but creates the deletion constraint).
- **User**: Frappe's built-in User DocType that Person links to via frappe_user for system access.
- **Person Merge Log**: Child table of Person that captures merge audit history. Contains: source_person (Link), target_person (Link), merged_at (Datetime), merged_by (Link to User).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All Person records have a valid, unique primary_email - 100% uniqueness enforcement with no duplicates possible.
- **SC-002**: Duplicate Person creation attempts are rejected within 1 second with a clear error message.
- **SC-003**: Person records linked to Org Members cannot be deleted - 100% of deletion attempts on linked Persons are blocked.
- **SC-004**: Auto-creation of Frappe User from Keycloak ID completes within 2 seconds when enabled.
- **SC-005**: All Person records have valid status values (Active, Inactive, or Merged) - no orphaned or invalid states.
- **SC-006**: Person merge operations transfer all Org Member links to the surviving record without data loss.

## Clarifications

### Session 2025-12-01

- Q: What operations should be blocked when consent_captured is false for a minor? → A: Block all write operations (updates, status changes) until consent captured
- Q: How should merge operations be audited? → A: Create a separate Merge Log child table on Person with full history (source, target, timestamp, actor)
- Q: What happens when Keycloak/User creation fails during Person save? → A: Save Person but mark frappe_user as pending; queue retry via background job

## Assumptions

- Keycloak integration exists or will be implemented separately; this feature provides the data fields to support it.
- The Organization DocType exists and can be linked to via personal_org.
- The Org Member DocType will be implemented as a separate feature that references Person.
- Site configuration for auto-creation of Frappe Users will be managed outside this feature.
- Mobile number validation rules will follow E.164 or similar international standard based on country context.
- The default role "Dartwing User" exists or will be created as part of system setup.
