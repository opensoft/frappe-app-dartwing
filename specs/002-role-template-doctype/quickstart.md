# Quickstart: Role Template DocType

**Feature**: 002-role-template-doctype
**Date**: 2025-12-03

## Prerequisites

- Frappe Bench installed with Dartwing app
- Site created and app installed
- System Manager permissions for development

## Development Setup

### 1. Switch to Feature Branch

```bash
cd apps/dartwing
git checkout 002-role-template-doctype
```

### 2. Create DocType Directory

```bash
mkdir -p dartwing/dartwing_core/doctype/role_template
touch dartwing/dartwing_core/doctype/role_template/__init__.py
```

### 3. Create DocType JSON

Copy the DocType definition from `data-model.md` to:
```
dartwing/dartwing_core/doctype/role_template/role_template.json
```

### 4. Create Controller

Create `dartwing/dartwing_core/doctype/role_template/role_template.py`:

```python
import frappe
from frappe.model.document import Document


class RoleTemplate(Document):
    def validate(self):
        self.validate_hourly_rate()

    def validate_hourly_rate(self):
        """Clear hourly rate for Family roles (non-employment relationships)."""
        if self.applies_to_org_type == "Family":
            self.default_hourly_rate = 0

    def on_trash(self):
        """Prevent deletion if role is in use."""
        self.check_linked_org_members()

    def check_linked_org_members(self):
        """Check if any Org Members reference this role."""
        if not frappe.db.exists("DocType", "Org Member"):
            return  # Org Member not implemented yet

        linked_count = frappe.db.count("Org Member", {"role": self.name})
        if linked_count > 0:
            frappe.throw(
                f"Cannot delete Role Template '{self.role_name}': "
                f"{linked_count} Org Member(s) are using this role.",
                frappe.LinkExistsError
            )
```

### 5. Create Fixtures

Create `dartwing/fixtures/role_template.json`:

```json
[
  {"doctype": "Role Template", "role_name": "Parent", "applies_to_org_type": "Family", "is_supervisor": 1},
  {"doctype": "Role Template", "role_name": "Child", "applies_to_org_type": "Family", "is_supervisor": 0},
  {"doctype": "Role Template", "role_name": "Guardian", "applies_to_org_type": "Family", "is_supervisor": 1},
  {"doctype": "Role Template", "role_name": "Extended Family", "applies_to_org_type": "Family", "is_supervisor": 0},
  {"doctype": "Role Template", "role_name": "Owner", "applies_to_org_type": "Company", "is_supervisor": 1, "default_hourly_rate": 0},
  {"doctype": "Role Template", "role_name": "Manager", "applies_to_org_type": "Company", "is_supervisor": 1, "default_hourly_rate": 0},
  {"doctype": "Role Template", "role_name": "Employee", "applies_to_org_type": "Company", "is_supervisor": 0, "default_hourly_rate": 0},
  {"doctype": "Role Template", "role_name": "Contractor", "applies_to_org_type": "Company", "is_supervisor": 0, "default_hourly_rate": 0},
  {"doctype": "Role Template", "role_name": "Board Member", "applies_to_org_type": "Nonprofit", "is_supervisor": 1},
  {"doctype": "Role Template", "role_name": "Volunteer", "applies_to_org_type": "Nonprofit", "is_supervisor": 0},
  {"doctype": "Role Template", "role_name": "Staff", "applies_to_org_type": "Nonprofit", "is_supervisor": 0},
  {"doctype": "Role Template", "role_name": "President", "applies_to_org_type": "Association", "is_supervisor": 1},
  {"doctype": "Role Template", "role_name": "Member", "applies_to_org_type": "Association", "is_supervisor": 0},
  {"doctype": "Role Template", "role_name": "Honorary", "applies_to_org_type": "Association", "is_supervisor": 0}
]
```

### 6. Update hooks.py

Add fixture export configuration:

```python
# In dartwing/hooks.py
fixtures = [
    {"dt": "Role Template", "filters": []},
    # ... other fixtures
]
```

### 7. Migrate Database

```bash
cd ~/frappe-bench
bench --site dartwing.localhost migrate
```

### 8. Load Fixtures

```bash
bench --site dartwing.localhost import-fixtures
```

## Verification

### Check DocType Created

```bash
bench --site dartwing.localhost console
>>> frappe.get_doc("DocType", "Role Template")
```

### List Role Templates

```bash
bench --site dartwing.localhost console
>>> frappe.get_all("Role Template", fields=["role_name", "applies_to_org_type", "is_supervisor"])
```

### Test API Access

```bash
# List all roles
curl -X GET "http://dartwing.localhost:8000/api/resource/Role%20Template" \
  -H "Cookie: sid=<your-session-id>"

# Filter by org type
curl -X GET "http://dartwing.localhost:8000/api/resource/Role%20Template?filters=[[\"applies_to_org_type\",\"=\",\"Family\"]]" \
  -H "Cookie: sid=<your-session-id>"
```

## Running Tests

```bash
cd ~/frappe-bench
bench --site dartwing.localhost run-tests \
  --app dartwing \
  --module dartwing.dartwing_core.doctype.role_template
```

## Common Issues

### Issue: Fixture not loading

**Solution**: Ensure `hooks.py` includes the Role Template fixture configuration and run `bench --site [site] import-fixtures`.

### Issue: Permission denied on API

**Solution**: For write operations, ensure user has System Manager role. For read operations, ensure user has Dartwing User role.

### Issue: Duplicate key error on fixture import

**Solution**: This is expected if fixtures already exist. Frappe updates existing records by name.

## Role Filtering for Org Member (Feature 3)

When implementing the Org Member form, use this pattern to filter roles by organization type:

### JavaScript (org_member.js)

```javascript
frappe.ui.form.on('Org Member', {
    organization: function(frm) {
        // Get the organization's type
        if (frm.doc.organization) {
            frappe.db.get_value('Organization', frm.doc.organization, 'org_type', (r) => {
                if (r && r.org_type) {
                    frm.set_query('role', function() {
                        return {
                            filters: {
                                applies_to_org_type: r.org_type
                            }
                        };
                    });
                }
            });
        }
    }
});
```

### Python API (alternative)

```python
from dartwing.dartwing_core.doctype.role_template.role_template import get_roles_for_org_type

# Get all Family roles
family_roles = get_roles_for_org_type("Family")
# Returns: [{"name": "Parent", "role_name": "Parent", "is_supervisor": 1, ...}, ...]
```

## Supervisor Hierarchy (Feature 5)

The `is_supervisor` flag indicates roles with supervisory privileges:

| Org Type | Supervisor Roles | Non-Supervisor Roles |
|----------|------------------|----------------------|
| Family | Parent, Guardian | Child, Extended Family |
| Company | Owner, Manager | Employee, Contractor |
| Nonprofit | Board Member | Volunteer, Staff |
| Association | President | Member, Honorary |

### Check Supervisor Status

```python
from dartwing.dartwing_core.doctype.role_template.role_template import is_supervisor_role

if is_supervisor_role("Manager"):
    # Grant additional permissions
    pass
```

## Next Steps

After Role Template is complete:
1. Implement Feature 3: Org Member DocType (depends on Role Template)
2. Add role filtering in Org Member form using the pattern above
3. Implement permission propagation (Feature 5) using is_supervisor flag
