# Feature Specification: Role Template DocType

**Feature Branch**: `002-role-template-doctype`
**Created**: 2025-12-03
**Status**: Draft
**Input**: User description: "Create organization-type-specific role definitions with supervisor flags and conditional fields. Roles include Family roles (Parent, Child, Guardian, Extended Family), Company roles (Owner, Manager, Employee, Contractor), Nonprofit roles (Board Member, Volunteer, Staff), and Association roles (President, Member, Honorary). Seed data required for all org types (14 predefined roles total)."

## Overview

The Role Template DocType provides a centralized system for defining organization-type-specific roles that are assigned to members when they join an organization. This is a foundational component that enables the Org Member DocType (Feature 3) to assign roles and the permission system (Feature 5) to enforce role-based access control.

Role Templates are system-wide definitions (not per-organization) that categorize roles by organization type and specify role capabilities like supervisor status and conditional fields such as hourly rate for Company roles.

## Clarifications

### Session 2025-12-03

- Q: What is the canonical name for the "Club/Association" organization type? → A: "Association" is the canonical org type. Club is a subtype of Association (along with HOA, etc.). PRD needs update to show Association has multiple subtypes.
- Q: Should Association subtypes (Club, HOA) have their own role sets or share roles? → A: All Association subtypes share the same Role Templates (President, Member, Honorary).

## User Scenarios & Testing _(mandatory)_

### User Story 1 - System Administrator Seeds Role Data (Priority: P1)

As a platform administrator deploying Dartwing, I need predefined role templates for each organization type so that organizations can immediately assign roles to their members without manual setup.

**Why this priority**: Without seed data, no organization can assign roles to members. This blocks Org Member creation (Feature 3) and the entire permission system. This is the minimum viable foundation.

**Independent Test**: Can be fully tested by deploying the system and verifying all expected roles exist for each organization type. Delivers immediate value by enabling member role assignment.

**Acceptance Scenarios**:

1. **Given** a fresh Dartwing installation, **When** the system is initialized, **Then** all Family roles (Parent, Child, Guardian, Extended Family) are available
2. **Given** a fresh Dartwing installation, **When** the system is initialized, **Then** all Company roles (Owner, Manager, Employee, Contractor) are available
3. **Given** a fresh Dartwing installation, **When** the system is initialized, **Then** all Nonprofit roles (Board Member, Volunteer, Staff) are available
4. **Given** a fresh Dartwing installation, **When** the system is initialized, **Then** all Association roles (President, Member, Honorary) are available

---

### User Story 2 - Organization Admin Assigns Roles to Members (Priority: P1)

As an organization administrator, I want to select from roles appropriate to my organization type when adding a member, so that I can properly define their permissions and responsibilities.

**Why this priority**: This is the core use case for Role Templates - enabling contextual role assignment. Without role filtering by org type, administrators would see irrelevant options (e.g., "Parent" role in a Company).

**Independent Test**: Can be tested by creating an organization of each type and verifying only relevant roles appear in the role selection dropdown when adding a member.

**Acceptance Scenarios**:

1. **Given** a Family organization, **When** an admin adds a member, **Then** only Family roles (Parent, Child, Guardian, Extended Family) are available for selection
2. **Given** a Company organization, **When** an admin adds a member, **Then** only Company roles (Owner, Manager, Employee, Contractor) are available for selection
3. **Given** a Nonprofit organization, **When** an admin adds a member, **Then** only Nonprofit roles (Board Member, Volunteer, Staff) are available for selection
4. **Given** an Association organization, **When** an admin adds a member, **Then** only Association roles (President, Member, Honorary) are available for selection

---

### User Story 3 - System Enforces Supervisor Hierarchy (Priority: P2)

As a system, I need to distinguish between supervisor and non-supervisor roles so that I can enforce appropriate permissions hierarchies (e.g., Managers can view Employee timesheets, Parents can manage Child accounts).

**Why this priority**: While important for permission enforcement, this builds upon the basic role structure. The core role assignment works without supervisor flags initially.

**Independent Test**: Can be tested by checking supervisor flag values on each role and verifying supervisor-only capabilities are correctly restricted.

**Acceptance Scenarios**:

1. **Given** a Manager role in a Company, **When** checking the role definition, **Then** the supervisor flag is enabled
2. **Given** an Employee role in a Company, **When** checking the role definition, **Then** the supervisor flag is disabled
3. **Given** a Parent role in a Family, **When** checking the role definition, **Then** the supervisor flag is enabled
4. **Given** a Child role in a Family, **When** checking the role definition, **Then** the supervisor flag is disabled

---

### User Story 4 - Paid Organization Roles Include Hourly Rate (Priority: P3)

As an organization administrator, I want roles to optionally include a default hourly rate so that payroll calculations have sensible defaults when adding paid staff members.

**Why this priority**: This is a conditional enhancement for organizations with paid staff. The system works without hourly rates but this improves the user experience for employment-related workflows.

**Independent Test**: Can be tested by viewing roles for any non-Family org type and verifying hourly rate field is visible, while verifying it's hidden for Family org types (which represent unpaid family relationships).

**Acceptance Scenarios**:

1. **Given** a Company role (Employee or Contractor), **When** viewing the role definition, **Then** the default hourly rate field is visible and editable
2. **Given** a Nonprofit role (Staff), **When** viewing the role definition, **Then** the default hourly rate field is visible and editable (paid staff)
3. **Given** an Association role (any), **When** viewing the role definition, **Then** the default hourly rate field is visible and editable (associations may have paid staff)
4. **Given** a Family role (Parent or Child), **When** viewing the role definition, **Then** the default hourly rate field is hidden (family relationships are not employment)

---

### Edge Cases

- What happens when a role name is duplicated? System must reject duplicate role names with a clear error message.
- What happens if an organization changes type after members have roles assigned? **Out of scope for Feature 2.** This edge case will be handled by Feature 3 (Org Member DocType) which owns the relationship between organizations and member roles. Role Template only provides the reference data.
- What happens when a Role Template is deleted while Org Members reference it? System must prevent deletion of in-use roles.
- What if a user tries to create a role without specifying organization type? System must require org_type as mandatory.

## Requirements _(mandatory)_

### Functional Requirements

- **FR-001**: System MUST provide a Role Template DocType with fields: role_name (unique), applies_to_org_type, is_supervisor, and default_hourly_rate
- **FR-002**: System MUST enforce uniqueness on the role_name field to prevent duplicate role definitions
- **FR-003**: System MUST support four organization types for role filtering: Family, Company, Nonprofit, and Association
- **FR-004**: System MUST include a boolean is_supervisor flag on each role to indicate supervisory capabilities
- **FR-005**: System MUST conditionally display the default_hourly_rate field for all organization types except Family (which represents unpaid family relationships)
- **FR-006**: System MUST include seed data fixtures for all predefined roles across all organization types
- **FR-007**: System MUST filter role options in Org Member forms based on the parent organization's org_type
- **FR-008**: System MUST prevent deletion of Role Templates that are currently referenced by Org Member records
- **FR-009**: System MUST provide read access to Role Templates for all authenticated users (read-only reference data)
- **FR-010**: System MUST restrict Role Template creation/modification to System Managers only

### Seed Data Requirements

- **SD-001**: Family organization type MUST include roles: Parent (supervisor), Child (non-supervisor), Guardian (supervisor), Extended Family (non-supervisor)
- **SD-002**: Company organization type MUST include roles: Owner (supervisor), Manager (supervisor), Employee (non-supervisor), Contractor (non-supervisor)
- **SD-003**: Nonprofit organization type MUST include roles: Board Member (supervisor), Volunteer (non-supervisor), Staff (non-supervisor)
- **SD-004**: Association organization type MUST include roles: President (supervisor), Member (non-supervisor), Honorary (non-supervisor)

### Key Entities

- **Role Template**: A system-wide role definition that specifies: role_name (unique identifier), applies_to_org_type (which organization types can use this role), is_supervisor (whether this role has supervisory permissions), and default_hourly_rate (optional, for paid roles in Company, Nonprofit, and Association organizations)
- **Organization Type**: An enumeration of valid organization types (Family, Company, Nonprofit, Association) that determines which Role Templates are applicable. Note: Association is the parent type with subtypes including Club, HOA (Home Owners Association), and others. All Association subtypes share the same Role Templates.

## Success Criteria _(mandatory)_

### Measurable Outcomes

- **SC-001**: 100% of organization types (Family, Company, Nonprofit, Association) have at least 3 predefined roles after system initialization
- **SC-002**: Role filtering by org_type reduces irrelevant options by 75%+ (showing only 3-4 roles instead of all 14 total)
- **SC-003**: Administrators can assign a role to a new member in under 5 seconds (measured from dropdown open to selection confirmation)
- **SC-004**: System prevents 100% of attempts to delete in-use Role Templates
- **SC-005**: Conditional field visibility (hourly_rate) works correctly for 100% of role views: visible for all non-Family org types, hidden for Family
- **SC-006**: Role Template data loads and displays in under 500ms (server response time, excluding network latency)

## Assumptions

- Role Templates are system-wide and not customizable per organization (organizations select from predefined roles)
- The Organization DocType already exists with an org_type field containing the valid organization types
- The Org Member DocType (Feature 3) will consume Role Templates via a Link field
- Staff role in Nonprofit is non-supervisor (paid staff without board oversight responsibilities); hourly rate field is available for Staff since they are compensated employees
- "Association" is the canonical organization type; Club and HOA are subtypes of Association (PRD update required to reflect this hierarchy)
- Seed data will be installed during app installation or via fixtures
