# Quickstart: Equipment DocType

**Feature**: 007-equipment-doctype
**Date**: 2025-12-14

## Prerequisites

Before implementing this feature, ensure:

1. **Feature 1 (Person DocType)** is implemented - Required for `assigned_to` field
2. **Feature 5 (User Permission Propagation)** is implemented - Required for Organization-based filtering
3. **Organization DocType** exists with hybrid architecture
4. You're on a Frappe 15.x bench with Python 3.11+

## Quick Implementation Steps

### 1. Create Child Tables First

Create the child tables before the main Equipment doctype:

```bash
# From bench directory
cd apps/dartwing

# Create Equipment Document child table
mkdir -p dartwing/dartwing_core/doctype/equipment_document
touch dartwing/dartwing_core/doctype/equipment_document/__init__.py

# Create Equipment Maintenance child table
mkdir -p dartwing/dartwing_core/doctype/equipment_maintenance
touch dartwing/dartwing_core/doctype/equipment_maintenance/__init__.py

# Create main Equipment doctype
mkdir -p dartwing/dartwing_core/doctype/equipment
touch dartwing/dartwing_core/doctype/equipment/__init__.py
```

### 2. Create DocType JSON Files

**Equipment Document** (`equipment_document.json`):
```json
{
  "doctype": "DocType",
  "name": "Equipment Document",
  "module": "Dartwing Core",
  "istable": 1,
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

**Equipment Maintenance** (`equipment_maintenance.json`):
```json
{
  "doctype": "DocType",
  "name": "Equipment Maintenance",
  "module": "Dartwing Core",
  "istable": 1,
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

**Equipment** (`equipment.json`):
```json
{
  "doctype": "DocType",
  "name": "Equipment",
  "module": "Dartwing Core",
  "autoname": "naming_series:",
  "fields": [
    {
      "fieldname": "naming_series",
      "fieldtype": "Select",
      "options": "EQ-.#####",
      "default": "EQ-.#####",
      "hidden": 1
    },
    {
      "fieldname": "equipment_name",
      "label": "Equipment Name",
      "fieldtype": "Data",
      "reqd": 1
    },
    {
      "fieldname": "equipment_type",
      "label": "Equipment Type",
      "fieldtype": "Select",
      "options": "\nVehicle\nElectronics\nFurniture\nMachinery\nTools\nOther"
    },
    {
      "fieldname": "serial_number",
      "label": "Serial Number",
      "fieldtype": "Data",
      "unique": 1
    },
    {
      "fieldname": "column_break_1",
      "fieldtype": "Column Break"
    },
    {
      "fieldname": "status",
      "label": "Status",
      "fieldtype": "Select",
      "default": "Active",
      "options": "Active\nIn Repair\nRetired"
    },
    {
      "fieldname": "owner_organization",
      "label": "Owner Organization",
      "fieldtype": "Link",
      "options": "Organization",
      "reqd": 1
    },
    {
      "fieldname": "assigned_to",
      "label": "Assigned To",
      "fieldtype": "Link",
      "options": "Person"
    },
    {
      "fieldname": "section_location",
      "fieldtype": "Section Break",
      "label": "Location"
    },
    {
      "fieldname": "current_location",
      "label": "Current Location",
      "fieldtype": "Link",
      "options": "Address"
    },
    {
      "fieldname": "section_documents",
      "fieldtype": "Section Break",
      "label": "Documents"
    },
    {
      "fieldname": "documents",
      "label": "Documents",
      "fieldtype": "Table",
      "options": "Equipment Document"
    },
    {
      "fieldname": "section_maintenance",
      "fieldtype": "Section Break",
      "label": "Maintenance Schedule"
    },
    {
      "fieldname": "maintenance_schedule",
      "label": "Maintenance Schedule",
      "fieldtype": "Table",
      "options": "Equipment Maintenance"
    }
  ],
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "create": 1}
  ],
  "user_permission_dependant_doctype": "Organization"
}
```

### 3. Create Python Controller

**`equipment.py`**:
```python
import frappe
from frappe import _
from frappe.model.document import Document


class Equipment(Document):
    def validate(self):
        self.validate_assigned_person()

    def validate_assigned_person(self):
        """Ensure assigned_to is an active Org Member of owner_organization."""
        if not self.assigned_to:
            return

        is_member = frappe.db.exists("Org Member", {
            "organization": self.owner_organization,
            "person": self.assigned_to,
            "status": "Active"
        })

        if not is_member:
            frappe.throw(
                _("Assigned person {0} must be an active member of {1}").format(
                    self.assigned_to, self.owner_organization
                )
            )


@frappe.whitelist()
def get_org_members(doctype, txt, searchfield, start, page_len, filters):
    """Get Person records who are active Org Members of specified organization."""
    organization = filters.get("organization")
    if not organization:
        return []

    return frappe.db.sql("""
        SELECT p.name, CONCAT(p.first_name, ' ', IFNULL(p.last_name, '')) as description
        FROM `tabPerson` p
        INNER JOIN `tabOrg Member` om ON om.person = p.name
        WHERE om.organization = %s
          AND om.status = 'Active'
          AND (p.name LIKE %s OR p.first_name LIKE %s OR p.last_name LIKE %s)
        ORDER BY p.first_name
        LIMIT %s, %s
    """, (organization, f"%{txt}%", f"%{txt}%", f"%{txt}%", start, page_len))
```

### 4. Add Permission Hook

**`dartwing/permissions/equipment.py`**:
```python
import frappe


def get_permission_query_conditions(user):
    """Filter Equipment list by user's accessible Organizations."""
    if not user:
        user = frappe.session.user

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


def has_permission(doc, ptype, user):
    """Check if user has permission on specific Equipment record."""
    if not user:
        user = frappe.session.user

    if "System Manager" in frappe.get_roles(user):
        return True

    return frappe.db.exists("User Permission", {
        "user": user,
        "allow": "Organization",
        "for_value": doc.owner_organization
    })
```

### 5. Register in hooks.py

Add to `permission_query_conditions`:
```python
permission_query_conditions = {
    # ... existing entries ...
    "Equipment": "dartwing.permissions.equipment.get_permission_query_conditions",
}

has_permission = {
    # ... existing entries ...
    "Equipment": "dartwing.permissions.equipment.has_permission",
}
```

### 6. Add Deletion Protection Hooks

Update `organization.py` to check for equipment:
```python
def on_trash(self):
    """Delete linked concrete type and validate no equipment."""
    self.validate_no_equipment()
    self.delete_concrete_type()

def validate_no_equipment(self):
    """Prevent deletion if equipment exists."""
    equipment_count = frappe.db.count("Equipment", {"owner_organization": self.name})
    if equipment_count > 0:
        frappe.throw(
            _("Cannot delete Organization with {0} equipment item(s). "
              "Transfer or delete equipment first.").format(equipment_count)
        )
```

Update Org Member hooks to check for equipment assignments:
```python
# In org_member.py or permissions/helpers.py
def validate_no_equipment_assignments(doc):
    """Prevent removal if person has assigned equipment."""
    equipment_count = frappe.db.count("Equipment", {
        "owner_organization": doc.organization,
        "assigned_to": doc.person
    })
    if equipment_count > 0:
        frappe.throw(
            _("Cannot remove Org Member with {0} assigned equipment. "
              "Reassign equipment first.").format(equipment_count)
        )
```

### 7. Run Migrations

```bash
# From bench directory
bench --site yoursite.local migrate
```

## Testing

### Manual Test Checklist

1. **Create Equipment**
   - Create equipment with all fields
   - Verify serial number uniqueness
   - Verify equipment_name is required

2. **Permission Test**
   - Log in as non-System Manager user
   - Verify only equipment from user's organizations visible
   - Verify cannot create equipment for unauthorized organization

3. **Assignment Validation**
   - Try assigning to person not in organization (should fail)
   - Try assigning to active Org Member (should succeed)

4. **Deletion Protection**
   - Try deleting Organization with equipment (should fail)
   - Try removing Org Member with assigned equipment (should fail)

### Automated Tests

Run the test suite:
```bash
bench --site yoursite.local run-tests --module dartwing --doctype Equipment
```

## API Usage Examples

### Create Equipment
```bash
curl -X POST \
  'http://yoursite.local/api/resource/Equipment' \
  -H 'Authorization: token api_key:api_secret' \
  -H 'Content-Type: application/json' \
  -d '{
    "equipment_name": "Forklift #1",
    "equipment_type": "Machinery",
    "serial_number": "FL-2024-001",
    "owner_organization": "ORG-2025-00001",
    "status": "Active"
  }'
```

### List Equipment by Organization
```bash
curl -X GET \
  'http://yoursite.local/api/resource/Equipment?filters=[["owner_organization","=","ORG-2025-00001"]]' \
  -H 'Authorization: token api_key:api_secret'
```

### Assign Equipment to Person
```bash
curl -X PUT \
  'http://yoursite.local/api/resource/Equipment/EQ-00001' \
  -H 'Authorization: token api_key:api_secret' \
  -H 'Content-Type: application/json' \
  -d '{
    "assigned_to": "PER-00001"
  }'
```

## Common Issues

### "Permission denied" on equipment list
- Check that user has User Permission for the Organization
- Verify user has "Dartwing User" role

### "Assigned person must be an active member"
- Verify the Person has an active Org Member record for the organization
- Check Org Member status is "Active" not "Pending" or "Inactive"

### Serial number uniqueness error
- Serial numbers are globally unique across all equipment
- Check if serial number exists with another equipment record
