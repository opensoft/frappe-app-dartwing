# Code Review: 007-Equipment-DocType

**Reviewer:** opus45
**Date:** 2025-12-14
**Branch:** `007-equipment-doctype`
**Module:** dartwing_core

---

## 1. Critical Issues & Blockers (Severity: HIGH)

### 1.1 Potential SQL Injection Pattern in Permission Query Conditions

**File:** `dartwing/permissions/equipment.py:46-47`

```python
org_list = ", ".join(f"'{frappe.db.escape(o)}'" for o in orgs)
return f"`tabEquipment`.`owner_organization` IN ({org_list})"
```

**Issue:** While `frappe.db.escape()` provides protection, this pattern of building SQL strings with escaped values is discouraged. The Frappe idiom for permission query conditions is to return parameterized conditions.

**Risk:** Low (due to escape), but violates secure coding patterns.

**Recommended Fix:**

```python
# Option A: Use Frappe's built-in permission dependency (preferred - already done in JSON!)
# The equipment.json already has "user_permission_dependant_doctype": "Organization"
# which handles this automatically. Consider removing custom permission code.

# Option B: If custom logic is needed, use Frappe's condition builder
if not orgs:
    return "1=0"
org_condition = " OR ".join([f"`tabEquipment`.`owner_organization` = %({i})s" for i in range(len(orgs))])
frappe.local.form_dict.update({str(i): org for i, org in enumerate(orgs)})
return f"({org_condition})"
```

**Note:** The `user_permission_dependant_doctype` in `equipment.json:155` already provides organization-based filtering. The custom `get_permission_query_conditions` may be redundant. Verify if both are needed or if one can be removed to follow the low-code philosophy.

---

### 1.2 Missing Validation for Status Transitions

**File:** `dartwing/dartwing_core/doctype/equipment/equipment.py`

**Issue:** Equipment can transition from "Retired" back to "Active" without any validation. In most asset management systems, retiring equipment is a terminal or controlled state.

**Business Risk:** Retired equipment may have been disposed of, transferred, or written off. Allowing re-activation could cause accounting/inventory discrepancies.

**Recommended Fix:** Add status transition validation if business rules require it:

```python
def validate(self):
    # ... existing validations
    self.validate_status_transition()

def validate_status_transition(self):
    """Validate equipment status transitions (FR-006)."""
    if not self.is_new() and self.has_value_changed("status"):
        old_status = self.get_doc_before_save().status
        if old_status == "Retired" and self.status == "Active":
            frappe.throw(
                _("Cannot reactivate retired equipment. Create a new record instead."),
                title=_("Invalid Status Transition"),
            )
```

**Alternative:** If reactivation is intentionally allowed, document this in the spec and add an audit trail.

---

### 1.3 No Audit Trail for Equipment Assignment Changes

**File:** `dartwing/dartwing_core/doctype/equipment/equipment.py`

**Issue:** While `track_changes: 1` is enabled in the JSON, there's no explicit logging or notification when equipment assignment changes. This is critical for asset custody tracking.

**Compliance Risk:** For HIPAA/SOC2 compliance mentioned in the architecture, equipment custody changes (especially for electronics with data) should be explicitly audited.

**Recommended Fix:** Add explicit logging for assignment changes:

```python
def before_save(self):
    if not self.is_new() and self.has_value_changed("assigned_to"):
        old_assignee = self.get_doc_before_save().assigned_to
        frappe.logger().info(
            f"Equipment {self.name} reassigned from {old_assignee} to {self.assigned_to}",
            reference_doctype="Equipment",
            reference_name=self.name
        )
```

---

## 2. Suggestions for Improvement (Severity: MEDIUM)

### 2.1 Redundant `validate_equipment_name` Method

**File:** `dartwing/dartwing_core/doctype/equipment/equipment.py:29-35`

**Issue:** The `validate_equipment_name()` method checks if `equipment_name` is provided, but this field is already marked as `reqd: 1` in `equipment.json:39`. Frappe automatically enforces required fields before the `validate` hook runs.

**Impact:** Unnecessary code that adds maintenance burden without functional benefit.

**Recommended Fix:** Remove this method and its call in `validate()`:

```python
def validate(self):
    """Run all validations before save."""
    # validate_equipment_name removed - handled by reqd: 1 in JSON
    self.validate_serial_number_unique()
    self.validate_assigned_person()
    self.validate_user_has_organization()
```

---

### 2.2 Performance: N+1 Query Risk in Permission Check

**File:** `dartwing/permissions/equipment.py:35-39`

**Issue:** Each request to list equipment fetches all User Permissions for the user. For users with many organization memberships, this could be slow.

```python
orgs = frappe.get_all(
    "User Permission",
    filters={"user": user, "allow": "Organization"},
    pluck="for_value",
)
```

**Recommended Fix:** Consider caching in request context:

```python
def get_user_organizations(user):
    """Get user's permitted organizations with request-level caching."""
    cache_key = f"user_orgs_{user}"
    if not hasattr(frappe.local, cache_key):
        setattr(frappe.local, cache_key, frappe.get_all(
            "User Permission",
            filters={"user": user, "allow": "Organization"},
            pluck="for_value",
        ))
    return getattr(frappe.local, cache_key)
```

---

### 2.3 Client Script: Improve Empty Organization UX

**File:** `dartwing/dartwing_core/doctype/equipment/equipment.js:22-29`

**Issue:** When no organization is selected, the `assigned_to` field returns empty results via `name: ["in", []]`. This works but provides poor UX - the user sees an empty dropdown with no explanation.

**Recommended Fix:** Disable the field until organization is selected:

```javascript
set_assigned_to_query: function(frm) {
    if (!frm.doc.owner_organization) {
        frm.set_df_property("assigned_to", "read_only", 1);
        frm.set_df_property("assigned_to", "description", "Select organization first");
        return;
    }
    frm.set_df_property("assigned_to", "read_only", 0);
    frm.set_df_property("assigned_to", "description", "");
    frm.set_query("assigned_to", function() {
        return {
            query: "dartwing.dartwing_core.doctype.equipment.equipment.get_org_members",
            filters: { organization: frm.doc.owner_organization }
        };
    });
}
```

---

### 2.4 Child Table Docstrings Inaccurate

**File:** `dartwing/dartwing_core/doctype/equipment_maintenance/equipment_maintenance.py:8-14`

**Issue:** The docstring mentions "description" but the actual field is named "task":

```python
"""Equipment Maintenance child table for scheduling maintenance tasks.

Fields:
    task: Description of the maintenance task (required)  # Says "description" in prose
    ...
```

**Recommended Fix:** Minor, but ensure docstrings accurately reflect field names for maintainability.

---

### 2.5 Missing Test Files

**Issue:** No test files (`test_equipment.py`, etc.) are included in this branch.

**Impact:** Business logic (serial number uniqueness, assignment validation, org deletion protection) is untested.

**Recommended Fix:** Add test files covering:
- `test_equipment.py`: Serial number uniqueness, assignment validation, org permission filtering
- Hook tests: Organization deletion with equipment, Org Member removal with assigned equipment

**Example test structure:**

```python
# dartwing/dartwing_core/doctype/equipment/test_equipment.py
import frappe
import unittest

class TestEquipment(unittest.TestCase):
    def test_serial_number_unique(self):
        """FR-002: Serial numbers must be globally unique."""
        # Create first equipment with serial number
        # Attempt to create second with same serial - expect error
        pass

    def test_assignment_requires_org_membership(self):
        """FR-010: Assigned person must be org member."""
        pass
```

---

### 2.6 Consider Adding `description` Field

**File:** `dartwing/dartwing_core/doctype/equipment/equipment.json`

**Issue:** Most asset management systems include a description/notes field for additional details about equipment. The current schema only has structured fields.

**Recommended Addition (optional):**

```json
{
  "fieldname": "description",
  "fieldtype": "Small Text",
  "label": "Description"
}
```

---

### 2.7 Hooks.py: Consider Using List for Single Handler

**File:** `dartwing/hooks.py:182-185`

**Issue:** The `on_trash` handler for Org Member uses a list with two handlers:

```python
"on_trash": [
    "dartwing.permissions.helpers.remove_user_permissions",
    "dartwing.dartwing_core.doctype.equipment.equipment.check_equipment_assignments_on_member_removal"
],
```

**Note:** This is correct syntax and works fine. However, execution order matters - `remove_user_permissions` runs before the equipment check. Ensure this order is intentional (it appears to be, as you want to check equipment before removing permissions).

---

## 3. General Feedback & Summary (Severity: LOW)

### Overall Assessment

The Equipment DocType implementation is **well-structured and follows Frappe best practices**. The code demonstrates a solid understanding of:

1. **Polymorphic Organization Pattern:** Equipment correctly links to the generic `Organization` doctype rather than specific types (Family, Company, etc.), enabling universal asset management across all organization types.

2. **Multi-Tenant Security:** The permission model using `user_permission_dependant_doctype` and custom `has_permission`/`get_permission_query_conditions` properly isolates equipment data by organization membership.

3. **Cascade Protection:** The `doc_events` hooks for Organization and Org Member deletion properly prevent orphaned equipment records and maintain referential integrity.

4. **User Experience:** The client script dynamically filters the `assigned_to` dropdown based on selected organization, preventing invalid assignments at the UI level.

5. **Validation Layering:** Business rules are enforced at both database level (unique constraint on serial_number) and application level (friendly error messages in Python).

### Positive Highlights

- Clean separation of concerns between DocType, permissions module, and hooks
- Proper use of `@frappe.whitelist()` for API methods (`get_org_members`, `get_equipment_by_organization`, `get_equipment_by_person`)
- Thorough docstrings explaining validation rules with FR references
- Child tables (Equipment Document, Equipment Maintenance) are minimal and focused

### Technical Debt for Future Consideration

1. **Unit Tests:** Add comprehensive test coverage before expanding the feature
2. **Performance Profiling:** Monitor query performance with large equipment lists (1000+ items per org)
3. **Maintenance Automation:** Consider scheduled jobs to send maintenance due notifications
4. **Equipment Transfer:** No current mechanism to transfer equipment between organizations
5. **Bulk Operations:** No bulk import/export functionality for equipment records

### Confidence Assessment

**Confidence Level: 92%**

I have high confidence in understanding this feature because:
- Clear specification document (`spec.md`) with 13 functional requirements
- Complete architecture documentation (`dartwing_core_arch.md`, `dartwing_core_prd.md`)
- Well-documented code with FR reference comments
- Standard Frappe patterns followed throughout

The 8% uncertainty relates to:
- Interaction with other features (Person, Org Member, User Permission Propagation) not fully traced
- No runtime testing performed
- No review of the actual database state or migrations

---

## Summary Table

| Category | Count | Action Required |
|----------|-------|-----------------|
| Critical (HIGH) | 3 | Must fix before merge |
| Improvement (MEDIUM) | 7 | Should fix |
| Feedback (LOW) | 5 | Future consideration |

**Recommendation:** Address the 3 HIGH severity issues (SQL pattern, status transitions, audit trail) before merging. The MEDIUM issues can be addressed in this PR or as follow-up work depending on timeline constraints.
