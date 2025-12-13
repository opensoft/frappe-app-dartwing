# Quickstart: User Permission Propagation

**Feature**: 005-user-permission-propagation
**Date**: 2025-12-13

## Prerequisites

Before implementing this feature, ensure these are in place:

1. **Feature 1: Person DocType** - Person records with `frappe_user` Link field
2. **Feature 3: Org Member DocType** - Org Member records linking Person to Organization
3. **Organization DocType** - Existing, with `linked_doctype` and `linked_name` fields

## Quick Setup

### 1. Create Permission Module Structure

```bash
# From dartwing app root
mkdir -p dartwing/permissions
touch dartwing/permissions/__init__.py
touch dartwing/permissions/organization.py
touch dartwing/permissions/family.py
touch dartwing/permissions/company.py
touch dartwing/permissions/association.py
touch dartwing/permissions/nonprofit.py
touch dartwing/permissions/helpers.py

# Utility for logging
mkdir -p dartwing/utils
touch dartwing/utils/permission_logger.py
```

### 2. Register Hooks

Add to `dartwing/hooks.py`:

```python
# Permission Query Conditions - filters list views
permission_query_conditions = {
    "Organization": "dartwing.permissions.organization.get_permission_query_conditions",
    "Family": "dartwing.permissions.family.get_permission_query_conditions",
    "Company": "dartwing.permissions.company.get_permission_query_conditions",
    "Association": "dartwing.permissions.association.get_permission_query_conditions",
    "Nonprofit": "dartwing.permissions.nonprofit.get_permission_query_conditions",
}

# Has Permission - single document access
has_permission = {
    "Organization": "dartwing.permissions.organization.has_permission",
    "Family": "dartwing.permissions.family.has_permission",
    "Company": "dartwing.permissions.company.has_permission",
    "Association": "dartwing.permissions.association.has_permission",
    "Nonprofit": "dartwing.permissions.nonprofit.has_permission",
}

# Doc Events - trigger permission propagation
doc_events = {
    "Org Member": {
        "after_insert": "dartwing.permissions.helpers.create_user_permissions",
        "on_trash": "dartwing.permissions.helpers.remove_user_permissions",
        "on_update": "dartwing.permissions.helpers.handle_status_change",
    }
}
```

### 3. Implement Core Helper Functions

Create `dartwing/permissions/helpers.py`:

```python
import frappe
from frappe import _
from dartwing.utils.permission_logger import log_permission_event

def create_user_permissions(doc, method):
    """Create User Permissions when Org Member is created."""
    user = frappe.db.get_value("Person", doc.person, "frappe_user")

    if not user:
        log_permission_event("skip", doc, reason="Person has no linked Frappe User")
        return

    org = frappe.get_doc("Organization", doc.organization)

    # Permission for Organization
    _create_permission(user, "Organization", doc.organization)
    log_permission_event("create", doc, user=user, doctype="Organization")

    # Permission for concrete type
    if org.linked_doctype and org.linked_name:
        _create_permission(user, org.linked_doctype, org.linked_name)
        log_permission_event("create", doc, user=user, doctype=org.linked_doctype)

def remove_user_permissions(doc, method):
    """Remove User Permissions when Org Member is deleted."""
    user = frappe.db.get_value("Person", doc.person, "frappe_user")
    if not user:
        return

    org = frappe.get_doc("Organization", doc.organization)

    _delete_permission(user, "Organization", doc.organization)
    log_permission_event("remove", doc, user=user, doctype="Organization")

    if org.linked_doctype and org.linked_name:
        _delete_permission(user, org.linked_doctype, org.linked_name)
        log_permission_event("remove", doc, user=user, doctype=org.linked_doctype)

def handle_status_change(doc, method):
    """Handle Org Member status changes."""
    if doc.has_value_changed("status"):
        old_status = doc.get_doc_before_save().status if doc.get_doc_before_save() else None
        if doc.status == "Inactive" and old_status == "Active":
            remove_user_permissions(doc, method)
        elif doc.status == "Active" and old_status == "Inactive":
            create_user_permissions(doc, method)

def _create_permission(user, allow, for_value):
    if not frappe.db.exists("User Permission", {
        "user": user, "allow": allow, "for_value": for_value
    }):
        frappe.get_doc({
            "doctype": "User Permission",
            "user": user,
            "allow": allow,
            "for_value": for_value,
            "apply_to_all_doctypes": 0
        }).insert(ignore_permissions=True)

def _delete_permission(user, allow, for_value):
    frappe.db.delete("User Permission", {
        "user": user, "allow": allow, "for_value": for_value
    })
```

### 4. Implement Organization Permission Functions

Create `dartwing/permissions/organization.py`:

```python
import frappe

def get_permission_query_conditions(user):
    """SQL WHERE clause for Organization list queries."""
    if "System Manager" in frappe.get_roles(user):
        return ""

    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value"
    )

    if not orgs:
        return "1=0"

    org_list = ", ".join(f"'{o}'" for o in orgs)
    return f"`tabOrganization`.`name` IN ({org_list})"

def has_permission(doc, ptype, user):
    """Single document permission check."""
    if "System Manager" in frappe.get_roles(user):
        return True

    return frappe.db.exists(
        "User Permission",
        {"user": user, "allow": "Organization", "for_value": doc.name}
    )
```

### 5. Implement Concrete Type Permission Functions

For each concrete type (Family, Company, etc.), create similar files. Example `dartwing/permissions/family.py`:

```python
import frappe

def get_permission_query_conditions(user):
    """SQL WHERE clause for Family list queries."""
    if "System Manager" in frappe.get_roles(user):
        return ""

    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value"
    )

    if not orgs:
        return "1=0"

    org_list = ", ".join(f"'{o}'" for o in orgs)
    return f"`tabFamily`.`organization` IN ({org_list})"

def has_permission(doc, ptype, user):
    """Single document permission check."""
    if "System Manager" in frappe.get_roles(user):
        return True

    return frappe.db.exists(
        "User Permission",
        {"user": user, "allow": "Organization", "for_value": doc.organization}
    )
```

## Testing

### Manual Test Steps

1. **Create test data**:
   ```python
   # In bench console
   import frappe

   # Create Organization
   org = frappe.get_doc({
       "doctype": "Organization",
       "org_name": "Test Corp",
       "org_type": "Company"
   }).insert()

   # Create Person with User
   person = frappe.get_doc({
       "doctype": "Person",
       "first_name": "Test",
       "last_name": "User",
       "primary_email": "test@example.com",
       "frappe_user": "test@example.com"
   }).insert()

   # Create Org Member (should trigger permissions)
   member = frappe.get_doc({
       "doctype": "Org Member",
       "person": person.name,
       "organization": org.name,
       "role": "Employee",
       "status": "Active"
   }).insert()
   ```

2. **Verify permissions created**:
   ```python
   frappe.get_all("User Permission", filters={
       "user": "test@example.com",
       "allow": "Organization"
   })
   ```

3. **Test list filtering**:
   ```python
   frappe.set_user("test@example.com")
   orgs = frappe.get_list("Organization")  # Should only see Test Corp
   ```

4. **Test permission removal**:
   ```python
   frappe.set_user("Administrator")
   frappe.delete_doc("Org Member", member.name)
   # Verify permissions removed
   ```

### Automated Tests

Run tests with:
```bash
bench --site [site] run-tests --module dartwing.tests.test_permission_propagation
```

## Troubleshooting

### Permissions not being created

1. Check if Person has `frappe_user` set
2. Check permission audit log for "skip" events
3. Verify hooks.py is registered correctly: `bench --site [site] clear-cache`

### List views showing all records

1. Verify `permission_query_conditions` is registered in hooks.py
2. Clear cache: `bench --site [site] clear-cache`
3. Check user has User Permissions: `frappe.get_all("User Permission", filters={"user": [user]})`

### Permission denied errors

1. Check if User Permission exists for the record
2. Verify `has_permission` function is registered
3. Check if user has System Manager role (should bypass)

## API Usage (Flutter)

```dart
// Get user's organizations
final response = await frappe.call(
  method: 'dartwing.permissions.get_user_organizations',
);
List<Organization> orgs = response.message;

// Check organization access
final accessCheck = await frappe.call(
  method: 'dartwing.permissions.check_organization_access',
  args: {'organization': 'ORG-2025-00001'},
);
bool hasAccess = accessCheck.message['has_access'];
```
