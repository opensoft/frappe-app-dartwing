# Data Model: Equipment DocType

**Feature**: 007-equipment-doctype
**Date**: 2025-12-14

## Entity Relationship Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              Organization                                │
│  ┌───────────┬──────────┬────────┬──────────────┬─────────────────┐     │
│  │ org_name  │ org_type │ status │ linked_doctype│ linked_name    │     │
│  │ "Acme"    │ Company  │ Active │ Company       │ CO-00001       │     │
│  └───────────┴──────────┴────────┴──────────────┴─────────────────┘     │
└─────────────────────────────────┬───────────────────────────────────────┘
                                  │ 1:N (polymorphic)
                                  ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                               Equipment                                  │
│  ┌────────────────┬────────────────┬─────────────┬──────────────────┐   │
│  │owner_organization│equipment_name│serial_number│ status           │   │
│  │ ORG-2025-1       │ Forklift #1  │ FL-123456   │ Active           │   │
│  └────────────────┴────────────────┴─────────────┴──────────────────┘   │
│                                                                          │
│  Links:                                                                  │
│  ┌──────────────────┐  ┌─────────────────────────────────────────────┐  │
│  │ assigned_to      │  │ current_location                            │  │
│  │ → Person         │  │ → Address                                   │  │
│  └──────────────────┘  └─────────────────────────────────────────────┘  │
│                                                                          │
│  Child Tables:                                                           │
│  ┌──────────────────────────┐  ┌─────────────────────────────────────┐  │
│  │  documents (Table)       │  │  maintenance_schedule (Table)       │  │
│  │  → Equipment Document    │  │  → Equipment Maintenance            │  │
│  └──────────────────────────┘  └─────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────┐   ┌─────────────────────────────────┐
│     Equipment Document              │   │     Equipment Maintenance       │
│     (Child Table - istable: 1)      │   │     (Child Table - istable: 1)  │
├─────────────────────────────────────┤   ├─────────────────────────────────┤
│ document_type → Select              │   │ task       → Data (reqd)        │
│ file          → Attach              │   │ frequency  → Select             │
└─────────────────────────────────────┘   │ next_due   → Date               │
                                          └─────────────────────────────────┘

┌─────────────────────────────────────┐   ┌─────────────────────────────────┐
│           Person                    │   │           Address               │
│        (Link target)                │   │        (Link target)            │
├─────────────────────────────────────┤   ├─────────────────────────────────┤
│ name          (primary key)         │   │ name          (primary key)     │
│ first_name, last_name               │   │ address_line1                   │
│ primary_email                       │   │ city, state, country            │
└─────────────────────────────────────┘   └─────────────────────────────────┘
```

---

## Entity: Equipment

**Module**: Dartwing Core
**Naming**: `EQ-.#####` (naming_series)
**Parent**: Organization (via `owner_organization` Link field)

### Fields

| Field Name | Type | Required | Unique | Options/Default | Description |
|------------|------|----------|--------|-----------------|-------------|
| naming_series | Select | Yes | - | `EQ-.#####` | Auto-naming series (hidden) |
| **Basic Information** |
| equipment_name | Data | Yes | - | - | Display name for the equipment |
| equipment_type | Select | No | - | See options below | Category classification |
| serial_number | Data | No | Yes | - | Manufacturer serial number (globally unique) |
| status | Select | No | - | Active | Operational status |
| **Organization & Assignment** |
| owner_organization | Link | Yes | - | Organization | Owning organization (required) |
| assigned_to | Link | No | - | Person | Person responsible for equipment |
| **Location** |
| current_location | Link | No | - | Address | Physical location of equipment |
| **Documents** |
| documents | Table | No | - | Equipment Document | Attached documents |
| **Maintenance** |
| maintenance_schedule | Table | No | - | Equipment Maintenance | Scheduled maintenance tasks |

### Equipment Type Options

```
(empty)
Vehicle
Electronics
Furniture
Machinery
Tools
Other
```

### Status Options

```
Active
In Repair
Retired
Lost
Stolen
```

### Permissions

| Role | Read | Write | Create | Delete |
|------|------|-------|--------|--------|
| System Manager | Yes | Yes | Yes | Yes |
| Dartwing User | Yes | Yes | Yes | No |

**Permission Dependency**: `user_permission_dependant_doctype = "Organization"`

### Validation Rules

1. **equipment_name** is required
2. **owner_organization** is required
3. **serial_number** must be globally unique if provided (database constraint)
4. **assigned_to** must be an active Org Member of the `owner_organization`
5. **status** defaults to "Active" on creation

### Link Field Filters

For the `assigned_to` field, filter to show only Persons who are active members of the selected organization:

```python
# In equipment.js (client script)
frappe.ui.form.on("Equipment", {
    owner_organization: function(frm) {
        frm.set_query("assigned_to", function() {
            return {
                query: "dartwing.dartwing_core.doctype.equipment.equipment.get_org_members",
                filters: {
                    organization: frm.doc.owner_organization
                }
            };
        });
    }
});
```

---

## Entity: Equipment Document (Child Table)

**Module**: Dartwing Core
**Type**: Child Table (`istable: 1`)
**Used By**: Equipment

### Fields

| Field Name | Type | Required | Options | Description |
|------------|------|----------|---------|-------------|
| document_type | Select | No | See options below | Classification of document |
| file | Attach | No | - | The attached file |

### Document Type Options

```
Manual
Warranty
Receipt
Inspection Report
Other
```

### Validation Rules

1. At least one of `document_type` or `file` should be provided (soft recommendation)

---

## Entity: Equipment Maintenance (Child Table)

**Module**: Dartwing Core
**Type**: Child Table (`istable: 1`)
**Used By**: Equipment

### Fields

| Field Name | Type | Required | Options | Description |
|------------|------|----------|---------|-------------|
| task | Data | Yes | - | Description of maintenance task |
| frequency | Select | No | See options below | How often task should be performed |
| next_due | Date | No | - | Next scheduled date for task |

### Frequency Options

```
Daily
Weekly
Monthly
Quarterly
Yearly
```

### Validation Rules

1. `task` is required
2. `next_due` should be in the future (soft validation - warning only)

---

## Relationships Summary

| From | To | Cardinality | Field | Description |
|------|----|-------------|-------|-------------|
| Equipment | Organization | N:1 | owner_organization | Organization that owns the equipment |
| Equipment | Person | 0..1 | assigned_to | Person responsible for equipment |
| Equipment | Address | 0..1 | current_location | Physical location |
| Equipment | Equipment Document | 1:N | documents | Child table |
| Equipment | Equipment Maintenance | 1:N | maintenance_schedule | Child table |

---

## Index Recommendations

For the Equipment DocType, Frappe will auto-create indexes on:
- `owner_organization` (Link field)
- `assigned_to` (Link field)
- `serial_number` (unique constraint)
- `name` (primary key)

Consider adding explicit indexes if query patterns emerge:
- `status` (if filtering by status is common in list views)
- `equipment_type` (if filtering by type is common)

---

## Deletion Behavior

### Equipment Deletion
- Standard Frappe deletion
- Child tables (Equipment Document, Equipment Maintenance) cascade delete automatically

### Organization Deletion (Blocked)
- Equipment validates Organization `on_trash` hook
- Throws error: "Cannot delete Organization with {N} equipment item(s)"
- User must transfer or delete equipment first

### Org Member Deletion (Blocked when equipment assigned)
- Equipment validates Org Member `on_trash` hook
- Throws error: "Cannot remove Org Member with {N} assigned equipment item(s)"
- User must reassign equipment first

---

## Migration Notes

### New Tables Created

1. `tabEquipment` - Main Equipment doctype
2. `tabEquipment Document` - Child table for documents
3. `tabEquipment Maintenance` - Child table for maintenance

### Updates to Existing Tables

1. None - Equipment is a new entity

### Updates to Existing Code

1. `organization.py` - Add equipment existence check in deletion flow
2. `permissions/helpers.py` or `org_member.py` - Add equipment assignment check
3. `hooks.py` - Register Equipment permission query conditions

### Fixtures Required

None for Equipment doctype itself. Role-based access uses existing Dartwing User role.
