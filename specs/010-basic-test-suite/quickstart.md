# Quickstart: Basic Test Suite

**Feature**: 010-basic-test-suite
**Date**: 2025-12-14

## Prerequisites

1. Frappe bench environment configured
2. Dartwing app installed on a test site
3. MariaDB running with test database

## Running Tests

### Full Test Suite

```bash
# Run all Dartwing tests
bench --site dartwing.local run-tests --app dartwing
```

### Specific Test Module

```bash
# Person DocType tests
bench --site dartwing.local run-tests --app dartwing \
  --module dartwing.dartwing_core.doctype.person.test_person

# Organization hooks tests
bench --site dartwing.local run-tests --app dartwing \
  --module dartwing.tests.test_organization_hooks

# Permission propagation tests
bench --site dartwing.local run-tests --app dartwing \
  --module dartwing.tests.test_permission_propagation

# OrganizationMixin tests
bench --site dartwing.local run-tests --app dartwing \
  --module dartwing.dartwing_core.mixins.test_organization_mixin

# Integration workflow tests
bench --site dartwing.local run-tests --app dartwing \
  --module dartwing.tests.integration.test_full_workflow

# Role Template tests
bench --site dartwing.local run-tests --app dartwing \
  --module dartwing.dartwing_core.doctype.role_template.test_role_template

# Permission API tests
bench --site dartwing.local run-tests --app dartwing \
  --module dartwing.tests.test_permission_api
```

### Pattern Matching

```bash
# All role-related tests
bench --site dartwing.local run-tests --app dartwing -k "role"

# All permission tests
bench --site dartwing.local run-tests --app dartwing -k "permission"

# All API tests
bench --site dartwing.local run-tests --app dartwing -k "api"

# All integration tests
bench --site dartwing.local run-tests --app dartwing -k "workflow"

# All mixin tests
bench --site dartwing.local run-tests --app dartwing -k "mixin"
```

### Verbose Output

```bash
# Show individual test results
bench --site dartwing.local run-tests --app dartwing -v

# Show even more detail
bench --site dartwing.local run-tests --app dartwing -vv
```

## Test Development

### Creating a New Test File

1. Create file in appropriate location:
   - DocType tests: `dartwing_core/doctype/{name}/test_{name}.py`
   - Cross-cutting tests: `dartwing/tests/test_{feature}.py`

2. Use template:

```python
# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for {Feature Name}.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.{path}
"""

import frappe
from frappe.tests.utils import FrappeTestCase


TEST_PREFIX = "_{Feature}Test_"


class Test{Feature}(FrappeTestCase):
    """Test cases for {Feature}."""

    def setUp(self):
        """Set up test fixtures."""
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Helper to clean up test data."""
        # Pattern-based cleanup
        for name in frappe.get_all(
            "DocType",
            filters={"field": ["like", f"{TEST_PREFIX}%"]},
            pluck="name"
        ):
            frappe.delete_doc("DocType", name, force=True)

    def test_example_scenario(self):
        """Test description."""
        # Arrange
        doc = frappe.get_doc({
            "doctype": "DocType",
            "field": f"{TEST_PREFIX}Value"
        })
        doc.insert()

        # Act
        result = some_function(doc.name)

        # Assert
        self.assertEqual(result["expected"], "value")
```

### Testing with User Context

```python
def test_permission_denied_for_unauthorized_user(self):
    """Test that unauthorized users cannot access the resource."""
    original_user = frappe.session.user

    try:
        frappe.set_user("unauthorized@example.com")

        with self.assertRaises(frappe.PermissionError):
            some_protected_function()

    finally:
        frappe.set_user(original_user)
```

### Mocking External Dependencies

```python
from unittest.mock import patch, MagicMock

def test_with_mocked_dependency(self):
    """Test with mocked external service."""
    with patch("dartwing.module.external_function") as mock_fn:
        mock_fn.return_value = {"status": "success"}

        result = function_under_test()

        mock_fn.assert_called_once()
        self.assertEqual(result["status"], "success")
```

## CI Integration

### GitHub Actions Example

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Frappe
        # ... frappe setup steps ...

      - name: Run Tests
        run: |
          bench --site test_site run-tests --app dartwing

      - name: Upload Results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: test-results.xml
```

## Troubleshooting

### Tests Failing Due to Missing DocType

```
frappe.exceptions.DoesNotExistError: DocType 'Org Member' not found
```

**Solution**: Ensure the DocType is created and app is migrated:
```bash
bench --site dartwing.local migrate
```

### Permission Errors in Tests

```
frappe.exceptions.PermissionError: Not permitted to access
```

**Solution**: Set user to Administrator or System Manager in setUp:
```python
def setUp(self):
    frappe.set_user("Administrator")
```

### Test Data Pollution

Tests failing randomly due to leftover data.

**Solution**: Ensure TEST_PREFIX is unique and cleanup is complete:
```python
TEST_PREFIX = "_UniquePrefix_"  # Use unique prefix per test module

def _cleanup_test_data(self):
    # Clean up ALL test patterns
    for pattern in [f"{TEST_PREFIX}%", "%@test.example.com"]:
        for name in frappe.get_all("DocType", filters={"field": ["like", pattern]}, pluck="name"):
            frappe.delete_doc("DocType", name, force=True, ignore_permissions=True)
```

### Slow Tests

Full suite taking too long.

**Solution**:
1. Run specific modules during development
2. Use `-k` pattern matching
3. Optimize database operations in fixtures
