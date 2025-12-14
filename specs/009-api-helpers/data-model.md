# Data Model: API Helpers (Whitelisted Methods)

**Date**: 2025-12-14
**Feature**: 009-api-helpers

## Overview

This feature primarily consumes existing data models rather than creating new ones. This document describes the entities involved and the response shapes returned by the API methods.

## Existing Entities (Read-Only)

### Organization

The polymorphic identity record for all organization types.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Primary key (e.g., "ORG-2025-00001") |
| org_name | string | Display name |
| org_type | select | Family/Company/Nonprofit/Association |
| logo | attach_image | Organization logo |
| status | select | Active/Inactive/Dissolved |
| linked_doctype | string | Concrete type name (e.g., "Family") |
| linked_name | string | Concrete type record name |

### Concrete Types

Type-specific records linked 1:1 with Organization.

**Family**
| Field | Type | Description |
|-------|------|-------------|
| name | string | Primary key (e.g., "FAM-00001") |
| organization | link | Reference to Organization |
| family_name | string | Family display name |
| family_nickname | string | Optional nickname |
| primary_residence | link | Address reference |
| parental_controls_enabled | check | Parental controls flag |
| screen_time_limit_minutes | int | Daily limit if controls enabled |
| status | select | Active/Inactive |

**Company**
| Field | Type | Description |
|-------|------|-------------|
| name | string | Primary key (e.g., "CO-00001") |
| organization | link | Reference to Organization |
| legal_name | string | Legal entity name |
| tax_id | string | EIN/Tax ID |
| entity_type | select | LLC/C-Corp/S-Corp/etc |
| jurisdiction_country | link | Country of formation |
| jurisdiction_state | string | State/Province |
| formation_date | date | Date of formation |
| officers | table | Organization Officer child table |
| members_partners | table | Member/Partner child table |
| status | select | Active/Inactive |

### Org Member

Junction record linking Person to Organization.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Primary key |
| person | link | Reference to Person |
| member_name | string | Person's full name (computed) |
| organization | link | Reference to Organization |
| organization_name | string | Org name (computed) |
| organization_type | string | Org type (computed) |
| role | link | Reference to Role Template |
| status | select | Active/Inactive/Pending |
| start_date | date | Membership start |
| end_date | date | Membership end (if inactive) |

### Person

Individual identity record.

| Field | Type | Description |
|-------|------|-------------|
| name | string | Primary key |
| full_name | string | Display name |
| first_name | string | First name |
| last_name | string | Last name |
| primary_email | string | Email address |
| mobile_no | string | Phone number |
| frappe_user | link | Linked Frappe User |

## API Response Shapes

### get_user_organizations Response

```json
{
    "data": [
        {
            "name": "ORG-2025-00001",
            "org_name": "Smith Family",
            "org_type": "Family",
            "logo": "/files/smith-logo.png",
            "status": "Active",
            "linked_doctype": "Family",
            "linked_name": "FAM-00001",
            "role": "Parent",
            "membership_status": "Active",
            "is_supervisor": 1
        }
    ],
    "total_count": 3
}
```

### get_organization_with_details Response

```json
{
    "name": "ORG-2025-00001",
    "org_name": "Smith Family",
    "org_type": "Family",
    "logo": "/files/smith-logo.png",
    "status": "Active",
    "linked_doctype": "Family",
    "linked_name": "FAM-00001",
    "creation": "2025-01-15 10:30:00",
    "modified": "2025-01-20 14:22:00",
    "concrete_type": {
        "name": "FAM-00001",
        "organization": "ORG-2025-00001",
        "family_name": "Smith Family",
        "family_nickname": "The Smiths",
        "primary_residence": "ADDR-00001",
        "parental_controls_enabled": 1,
        "screen_time_limit_minutes": 120,
        "status": "Active"
    }
}
```

### get_concrete_doc Response

```json
{
    "name": "FAM-00001",
    "organization": "ORG-2025-00001",
    "family_name": "Smith Family",
    "family_nickname": "The Smiths",
    "primary_residence": "ADDR-00001",
    "parental_controls_enabled": 1,
    "screen_time_limit_minutes": 120,
    "status": "Active",
    "creation": "2025-01-15 10:30:00",
    "modified": "2025-01-20 14:22:00"
}
```

Returns `null` if no concrete type linked.

### get_org_members Response

```json
{
    "data": [
        {
            "name": "OM-00001",
            "person": "PER-00001",
            "member_name": "John Smith",
            "organization": "ORG-2025-00001",
            "role": "Parent",
            "status": "Active",
            "start_date": "2025-01-15",
            "end_date": null,
            "is_supervisor": 1,
            "person_email": "john@example.com"
        },
        {
            "name": "OM-00002",
            "person": "PER-00002",
            "member_name": "Jane Smith",
            "organization": "ORG-2025-00001",
            "role": "Parent",
            "status": "Active",
            "start_date": "2025-01-15",
            "end_date": null,
            "is_supervisor": 1,
            "person_email": "jane@example.com"
        }
    ],
    "total_count": 4,
    "limit": 20,
    "offset": 0
}
```

## Error Response Shapes

### Not Found (404)

```json
{
    "exc_type": "DoesNotExistError",
    "message": "Organization ORG-2025-99999 not found"
}
```

### Permission Denied (403)

```json
{
    "exc_type": "PermissionError",
    "message": "Not permitted to access this organization"
}
```

### Authentication Required (401)

```json
{
    "exc_type": "AuthenticationError",
    "message": "Not logged in"
}
```

## Relationships Diagram

```
┌─────────────────┐     ┌──────────────────┐
│     Person      │     │  Role Template   │
│                 │     │                  │
│  name (PK)      │     │  name (PK)       │
│  full_name      │     │  applies_to_org  │
│  primary_email  │     │  is_supervisor   │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         │ person                │ role
         ▼                       ▼
┌─────────────────────────────────────────────┐
│                  Org Member                  │
│                                             │
│  name (PK)                                  │
│  person (FK → Person)                       │
│  organization (FK → Organization)           │
│  role (FK → Role Template)                  │
│  status                                     │
└─────────────────────┬───────────────────────┘
                      │ organization
                      ▼
              ┌───────────────────┐
              │   Organization    │
              │                   │
              │  name (PK)        │
              │  org_type         │
              │  linked_doctype   │
              │  linked_name      │
              └─────────┬─────────┘
                        │ 1:1 bidirectional
          ┌─────────────┼─────────────┬─────────────┐
          ▼             ▼             ▼             ▼
    ┌──────────┐  ┌──────────┐  ┌───────────┐  ┌──────────┐
    │  Family  │  │ Company  │  │Association│  │ Nonprofit│
    │          │  │          │  │           │  │          │
    │  FAM-*   │  │  CO-*    │  │  ASSOC-*  │  │  NPO-*   │
    └──────────┘  └──────────┘  └───────────┘  └──────────┘
```

## Constraints

1. **Unique Membership**: (person, organization) pair must be unique in Org Member
2. **Role-Org Type Match**: Role Template's `applies_to_org_type` must match Organization's `org_type`
3. **Bidirectional Link**: Organization.linked_name must match ConcreteType.organization
4. **Permission Cascade**: User Permission on Organization cascades to concrete type access
