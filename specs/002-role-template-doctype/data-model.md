# Data Model: Role Template DocType

**Feature**: 002-role-template-doctype
**Date**: 2025-12-03

## Entity: Role Template

A system-wide role definition that specifies organization-type-specific roles for member assignment.

### Fields

| Field                 | Type     | Required | Unique | Description                                                                          |
| --------------------- | -------- | -------- | ------ | ------------------------------------------------------------------------------------ |
| `name`                | Data     | Yes      | Yes    | Primary key (auto-set from role_name)                                                |
| `role_name`           | Data     | Yes      | Yes    | Human-readable role identifier                                                       |
| `applies_to_org_type` | Select   | Yes      | No     | Organization type filter (Family, Company, Nonprofit, Association)                   |
| `is_supervisor`       | Check    | No       | No     | Whether role has supervisory permissions                                             |
| `default_hourly_rate` | Currency | No       | No     | Default hourly rate (visible for Company, Nonprofit, Association; hidden for Family) |

### Field Details

#### role_name

- **Constraints**: Unique across all Role Templates
- **Validation**: Required, max 140 characters
- **Index**: Primary lookup field, in_list_view, in_standard_filter
- **Examples**: "Parent", "Manager", "Board Member", "President"

#### applies_to_org_type

- **Options**: Family, Company, Nonprofit, Association
- **Constraints**: Required, must match Organization.org_type values
- **Behavior**: Used to filter roles when assigning to Org Members
- **Note**: "Association" covers subtypes like Club, HOA, etc.

#### is_supervisor

- **Default**: 0 (false)
- **Purpose**: Identifies roles with supervisory/administrative capabilities
- **Usage**: Future permission system will use this for hierarchy enforcement

#### default_hourly_rate

- **Visibility**: Shown for organization types with paid staff (Company, Nonprofit, Association); hidden for Family
- **Precision**: Currency field with 2 decimal places
- **Default**: 0.00
- **Purpose**: Default value for payroll calculations when assigning paid staff (employees, contractors, paid nonprofit staff)

### Naming Convention

- **autoname**: Uses `role_name` field directly (no series)
- **Example**: Role with role_name="Parent" gets name="Parent"

### Relationships

```
┌─────────────────────┐
│   Role Template     │
│                     │
│ - role_name (PK)    │
│ - applies_to_org_type│
│ - is_supervisor     │
│ - default_hourly_rate│
└─────────────────────┘
          │
          │ (1:N) filtered by org_type
          ▼
┌─────────────────────┐
│   Org Member        │  ← Feature 3
│   (Future)          │
│                     │
│ - role_template (Link) │
│ - organization      │
└─────────────────────┘
          │
          │ (N:1)
          ▼
┌─────────────────────┐
│   Organization      │
│                     │
│ - org_type          │ ← Filters available roles
└─────────────────────┘
```

### State Transitions

Role Template has no state machine - it is static reference data.

- Created via fixtures or System Manager
- Read by all authenticated users
- Updated only by System Manager
- Deleted only if no Org Members reference it

---

## Seed Data

### Family Roles (4)

| role_name       | is_supervisor | default_hourly_rate |
| --------------- | ------------- | ------------------- |
| Parent          | Yes           | -                   |
| Child           | No            | -                   |
| Guardian        | Yes           | -                   |
| Extended Family | No            | -                   |

### Company Roles (4)

| role_name  | is_supervisor | default_hourly_rate |
| ---------- | ------------- | ------------------- |
| Owner      | Yes           | 0.00                |
| Manager    | Yes           | 0.00                |
| Employee   | No            | 0.00                |
| Contractor | No            | 0.00                |

### Nonprofit Roles (3)

| role_name    | is_supervisor | default_hourly_rate |
| ------------ | ------------- | ------------------- |
| Board Member | Yes           | 0.00                |
| Volunteer    | No            | 0.00                |
| Staff        | No            | 0.00                |

### Association Roles (3)

| role_name | is_supervisor | default_hourly_rate |
| --------- | ------------- | ------------------- |
| President | Yes           | -                   |
| Member    | No            | -                   |
| Honorary  | No            | -                   |

**Total Seed Records**: 14 roles

---

## Validation Rules

### On Insert/Update

1. `role_name` must be unique (enforced at DB level)
2. `applies_to_org_type` must be one of: Family, Company, Nonprofit, Association
3. `default_hourly_rate` should be cleared (set to 0) when `applies_to_org_type == 'Family'` (families don't have paid roles)

### On Delete

1. Check for linked Org Member records (when Org Member DocType exists)
2. Reject deletion if any Org Members reference this role
3. Provide clear error message with count of linked records

---

## Indexes

| Index   | Fields              | Purpose                           |
| ------- | ------------------- | --------------------------------- |
| Primary | name (role_name)    | Unique identifier                 |
| Filter  | applies_to_org_type | Fast filtering for role dropdowns |

---

## DocType JSON Structure

```json
{
  "doctype": "DocType",
  "name": "Role Template",
  "module": "Dartwing Core",
  "autoname": "field:role_name",
  "naming_rule": "By fieldname",
  "field_order": [
    "role_name",
    "applies_to_org_type",
    "column_break_1",
    "is_supervisor",
    "section_break_company",
    "default_hourly_rate"
  ],
  "fields": [
    {
      "fieldname": "role_name",
      "fieldtype": "Data",
      "label": "Role Name",
      "reqd": 1,
      "unique": 1,
      "in_list_view": 1,
      "in_standard_filter": 1
    },
    {
      "fieldname": "applies_to_org_type",
      "fieldtype": "Select",
      "label": "Applies To Organization Type",
      "options": "Family\nCompany\nNonprofit\nAssociation",
      "reqd": 1,
      "in_list_view": 1,
      "in_standard_filter": 1
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "is_supervisor",
      "fieldtype": "Check",
      "label": "Is Supervisor",
      "default": "0",
      "in_list_view": 1,
      "description": "Role has supervisory permissions"
    },
    {
      "fieldname": "section_break_company",
      "fieldtype": "Section Break",
      "label": "Employment Settings",
      "depends_on": "eval:doc.applies_to_org_type!='Family'",
      "collapsible": 1
    },
    {
      "fieldname": "default_hourly_rate",
      "fieldtype": "Currency",
      "label": "Default Hourly Rate",
      "depends_on": "eval:doc.applies_to_org_type!='Family'",
      "description": "Default hourly rate for this role"
    }
  ],
  "permissions": [
    {
      "role": "System Manager",
      "read": 1,
      "write": 1,
      "create": 1,
      "delete": 1,
      "export": 1,
      "report": 1
    },
    {
      "role": "Dartwing User",
      "read": 1
    }
  ],
  "track_changes": 1,
  "sort_field": "role_name",
  "sort_order": "ASC"
}
```
