# Research: Person DocType Implementation

**Feature Branch**: `001-person-doctype`
**Date**: 2025-12-01

## Overview

This document consolidates research findings for implementing the Person DocType in Frappe Framework 15.x. All NEEDS CLARIFICATION items from the Technical Context have been resolved.

---

## 1. Unique Field Constraints

### Decision: Hybrid JSON + Validate Hook Approach

**Rationale**: Frappe's `unique: 1` JSON property provides database-level enforcement for simple cases, but nullable unique fields (keycloak_user_id, frappe_user) require additional validation logic. Primary_email uses JSON-only since it's always required.

**Alternatives Considered**:

- JSON-only: Rejected because it doesn't provide custom error messages
- Validate-hook-only: Rejected because it loses database-level enforcement

### Implementation Details

| Field              | JSON `unique: 1` | Validate Hook | Notes                                  |
| ------------------ | ---------------- | ------------- | -------------------------------------- |
| `primary_email`    | Yes              | No            | Always required, simple uniqueness     |
| `keycloak_user_id` | Yes              | Yes           | Nullable, needs case-insensitive check |
| `frappe_user`      | Yes              | Yes           | Nullable Link field                    |

**Frappe's NULL Handling**: Frappe excludes empty/NULL values from uniqueness checks using:

```sql
WHERE ifnull(`fieldname`, '') != ''
```

This is correct behavior - multiple empty values are allowed, but non-null values must be unique.

**Code Pattern for Nullable Unique Fields**:

```python
def validate(self):
    if self.keycloak_user_id:
        existing = frappe.db.get_value(
            "Person",
            {
                "keycloak_user_id": self.keycloak_user_id,
                "name": ["!=", self.name]
            }
        )
        if existing:
            frappe.throw(
                _("Keycloak User ID {0} is already linked to another Person").format(
                    self.keycloak_user_id
                ),
                frappe.DuplicateEntryError
            )
```

**Supported Field Types for Unique**: Data, Link, Read Only, Int only

---

## 2. Background Jobs for User Sync Retry

### Decision: frappe.enqueue() with Custom Retry Logic

**Rationale**: Frappe's built-in retry (5 attempts on deadlock only) is insufficient for external service failures. Custom retry with exponential backoff provides resilient Keycloak integration.

**Alternatives Considered**:

- Built-in retry only: Rejected - only handles DB deadlocks, not service failures
- Immediate inline retry: Rejected - blocks request, poor UX
- Scheduled job polling: Rejected - inefficient, delayed resolution

### Retry Strategy

| Aspect      | Value                                                  |
| ----------- | ------------------------------------------------------ |
| Max Retries | 5                                                      |
| Backoff     | Exponential: 2s → 4s → 8s → 16s → 32s (capped at 120s) |
| Queue       | `default` (5-minute timeout)                           |
| Job ID      | `person-sync-{person_name}` (prevents duplicates)      |

**Retryable Errors**: Connection timeout, service unavailable (500, 503, 504)
**Non-Retryable Errors**: Auth failures, validation errors, duplicate entries

### Implementation Pattern

```python
# dartwing/utils/person_sync.py
import frappe
from frappe.utils import now

MAX_RETRIES = 5
BASE_DELAY = 2  # seconds

def queue_user_sync(person_name, attempt=1):
    """Queue background job for Frappe User creation."""
    delay = min(BASE_DELAY * (2 ** (attempt - 1)), 120)

    frappe.enqueue(
        'dartwing.utils.person_sync.sync_frappe_user',
        person_name=person_name,
        attempt=attempt,
        queue='default',
        timeout=300,
        job_id=f'person-sync-{person_name}',
        enqueue_after_commit=True,
        at_front=False
    )

def sync_frappe_user(person_name, attempt=1):
    """Create Frappe User from Person's keycloak_user_id."""
    person = frappe.get_doc("Person", person_name)

    try:
        # Create Frappe User logic here
        user = create_frappe_user(person)

        person.frappe_user = user.name
        person.user_sync_status = "synced"
        person.last_sync_at = now()
        person.sync_error_message = None
        person.save(ignore_permissions=True)

    except RetryableError as e:
        if attempt < MAX_RETRIES:
            person.user_sync_status = "pending"
            person.sync_error_message = str(e)
            person.save(ignore_permissions=True)
            queue_user_sync(person_name, attempt + 1)
        else:
            person.user_sync_status = "failed"
            person.sync_error_message = f"Max retries exceeded: {e}"
            person.save(ignore_permissions=True)
            frappe.log_error(f"Person sync failed: {person_name}", str(e))
```

### Status Tracking Fields

Add to Person DocType:

- `user_sync_status` (Select: synced/pending/failed) - Read-only
- `sync_error_message` (Text) - Read-only
- `last_sync_at` (Datetime) - Read-only

---

## 3. Child Table for Merge Audit Logging

### Decision: Separate Person Merge Log Child Table

**Rationale**: Child tables in Frappe provide structured, queryable audit trails attached to the parent document. This follows the Family Member pattern already in dartwing_core.

**Alternatives Considered**:

- Single field with JSON blob: Rejected - not queryable, hard to render
- Frappe's Version/Activity Log: Rejected - generic, doesn't capture merge-specific data
- Separate linked DocType: Rejected - child table is simpler and auto-loads with parent

### JSON Structure

```json
{
  "doctype": "DocType",
  "istable": 1,
  "module": "Dartwing Core",
  "name": "Person Merge Log",
  "field_order": [
    "source_person",
    "target_person",
    "merged_at",
    "merged_by",
    "notes"
  ],
  "fields": [
    {
      "fieldname": "source_person",
      "fieldtype": "Link",
      "options": "Person",
      "label": "Source Person",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "target_person",
      "fieldtype": "Link",
      "options": "Person",
      "label": "Target Person",
      "reqd": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "merged_at",
      "fieldtype": "Datetime",
      "label": "Merged At",
      "reqd": 1,
      "read_only": 1,
      "in_list_view": 1
    },
    {
      "fieldname": "merged_by",
      "fieldtype": "Link",
      "options": "User",
      "label": "Merged By",
      "reqd": 1,
      "read_only": 1
    },
    {
      "fieldname": "notes",
      "fieldtype": "Small Text",
      "label": "Notes"
    }
  ],
  "track_changes": 1
}
```

### Parent DocType Integration

Add to Person.json:

```json
{
  "fieldname": "merge_logs",
  "fieldtype": "Table",
  "options": "Person Merge Log",
  "label": "Merge History",
  "read_only": 1
}
```

### Adding Entries Programmatically

```python
def merge_persons(source_name, target_name, notes=None):
    target = frappe.get_doc("Person", target_name)
    target.append("merge_logs", {
        "source_person": source_name,
        "target_person": target_name,
        "merged_at": frappe.utils.now(),
        "merged_by": frappe.session.user,
        "notes": notes
    })
    target.save()
```

---

## 4. Mobile Number Validation

### Decision: phonenumbers Library with Country Context

**Rationale**: E.164 format ensures international compatibility. The `phonenumbers` library (Google's libphonenumber port) handles country-specific validation.

**Alternatives Considered**:

- Regex-only: Rejected - doesn't handle international formats correctly
- No validation: Rejected - spec requires "country-aware validation" (FR-010)

### Implementation

```python
import phonenumbers
from phonenumbers import NumberParseException

def validate_mobile(self):
    if not self.mobile_no:
        return

    try:
        # Parse with default country (can be overridden)
        parsed = phonenumbers.parse(self.mobile_no, "US")
        if not phonenumbers.is_valid_number(parsed):
            frappe.throw(_("Invalid mobile number format"))

        # Store in E.164 format
        self.mobile_no = phonenumbers.format_number(
            parsed, phonenumbers.PhoneNumberFormat.E164
        )
    except NumberParseException:
        frappe.throw(_("Invalid mobile number"))
```

**Note**: Add `phonenumbers` to `pyproject.toml` dependencies.

---

## 5. Consent Blocking for Minors

### Decision: Validate Hook with Before Save Check

**Rationale**: FR-013 requires blocking ALL write operations on minors without consent. This must be enforced in the validate() hook to catch both API and UI updates.

**Implementation**:

```python
def validate(self):
    self._check_minor_consent_block()

def _check_minor_consent_block(self):
    """Block updates to minor's record if consent not captured."""
    if not self.is_new() and self.is_minor and not self.consent_captured:
        # Check if this is a consent capture operation
        if self.has_value_changed("consent_captured") and self.consent_captured:
            return  # Allow this specific update

        frappe.throw(
            _("Cannot modify Person record for a minor until consent is captured"),
            frappe.PermissionError
        )
```

**Exception**: The consent capture operation itself must be allowed.

---

## 6. Deletion Prevention

### Decision: Before Delete Hook with Org Member Check

**Rationale**: FR-006 requires preventing deletion when linked to Org Member. Use `before_delete()` hook to check and block.

**Implementation**:

```python
def before_delete(self):
    """Prevent deletion if linked to Org Member."""
    linked_org_members = frappe.get_all(
        "Org Member",
        filters={"person": self.name},
        limit=1
    )

    if linked_org_members:
        frappe.throw(
            _("Cannot delete Person linked to Org Member. "
              "Please deactivate or merge instead."),
            frappe.LinkExistsError
        )
```

---

## Summary of Resolved Items

| Item                                  | Resolution                                            |
| ------------------------------------- | ----------------------------------------------------- |
| Unique constraints on nullable fields | Hybrid JSON + validate hook                           |
| Background job retry strategy         | frappe.enqueue() with exponential backoff (5 retries) |
| Merge audit logging                   | Person Merge Log child table                          |
| Mobile validation                     | phonenumbers library with E.164                       |
| Minor consent blocking                | validate() hook with exception for consent capture    |
| Deletion prevention                   | before_delete() hook checking Org Member links        |

All technical decisions align with the project constitution and existing dartwing patterns.
