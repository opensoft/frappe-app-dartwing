# Quickstart: Company DocType

**Feature**: 006-company-doctype
**Date**: 2025-12-13

## Prerequisites

- Frappe bench with dartwing app installed
- Python 3.11+
- MariaDB 10.6+
- Person DocType implemented (Feature #1)
- Organization hooks working (Feature #4)

## Setup Steps

### 1. Create Module Directory Structure

```bash
cd apps/dartwing/dartwing

# Create dartwing_company module
mkdir -p dartwing_company/doctype/company
touch dartwing_company/__init__.py
touch dartwing_company/doctype/__init__.py
touch dartwing_company/doctype/company/__init__.py
```

### 2. Register the Module

Add to `apps/dartwing/dartwing/modules.txt`:
```
Dartwing Core
Dartwing Company
```

### 3. Create Child Tables (in dartwing_core)

```bash
cd apps/dartwing/dartwing/dartwing_core/doctype

# Create Organization Officer child table
mkdir -p organization_officer
touch organization_officer/__init__.py

# Create Organization Member Partner child table
mkdir -p organization_member_partner
touch organization_member_partner/__init__.py
```

### 4. Install/Migrate

```bash
cd ~/frappe-bench
bench --site your-site.local migrate
```

## Quick Verification

### Test Organization → Company Auto-Creation

```python
# In bench console: bench --site your-site.local console

import frappe

# Create an Organization with org_type="Company"
org = frappe.new_doc("Organization")
org.org_name = "Test Company"
org.org_type = "Company"
org.insert()

# Verify Company was created
print(f"Linked DocType: {org.linked_doctype}")  # Should be "Company"
print(f"Linked Name: {org.linked_name}")        # Should be "CO-00001" or similar

# Fetch the Company
company = frappe.get_doc("Company", org.linked_name)
print(f"Company organization: {company.organization}")  # Should match org.name
```

### Test API Access

```bash
# List companies (requires authentication)
curl -X GET "http://your-site.local/api/resource/Company" \
  -H "Authorization: token api_key:api_secret"

# Get single company
curl -X GET "http://your-site.local/api/resource/Company/CO-00001" \
  -H "Authorization: token api_key:api_secret"
```

### Test Child Tables

```python
# In bench console

# Add an officer to a company
company = frappe.get_doc("Company", "CO-00001")
company.append("officers", {
    "person": "PERSON-2025-00001",
    "title": "CEO",
    "start_date": "2025-01-01"
})
company.save()

# Verify
print(company.officers[0].title)  # Should be "CEO"
```

### Test Conditional Visibility

1. Open Company in Frappe Desk
2. Set entity_type to "C-Corp" → Ownership section should be hidden
3. Set entity_type to "LLC" → Ownership section should be visible

## Common Issues

### "Company DocType does not exist"

- Run `bench migrate` to create tables
- Check that `company.json` is valid JSON

### "Organization Officer does not exist"

- Child tables must be created before Company
- Run `bench migrate` after creating child table JSON files

### Company not auto-created

- Check Organization.py has Company in ORG_TYPE_MAP
- Remove the `if concrete_doctype != "Family": return` guard
- Check Frappe error logs: `bench --site your-site.local show-logs`

### Permission denied

- Ensure User Permission exists for the Organization
- Check role assignments (System Manager or Dartwing User)

## Development Workflow

### Making Changes

1. Edit JSON/Python files
2. Run `bench migrate` (for schema changes)
3. Run tests: `bench --site your-site.local run-tests --module dartwing_company`
4. Restart: `bench restart` (for Python changes)

### Debugging

```python
# Enable debug logging
frappe.local.flags.in_test = True

# Check error logs
frappe.get_all("Error Log", limit=5)
```

## Next Steps

After basic setup works:

1. Implement permission hooks (`permissions.py`)
2. Add OrganizationMixin to Company controller
3. Write comprehensive tests
4. Test cascade delete behavior
