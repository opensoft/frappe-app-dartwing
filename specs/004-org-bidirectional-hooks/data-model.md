# Data Model: Organization Bidirectional Hooks

**Feature**: 004-org-bidirectional-hooks
**Date**: 2025-12-13

## Overview

This feature operates on existing doctypes and does not introduce new entities. It establishes and maintains the bidirectional relationship between Organization and its concrete type records.

---

## Entities

### Organization (Existing - Modified Behavior)

The thin reference shell that holds shared identity and links to concrete types.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | Data | Yes | Auto-generated primary key (naming_series: ORG-.YYYY.-) |
| org_name | Data | Yes | Display name of the organization |
| org_type | Select | Yes | Type: Family, Company, Nonprofit, Association (immutable after creation) |
| logo | Attach Image | No | Organization logo |
| status | Select | No | Active, Inactive, Dissolved (default: Active) |
| linked_doctype | Data | No | Auto-populated: doctype name of concrete type |
| linked_name | Data | No | Auto-populated: record name of concrete type |

**Validation Rules**:
- `org_type` must be one of: Family, Company, Nonprofit, Association
- `org_type` cannot be changed after creation (`set_only_once` + server validation)
- `linked_doctype` and `linked_name` are read-only, system-managed

**Lifecycle**:
```
Created → [after_insert hook] → Concrete type auto-created, linked_* fields populated
         ↓
Active (normal operations)
         ↓
Deleted → [on_trash hook] → Concrete type cascade-deleted
```

---

### Family (Existing - No Changes)

Concrete type for family organizations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | Data | Yes | Auto-generated (FAM-.#####) |
| organization | Link → Organization | Yes | Back-reference to parent Organization |
| family_nickname | Data | No | Family nickname |
| primary_residence | Link → Address | No | Primary residence address |
| parental_controls_enabled | Check | No | Enable parental controls |
| screen_time_limit_minutes | Int | No | Daily screen time limit |

---

### Company (Existing - No Changes)

Concrete type for business organizations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | Data | Yes | Auto-generated (CO-.#####) |
| organization | Link → Organization | Yes | Back-reference to parent Organization |
| legal_name | Data | No | Legal entity name |
| tax_id | Data | No | Tax ID / EIN |
| entity_type | Select | No | C-Corp, S-Corp, LLC, etc. |
| jurisdiction_country | Link → Country | No | Country of formation |
| jurisdiction_state | Data | No | State/Province |
| officers | Table → Organization Officer | No | Officers & Directors |
| members_partners | Table → Organization Member Partner | No | Members/Partners |

---

### Association (Existing - No Changes)

Concrete type for association organizations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | Data | Yes | Auto-generated (ASSOC-.#####) |
| organization | Link → Organization | Yes | Back-reference to parent Organization |
| association_type | Select | Yes | Club, HOA, Alumni Association, etc. |
| membership_tiers | Table → Organization Membership Tier | No | Membership tiers |
| default_dues_amount | Currency | No | Default annual dues |
| amenities | Small Text | No | Amenities description |
| facility_address | Link → Address | No | Primary facility address |

---

### Nonprofit (Existing - No Changes)

Concrete type for nonprofit organizations.

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | Data | Yes | Auto-generated (NPO-.#####) |
| organization | Link → Organization | Yes | Back-reference to parent Organization |
| tax_exempt_status | Select | No | 501(c)(3), 501(c)(4), etc. |
| ein | Data | No | EIN |
| determination_date | Date | No | IRS determination date |
| fiscal_year_end | Select | No | Fiscal year end month |
| mission_statement | Text | No | Mission statement |
| board_members | Table → Organization Officer | No | Board members |

---

## Relationships

```
┌─────────────────────────────────────────────────────────────────┐
│                         Organization                             │
│  ┌───────────┬──────────┬────────┬─────────────────────────┐    │
│  │ org_name  │ org_type │ status │ linked_doctype/name     │    │
│  └───────────┴──────────┴────────┴─────────────────────────┘    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ 1:1 Link (maintained by hooks)
          ┌─────────────────┼─────────────────┬─────────────────┐
          ▼                 ▼                 ▼                 ▼
     ┌─────────┐      ┌──────────┐      ┌───────────┐    ┌───────────┐
     │ Family  │      │ Company  │      │Association│    │ Nonprofit │
     ├─────────┤      ├──────────┤      ├───────────┤    ├───────────┤
     │org [FK] │      │ org [FK] │      │ org [FK]  │    │ org [FK]  │
     └─────────┘      └──────────┘      └───────────┘    └───────────┘
```

**Relationship Type**: 1:1 Bidirectional

**Forward Link** (Organization → Concrete):
- `linked_doctype`: Stores the doctype name (e.g., "Family")
- `linked_name`: Stores the record name (e.g., "FAM-00001")

**Reverse Link** (Concrete → Organization):
- `organization`: Link field pointing to parent Organization

---

## State Transitions

### Organization Lifecycle

```
[New] ──create──▶ [Created] ──after_insert hook──▶ [Linked]
                                                      │
                                                      ▼
                                              Normal Operations
                                                      │
                                                      ▼
                              [Deleting] ◀──delete──┘
                                   │
                                   ▼
                      [on_trash hook: cascade delete concrete]
                                   │
                                   ▼
                               [Deleted]
```

### org_type Immutability

```
[New] ──set org_type──▶ [Created with type]
                              │
                              ▼
                     [Type LOCKED - cannot change]
                              │
                              ▼
              [Validation error on attempt to modify]
```

---

## Indexes and Constraints

### Organization

| Constraint | Type | Fields | Purpose |
|------------|------|--------|---------|
| PRIMARY KEY | Unique | name | Record identifier |
| UNIQUE | Unique | (linked_doctype, linked_name) | Ensure 1:1 mapping |

### Concrete Types (Family, Company, Association, Nonprofit)

| Constraint | Type | Fields | Purpose |
|------------|------|--------|---------|
| PRIMARY KEY | Unique | name | Record identifier |
| FOREIGN KEY | Reference | organization → Organization.name | Referential integrity |
| UNIQUE | Unique | organization | Ensure 1:1 mapping (one concrete per org) |

---

## Data Integrity Rules

1. **Creation Integrity**: Every Organization MUST have exactly one linked concrete type after creation completes
2. **Link Consistency**: `Organization.linked_name` MUST reference a record where `ConcreteType.organization` points back
3. **Type Constraint**: `Organization.linked_doctype` MUST match the expected doctype for `org_type`
4. **Deletion Cascade**: Deleting Organization MUST delete the linked concrete type
5. **Orphan Prevention**: Concrete types SHOULD NOT exist without a valid Organization reference
