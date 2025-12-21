# Quickstart: OrganizationMixin Base Class

**Feature**: 008-organization-mixin
**Date**: 2025-12-14

## What This Feature Does

The OrganizationMixin provides a consistent API for concrete organization types (Family, Company, etc.) to access their parent Organization's data without writing repetitive code.

## Using the Mixin

### Inheriting from OrganizationMixin

```python
# In your concrete type controller (e.g., family.py)
from frappe.model.document import Document
from dartwing.dartwing_core.mixins import OrganizationMixin


class Family(Document, OrganizationMixin):
    """Family document with Organization access via mixin."""

    def validate(self):
        # Your existing validation logic...
        pass
```

### Accessing Organization Properties

```python
# Once your concrete type inherits from OrganizationMixin:
family = frappe.get_doc("Family", "FAM-00001")

# Read organization name
print(family.org_name)  # "Smith Family"

# Read organization logo
print(family.logo)  # "/files/smith-logo.png" or None

# Read organization status
print(family.org_status)  # "Active"

# Get the full Organization document
org_doc = family.get_organization_doc()
print(org_doc.name)  # "ORG-2025-00001"
```

### Updating Organization Name

```python
# Update the organization's display name
family.update_org_name("Johnson Family")

# Verify the change
print(family.org_name)  # "Johnson Family"
```

## Edge Case Handling

### Missing Organization Link

```python
# If the concrete type has no linked Organization:
orphan = frappe.get_doc("Family", "FAM-ORPHAN")
print(orphan.organization)  # None

# Properties return None silently
print(orphan.org_name)  # None
print(orphan.logo)  # None
print(orphan.org_status)  # None

# get_organization_doc() returns None
print(orphan.get_organization_doc())  # None

# update_org_name() raises an error
orphan.update_org_name("Test")  # Raises: "Cannot update organization name: No organization linked"
```

### Empty Name Validation

```python
# Attempting to set empty name raises error
family.update_org_name("")  # Raises: "Organization name cannot be empty"
family.update_org_name("   ")  # Raises: "Organization name cannot be empty"
```

### Permission Handling

```python
# If user lacks write permission on Organization:
# The standard Frappe PermissionError is raised
family.update_org_name("New Name")  # Raises: PermissionError (if no write access)
```

## Testing Your Implementation

### Unit Test Pattern

```python
import frappe
from frappe.tests.utils import FrappeTestCase


class TestOrganizationMixin(FrappeTestCase):
    def setUp(self):
        # Create test Organization and Family
        self.org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Family",
            "org_type": "Family",
            "status": "Active"
        }).insert()

    def test_org_name_property(self):
        family = frappe.get_doc("Family", {"organization": self.org.name})
        self.assertEqual(family.org_name, "Test Family")

    def test_update_org_name(self):
        family = frappe.get_doc("Family", {"organization": self.org.name})
        family.update_org_name("New Name")

        # Refresh and verify
        self.org.reload()
        self.assertEqual(self.org.org_name, "New Name")
        self.assertEqual(family.org_name, "New Name")
```

## Common Mistakes

### Wrong Inheritance Order

```python
# WRONG - Document must come first
class Family(OrganizationMixin, Document):
    pass

# CORRECT
class Family(Document, OrganizationMixin):
    pass
```

### Forgetting to Clear Cache After External Updates

```python
# If you update Organization directly (not via mixin):
frappe.db.set_value("Organization", family.organization, "org_name", "Direct Update")

# The mixin cache may be stale
print(family.org_name)  # Might still show old value

# Clear cache manually if needed
family._clear_organization_cache()
print(family.org_name)  # Now shows "Direct Update"
```

## Files Modified

| File | Change |
|------|--------|
| `dartwing/dartwing_core/mixins/organization_mixin.py` | Add `update_org_name()` method |
| `dartwing/dartwing_core/doctype/family/family.py` | Inherit from OrganizationMixin |
