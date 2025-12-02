# Data Model: Person DocType

**Feature Branch**: `001-person-doctype`
**Date**: 2025-12-01

## Entity Overview

```
┌─────────────────────────────────────────────────────────────┐
│                         Person                               │
│─────────────────────────────────────────────────────────────│
│ PK: name (auto-generated)                                   │
│ UK: primary_email, keycloak_user_id*, frappe_user*          │
│     (* nullable but unique when set)                        │
├─────────────────────────────────────────────────────────────┤
│ Identity                                                    │
│   primary_email     → Data (reqd, unique)                   │
│   keycloak_user_id  → Data (unique when set)                │
│   frappe_user       → Link:User (unique when set)           │
├─────────────────────────────────────────────────────────────┤
│ Personal Info                                               │
│   first_name        → Data (reqd)                           │
│   last_name         → Data (reqd)                           │
│   mobile_no         → Data (E.164 format)                   │
├─────────────────────────────────────────────────────────────┤
│ Organization                                                │
│   personal_org      → Link:Organization                     │
├─────────────────────────────────────────────────────────────┤
│ Privacy & Consent                                           │
│   is_minor          → Check                                 │
│   consent_captured  → Check                                 │
│   consent_timestamp → Datetime                              │
├─────────────────────────────────────────────────────────────┤
│ Status & Audit                                              │
│   source            → Select [signup,invite,import]         │
│   status            → Select [Active,Inactive,Merged]       │
│   user_sync_status  → Select [synced,pending,failed]        │
│   sync_error_message→ Text                                  │
│   last_sync_at      → Datetime                              │
├─────────────────────────────────────────────────────────────┤
│ Child Tables                                                │
│   merge_logs        → Table:Person Merge Log                │
└─────────────────────────────────────────────────────────────┘
         │
         │ 1:N (child table)
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Person Merge Log                          │
│─────────────────────────────────────────────────────────────│
│ PK: name (auto-generated)                                   │
│ FK: parent → Person                                         │
├─────────────────────────────────────────────────────────────┤
│   source_person     → Link:Person (reqd)                    │
│   target_person     → Link:Person (reqd)                    │
│   merged_at         → Datetime (reqd, read_only)            │
│   merged_by         → Link:User (reqd, read_only)           │
│   notes             → Small Text                            │
└─────────────────────────────────────────────────────────────┘
```

## Person DocType

### Field Definitions

| Fieldname | Fieldtype | Options | Required | Unique | Read Only | Default | Description |
|-----------|-----------|---------|----------|--------|-----------|---------|-------------|
| **Identity Section** |
| primary_email | Data | Email | Yes | Yes | No | - | Primary email address, main identifier |
| keycloak_user_id | Data | - | No | Yes* | No | - | Keycloak subject ID (nullable unique) |
| frappe_user | Link | User | No | Yes* | No | - | Link to Frappe User (nullable unique) |
| **Personal Info Section** |
| first_name | Data | - | Yes | No | No | - | First name |
| last_name | Data | - | Yes | No | No | - | Last name |
| full_name | Data | - | No | No | Yes | - | Computed: first_name + last_name |
| mobile_no | Data | Phone | No | No | No | - | Mobile number (E.164 format) |
| **Organization Section** |
| personal_org | Link | Organization | No | No | No | - | Personal/family organization |
| **Privacy Section** |
| is_minor | Check | - | No | No | No | 0 | Person is a minor |
| consent_captured | Check | - | No | No | No | 0 | Consent has been captured |
| consent_timestamp | Datetime | - | No | No | Yes | - | When consent was captured |
| **Status Section** |
| source | Select | signup\ninvite\nimport | Yes | No | No | - | How Person was created |
| status | Select | Active\nInactive\nMerged | Yes | No | No | Active | Person status |
| **Sync Status Section** |
| user_sync_status | Select | synced\npending\nfailed | No | No | Yes | - | Frappe User creation status |
| sync_error_message | Text | - | No | No | Yes | - | Last sync error message |
| last_sync_at | Datetime | - | No | No | Yes | - | Last successful sync timestamp |
| **Audit Section** |
| merge_logs | Table | Person Merge Log | No | No | Yes | - | Merge operation history |

*Nullable unique: NULL values allowed, but non-NULL values must be unique

### Field Order

```json
[
  "section_identity",
  "primary_email",
  "column_break_identity",
  "keycloak_user_id",
  "frappe_user",

  "section_personal",
  "first_name",
  "last_name",
  "full_name",
  "column_break_personal",
  "mobile_no",

  "section_organization",
  "personal_org",

  "section_privacy",
  "is_minor",
  "consent_captured",
  "consent_timestamp",

  "section_status",
  "source",
  "status",
  "column_break_status",
  "user_sync_status",
  "sync_error_message",
  "last_sync_at",

  "section_audit",
  "merge_logs"
]
```

### Validation Rules

| Rule ID | Field(s) | Validation | Error Message |
|---------|----------|------------|---------------|
| V-001 | primary_email | Unique across all Person records | "Email {0} is already in use" |
| V-002 | keycloak_user_id | Unique when set | "Keycloak User ID {0} is already linked to another Person" |
| V-003 | frappe_user | Unique when set | "Frappe User {0} is already linked to another Person" |
| V-004 | mobile_no | Valid E.164 format when set | "Invalid mobile number format" |
| V-005 | is_minor + consent_captured | Block writes if is_minor=1 and consent_captured=0 | "Cannot modify Person record for a minor until consent is captured" |
| V-006 | source | Must be one of: signup, invite, import | "Invalid source value" |
| V-007 | status | Must be one of: Active, Inactive, Merged | "Invalid status value" |

### State Transitions

```
                    ┌──────────────────────────────────────────┐
                    │                                          │
                    ▼                                          │
    ┌─────────┐   ┌─────────────┐   ┌───────────────┐          │
    │ (new)   │──▶│   Active    │──▶│   Inactive    │──────────┘
    └─────────┘   └─────────────┘   └───────────────┘
                        │                   │
                        │                   │
                        ▼                   ▼
                  ┌───────────────────────────┐
                  │         Merged            │  (terminal state)
                  └───────────────────────────┘

Allowed Transitions:
- (new) → Active: Default on creation
- Active → Inactive: Deactivate person
- Inactive → Active: Reactivate person
- Active → Merged: Merge into another person
- Inactive → Merged: Merge into another person
```

---

## Person Merge Log (Child Table)

### Field Definitions

| Fieldname | Fieldtype | Options | Required | Read Only | In List View | Description |
|-----------|-----------|---------|----------|-----------|--------------|-------------|
| source_person | Link | Person | Yes | No | Yes | Person being merged from |
| target_person | Link | Person | Yes | No | Yes | Person being merged into |
| merged_at | Datetime | - | Yes | Yes | Yes | Timestamp of merge |
| merged_by | Link | User | Yes | Yes | No | User who performed merge |
| notes | Small Text | - | No | No | No | Optional merge notes |

### Properties

```json
{
  "istable": 1,
  "track_changes": 1,
  "editable_grid": 0
}
```

---

## Relationships

### Person → User (Optional 1:1)

```
Person.frappe_user ──────────────▶ User.name
         │
         └── Constraint: Unique when set
             Behavior: Auto-create User on keycloak_user_id if enabled
```

### Person → Organization (Optional 1:1)

```
Person.personal_org ─────────────▶ Organization.name
         │
         └── Behavior: Represents person's personal/family org
```

### Person → Org Member (1:N - External)

```
Org Member.person ───────────────▶ Person.name
         │
         └── Constraint: Deletion blocked if links exist
             Behavior: Must deactivate or merge instead
```

### Person → Person Merge Log (1:N - Child Table)

```
Person.merge_logs[] ─────────────▶ Person Merge Log
         │
         └── Behavior: Audit trail of merge operations
```

---

## Indexes

| Index Name | Fields | Type | Purpose |
|------------|--------|------|---------|
| idx_primary_email | primary_email | Unique | Enforce email uniqueness |
| idx_keycloak_user_id | keycloak_user_id | Unique (nullable) | Enforce Keycloak ID uniqueness |
| idx_frappe_user | frappe_user | Unique (nullable) | Enforce User link uniqueness |
| idx_status | status | Non-unique | Filter by status |
| idx_source | source | Non-unique | Filter by source |
| idx_personal_org | personal_org | Non-unique | Query by organization |

---

## Database Schema (MariaDB)

```sql
CREATE TABLE `tabPerson` (
  `name` varchar(140) NOT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) DEFAULT NULL,
  `owner` varchar(140) DEFAULT NULL,
  `docstatus` int(1) NOT NULL DEFAULT 0,
  `idx` int(8) NOT NULL DEFAULT 0,

  -- Identity
  `primary_email` varchar(140) NOT NULL,
  `keycloak_user_id` varchar(140) DEFAULT NULL,
  `frappe_user` varchar(140) DEFAULT NULL,

  -- Personal Info
  `first_name` varchar(140) NOT NULL,
  `last_name` varchar(140) NOT NULL,
  `full_name` varchar(140) DEFAULT NULL,
  `mobile_no` varchar(140) DEFAULT NULL,

  -- Organization
  `personal_org` varchar(140) DEFAULT NULL,

  -- Privacy
  `is_minor` int(1) NOT NULL DEFAULT 0,
  `consent_captured` int(1) NOT NULL DEFAULT 0,
  `consent_timestamp` datetime(6) DEFAULT NULL,

  -- Status
  `source` varchar(140) NOT NULL,
  `status` varchar(140) NOT NULL DEFAULT 'Active',

  -- Sync Status
  `user_sync_status` varchar(140) DEFAULT NULL,
  `sync_error_message` longtext DEFAULT NULL,
  `last_sync_at` datetime(6) DEFAULT NULL,

  PRIMARY KEY (`name`),
  UNIQUE KEY `unique_primary_email` (`primary_email`),
  UNIQUE KEY `unique_keycloak_user_id` (`keycloak_user_id`),
  UNIQUE KEY `unique_frappe_user` (`frappe_user`),
  KEY `idx_status` (`status`),
  KEY `idx_source` (`source`),
  KEY `idx_personal_org` (`personal_org`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE `tabPerson Merge Log` (
  `name` varchar(140) NOT NULL,
  `creation` datetime(6) DEFAULT NULL,
  `modified` datetime(6) DEFAULT NULL,
  `modified_by` varchar(140) DEFAULT NULL,
  `owner` varchar(140) DEFAULT NULL,
  `docstatus` int(1) NOT NULL DEFAULT 0,
  `parent` varchar(140) DEFAULT NULL,
  `parentfield` varchar(140) DEFAULT NULL,
  `parenttype` varchar(140) DEFAULT NULL,
  `idx` int(8) NOT NULL DEFAULT 0,

  `source_person` varchar(140) NOT NULL,
  `target_person` varchar(140) NOT NULL,
  `merged_at` datetime(6) NOT NULL,
  `merged_by` varchar(140) NOT NULL,
  `notes` longtext DEFAULT NULL,

  PRIMARY KEY (`name`),
  KEY `parent` (`parent`),
  KEY `idx_source_person` (`source_person`),
  KEY `idx_target_person` (`target_person`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```
