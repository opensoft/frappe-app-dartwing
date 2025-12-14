# Data Model: Org Member DocType

**Feature**: 003-org-member-doctype
**Date**: 2025-12-12

## Entity Overview

The Org Member DocType establishes the membership relationship between a Person and an Organization, with an assigned Role Template.

```
┌─────────────┐       ┌─────────────┐       ┌─────────────────┐
│   Person    │       │  Org Member │       │  Organization   │
│             │ 1   n │             │ n   1 │                 │
│ PERSON-XXX  │◄──────┤ (hash name) ├──────►│   ORG-XXX       │
│             │       │             │       │                 │
└─────────────┘       └──────┬──────┘       └─────────────────┘
                             │
                             │ n   1
                             ▼
                      ┌─────────────────┐
                      │  Role Template  │
                      │                 │
                      │  (role_name)    │
                      └─────────────────┘
```

## Org Member DocType Definition

### Basic Configuration

| Property | Value |
|----------|-------|
| DocType Name | Org Member |
| Module | Dartwing Core |
| Naming Rule | Random (hash) |
| Track Changes | Yes |
| Allow Rename | No |
| Engine | InnoDB |

### Fields

| Field Name | Field Type | Options | Required | Unique | Default | Description |
|------------|------------|---------|----------|--------|---------|-------------|
| **Core References** |
| person | Link | Person | Yes | No | - | Reference to Person document |
| organization | Link | Organization | Yes | No | - | Reference to Organization document |
| role | Link | Role Template | Yes | No | - | Assigned role within the organization |
| **Status & Dates** |
| status | Select | Active\nInactive\nPending | Yes | No | Active | Current membership status |
| start_date | Date | - | No | No | (today) | Date membership began |
| end_date | Date | - | No | No | - | Date membership ended (if applicable) |
| **Display Fields** |
| member_name | Data | - | No | No | - | Read-only computed: Person's full_name |
| organization_name | Data | - | No | No | - | Read-only computed: Organization's org_name |
| organization_type | Data | - | No | No | - | Read-only fetched: Organization's org_type |

### Field Details

#### Section: Member Information

```json
{
  "fieldname": "section_member",
  "fieldtype": "Section Break",
  "label": "Member Information"
}
```

#### person (Link)

```json
{
  "fieldname": "person",
  "fieldtype": "Link",
  "options": "Person",
  "label": "Person",
  "reqd": 1,
  "in_list_view": 1,
  "in_standard_filter": 1
}
```

#### organization (Link)

```json
{
  "fieldname": "organization",
  "fieldtype": "Link",
  "options": "Organization",
  "label": "Organization",
  "reqd": 1,
  "in_list_view": 1,
  "in_standard_filter": 1
}
```

#### role (Link with Dynamic Filter)

```json
{
  "fieldname": "role",
  "fieldtype": "Link",
  "options": "Role Template",
  "label": "Role",
  "reqd": 1,
  "in_list_view": 1,
  "in_standard_filter": 1,
  "description": "Role must match organization type"
}
```

**Note**: Role filtering by org_type handled via `get_query` in JavaScript or validate() in Python.

#### Section: Status

```json
{
  "fieldname": "section_status",
  "fieldtype": "Section Break",
  "label": "Status"
}
```

#### status (Select)

```json
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Active\nInactive\nPending",
  "default": "Active",
  "reqd": 1,
  "in_list_view": 1,
  "in_standard_filter": 1
}
```

#### start_date (Date)

```json
{
  "fieldname": "start_date",
  "fieldtype": "Date",
  "label": "Start Date",
  "description": "Date membership began (defaults to today)"
}
```

#### end_date (Date)

```json
{
  "fieldname": "end_date",
  "fieldtype": "Date",
  "label": "End Date",
  "description": "Date membership ended (optional)"
}
```

#### Section: Display (Read-only)

```json
{
  "fieldname": "section_display",
  "fieldtype": "Section Break",
  "label": "Display",
  "collapsible": 1
}
```

#### member_name (Computed)

```json
{
  "fieldname": "member_name",
  "fieldtype": "Data",
  "label": "Member Name",
  "read_only": 1,
  "fetch_from": "person.full_name"
}
```

#### organization_name (Computed)

```json
{
  "fieldname": "organization_name",
  "fieldtype": "Data",
  "label": "Organization Name",
  "read_only": 1,
  "fetch_from": "organization.org_name"
}
```

#### organization_type (Fetched)

```json
{
  "fieldname": "organization_type",
  "fieldtype": "Data",
  "label": "Organization Type",
  "read_only": 1,
  "fetch_from": "organization.org_type"
}
```

### Validation Rules

| Rule ID | Field(s) | Validation | Error Message |
|---------|----------|------------|---------------|
| V-001 | person, organization | Unique combination (regardless of status) | "Person is already a member of this organization" |
| V-002 | role, organization | Role's applies_to_org_type must match Organization's org_type | "Role '{role}' is not valid for {org_type} organizations" |
| V-003 | status | If changing to Inactive, check not last supervisor | "Cannot deactivate: at least one supervisor must remain" |
| V-004 | start_date | Default to today if not provided on insert | - |
| V-005 | end_date | Must be >= start_date if provided | "End date cannot be before start date" |

### State Transitions

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
                    ▼                                          │
┌─────────┐    ┌────────┐    ┌──────────┐                     │
│ Pending │───►│ Active │───►│ Inactive │─────────────────────┘
└─────────┘    └────────┘    └──────────┘
     │              ▲              │
     │              │              │
     └──────────────┴──────────────┘
            (reactivation)
```

- **Pending → Active**: Invitation accepted or admin activates
- **Active → Inactive**: Member removed/deactivated (with end_date)
- **Inactive → Active**: Member reactivated (clears end_date, updates start_date)
- **Pending → Inactive**: Invitation declined/expired

### Permissions

| Role | Read | Write | Create | Delete | Export | Report |
|------|------|-------|--------|--------|--------|--------|
| System Manager | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Dartwing User | ✅ | ❌ | ❌ | ❌ | ✅ | ✅ |

**Note**: Write/Create operations for Dartwing User handled via whitelisted API methods with additional business logic validation.

### Indexes

| Index Name | Fields | Type | Purpose |
|------------|--------|------|---------|
| idx_person_org | person, organization | UNIQUE | Enforce (Person, Organization) uniqueness |
| idx_organization | organization | INDEX | Fast member list queries |
| idx_person | person | INDEX | Fast organization list for person |
| idx_status | status | INDEX | Filter by membership status |

## Related DocType Changes

### Person DocType

**Change**: Add doc_events hook for soft-cascade on deletion

```python
# In hooks.py doc_events
"Person": {
    "on_trash": "dartwing.dartwing_core.doctype.org_member.org_member.handle_person_deletion"
}
```

### Organization DocType

**Change**: Standard Link cascade behavior handles Org Member cleanup on Organization deletion. No additional hooks needed as Frappe's default behavior deletes linked documents.

### Role Template DocType

**Change**: None - existing `on_trash` hook already checks for linked Org Members.
