# Feature Specification: Org Member DocType

**Feature Branch**: `003-org-member-doctype`
**Created**: 2025-12-12
**Status**: Draft
**Input**: User description: "Org Member DocType - Links Person to Organization with Role assignment, enabling multi-user functionality and permission propagation"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add Member to Organization (Priority: P1)

An organization administrator adds a new member to their organization by selecting an existing Person and assigning them a role. This is the foundational action that enables all multi-user functionality within the system.

**Why this priority**: This is the core purpose of the Org Member entity - without the ability to add members to organizations, no multi-user collaboration is possible. Every subsequent feature (permissions, role-based access, member management) depends on this capability.

**Independent Test**: Can be fully tested by creating an Organization, a Person, a Role Template, and then creating an Org Member linking them. Delivers immediate value by establishing the person's membership in the organization.

**Acceptance Scenarios**:

1. **Given** an existing Organization, Person, and Role Template matching the organization type, **When** an administrator creates an Org Member record linking the Person to the Organization with the selected role, **Then** the membership is recorded with status "Active", start_date defaults to today, and the Person appears in the organization's member list.

2. **Given** an Organization of type "Family" and a Role Template that applies to "Company", **When** an administrator attempts to assign that role to a new member, **Then** the system prevents the assignment and displays a message indicating the role is not valid for this organization type.

3. **Given** a Person who is already an active member of an Organization, **When** an administrator attempts to add them again to the same Organization, **Then** the system prevents the duplicate and displays a message indicating the person is already a member.

4. **Given** a Person who was previously a member (Inactive status) of an Organization, **When** an administrator adds them to the same Organization, **Then** the system reactivates the existing Org Member record by setting status to "Active" and updating start_date to today.

---

### User Story 2 - View Organization Members (Priority: P1)

An organization administrator or member views the list of all members belonging to their organization, including each member's role, status, and membership duration.

**Why this priority**: Visibility into who belongs to an organization is essential for collaboration, communication, and management. This enables administrators to understand their team composition.

**Independent Test**: Can be fully tested by creating multiple Org Member records for an Organization and verifying they all appear in a member list view with correct details.

**Acceptance Scenarios**:

1. **Given** an Organization with multiple members in various roles, **When** a user with access to that Organization views the member list, **Then** they see all active members with their names, roles, and start dates.

2. **Given** an Organization with both Active and Inactive members, **When** a user views the member list, **Then** they can distinguish between active and inactive members (inactive members may be hidden by default or visually distinguished).

---

### User Story 3 - Manage Member Status (Priority: P2)

An organization administrator changes a member's status (Active, Inactive, Pending) to reflect their current relationship with the organization without deleting historical membership records.

**Why this priority**: Organizations need to manage member lifecycles - people leave, go on leave, or have pending invitations. Maintaining status rather than deleting records preserves audit history and enables reactivation.

**Independent Test**: Can be fully tested by creating an Org Member, changing their status from Active to Inactive, and verifying the status change persists and affects visibility.

**Acceptance Scenarios**:

1. **Given** an active Org Member, **When** an administrator changes their status to "Inactive" and optionally sets an end_date, **Then** the member's status updates to Inactive, they no longer appear in active member counts, but their membership record is preserved.

2. **Given** an inactive Org Member, **When** an administrator changes their status back to "Active", **Then** the member's status updates to Active and they regain visibility in active member lists.

3. **Given** a new Org Member created with status "Pending", **When** the invitation is accepted (or administrator manually activates), **Then** the status changes to "Active" with the current date as the effective start.

---

### User Story 4 - Change Member Role (Priority: P2)

An organization administrator changes a member's assigned role to reflect promotions, demotions, or role reassignments within the organization.

**Why this priority**: Organizations evolve and people's responsibilities change. The ability to update roles without removing and re-adding members maintains continuity and history.

**Independent Test**: Can be fully tested by creating an Org Member with one role, changing to a different valid role, and verifying the role change is reflected.

**Acceptance Scenarios**:

1. **Given** an Org Member with role "Employee" in a Company organization, **When** an administrator changes their role to "Manager", **Then** the member's role updates to Manager and any role-based access changes take effect.

2. **Given** an Org Member in a Family organization, **When** an administrator attempts to change their role to a Company-specific role (e.g., "Employee"), **Then** the system prevents the change and displays a message indicating the role is not valid for this organization type.

---

### User Story 5 - Remove Member from Organization (Priority: P3)

An organization administrator removes a member from the organization, ending their membership relationship. This action should be deliberate and may require confirmation.

**Why this priority**: While less common than adding members, the ability to remove members is necessary for complete lifecycle management. The system should preserve historical records when appropriate.

**Independent Test**: Can be fully tested by creating an Org Member and then removing them, verifying the membership is ended.

**Acceptance Scenarios**:

1. **Given** an active Org Member, **When** an administrator removes them from the organization, **Then** the membership is ended by setting status to "Inactive" with end_date set to today (preserving membership history for audit purposes).

2. **Given** an Org Member who is the last member with an admin-level role in an Organization, **When** an administrator attempts to remove or deactivate them, **Then** the system prevents the action and displays a message indicating at least one administrator must remain.

---

### Edge Cases

- What happens when a Person is deleted who has Org Member records? The system performs a soft-cascade: all associated Org Member records are set to status "Inactive" with end_date set to the deletion date, preserving membership history.
- How does the system handle when a Role Template is deleted that is assigned to existing Org Members? The system should prevent deletion of in-use roles.
- What happens when an Organization is deleted that has Org Members? The Org Member records should be cleaned up as part of the cascade.
- How does the system handle concurrent membership in multiple organizations? A Person can be a member of multiple Organizations, each with different roles.
- What happens when the organization type changes (if ever allowed)? Organization type is immutable after creation per architecture, so role compatibility is ensured at creation time.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow creating an Org Member record that links a Person to an Organization with an assigned Role Template.
- **FR-002**: System MUST enforce that the (Person, Organization) combination is unique regardless of status - only one Org Member record per Person-Organization pair. Rejoining is handled by updating the existing record's status back to Active.
- **FR-003**: System MUST validate that the assigned Role Template is compatible with the Organization's type (e.g., Family roles only for Family organizations).
- **FR-004**: System MUST default the start_date to the current date when creating a new Org Member if not specified.
- **FR-005**: System MUST default the status to "Active" when creating a new Org Member if not specified.
- **FR-006**: System MUST track membership status with values: Active, Inactive, Pending.
- **FR-007**: System MUST allow updating the status of an Org Member (Active to Inactive, Pending to Active, etc.).
- **FR-008**: System MUST allow changing the assigned Role Template (within valid roles for the organization type).
- **FR-009**: System MUST optionally track an end_date when a membership ends.
- **FR-010**: System MUST soft-cascade when a Person is deleted: set all associated Org Member records to status "Inactive" with end_date set to deletion date.
- **FR-011**: System MUST prevent deletion of a Role Template that is currently assigned to any Org Member.
- **FR-012**: System MUST cascade delete Org Member records when their parent Organization is deleted.
- **FR-013**: System MUST provide a way to list all Org Members for a given Organization.
- **FR-014**: System MUST provide a way to list all Organizations a given Person belongs to.
- **FR-015**: System MUST prevent removal or deactivation of the last Org Member with a supervisor role in an Organization (uses Role Template's `is_supervisor` flag).

### Key Entities

- **Org Member**: The membership record linking a Person to an Organization with a specific role. Key attributes: person reference, organization reference, role reference, start date, optional end date, status (Active/Inactive/Pending).
- **Person**: An individual human identity in the system. Referenced by Org Member to identify who the member is.
- **Organization**: The polymorphic organization entity (Family, Company, Nonprofit, Association). Referenced by Org Member to identify which organization the membership belongs to.
- **Role Template**: Defines roles available per organization type. Referenced by Org Member to specify what role the person has within the organization.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Administrators can add a new member to an organization in under 30 seconds.
- **SC-002**: 100% of Org Member records correctly enforce the unique (Person, Organization) constraint.
- **SC-003**: 100% of role assignments are validated against the organization type before saving.
- **SC-004**: Users can view the member list for any organization they have access to within 2 seconds.
- **SC-005**: Member status changes (Active to Inactive or vice versa) take effect immediately upon save.
- **SC-006**: The system correctly cascades Org Member deletion when an Organization is deleted in 100% of cases.
- **SC-007**: Administrators successfully complete the member addition flow on first attempt at least 90% of the time.

## Clarifications

### Session 2025-12-12

- Q: When a Person is deleted, what should happen to their Org Member records? → A: Soft delete cascade - set Org Member status to "Inactive" with end_date when Person is deleted
- Q: Should the unique constraint on (Person, Organization) allow multiple records if status differs? → A: One record per (Person, Org) - update existing record's status when rejoining
- Q: Should the "last administrator protection" be implemented in this feature or deferred to the permission system? → A: Implement now - validate against removing last admin-level role holder in this feature

## Assumptions

- Person DocType is already implemented and available for linking.
- Role Template DocType is already implemented with roles filtered by applies_to_org_type and includes an `is_supervisor` flag to identify admin-level roles.
- Organization DocType exists with org_type field that determines which Role Templates are valid.
- The permission system (Feature 5 in roadmap) will be implemented separately to handle user access propagation based on Org Member records.
- Org Member is a standalone DocType (not a child table) to support direct querying and independent permissions.
