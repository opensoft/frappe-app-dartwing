# Quickstart: Org Member DocType

**Feature**: 003-org-member-doctype
**Date**: 2025-12-12

## Prerequisites

- Frappe bench environment configured
- dartwing app installed
- Person, Organization, and Role Template DocTypes already exist
- Role Template fixtures loaded (14 predefined roles)

## Quick Setup

### 1. Create the DocType Files

```bash
# Navigate to the dartwing app
cd ~/frappe-bench/apps/dartwing

# Create the org_member doctype directory
mkdir -p dartwing/dartwing_core/doctype/org_member
touch dartwing/dartwing_core/doctype/org_member/__init__.py
```

### 2. After Implementation - Migrate

```bash
# Run migrations to create the database table
bench --site your-site migrate

# Verify the DocType was created
bench --site your-site console
>>> frappe.get_meta("Org Member").fields
```

### 3. Run Tests

```bash
# Run all Org Member tests
bench --site your-site run-tests --module dartwing.dartwing_core.doctype.org_member

# Run a specific test
bench --site your-site run-tests --module dartwing.dartwing_core.doctype.org_member.test_org_member --test test_create_basic_membership
```

## Basic Usage Examples

### Creating an Org Member (Python)

```python
import frappe

# Create a new membership
org_member = frappe.get_doc({
    "doctype": "Org Member",
    "person": "PERSON-2025-00001",
    "organization": "ORG-2025-00001",
    "role": "Employee",  # Must match org's type (Company)
    "status": "Active",
    "start_date": frappe.utils.today()
})
org_member.insert()
frappe.db.commit()

print(f"Created membership: {org_member.name}")
```

### Querying Members (Python)

```python
import frappe

# Get all active members of an organization
members = frappe.get_all(
    "Org Member",
    filters={
        "organization": "ORG-2025-00001",
        "status": "Active"
    },
    fields=["name", "person", "member_name", "role", "start_date"]
)

for m in members:
    print(f"{m.member_name} - {m.role} (since {m.start_date})")
```

### Using API Methods (Python)

```python
from dartwing.dartwing_core.doctype.org_member.org_member import (
    get_members_for_organization,
    get_organizations_for_person,
    add_member_to_organization,
)

# Get members for an organization
members = get_members_for_organization("ORG-2025-00001")

# Get organizations for a person
orgs = get_organizations_for_person("PERSON-2025-00001")

# Add a new member (handles reactivation automatically)
result = add_member_to_organization(
    person="PERSON-2025-00003",
    organization="ORG-2025-00001",
    role="Employee"
)
```

### Using API via REST (curl)

```bash
# Get members for an organization
curl -X POST "http://your-site/api/method/dartwing.dartwing_core.doctype.org_member.org_member.get_members_for_organization" \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"organization": "ORG-2025-00001"}'

# Add a member
curl -X POST "http://your-site/api/method/dartwing.dartwing_core.doctype.org_member.org_member.add_member_to_organization" \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{"person": "PERSON-2025-00003", "organization": "ORG-2025-00001", "role": "Employee"}'
```

## Common Validation Errors

### Duplicate Membership

```python
# This will raise ValidationError
frappe.get_doc({
    "doctype": "Org Member",
    "person": "PERSON-2025-00001",  # Already a member
    "organization": "ORG-2025-00001",
    "role": "Manager"
}).insert()
# Error: "Person is already a member of this organization"
```

### Invalid Role for Org Type

```python
# Organization ORG-2025-00001 is type "Company"
# "Parent" role is for "Family" org type
frappe.get_doc({
    "doctype": "Org Member",
    "person": "PERSON-2025-00002",
    "organization": "ORG-2025-00001",  # Company
    "role": "Parent"  # Family role
}).insert()
# Error: "Role 'Parent' is not valid for Company organizations"
```

### Last Supervisor Protection

```python
# If there's only one supervisor in the org
member = frappe.get_doc("Org Member", "abc123xyz")
member.status = "Inactive"
member.save()
# Error: "Cannot deactivate: at least one supervisor must remain in the organization"
```

## File Structure After Implementation

```
dartwing/dartwing_core/doctype/org_member/
├── __init__.py
├── org_member.json          # DocType definition (fields, permissions)
├── org_member.py            # Controller (validation, API methods)
└── test_org_member.py       # Integration tests

dartwing/hooks.py            # Updated with doc_events for Person cascade
```

## Key Implementation Notes

1. **Unique Constraint**: (person, organization) must be unique - implement in `validate()` method
2. **Role Validation**: Check role's `applies_to_org_type` matches organization's `org_type`
3. **Supervisor Check**: Use `is_supervisor` field from Role Template for last-supervisor protection
4. **Soft Cascade**: Person deletion triggers status change to Inactive via hooks.py `doc_events`
5. **Reactivation**: When adding a member who has an Inactive record, update existing instead of creating new
