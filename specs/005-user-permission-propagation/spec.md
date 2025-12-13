# Feature Specification: User Permission Propagation

**Feature Branch**: `005-user-permission-propagation`
**Created**: 2025-12-13
**Status**: Draft
**Input**: User description: "User Permission Propagation - Security foundation for multi-org data access control"

## Clarifications

### Session 2025-12-13

- Q: How is "Dartwing Admin" administrative scope determined? → A: Admins access orgs where they have an Org Member with supervisor/admin role
- Q: What permission-related events should be logged for audit/debugging? → A: Log all permission create/remove events plus skip events (standard level)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Single Organization Member Access (Priority: P1)

A user joins an organization as a member and can immediately see only that organization's data. When Sarah is added as a member of "Acme Corp" organization, she should be able to view Acme Corp's records, employees, and equipment, but cannot see data from other organizations like "Beta LLC" or "Smith Family".

**Why this priority**: This is the foundational security requirement. Without proper permission isolation, users could access unauthorized data, creating compliance and privacy violations.

**Independent Test**: Can be fully tested by creating a user, adding them to one organization as a member, and verifying they can only see that organization's data in list views and individual record access.

**Acceptance Scenarios**:

1. **Given** a Person record exists and is linked to a Frappe User, **When** an Org Member record is created linking that Person to an Organization, **Then** the user receives permission to access that Organization's records.

2. **Given** a user has permission to access Organization A, **When** they attempt to view Organization B's data (which they are not a member of), **Then** the system denies access and returns an appropriate error.

3. **Given** a user is a member of an Organization, **When** they view list pages for Organization, Equipment, or other org-linked records, **Then** only records belonging to their Organization(s) are displayed.

---

### User Story 2 - Multi-Organization Access (Priority: P1)

A user who belongs to multiple organizations can access data from all their organizations while still being restricted from others. When John is a member of both "Smith Family" and "Smith Consulting LLC", he should be able to see and manage data for both organizations, but not for unrelated organizations.

**Why this priority**: Many real-world users (business owners, family members with side businesses) belong to multiple organizations. This use case is essential for the platform's target market.

**Independent Test**: Can be fully tested by adding a user as a member of two different organizations and verifying they can access both, but not a third organization they're not a member of.

**Acceptance Scenarios**:

1. **Given** a Person is linked to Org Members in Organization A and Organization B, **When** the user views organization-filtered lists, **Then** records from both Organization A and Organization B are visible.

2. **Given** a user has access to multiple organizations, **When** they access a specific record from one of their organizations, **Then** permission is granted and the record is displayed.

3. **Given** a user has access to Organizations A and B, **When** they attempt to access Organization C (not a member), **Then** access is denied.

---

### User Story 3 - Concrete Type Permission Inheritance (Priority: P2)

When a user has permission to access an Organization, they automatically have permission to access its concrete type record (Family, Company, etc.) and related type-specific records. When Maria has access to "Tech Corp" Organization, she should also be able to access the "Tech Corp" Company record with its tax information, officers, and partners.

**Why this priority**: The hybrid Organization model requires seamless permission inheritance to prevent users from accessing the shell but not the meaningful data, or vice versa.

**Independent Test**: Can be fully tested by granting Organization access and verifying automatic access to the linked concrete type (Family or Company) without additional permission configuration.

**Acceptance Scenarios**:

1. **Given** a user has permission to access an Organization with org_type "Company", **When** they access the linked Company concrete type record, **Then** permission is granted automatically.

2. **Given** a user has permission to access an Organization with org_type "Family", **When** they view Family records in list view, **Then** only Families linked to their permitted Organizations are shown.

3. **Given** a user does NOT have permission to an Organization, **When** they attempt to access that Organization's concrete type directly, **Then** access is denied.

---

### User Story 4 - Permission Removal on Membership End (Priority: P2)

When a user's membership in an organization ends (deleted or made inactive), their permissions to that organization's data are immediately revoked. When David leaves "Acme Corp", his access to Acme Corp's data should be removed while preserving his access to other organizations he belongs to.

**Why this priority**: Proper offboarding prevents data leaks and unauthorized access by former members. This is critical for compliance and security.

**Independent Test**: Can be fully tested by creating an Org Member, verifying access exists, then deleting the Org Member and verifying access is removed.

**Acceptance Scenarios**:

1. **Given** a user is a member of Organization A, **When** their Org Member record is deleted, **Then** their permission to access Organization A is removed.

2. **Given** a user is a member of Organizations A and B, **When** their Org Member for Organization A is deleted, **Then** they lose access to Organization A but retain access to Organization B.

3. **Given** a user's Org Member status changes to "Inactive", **When** they attempt to access that Organization's data, **Then** access is denied (permissions treated same as deleted).

---

### User Story 5 - System Administrator Override (Priority: P3)

System administrators can access all organizations regardless of membership for troubleshooting and support purposes.

**Why this priority**: Administrative access is needed for platform operations, but is a lower priority than user-facing security because it affects fewer users.

**Independent Test**: Can be fully tested by verifying a System Manager role user can access any Organization's data without Org Member records.

**Acceptance Scenarios**:

1. **Given** a user has the "System Manager" role, **When** they view any Organization's data, **Then** access is granted regardless of Org Member records.

2. **Given** a user has the "Dartwing Admin" role (multi-org admin), **When** they view Organizations where they have an Org Member record with a supervisor or admin-level role, **Then** access is granted to those Organizations.

---

### Edge Cases

- What happens when a Person record exists but is not linked to a Frappe User yet? Permissions should not be created until the Person-User linkage exists.
- What happens when an Org Member is created for a Person without a linked User? Permission creation should be skipped gracefully and logged.
- What happens when the same Person is added as Org Member twice to the same Organization? Feature 3's unique constraint prevents this. This feature's permission helpers are idempotent as a defensive measure.
- What happens when an Organization is deleted? Cascade deletion should remove Org Members and their associated User Permissions.
- What happens when a Person's linked User account is disabled? Permissions remain but are ineffective since the User cannot log in.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST automatically create a User Permission for the Organization when an Org Member record is created.
- **FR-002**: System MUST automatically create a User Permission for the concrete type (Family/Company/Association/Nonprofit) when an Org Member record is created.
- **FR-003**: System MUST automatically remove User Permissions for both Organization and concrete type when an Org Member record is deleted.
- **FR-004**: System MUST filter list views to show only records the user has permission to access.
- **FR-005**: System MUST deny access to individual records the user does not have permission to view.
- **FR-006**: System MUST allow users with "System Manager" role to bypass permission checks.
- **FR-007**: System MUST handle the case where a Person has no linked Frappe User by skipping permission creation without error.
- **FR-008**: System MUST prevent duplicate Org Member records for the same person and organization combination. *(Implemented by Feature 3 via unique constraint; this feature assumes the constraint exists.)*
- **FR-009**: System MUST treat "Inactive" Org Member status the same as deleted for permission purposes (remove permissions when status changes to Inactive).
- **FR-010**: System MUST provide permission query condition functions that can be registered for each doctype that needs Organization-based filtering.
- **FR-011**: System MUST provide a has_permission function for single document access checks.
- **FR-012**: System MUST log all permission lifecycle events: permission creation, permission removal, and permission skip events (when Person has no linked User), for audit and debugging purposes.

### Key Entities

- **User Permission**: A record that grants a specific user access to a specific value of a specific doctype. Links a Frappe User to an "allow" doctype (Organization or concrete type) and a "for_value" (the specific record name).
- **Org Member**: The junction record linking a Person to an Organization with a role. This is the trigger for permission propagation.
- **Person**: Individual identity that may or may not be linked to a Frappe User. Only Persons with linked Users receive permissions.
- **Organization**: The polymorphic identity shell that serves as the primary permission target.
- **Concrete Types (Family/Company/Association/Nonprofit)**: Type-specific records that inherit permissions from their linked Organization.

## Assumptions

- The Person doctype includes a `frappe_user` field that links to the Frappe User doctype.
- The Org Member doctype has fields for `person`, `organization`, `role`, and `status`.
- Each concrete type (Family, Company, etc.) has an `organization` field linking back to its parent Organization.
- Frappe's built-in permission system supports permission query conditions and has_permission hooks.

## Dependencies

This feature depends on the following being implemented by other features:

| Dependency | Feature | Description |
|------------|---------|-------------|
| Org Member unique constraint | Feature 3 (Org Member DocType) | Unique constraint on `person + organization` prevents duplicate memberships. This feature's permission logic assumes no duplicates exist. |
| Person.frappe_user field | Feature 1 (Person DocType) | Link field to Frappe User that determines which user receives permissions. |
| Organization.linked_doctype/linked_name | Feature 2 (Organization DocType) | Fields that identify the concrete type for permission inheritance. |

## Security Considerations

### Backward Compatibility for Orphaned Records

Records created before org-based permissions were implemented may lack an `organization` field value. The permission system handles these "orphaned" records by **allowing access** rather than denying it.

**Rationale**: Denying access to orphaned records would lock users out of legitimate data they created before the permission system existed. This is a deliberate trade-off:

- **Risk**: Orphaned records are accessible to any authenticated user until migrated
- **Mitigation**: All access to orphaned records is logged as a "Permission Warning" for audit visibility
- **Remediation**: Orphaned records should be migrated to have an organization assignment

**Affected DocTypes**: Organization, Family, Company, Association, Nonprofit

**Migration Recommendation**: After deploying this feature, run a data migration to assign organizations to any records with null `organization` fields. Monitor the "Permission Warning" error logs to identify orphaned records requiring migration.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can only see records from Organizations they are members of, verified by 100% of list view queries returning correctly filtered results.
- **SC-002**: Adding a new Org Member grants access within 1 second (permission creation happens synchronously with Org Member creation).
- **SC-003**: Removing an Org Member revokes access immediately (no cached access persists).
- **SC-004**: Multi-organization users see combined results from all their organizations in list views without additional configuration.
- **SC-005**: Zero unauthorized data access incidents in testing (all permission boundary tests pass).
- **SC-006**: Permission checks add no more than 50ms latency to typical page loads.
