# Data Model: Company DocType

**Feature**: 006-company-doctype
**Date**: 2025-12-13

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Organization                                │
│  ┌───────────┬──────────┬────────┬──────────────┬─────────────────┐     │
│  │ org_name  │ org_type │ status │ linked_doctype│ linked_name    │     │
│  │ "Acme"    │ Company  │ Active │ Company       │ CO-00001       │     │
│  └───────────┴──────────┴────────┴──────────────┴─────────────────┘     │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │ 1:1
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                               Company                                    │
│  ┌────────────┬───────────┬─────────────┬───────────────────────────┐   │
│  │organization│legal_name │ tax_id      │ entity_type               │   │
│  │ ORG-2025-1 │ Acme Inc  │ 12-3456789  │ LLC                       │   │
│  └────────────┴───────────┴─────────────┴───────────────────────────┘   │
│                                                                          │
│  Child Tables:                                                           │
│  ┌─────────────────────────┐  ┌────────────────────────────────────┐    │
│  │  officers (Table)       │  │  members_partners (Table)          │    │
│  │  → Organization Officer │  │  → Organization Member Partner     │    │
│  └─────────────────────────┘  └────────────────────────────────────┘    │
│                                                                          │
│  Links:                                                                  │
│  ┌────────────────────┐  ┌─────────────────────┐  ┌─────────────────┐   │
│  │ registered_address │  │ physical_address    │  │ registered_agent│   │
│  │ → Address          │  │ → Address           │  │ → Person        │   │
│  └────────────────────┘  └─────────────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────┐   ┌─────────────────────────────────┐
│     Organization Officer            │   │   Organization Member Partner   │
│     (Child Table - istable: 1)      │   │   (Child Table - istable: 1)    │
├─────────────────────────────────────┤   ├─────────────────────────────────┤
│ person     → Person (Link, reqd)    │   │ person           → Person (Link)│
│ title      → Data (reqd)            │   │ ownership_percent → Percent     │
│ start_date → Date                   │   │ capital_contribution → Currency │
│ end_date   → Date                   │   │ voting_rights    → Percent      │
└─────────────────────────────────────┘   └─────────────────────────────────┘
```

---

## Entity: Company

**Module**: Dartwing Company
**Naming**: `CO-.#####` (naming_series)
**Parent**: Organization (via `organization` Link field)

### Fields

| Field Name | Type | Required | Unique | Options/Default | Description |
|------------|------|----------|--------|-----------------|-------------|
| naming_series | Select | Yes | - | `CO-.#####` | Auto-naming series |
| organization | Link | Yes | - | Organization | Parent org reference (read_only) |
| **Legal Information** |
| legal_name | Data | No | - | - | Official legal entity name |
| tax_id | Data | No | - | - | Tax ID / EIN / Unified Social Credit Code |
| entity_type | Select | No | - | See options below | Legal entity classification |
| jurisdiction_country | Link | No | - | Country | Country of formation |
| jurisdiction_state | Data | No | - | - | State/Province of formation |
| formation_date | Date | No | - | - | Date of formation/incorporation |
| **Addresses** |
| registered_address | Link | No | - | Address | Legal address for service of process |
| physical_address | Link | No | - | Address | Principal/physical business address |
| registered_agent | Link | No | - | Person | Person designated as registered agent |
| **Officers & Directors** |
| officers | Table | No | - | Organization Officer | List of officers and directors |
| **Ownership (conditional)** |
| members_partners | Table | No | - | Organization Member Partner | LLC members or partnership partners |

### Entity Type Options

```
(empty)
C-Corp
S-Corp
LLC
Limited Partnership (LP)
General Partnership
LLP
WFOE (China)
Benefit Corporation
Cooperative
```

### Conditional Visibility Rules

| Section/Field | Condition |
|---------------|-----------|
| Ownership Section (`section_ownership`) | `entity_type` in ['LLC', 'Limited Partnership (LP)', 'LLP', 'General Partnership'] |

### Permissions

| Role | Read | Write | Create | Delete |
|------|------|-------|--------|--------|
| System Manager | Yes | Yes | Yes | Yes |
| Dartwing User | Yes | Yes | No | No |

**Permission Dependency**: `user_permission_dependant_doctype = "Organization"`

### Validation Rules

1. **organization** field is required and read-only (set by Organization hook)
2. **Soft validation**: If `members_partners` total ownership > 100%, display warning
3. **No hard uniqueness** constraints on tax_id (some jurisdictions don't require unique)

### State Transitions

Company doesn't have its own status field - it inherits status from parent Organization:
- Active → Inactive → Dissolved (managed on Organization)

---

## Entity: Organization Officer (Child Table)

**Module**: Dartwing Core
**Type**: Child Table (`istable: 1`)
**Used By**: Company, Nonprofit (future)

### Fields

| Field Name | Type | Required | Options | Description |
|------------|------|----------|---------|-------------|
| person | Link | Yes | Person | The individual serving as officer |
| title | Data | Yes | - | Position title (CEO, CFO, Director, etc.) |
| start_date | Date | No | - | Date position started |
| end_date | Date | No | - | Date position ended (null = current) |

### Validation Rules

1. `person` is required
2. `title` is required
3. `end_date` must be >= `start_date` if both provided

---

## Entity: Organization Member Partner (Child Table)

**Module**: Dartwing Core
**Type**: Child Table (`istable: 1`)
**Used By**: Company (LLC/Partnership), Association (future)

### Fields

| Field Name | Type | Required | Options | Description |
|------------|------|----------|---------|-------------|
| person | Link | Yes | Person | The member or partner (required) |
| ownership_percent | Percent | No | - | Percentage of ownership |
| capital_contribution | Currency | No | - | Amount of capital contributed |
| voting_rights | Percent | No | - | Percentage of voting rights |

### Validation Rules

1. `person` is required
2. `ownership_percent` should be between 0 and 100 (Frappe Percent type enforces)
3. `voting_rights` should be between 0 and 100

---

## Relationships Summary

| From | To | Cardinality | Field | Description |
|------|----|-------------|-------|-------------|
| Company | Organization | 1:1 | organization | Parent org reference |
| Company | Address | 0..1 | registered_address | Legal address |
| Company | Address | 0..1 | physical_address | Business address |
| Company | Person | 0..1 | registered_agent | Agent for legal service |
| Company | Organization Officer | 1:N | officers | Child table |
| Company | Organization Member Partner | 1:N | members_partners | Child table |
| Organization Officer | Person | N:1 | person | Officer identity |
| Organization Member Partner | Person | N:1 | person | Member identity |

---

## Index Recommendations

For the Company DocType, Frappe will auto-create indexes on:
- `organization` (Link field)
- `name` (primary key)

Consider adding explicit indexes if query patterns emerge:
- `entity_type` (if filtering by type is common)
- `jurisdiction_country` (if filtering by country is common)

---

## Migration Notes

### New Tables Created

1. `tabCompany` - Main Company doctype
2. `tabOrganization Officer` - Child table for officers
3. `tabOrganization Member Partner` - Child table for members/partners

### Updates to Existing Tables

1. `tabOrganization` - No schema changes; only Python hook logic updated

### Fixtures Required

None for Company doctype itself. Role Templates are managed separately (Feature #2).
