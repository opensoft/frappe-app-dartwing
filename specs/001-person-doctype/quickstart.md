# Quickstart: Person DocType

**Feature Branch**: `001-person-doctype`
**Date**: 2025-12-01

## Overview

The Person DocType is the foundational identity layer for Dartwing. It links individuals to Frappe Users (system access), Keycloak (external auth), and Organizations.

## Prerequisites

- Frappe 16.x installed and running
- MariaDB 10.6+
- Redis (for background jobs)
- Organization DocType exists (from dartwing_core)
- "Dartwing User" role exists in fixtures

## Quick Setup

### 1. Install the DocTypes

After checkout, run migrations:

```bash
cd ~/frappe-bench
bench --site your-site.local migrate
```

This creates:
- `tabPerson` table
- `tabPerson Merge Log` table (child table)

### 2. Create Your First Person

**Via Python:**
```python
import frappe

person = frappe.get_doc({
    "doctype": "Person",
    "primary_email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "source": "signup"
})
person.insert()
frappe.db.commit()

print(f"Created Person: {person.name}")
```

**Via REST API:**
```bash
curl -X POST "https://your-site.local/api/resource/Person" \
  -H "Authorization: token api_key:api_secret" \
  -H "Content-Type: application/json" \
  -d '{
    "primary_email": "john.doe@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "source": "signup"
  }'
```

### 3. Link to Keycloak User

When a Keycloak user signs up:

```python
person = frappe.get_doc("Person", {"primary_email": email})
person.keycloak_user_id = keycloak_sub  # from OIDC callback
person.save()

# If auto-creation enabled, frappe_user is created automatically
# Check sync status:
print(f"Sync status: {person.user_sync_status}")
```

### 4. Handle Minors with Consent

```python
# Create minor (consent blocking enabled)
person = frappe.get_doc({
    "doctype": "Person",
    "primary_email": "child@example.com",
    "first_name": "Child",
    "last_name": "User",
    "source": "import",
    "is_minor": 1
})
person.insert()

# Attempting updates will fail until consent captured
# person.last_name = "Updated"  # This will throw PermissionError

# Capture consent via API
frappe.call(
    "dartwing.api.person.capture_consent",
    person_name=person.name
)

# Now updates work
person.reload()
person.last_name = "Updated"
person.save()  # Works!
```

### 5. Merge Duplicate Persons

```python
# Merge person2 into person1
result = frappe.call(
    "dartwing.api.person.merge_persons",
    source_person="PERSON-00002",
    target_person="PERSON-00001",
    notes="Duplicate from data import"
)

print(f"Transferred {result['org_members_transferred']} Org Members")

# Check merge history
person1 = frappe.get_doc("Person", "PERSON-00001")
for log in person1.merge_logs:
    print(f"Merged {log.source_person} at {log.merged_at} by {log.merged_by}")
```

## Common Operations

### Query Active Persons

```python
persons = frappe.get_all(
    "Person",
    filters={"status": "Active"},
    fields=["name", "primary_email", "first_name", "last_name"],
    order_by="modified desc",
    limit=20
)
```

### Find Person by Email

```python
person = frappe.get_doc("Person", {"primary_email": "john@example.com"})
# or
person_name = frappe.db.get_value("Person", {"primary_email": email}, "name")
```

### Check if Email Exists

```python
if frappe.db.exists("Person", {"primary_email": email}):
    frappe.throw("Email already in use")
```

### Retry Failed User Sync

```python
# Check status
person = frappe.get_doc("Person", person_name)
if person.user_sync_status == "failed":
    print(f"Error: {person.sync_error_message}")

    # Retry
    frappe.call(
        "dartwing.api.person.retry_sync",
        person_name=person.name
    )
```

## API Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| List Persons | GET | `/api/resource/Person` |
| Create Person | POST | `/api/resource/Person` |
| Get Person | GET | `/api/resource/Person/{name}` |
| Update Person | PUT | `/api/resource/Person/{name}` |
| Delete Person | DELETE | `/api/resource/Person/{name}` |
| Merge Persons | POST | `/api/method/dartwing.api.person.merge_persons` |
| Get Sync Status | GET | `/api/method/dartwing.api.person.get_sync_status` |
| Retry Sync | POST | `/api/method/dartwing.api.person.retry_sync` |
| Capture Consent | POST | `/api/method/dartwing.api.person.capture_consent` |

## Key Constraints

1. **Unique Email**: `primary_email` must be unique across all Person records
2. **Unique Keycloak ID**: `keycloak_user_id` unique when set (null allowed)
3. **Unique Frappe User**: `frappe_user` unique when set (null allowed)
4. **Minor Consent Block**: Cannot modify minors until consent captured
5. **Deletion Block**: Cannot delete if linked to Org Member

## Testing

Run tests:

```bash
cd ~/frappe-bench
bench --site your-site.local run-tests --app dartwing --module dartwing.dartwing_core.doctype.person
```

Key test cases:
- `test_duplicate_email_rejected`: Verify uniqueness enforcement
- `test_minor_consent_blocking`: Verify write blocking
- `test_deletion_blocked_with_org_member`: Verify referential integrity
- `test_user_sync_retry`: Verify background job retry logic

## Troubleshooting

### "Email already in use" Error

The email exists on another Person. Query to find it:
```python
existing = frappe.get_value("Person", {"primary_email": email}, "name")
print(f"Email in use by: {existing}")
```

### "Cannot modify Person record for a minor"

Person is marked as minor without consent. Capture consent first:
```python
frappe.call("dartwing.api.person.capture_consent", person_name=name)
```

### User Sync Stuck in "pending"

Check Redis/RQ is running:
```bash
bench --site your-site.local show-pending-jobs
```

Manually retry:
```python
frappe.call("dartwing.api.person.retry_sync", person_name=name)
```

### Cannot Delete Person

Person is linked to Org Member. Options:
1. Transfer Org Member to different Person
2. Delete the Org Member first
3. Merge into another Person instead of deleting
