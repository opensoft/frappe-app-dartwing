# Quickstart: Organization Bidirectional Hooks

**Feature**: 004-org-bidirectional-hooks
**Date**: 2025-12-13

## Overview

This guide explains how to work with the Organization bidirectional hooks feature. After implementation, Organizations will automatically create and link their concrete type records (Family, Company, Association, Nonprofit).

---

## Prerequisites

- Frappe 15.x development environment
- dartwing_core app installed
- Organization, Family, Company, Association, and Nonprofit doctypes exist

---

## Creating an Organization

When you create an Organization, the concrete type is automatically created:

### Via Frappe Desk

1. Navigate to **Organization** list
2. Click **+ Add Organization**
3. Fill in:
   - **Organization Name**: "Smith Family"
   - **Organization Type**: "Family"
4. Click **Save**

The system will automatically:
- Create a Family record linked to this Organization
- Populate `linked_doctype` = "Family"
- Populate `linked_name` = the new Family record name

### Via API

```python
import frappe

# Create Organization - concrete type is auto-created
org = frappe.get_doc({
    "doctype": "Organization",
    "org_name": "Smith Family",
    "org_type": "Family"
})
org.insert()

# The Organization now has linked_doctype and linked_name populated
print(f"Linked to: {org.linked_doctype} - {org.linked_name}")
# Output: Linked to: Family - FAM-00001
```

### Via REST API

```bash
curl -X POST \
  'https://your-site.com/api/resource/Organization' \
  -H 'Authorization: token api_key:api_secret' \
  -H 'Content-Type: application/json' \
  -d '{
    "org_name": "Smith Family",
    "org_type": "Family"
  }'
```

---

## Retrieving Organization with Details

### Get Concrete Type Only

```python
from dartwing.dartwing_core.doctype.organization.organization import get_concrete_doc

# Returns just the Family/Company/etc record
concrete = get_concrete_doc("ORG-2025-00001")
print(concrete)
# {
#   "name": "FAM-00001",
#   "doctype": "Family",
#   "organization": "ORG-2025-00001",
#   "family_nickname": "The Smiths",
#   ...
# }
```

### Get Organization with Merged Details

```python
from dartwing.dartwing_core.doctype.organization.organization import get_organization_with_details

# Returns Organization with nested concrete_type
result = get_organization_with_details("ORG-2025-00001")
print(result)
# {
#   "name": "ORG-2025-00001",
#   "org_name": "Smith Family",
#   "org_type": "Family",
#   "linked_doctype": "Family",
#   "linked_name": "FAM-00001",
#   "concrete_type": {
#     "name": "FAM-00001",
#     "family_nickname": "The Smiths",
#     ...
#   }
# }
```

### Via REST API

```bash
# Get concrete type only
curl -X POST \
  'https://your-site.com/api/method/dartwing.dartwing_core.doctype.organization.organization.get_concrete_doc' \
  -H 'Authorization: token api_key:api_secret' \
  -H 'Content-Type: application/json' \
  -d '{"organization": "ORG-2025-00001"}'

# Get organization with details
curl -X POST \
  'https://your-site.com/api/method/dartwing.dartwing_core.doctype.organization.organization.get_organization_with_details' \
  -H 'Authorization: token api_key:api_secret' \
  -H 'Content-Type: application/json' \
  -d '{"organization": "ORG-2025-00001"}'
```

---

## Deleting an Organization

When you delete an Organization, the concrete type is automatically deleted:

```python
# Delete Organization - concrete type is cascade-deleted
frappe.delete_doc("Organization", "ORG-2025-00001")
# The linked Family record is automatically deleted
```

**Note**: If the Organization is referenced by other records (Org Members, Tasks, etc.), deletion will be blocked by Frappe's referential integrity checks.

---

## Organization Type Immutability

Once created, an Organization's `org_type` cannot be changed:

```python
org = frappe.get_doc("Organization", "ORG-2025-00001")
org.org_type = "Company"  # Attempt to change
org.save()  # Raises ValidationError: "Organization type cannot be changed after creation"
```

This is enforced both at the UI level (field is read-only after save) and at the API level (server-side validation).

---

## Audit Logs

Hook executions are logged for debugging and audit purposes. Check the Frappe logs:

```bash
# View hook execution logs
tail -f ~/frappe-bench/logs/worker.log | grep "dartwing_core.hooks"
```

Log format:
```
[INFO] dartwing_core.hooks: Created Family FAM-00001 for Organization ORG-2025-00001
[INFO] dartwing_core.hooks: Cascade deleted Family FAM-00001 for Organization ORG-2025-00001
```

---

## Testing

Run the test suite to verify hook behavior:

```bash
cd ~/frappe-bench
bench --site your-site run-tests --app dartwing --module dartwing.tests.test_organization_hooks
```

Key test scenarios:
- Creating Organization creates linked concrete type
- Deleting Organization cascade-deletes concrete type
- Changing org_type is blocked
- Invalid org_type is rejected

---

## Troubleshooting

### Concrete type not created
- Check that the concrete doctype (Family, Company, etc.) exists
- Check Frappe error logs for hook failures
- Verify hooks.py registration is correct

### Permission errors
- Hook operations run with system privileges
- Ensure the Organization creation permission is granted to the user

### Orphaned records
- If concrete type exists without Organization, it may be from failed transactions
- Manual cleanup may be needed for legacy data
