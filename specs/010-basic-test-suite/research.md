# Research: Basic Test Suite

**Feature**: 010-basic-test-suite
**Date**: 2025-12-14

## Overview

This research documents the findings from analyzing the existing Dartwing test infrastructure and determining the best approach to complete test coverage for Features 1-9.

---

## Research Topic 1: Existing Test Infrastructure

### Decision
Use the existing Frappe test patterns (FrappeTestCase, TEST_PREFIX cleanup, doctype-level tests) without introducing new testing frameworks.

### Rationale
- The codebase already has 14+ test files with established patterns
- FrappeTestCase provides transaction rollback and Frappe context initialization
- TEST_PREFIX pattern (e.g., `_OrgHooksTest_`) provides reliable test isolation
- `bench run-tests` integrates with pytest for test discovery and execution
- No learning curve for developers already familiar with the codebase

### Alternatives Considered
1. **pytest-frappe standalone** - Would require additional setup and may conflict with `bench run-tests`
2. **unittest directly** - Lacks Frappe-specific fixtures and transaction handling
3. **New test framework** - Adds complexity without clear benefits

### Evidence
From `test_organization_hooks.py`:
```python
TEST_PREFIX = "_OrgHooksTest_"

def cleanup_test_organizations() -> None:
    """Shared utility for cleaning up test organizations."""
    pattern = f"{TEST_PREFIX}%"
    for org_name in frappe.get_all(...):
        frappe.delete_doc(...)
```

From `test_person.py`:
```python
class TestPerson(FrappeTestCase):
    def setUp(self):
        for person_name in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@test.example.com"]},
            pluck="name"
        ):
            frappe.delete_doc("Person", person_name, force=True)
```

---

## Research Topic 2: Test Organization Pattern

### Decision
Place DocType-specific tests in `dartwing_core/doctype/{doctype}/test_{doctype}.py` and cross-cutting tests in `dartwing/tests/`.

### Rationale
- Follows Frappe convention for automatic test discovery
- DocType tests are co-located with the code they test
- Integration and API tests that span multiple DocTypes belong in central `tests/` folder
- Consistent with existing project structure

### Alternatives Considered
1. **All tests in single folder** - Harder to find relevant tests, conflicts with Frappe convention
2. **Separate tests/ package at repo root** - Already exists but secondary to doctype-level tests

### File Mapping
| Test Type | Location | Example |
|-----------|----------|---------|
| DocType validation | `dartwing_core/doctype/{name}/test_{name}.py` | `test_person.py` |
| Hook tests | `dartwing/tests/test_*.py` | `test_organization_hooks.py` |
| Permission tests | `dartwing/tests/test_permission_*.py` | `test_permission_propagation.py` |
| API tests | `dartwing/tests/test_*_api.py` | `test_person_api.py` |
| Integration tests | `dartwing/tests/integration/` | `test_company_integration.py` |

---

## Research Topic 3: Test Coverage Gaps

### Decision
Create 4 new test files to achieve 80%+ coverage of Features 1-9.

### Current Coverage Analysis

| Feature | Files Covering | Coverage Level |
|---------|---------------|----------------|
| 1. Person DocType | `test_person.py` (50+ tests) | Comprehensive |
| 2. Role Template | `test_role_template.py` (basic) | Needs seed data tests |
| 3. Org Member | `test_org_member.py` | Needs role filtering |
| 4. Organization Hooks | `test_organization_hooks.py` (40+ tests) | Comprehensive |
| 5. Permission Propagation | `test_permission_propagation.py` (20+ tests) | Comprehensive |
| 6. Company DocType | `test_company.py`, `test_company_integration.py` | Adequate |
| 7. Equipment DocType | None found | Not yet implemented |
| 8. OrganizationMixin | None | Needs full implementation |
| 9. API Helpers | `test_person_api.py` (partial) | Needs org helpers |

### Gap Analysis Result
1. **test_role_template.py** - Need seed data verification for all 4 org types
2. **test_organization_mixin.py** - New file for mixin property tests
3. **test_api_helpers.py** - Tests for `get_user_organizations()`, `get_org_members()`
4. **test_org_member.py** - Add role filtering validation (extend existing)

---

## Research Topic 4: Frappe Test Execution Best Practices

### Decision
Use `bench run-tests` with module-specific targeting for development, full suite for CI.

### Rationale
- `bench run-tests` handles Frappe context initialization
- Module targeting (`--module`) speeds up development iteration
- Pattern matching (`-k`) enables running related tests
- Verbose mode (`-v`) aids debugging

### Commands Reference
```bash
# Development (single module)
bench --site dartwing.local run-tests --app dartwing --module dartwing.dartwing_core.doctype.role_template.test_role_template

# Development (pattern match)
bench --site dartwing.local run-tests --app dartwing -k "test_role" -v

# CI (full suite)
bench --site dartwing.local run-tests --app dartwing

# CI with JUnit output (for CI systems)
bench --site dartwing.local run-tests --app dartwing --junit-xml-output results.xml
```

---

## Research Topic 5: Test Data Cleanup Strategy

### Decision
Use TEST_PREFIX pattern with setUp/tearDown methods for automatic cleanup.

### Rationale
- Prevents test pollution across runs
- Pattern-based deletion is efficient and reliable
- Works with Frappe's transaction model
- Already proven in existing test files

### Implementation Pattern
```python
TEST_PREFIX = "_RoleTemplateTest_"

class TestRoleTemplate(FrappeTestCase):
    def setUp(self):
        self._cleanup_test_data()

    def tearDown(self):
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        for name in frappe.get_all(
            "Role Template",
            filters={"role_name": ["like", f"{TEST_PREFIX}%"]},
            pluck="name"
        ):
            frappe.delete_doc("Role Template", name, force=True)
```

---

## Research Topic 6: API Helper Testing Approach

### Decision
Test API helpers by calling them directly with mocked user context, verifying both data and permission enforcement.

### Rationale
- Direct function calls are faster than HTTP requests
- `frappe.set_user()` allows testing permission logic
- Existing `test_person_api.py` demonstrates this pattern
- Can verify both success and permission-denied scenarios

### Implementation Pattern
```python
def test_get_user_organizations_with_access(self):
    """Test user sees only organizations they have access to."""
    frappe.set_user("test_user@example.com")

    result = get_user_organizations()

    self.assertEqual(len(result), 1)
    self.assertEqual(result[0]["name"], self.org_with_access.name)

def test_get_org_members_permission_denied(self):
    """Test permission error when accessing unauthorized org."""
    frappe.set_user("other_user@example.com")

    with self.assertRaises(frappe.PermissionError):
        get_org_members(self.org_without_access.name)
```

---

## Summary of Decisions

| Topic | Decision |
|-------|----------|
| Test Framework | Use existing FrappeTestCase patterns |
| Test Organization | DocType-level + central tests/ folder |
| Coverage Gaps | 4 new test files needed |
| Execution | `bench run-tests` with targeting options |
| Cleanup | TEST_PREFIX pattern with setUp/tearDown |
| API Testing | Direct function calls with user context |

All NEEDS CLARIFICATION items from Technical Context have been resolved through this research.
