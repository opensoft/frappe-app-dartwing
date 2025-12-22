# Feature Specification: Basic Test Suite

**Feature Branch**: `010-basic-test-suite`
**Created**: 2025-12-14
**Status**: Draft
**Input**: User description: "Basic Test Suite - Comprehensive test coverage for all core Dartwing features including Person DocType, Role Template, Org Member, Organization hooks, User Permission propagation, Company DocType, Equipment DocType, OrganizationMixin, and API helpers"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Developer Validates Core Data Integrity (Priority: P1)

As a developer working on Dartwing, I need to verify that the core identity layer (Person DocType) correctly enforces data uniqueness and relationship constraints so that user data remains consistent and reliable across the system.

**Why this priority**: Person is the foundational identity layer - every other feature depends on it. Without validated Person functionality, Org Members cannot be created, permissions cannot be assigned, and no user flows can work correctly.

**Independent Test**: Can be fully tested by running the Person test module and verifying all assertions pass. Delivers confidence that the identity layer is working before building dependent features.

**Acceptance Scenarios**:

1. **Given** a new Person record with an email address, **When** another Person is created with the same email, **Then** the system rejects the duplicate and returns a validation error.
2. **Given** a Person record linked to an Org Member, **When** attempting to delete that Person, **Then** the system prevents deletion and displays an appropriate error message.
3. **Given** a Person record with a keycloak_user_id, **When** another Person is created with the same keycloak_user_id, **Then** the system rejects the duplicate.

---

### User Story 2 - Developer Validates Organization Lifecycle (Priority: P1)

As a developer, I need to verify that the Organization hybrid model correctly creates and manages bidirectional links between Organizations and their concrete types (Family, Company, etc.) so that data integrity is maintained throughout the organization lifecycle.

**Why this priority**: The hybrid Organization model is central to Dartwing's architecture. If bidirectional hooks fail, concrete types won't be created/deleted properly, breaking the entire multi-org paradigm.

**Independent Test**: Can be fully tested by creating Organizations of different types and verifying concrete types are automatically created and properly linked. Cascade delete can be tested independently.

**Acceptance Scenarios**:

1. **Given** a user creates a new Organization with org_type "Family", **When** the Organization is saved, **Then** a corresponding Family record is automatically created with a back-reference to the Organization.
2. **Given** an existing Organization with a linked Family record, **When** the Organization is deleted, **Then** the linked Family record is also deleted (cascade delete).
3. **Given** an existing Organization, **When** attempting to change the org_type after creation, **Then** the system prevents the change and displays an error.
4. **Given** an Organization with linked_doctype and linked_name populated, **When** calling the get_concrete_doc API helper, **Then** the correct concrete type document is returned.

---

### User Story 3 - Developer Validates Permission Propagation (Priority: P1)

As a developer, I need to verify that creating an Org Member correctly propagates User Permissions so that users can only access data belonging to their organizations.

**Why this priority**: Security is foundational - without correct permission propagation, users could see other organizations' data. This is a P1 security requirement that must work before any multi-tenant deployment.

**Independent Test**: Can be fully tested by creating an Org Member and verifying that User Permissions are created, then testing that list views are properly filtered.

**Acceptance Scenarios**:

1. **Given** a Person linked to a Frappe User, **When** an Org Member is created linking that Person to an Organization, **Then** a User Permission record is automatically created granting access to that Organization.
2. **Given** a user with User Permission for Organization A only, **When** that user views the Organization list, **Then** only Organization A is visible (not Organization B or others).
3. **Given** an Org Member record, **When** that Org Member is deleted, **Then** the corresponding User Permission is also removed.
4. **Given** a user who is a member of Organizations A and B, **When** viewing list views filtered by User Permission, **Then** both Organizations A and B are visible.

---

### User Story 4 - Developer Validates Role-Based Filtering (Priority: P2)

As a developer, I need to verify that Role Templates are correctly filtered by organization type so that users only see relevant roles when assigning members.

**Why this priority**: Role filtering ensures correct UX - families shouldn't see "Employee" roles and companies shouldn't see "Parent" roles. Important for usability but not blocking for core functionality.

**Independent Test**: Can be fully tested by creating Role Templates for different org types and verifying filtering in Org Member role selection.

**Acceptance Scenarios**:

1. **Given** Role Templates for "Family" (Parent, Child) and "Company" (Employee, Manager), **When** creating an Org Member for a Family-type Organization, **Then** only Family-applicable roles (Parent, Child) are shown in the role dropdown.
2. **Given** an Org Member record with a role, **When** the linked Organization's org_type differs from the role's applies_to_org_type, **Then** the system displays a validation error.

---

### User Story 5 - Developer Validates Org Member Uniqueness (Priority: P2)

As a developer, I need to verify that the same Person cannot be added to the same Organization multiple times with different roles, maintaining data consistency.

**Why this priority**: Prevents duplicate memberships which would cause confusion in permission calculations and UI displays. Important for data quality.

**Independent Test**: Can be fully tested by attempting to create duplicate Org Member records.

**Acceptance Scenarios**:

1. **Given** an existing Org Member linking Person A to Organization X, **When** attempting to create another Org Member with Person A and Organization X, **Then** the system rejects the duplicate with an appropriate error.
2. **Given** Person A is a member of Organization X, **When** creating an Org Member for Person A with Organization Y (different org), **Then** the creation succeeds (multi-org membership is allowed).

---

### User Story 6 - Developer Validates API Helpers (Priority: P2)

As a developer integrating with Flutter or external clients, I need to verify that whitelisted API methods return correct data with proper permission enforcement.

**Why this priority**: API helpers are required for mobile app integration. Without validated APIs, Flutter development is blocked.

**Independent Test**: Can be fully tested by calling each API method with test data and verifying response structure and permission enforcement.

**Acceptance Scenarios**:

1. **Given** an authenticated user with access to Organization A, **When** calling get_user_organizations(), **Then** the response includes Organization A with all expected fields.
2. **Given** an authenticated user without access to Organization B, **When** calling get_organization_with_details(organization=B), **Then** the request is denied with a permission error.
3. **Given** an Organization with members, **When** calling get_org_members(organization=A), **Then** all active members are returned with person and role details.

---

### User Story 7 - Developer Validates OrganizationMixin Functionality (Priority: P3)

As a developer, I need to verify that the OrganizationMixin provides correct access to parent Organization properties from concrete type controllers.

**Why this priority**: Code quality and consistency across concrete types. Not blocking for MVP but reduces code duplication.

**Independent Test**: Can be fully tested by calling mixin properties on Family and Company instances.

**Acceptance Scenarios**:

1. **Given** a Family record linked to an Organization with org_name "Smith Family", **When** accessing family.org_name via the mixin, **Then** "Smith Family" is returned.
2. **Given** a Company record linked to an Organization, **When** calling update_org_name("New Name"), **Then** the parent Organization's org_name is updated to "New Name".
3. **Given** a concrete type record, **When** calling get_organization_doc(), **Then** the full parent Organization document is returned.

---

### Edge Cases

- What happens when a Person is deleted while having pending (not yet active) Org Members?
- How does the system handle creating an Organization when the concrete type doctype doesn't exist (module not installed)?
- What happens when User Permissions are manually deleted but Org Member still exists?
- How does the system behave when a Role Template is deleted while Org Members reference it?
- What happens when the same test runs multiple times without cleanup (test isolation)?
- How does the system handle concurrent creation of Org Members for the same Person/Organization pair?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Test suite MUST include tests for Person DocType validating email uniqueness, keycloak_user_id uniqueness, and deletion prevention when linked.
- **FR-002**: Test suite MUST include tests for Organization hooks validating automatic concrete type creation, bidirectional linking, and cascade delete.
- **FR-003**: Test suite MUST include tests for Org Member validating person+organization uniqueness constraint and role filtering by org_type.
- **FR-004**: Test suite MUST include tests for User Permission propagation verifying automatic creation on Org Member insert and removal on delete.
- **FR-005**: Test suite MUST include permission tests verifying list view filtering and single document access control.
- **FR-006**: Test suite MUST include API helper tests for get_concrete_doc, get_organization_with_details, get_user_organizations, and get_org_members methods.
- **FR-007**: Test suite MUST include OrganizationMixin tests validating property accessors (org_name, logo, org_status) and methods (get_organization_doc, update_org_name).
- **FR-008**: All tests MUST properly set up and tear down test data to ensure test isolation and repeatability.
- **FR-009**: Test suite MUST be runnable from the command line using standard test runners.
- **FR-010**: Test suite MUST provide clear failure messages indicating which specific assertion failed and why.
- **FR-011**: Test suite MUST include negative test cases (e.g., verifying errors are raised for invalid inputs).
- **FR-012**: Test suite MUST test Role Template seed data existence for all organization types (Family, Company, Nonprofit, Association).

### Key Entities

- **Test Case**: A single testable scenario with setup, execution, and assertion phases. Contains name, description, and expected outcome.
- **Test Module**: A collection of related test cases grouped by feature area (e.g., test_person.py, test_organization.py).
- **Test Fixture**: Reusable test data setup that can be shared across multiple test cases.
- **Test Result**: Outcome of a test run including pass/fail status, execution time, and error details if failed.

## Assumptions

- Frappe's pytest integration is available and configured in the development environment.
- All prerequisite DocTypes (Person, Organization, Family, Company, Org Member, Role Template) are already implemented before this test suite is created.
- Test database can be created/destroyed without affecting production data.
- Role Template seed data fixtures are installed before running tests.
- User Permission system from Frappe framework is functioning correctly.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All implemented tests pass on a clean test environment with 100% success rate.
- **SC-002**: Test suite covers at least 80% of the core flows defined in Features 1-9 of the priority document.
- **SC-003**: Each test module can run independently without requiring other test modules to pass first.
- **SC-004**: Test execution completes within 5 minutes for the entire suite.
- **SC-005**: Zero test flakiness - tests produce consistent results across 10 consecutive runs.
- **SC-006**: Regression detection - modifying core DocType behavior causes related tests to fail.
- **SC-007**: Test failures provide sufficient information to identify the root cause without additional debugging in 90% of cases.
