# Data Model: User Permission Propagation

**Feature**: 005-user-permission-propagation
**Date**: 2025-12-13

## Overview

This feature does not introduce new DocTypes. Instead, it leverages Frappe's built-in `User Permission` DocType and adds hooks/functions to manage permissions automatically based on `Org Member` records.

## Entities Used

### 1. User Permission (Frappe Built-in)

**Description**: Grants a specific user access to a specific record of a specific DocType.

| Field | Type | Description |
|-------|------|-------------|
| user | Link (User) | The Frappe User receiving the permission |
| allow | Data | DocType name being permitted (e.g., "Organization") |
| for_value | Data | Specific record name being permitted |
| apply_to_all_doctypes | Check | If checked, applies to all doctypes with Link to this |
| applicable_for | Data | Specific DocType to apply permission to |

**Usage in this feature**:
- Created when Org Member is created (if Person has frappe_user)
- Deleted when Org Member is deleted or status becomes Inactive
- Queried in permission_query_conditions to filter list views

### 2. Org Member (Feature 3)

**Description**: Links a Person to an Organization with a role. This is the trigger for permission propagation.

| Field | Type | Description |
|-------|------|-------------|
| person | Link (Person) | The person being added as member |
| organization | Link (Organization) | The organization they're joining |
| role | Link (Role Template) | Their role in the organization |
| status | Select | Active/Inactive/Pending |
| start_date | Date | Membership start date |
| end_date | Date | Membership end date |

**Events triggering permission propagation**:
- `after_insert`: Creates User Permissions for Organization + concrete type
- `on_trash`: Removes User Permissions
- `on_update`: Handles status changes (Active ↔ Inactive)

### 3. Person (Feature 1)

**Description**: Individual identity that may be linked to a Frappe User.

**Relevant field**:
| Field | Type | Description |
|-------|------|-------------|
| frappe_user | Link (User) | The Frappe User account (if any) |

**Used to**: Look up the User email when creating User Permissions

### 4. Organization (Existing)

**Description**: Polymorphic identity shell for organizations.

**Relevant fields**:
| Field | Type | Description |
|-------|------|-------------|
| name | Data | Organization ID (e.g., "ORG-2025-00001") |
| org_type | Select | Family/Company/Nonprofit/Association |
| linked_doctype | Data | Concrete type name (e.g., "Family") |
| linked_name | Data | Concrete type record name |

**Used to**: Determine which concrete type permission to create

## Entity Relationships

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Permission Flow                              │
└─────────────────────────────────────────────────────────────────────┘

                    ┌─────────────┐
                    │   Person    │
                    │             │
                    │ frappe_user ├────────────┐
                    └──────┬──────┘            │
                           │                   │
                           │ person            │
                           ▼                   ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│Organization │◄────┤ Org Member  │     │    User     │
│             │org  │             │     │  (Frappe)   │
│linked_doctype     │   status    │     └──────┬──────┘
│linked_name  │     └─────────────┘            │
└──────┬──────┘           │                    │
       │                  │ triggers           │
       │ 1:1              ▼                    │
       ▼           ┌─────────────┐             │
┌─────────────┐    │   Hooks     │             │
│ Family/     │    │             │             │
│ Company/    │    │after_insert │────────────►│
│ Association/│    │  on_trash   │  creates    │
│ Nonprofit   │    │  on_update  │  removes    │
└─────────────┘    └─────────────┘             │
                                               │
                         ┌─────────────────────┘
                         │
                         ▼
                  ┌─────────────────┐
                  │ User Permission │
                  │                 │
                  │ user: User      │
                  │ allow: DocType  │
                  │ for_value: name │
                  └─────────────────┘
```

## User Permission Records Created

For each Org Member with an active Person.frappe_user:

| Permission # | allow | for_value | Purpose |
|--------------|-------|-----------|---------|
| 1 | Organization | {organization.name} | Access to Organization record |
| 2 | {linked_doctype} | {linked_name} | Access to concrete type (Family/Company/etc.) |

**Example**:
When John (Person with frappe_user="john@example.com") becomes an Org Member of "ORG-2025-00001" (a Company):

```
User Permission 1:
  user: john@example.com
  allow: Organization
  for_value: ORG-2025-00001

User Permission 2:
  user: john@example.com
  allow: Company
  for_value: CO-00001
```

## State Transitions

### Org Member Status → Permission State

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│   Pending   │──────►│   Active    │──────►│  Inactive   │
└─────────────┘       └─────────────┘       └─────────────┘
      │                     │                     │
      │                     │                     │
      ▼                     ▼                     ▼
 No Permissions      Permissions           Permissions
    Created            Exist                 Removed
```

**Transitions**:
- Pending → Active: No permission action (permissions created on insert if status = Active)
- Active → Inactive: Remove permissions (FR-009)
- Inactive → Active: Re-create permissions
- Delete (any status): Remove permissions

## Validation Rules

### User Permission Creation

1. Person MUST have a linked frappe_user
2. Organization MUST exist
3. User Permission for same (user, allow, for_value) MUST NOT exist

### User Permission Deletion

1. All User Permissions matching (user, allow, for_value) MUST be deleted
2. Deletion MUST succeed even if permission doesn't exist (idempotent)

## Indexes (Frappe Default)

User Permission has default indexes on:
- `user`
- `allow`
- `for_value`

These support efficient queries for permission checks.

## Data Integrity Constraints

| Constraint | Enforcement | Location |
|------------|-------------|----------|
| Org Member unique (person, organization) | Unique constraint | org_member.json / validate() |
| User Permission unique (user, allow, for_value) | Insert check | helpers.create_permission() |
| Person.frappe_user exists before permission | Validation | helpers.create_user_permissions() |
