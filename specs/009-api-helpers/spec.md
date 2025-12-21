# Feature Specification: API Helpers (Whitelisted Methods)

**Feature Branch**: `009-api-helpers`
**Created**: 2025-12-14
**Status**: Draft
**Input**: User description: "API Helpers (Whitelisted Methods) for Flutter integration - Standardized REST API endpoints enabling the Flutter client to retrieve organization data, member information, and concrete type details"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Retrieve User's Organizations (Priority: P1)

A mobile app user opens the Flutter application and needs to see a list of all organizations they belong to. The system must provide a single API call that returns all organizations the authenticated user has access to, enabling the app to display an organization selector or dashboard.

**Why this priority**: This is the foundation for all organization-scoped operations in the mobile app. Without this, users cannot navigate to or interact with any organization.

**Independent Test**: Can be fully tested by authenticating a user with multiple organization memberships and verifying the API returns exactly those organizations, delivering immediate value for the app's home screen.

**Acceptance Scenarios**:

1. **Given** a user is authenticated and belongs to 3 organizations (2 active, 1 inactive), **When** they call the get_user_organizations endpoint, **Then** they receive a list containing all 3 organizations with their basic details (name, type, status, logo).
2. **Given** a user is authenticated but belongs to no organizations, **When** they call the get_user_organizations endpoint, **Then** they receive an empty list (not an error).
3. **Given** an unauthenticated request is made, **When** the get_user_organizations endpoint is called, **Then** the system returns an authentication error.

---

### User Story 2 - View Organization with Concrete Type Details (Priority: P1)

A user selects an organization from their list and the app needs to display the organization's full details, including type-specific information (e.g., tax_id for a Company, parental_controls for a Family). The system must provide a single API call that returns both the base Organization data and its associated concrete type data.

**Why this priority**: Essential for displaying organization details screens. The hybrid Organization model requires fetching both the base record and concrete type, which should be done in a single call for mobile performance.

**Independent Test**: Can be tested by fetching a Company organization and verifying both Organization fields (name, logo) and Company-specific fields (tax_id, entity_type) are returned together.

**Acceptance Scenarios**:

1. **Given** an Organization of type "Company" exists with tax_id "12-3456789", **When** the user calls get_organization_with_details for that organization, **Then** they receive both the Organization data (org_name, logo, status) and nested Company data (tax_id, entity_type, officers).
2. **Given** an Organization of type "Family" exists, **When** the user calls get_organization_with_details, **Then** they receive the Organization data with nested Family data (family_nickname, parental_controls_enabled).
3. **Given** a user does NOT have permission to view an organization, **When** they call get_organization_with_details for it, **Then** they receive a permission denied error.

---

### User Story 3 - Retrieve Concrete Type Document Directly (Priority: P2)

A developer building a specific feature (e.g., a Company management screen) needs to retrieve just the concrete type document (Company, Family, etc.) given an Organization ID, without the extra wrapper data. This enables efficient partial updates and focused data retrieval.

**Why this priority**: Supports advanced use cases where only type-specific data is needed, such as editing Company tax information without loading full organization details.

**Independent Test**: Can be tested by calling get_concrete_doc with an Organization ID and verifying only the concrete type fields are returned.

**Acceptance Scenarios**:

1. **Given** an Organization "ORG-2025-00001" of type "Family", **When** the user calls get_concrete_doc with that organization ID, **Then** they receive only the Family document fields (family_nickname, primary_residence, parental_controls_enabled).
2. **Given** an Organization exists but has no linked concrete type (error state), **When** get_concrete_doc is called, **Then** the system returns null or an appropriate error response.
3. **Given** a user has view-only permission for the organization, **When** they call get_concrete_doc, **Then** they successfully receive the document (read access is sufficient).

---

### User Story 4 - List Organization Members (Priority: P2)

An organization administrator opens the members management screen and needs to see all people who belong to their organization, along with their roles and membership status. The system must provide an API to retrieve all Org Members for a given organization.

**Why this priority**: Member management is a core feature for all organization types, but it depends on basic organization retrieval being functional first.

**Independent Test**: Can be tested by creating an Organization with 5 members and verifying the API returns all 5 with correct role and status information.

**Acceptance Scenarios**:

1. **Given** an Organization has 3 active members and 1 inactive member, **When** the user calls get_org_members with default parameters, **Then** they receive all 4 members with their person details, role, and status.
2. **Given** an Organization has 100 members, **When** the user calls get_org_members with pagination (limit: 20, offset: 0), **Then** they receive only the first 20 members plus total count information.
3. **Given** a user is not a member of an organization, **When** they try to call get_org_members for it, **Then** they receive a permission denied error.
4. **Given** an Organization has members, **When** the user calls get_org_members with status filter "Active", **Then** they receive only active members.

---

### Edge Cases

- What happens when an organization's concrete type record is missing (data integrity issue)? The system should return the Organization data with a null concrete_type field and log a warning for administrators.
- How does the system handle requests for organizations that don't exist? Return a standard "not found" error with appropriate HTTP status.
- What happens when a user's session expires mid-request? Return authentication error, prompting the mobile app to refresh tokens.
- How are large member lists handled? Pagination is required, with configurable page size and total count in response.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide an API method `get_user_organizations()` that returns all organizations the authenticated user is a member of.
- **FR-002**: System MUST provide an API method `get_organization_with_details(organization: str)` that returns an Organization document merged with its concrete type data.
- **FR-003**: System MUST provide an API method `get_concrete_doc(organization: str)` that returns only the concrete type document for a given Organization.
- **FR-004**: System MUST provide an API method `get_org_members(organization: str)` that returns all Org Member records for a given organization.
- **FR-005**: System MUST enforce permission checks on all API methods, ensuring users can only access data for organizations they belong to.
- **FR-006**: System MUST support pagination for `get_org_members()` via limit and offset parameters.
- **FR-007**: System MUST support filtering `get_org_members()` by member status (Active/Inactive/Pending).
- **FR-008**: System MUST return consistent response formats across all API methods for predictable client-side handling.
- **FR-009**: System MUST log all API calls for audit purposes at INFO level, including user, organization, and timestamp (using frappe.logger pattern).
- **FR-010**: System MUST return appropriate error responses (not found, permission denied, validation error) with consistent error structure.

### Key Entities *(include if feature involves data)*

- **Organization**: The polymorphic identity record that all users interact with; contains org_name, org_type, logo, status, and links to concrete type.
- **Concrete Types (Family, Company, Association, Nonprofit)**: Type-specific records containing domain-specific fields (tax_id for Company, parental_controls for Family, etc.).
- **Org Member**: Junction record linking a Person to an Organization with a role and status.
- **Person**: The identity record representing a human user in the system.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can retrieve their organization list in under 1 second for up to 50 organizations.
- **SC-002**: Users can retrieve full organization details (with concrete type) in a single request, reducing mobile app load times by eliminating multiple sequential API calls.
- **SC-003**: System handles concurrent requests from 1,000 users requesting organization data without degradation.
- **SC-004**: 100% of API calls correctly enforce permissions, with no unauthorized data access.
- **SC-005**: All API methods return responses in under 500ms for standard operations (non-bulk).
- **SC-006**: API response format is consistent, enabling the Flutter team to implement a single response parser.
- **SC-007**: Zero unhandled errors in production - all error conditions return appropriate error responses rather than system exceptions.
