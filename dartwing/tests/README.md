# Dartwing Test Suite

## Test Organization

Tests are organized by domain for better maintainability, rather than consolidated into a single monolithic file.

### API Tests (P2-002 Note)

API helper tests are **distributed by domain** rather than in one `test_api_helpers.py` file:

- **`test_permission_api.py`** - Permission-related APIs
  - `get_user_organizations()` - Get organizations accessible to current user
  - Permission filtering and User Permission propagation

- **`test_organization_hooks.py`** - Organization lifecycle APIs
  - `get_organization_with_details()` - Fetch organization with linked concrete type
  - Organization creation and bidirectional linking hooks

- **Future**: Additional API tests will be added to domain-specific files as features are implemented

### Test File Structure

```
dartwing/tests/
├── __init__.py
├── README.md (this file)
├── fixtures.py                    # Shared test fixtures (P2-001)
├── test_permission_api.py          # Permission & User Permission APIs
├── integration/
│   ├── __init__.py
│   └── test_full_workflow.py      # End-to-end integration tests
└── [future domain-specific tests]

dartwing/dartwing_core/
├── doctype/
│   ├── person/
│   │   └── test_person.py         # Person DocType tests
│   ├── organization/
│   │   └── test_organization.py   # Organization DocType tests
│   ├── role_template/
│   │   └── test_role_template.py  # Role Template DocType tests
│   └── [other doctypes...]
└── mixins/
    └── [mixin tests if/when implemented]
```

## Running Tests

### Full Suite
```bash
bench --site <site> run-tests --app dartwing
```

### Specific Module
```bash
bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_api
```

### Integration Tests Only
```bash
bench --site <site> run-tests --app dartwing --module dartwing.tests.integration
```

### Specific DocType
```bash
bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.person.test_person
```

## Test Requirements

- **SC-004**: Full test suite must complete in < 5 minutes
- **SC-005**: Zero test flakiness (all tests must be deterministic)
- **Test Isolation**: Each test must clean up all data created
- **Prefix Pattern**: All test data must use consistent prefix (e.g., `_Test_`, `TEST_PREFIX`)

## Shared Fixtures

Use `DartwingTestFixtures` class from `dartwing.tests.fixtures` for:
- Consistent test data creation
- Automatic cleanup tracking
- DRY principle adherence

Example:
```python
from dartwing.tests.fixtures import DartwingTestFixtures

class TestMyFeature(FrappeTestCase):
    def setUp(self):
        self.fixtures = DartwingTestFixtures(prefix="_MyTest_")

    def tearDown(self):
        self.fixtures.cleanup_all()

    def test_something(self):
        user = self.fixtures.create_test_user("user1")
        person = self.fixtures.create_test_person("person1", frappe_user=user)
        org, concrete = self.fixtures.create_test_organization("org1", "Family")
```
