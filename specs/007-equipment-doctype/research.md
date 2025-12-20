# Research: Equipment DocType

**Feature**: 007-equipment-doctype
**Date**: 2025-12-14

## Overview

This document consolidates research findings for implementing the Equipment DocType as a polymorphic asset management entity in Dartwing. Equipment is linked to Organization (not concrete types) enabling all organization types to track their assets.

---

## 1. DocType Module Placement

### Decision
Place Equipment and its child tables in `dartwing_core` module, not a separate module.

### Rationale
- Architecture doc Section 3.11 explicitly lists Equipment under `dartwing_core` module
- Equipment is a generic utility across all organization types (Family, Company, Nonprofit, Association)
- Unlike Company which has domain-specific legal/tax concerns, Equipment is a simple asset tracker
- Child tables (Equipment Document, Equipment Maintenance) are Equipment-specific, not shared

### Alternatives Considered
1. **Separate dartwing_assets module** - Rejected: Over-engineering for a single doctype; no other asset-related doctypes planned
2. **In dartwing_company** - Rejected: Equipment isn't company-specific; families and nonprofits also have equipment

### Implementation
```
dartwing/
├── dartwing_core/
│   └── doctype/
│       ├── equipment/
│       ├── equipment_document/
│       └── equipment_maintenance/
```

---

## 2. Naming Series Pattern

### Decision
Use `EQ-.#####` naming series for Equipment, following established patterns.

### Rationale
- Consistent with existing patterns: Family (`FAM-.#####`), Company (`CO-.#####`)
- Two-letter prefix `EQ` is clear and concise
- Five-digit suffix supports up to 99,999 equipment items per instance

### Alternatives Considered
1. **EQUIP-.####** - Rejected: Longer prefix, no added clarity
2. **Hash autoname** - Rejected: Less human-readable for support/debugging
3. **Field-based autoname** - Rejected: Equipment names aren't unique

### Implementation
```json
{
  "autoname": "naming_series:",
  "fields": [
    {
      "fieldname": "naming_series",
      "fieldtype": "Select",
      "options": "EQ-.#####",
      "default": "EQ-.#####",
      "hidden": 1
    }
  ]
}
```

---

## 3. Permission Inheritance Strategy

### Decision
Use `user_permission_dependant_doctype` pointing to Organization, plus a permission query hook for list filtering.

### Rationale
- Established pattern from Company DocType (Feature 6)
- Architecture doc Section 8.2.1 specifies this exact approach
- Equipment links to Organization; User Permissions on Organization automatically filter Equipment
- No need for Equipment-specific User Permissions

### Alternatives Considered
1. **Direct User Permission on Equipment** - Rejected: Would require permission management per equipment item
2. **Role-based only** - Rejected: Doesn't provide organization-level isolation

### Implementation
In `equipment.json`:
```json
{
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1}
  ],
  "user_permission_dependant_doctype": "Organization"
}
```

Plus permission hook in `dartwing/permissions/equipment.py`:
```python
def get_permission_query_conditions(user):
    """Filter Equipment list by user's accessible Organizations."""
    if "System Manager" in frappe.get_roles(user):
        return ""

    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value"
    )

    if not orgs:
        return "1=0"

    org_list = ", ".join(f"'{o}'" for o in orgs)
    return f"`tabEquipment`.`owner_organization` IN ({org_list})"
```

---

## 4. Serial Number Uniqueness

### Decision
Enforce global uniqueness of serial numbers across all equipment, not per-organization.

### Rationale
- Spec FR-002 states: "System MUST enforce uniqueness of serial numbers"
- Edge case in spec confirms: "Serial numbers should be globally unique to prevent confusion in multi-tenant scenarios"
- Global uniqueness is safer for asset tracking across the platform

### Alternatives Considered
1. **Per-organization uniqueness** - Rejected: Same physical asset could be transferred between orgs
2. **No uniqueness** - Rejected: Defeats purpose of serial number tracking

### Implementation
In `equipment.json`:
```json
{
  "fieldname": "serial_number",
  "label": "Serial Number",
  "fieldtype": "Data",
  "unique": 1
}
```

Note: Frappe's `unique: 1` creates a database unique index. Empty values are treated as NULL and don't violate uniqueness (allowing equipment without serial numbers).

---

## 5. Organization Deletion Protection

### Decision
Add hook to prevent Organization deletion when Equipment exists, following the clarified spec.

### Rationale
- Spec clarification states: "Block deletion - Organization cannot be deleted while equipment exists"
- Prevents orphaned equipment records
- Aligns with data integrity principle

### Alternatives Considered
1. **Cascade delete** - Rejected per spec clarification
2. **Orphan with flag** - Rejected per spec clarification

### Implementation
Add to Organization's `on_trash` or `before_delete` hook in `organization.py`:
```python
def validate_no_equipment(self):
    """Prevent deletion if equipment exists."""
    equipment_count = frappe.db.count("Equipment", {"owner_organization": self.name})
    if equipment_count > 0:
        frappe.throw(
            _("Cannot delete Organization with {0} equipment item(s). "
              "Transfer or delete equipment first.").format(equipment_count)
        )
```

---

## 6. Org Member Removal Protection

### Decision
Add hook to prevent Org Member deactivation/deletion when Person has assigned equipment.

### Rationale
- Spec clarification states: "Block removal - Prevent person removal from org while equipment is assigned"
- Ensures equipment always has valid assignee reference
- Forces explicit equipment reassignment before member removal

### Alternatives Considered
1. **Auto-clear assignment** - Rejected per spec clarification
2. **Flag for review** - Rejected per spec clarification

### Implementation
Add to Org Member's `on_trash` and status change hooks:
```python
def validate_no_equipment_assignments(doc):
    """Prevent removal if person has assigned equipment in this org."""
    equipment_count = frappe.db.count("Equipment", {
        "owner_organization": doc.organization,
        "assigned_to": doc.person
    })
    if equipment_count > 0:
        frappe.throw(
            _("Cannot remove Org Member with {0} assigned equipment item(s). "
              "Reassign equipment first.").format(equipment_count)
        )
```

---

## 7. Assigned Person Validation

### Decision
Validate that `assigned_to` Person is an active member of the equipment's `owner_organization`.

### Rationale
- Spec FR-010: "System MUST validate that assigned person is a member of the same organization as the equipment"
- Prevents assignment to people outside the organization
- Uses existing Org Member doctype for validation

### Alternatives Considered
1. **No validation** - Rejected: Could assign to anyone in the system
2. **Filter in Link field only** - Rejected: Doesn't prevent API/import bypass

### Implementation
In `equipment.py` validate method:
```python
def validate(self):
    if self.assigned_to:
        is_member = frappe.db.exists("Org Member", {
            "organization": self.owner_organization,
            "person": self.assigned_to,
            "status": "Active"
        })
        if not is_member:
            frappe.throw(
                _("Assigned person {0} must be an active member of organization {1}").format(
                    self.assigned_to, self.owner_organization
                )
            )
```

---

## 8. Equipment Type Categories

### Decision
Use Select field with predefined categories: Vehicle, Electronics, Furniture, Machinery, Tools, Other.

### Rationale
- Spec FR-011: "System MUST support equipment categorization by type"
- Predefined list ensures consistent categorization
- "Other" allows flexibility for edge cases

### Alternatives Considered
1. **Link to separate DocType** - Rejected: Over-engineering for simple categorization
2. **Free-form text** - Rejected: Would create inconsistent data

### Implementation
```json
{
  "fieldname": "equipment_type",
  "label": "Equipment Type",
  "fieldtype": "Select",
  "options": "\nVehicle\nElectronics\nFurniture\nMachinery\nTools\nOther"
}
```

---

## 9. Equipment Status Values

### Decision
Use Select field with five values: Active, In Repair, Retired, Lost, Stolen.

### Rationale
- Spec FR-006: "System MUST support equipment status values: Active, In Repair, and Retired"
- Simple lifecycle model covers most use cases
- Default to "Active" for new equipment

### Alternatives Considered
1. **More granular statuses** - Rejected: Adds complexity without clear benefit
2. **Link to status doctype** - Rejected: Over-engineering

### Implementation
```json
{
  "fieldname": "status",
  "label": "Status",
  "fieldtype": "Select",
  "default": "Active",
  "options": "Active\nIn Repair\nRetired"
}
```

---

## 10. Child Table: Equipment Document

### Decision
Create `Equipment Document` as a child table with document type label and file attachment.

### Rationale
- Spec FR-007: "System MUST allow multiple documents to be attached to equipment with type labels"
- Child table pattern consistent with architecture doc Section 3.13

### Alternatives Considered
1. **Frappe's native attachments** - Rejected: Doesn't support type labels
2. **Separate linked doctype** - Rejected: Adds complexity; child table is simpler

### Implementation
```json
{
  "doctype": "Equipment Document",
  "istable": 1,
  "module": "Dartwing Core",
  "fields": [
    {
      "fieldname": "document_type",
      "label": "Document Type",
      "fieldtype": "Select",
      "options": "Manual\nWarranty\nReceipt\nInspection Report\nOther"
    },
    {
      "fieldname": "file",
      "label": "File",
      "fieldtype": "Attach"
    }
  ]
}
```

---

## 11. Child Table: Equipment Maintenance

### Decision
Create `Equipment Maintenance` as a child table with task, frequency, and next due date.

### Rationale
- Spec FR-008: "System MUST allow maintenance tasks to be scheduled with frequency and next due date"
- Architecture doc Section 3.14 provides the exact pattern

### Alternatives Considered
1. **Separate Maintenance Schedule doctype** - Rejected: Over-engineering for simple scheduling
2. **Integration with ToDo/Task** - Rejected: Maintenance is equipment-specific, not general task

### Implementation
```json
{
  "doctype": "Equipment Maintenance",
  "istable": 1,
  "module": "Dartwing Core",
  "fields": [
    {
      "fieldname": "task",
      "label": "Task",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "frequency",
      "label": "Frequency",
      "fieldtype": "Select",
      "options": "Daily\nWeekly\nMonthly\nQuarterly\nYearly"
    },
    {
      "fieldname": "next_due",
      "label": "Next Due",
      "fieldtype": "Date"
    }
  ]
}
```

---

## 12. Address Integration

### Decision
Use standard Frappe Link field to the built-in `Address` DocType.

### Rationale
- Spec FR-005: "System MUST allow equipment to be linked to an Address for location tracking"
- Frappe ships with Address DocType
- Consistent with Company DocType's address handling

### Alternatives Considered
1. **Embedded address fields** - Rejected: Violates normalization
2. **Custom Location doctype** - Rejected: Unnecessary; Address is sufficient

### Implementation
```json
{
  "fieldname": "current_location",
  "label": "Current Location",
  "fieldtype": "Link",
  "options": "Address"
}
```

---

## Summary of Key Decisions

| Topic | Decision |
|-------|----------|
| Module location | `dartwing_core` module (not separate module) |
| Naming series | `EQ-.#####` |
| Permission model | `user_permission_dependant_doctype` on Organization |
| Serial number | Globally unique (database constraint) |
| Org deletion | Block if equipment exists |
| Member removal | Block if equipment assigned |
| Assigned person | Validate is active Org Member |
| Equipment type | Select field with 6 options |
| Status | Select with Active/In Repair/Retired |
| Documents | Child table `Equipment Document` |
| Maintenance | Child table `Equipment Maintenance` |
| Location | Link to standard Address DocType |
