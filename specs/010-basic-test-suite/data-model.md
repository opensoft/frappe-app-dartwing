# Data Model: Basic Test Suite

**Feature**: 010-basic-test-suite
**Date**: 2025-12-14

## Overview

This document defines the test entities and their relationships for the Basic Test Suite feature. Since this is a test feature, the "data model" represents test infrastructure rather than business entities.

---

## Test Entities

### Test Case

A single executable test scenario.

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Test function name (e.g., `test_duplicate_email_rejected`) |
| module | string | Python module path (e.g., `dartwing.tests.test_api_helpers`) |
| class_name | string | Test class containing the test (e.g., `TestApiHelpers`) |
| docstring | string | Description of what the test validates |
| priority | enum | P1 (critical), P2 (important), P3 (nice-to-have) |
| feature_ref | string | FR-XXX requirement being validated |

### Test Module

A collection of related test cases in a single Python file.

| Attribute | Type | Description |
|-----------|------|-------------|
| file_path | string | Path relative to app root (e.g., `tests/test_api_helpers.py`) |
| test_class | string | Primary FrappeTestCase subclass name |
| test_prefix | string | Unique prefix for test data isolation |
| dependencies | list[string] | DocTypes required for tests to run |
| test_count | int | Number of test_ methods in the module |

### Test Fixture

Reusable test data setup.

| Attribute | Type | Description |
|-----------|------|-------------|
| name | string | Fixture identifier (e.g., `test_person_with_user`) |
| doctype | string | Frappe DocType being created |
| fields | dict | Field values for the fixture document |
| cleanup_pattern | string | Pattern for identifying fixture data (e.g., `%@test.example.com`) |

### Test Result

Outcome of a test run.

| Attribute | Type | Description |
|-----------|------|-------------|
| test_name | string | Full test path (module.class.method) |
| status | enum | passed, failed, skipped, error |
| duration_ms | int | Execution time in milliseconds |
| error_message | string | Failure reason (if status != passed) |
| traceback | string | Stack trace for debugging |

---

## Test Module Inventory

### Existing Modules (No Changes Required)

| Module | Test Class | Prefix | Features Covered |
|--------|-----------|--------|------------------|
| `dartwing_core/doctype/person/test_person.py` | TestPerson | `%@test.example.com` | FR-001 |
| `tests/test_organization_hooks.py` | TestOrganizationBidirectionalHooks | `_OrgHooksTest_` | FR-002 |
| `tests/test_permission_propagation.py` | TestPermissionPropagation | `%@perm-test.example.com` | FR-004 |
| `tests/test_permission_helpers.py` | TestPermissionHelpers | N/A | FR-005 |

### New Modules (To Be Created)

| Module | Test Class | Prefix | Features Covered |
|--------|-----------|--------|------------------|
| `dartwing_core/doctype/role_template/test_role_template.py` | TestRoleTemplate | `_RoleTemplateTest_` | FR-003, FR-012 |
| `tests/test_api_helpers.py` | TestApiHelpers | `_ApiTest_` | FR-006 |
| `mixins/test_organization_mixin.py` | TestOrganizationMixin | `_MixinTest_` | FR-007 |
| `tests/integration/test_full_workflow.py` | TestFullWorkflow | `_WorkflowTest_` | FR-001 to FR-007 |

---

## Test Data Fixtures

### Standard Test User

```python
TEST_USER = {
    "doctype": "User",
    "email": "test_user@example.com",
    "first_name": "Test",
    "last_name": "User",
    "enabled": 1,
    "user_type": "System User",
    "roles": [{"role": "System Manager"}]
}
```

### Standard Test Person

```python
TEST_PERSON = {
    "doctype": "Person",
    "primary_email": "{prefix}@test.example.com",
    "first_name": "Test",
    "last_name": "Person",
    "source": "manual",
    "frappe_user": "test_user@example.com"  # Optional
}
```

### Standard Test Organization

```python
TEST_ORGANIZATION = {
    "doctype": "Organization",
    "org_name": "{prefix} Test Org",
    "org_type": "Family"  # or Company, Nonprofit, Association
}
```

### Role Template Seed Data

```python
ROLE_TEMPLATES = {
    "Family": ["Parent", "Child", "Guardian", "Extended Family"],
    "Company": ["Owner", "Manager", "Employee", "Contractor"],
    "Nonprofit": ["Board Member", "Volunteer", "Staff"],
    "Association": ["President", "Member", "Honorary"]
}
```

---

## Entity Relationships

```
┌─────────────┐       ┌──────────────┐
│ Test Module │──1:N──│  Test Case   │
└─────────────┘       └──────────────┘
       │                     │
       │                     │
       ▼                     ▼
┌─────────────┐       ┌──────────────┐
│Test Fixture │       │ Test Result  │
└─────────────┘       └──────────────┘
```

- A Test Module contains multiple Test Cases
- Test Cases use Test Fixtures for setup
- Test Cases produce Test Results when executed
- Test Modules define cleanup patterns for fixture isolation

---

## Validation Rules

1. **Test Isolation**: Each test module MUST have a unique TEST_PREFIX
2. **Cleanup**: setUp and tearDown MUST clean up all test data using TEST_PREFIX
3. **Independence**: Tests MUST NOT depend on execution order
4. **Idempotency**: Tests MUST be runnable multiple times with same results
5. **Error Handling**: Tests MUST restore Frappe user context in finally blocks
