# Research: Role Template DocType

**Feature**: 002-role-template-doctype
**Date**: 2025-12-03

## Research Topics

This document consolidates findings for technical decisions required by the Role Template DocType implementation.

---

## 1. Frappe Fixture Best Practices

### Decision
Use JSON fixtures in `dartwing/fixtures/role_template.json` with `name` field as primary key.

### Rationale
- Frappe fixtures are automatically loaded during `bench --site [site] install-app dartwing`
- JSON format is declarative and version-controllable
- `name` field ensures idempotency - Frappe updates existing records by name

### Alternatives Considered

| Approach | Pros | Cons | Rejected Because |
|----------|------|------|------------------|
| Python fixtures (hooks.py) | Programmatic control | Requires code execution | Overkill for static seed data |
| Migration scripts | One-time execution | Not idempotent | Would fail on re-run |
| Manual data entry | Flexible | Not reproducible | Violates automation principle |

### Implementation Pattern

```json
[
  {
    "doctype": "Role Template",
    "name": "Parent",
    "role_name": "Parent",
    "applies_to_org_type": "Family",
    "is_supervisor": 1,
    "default_hourly_rate": 0
  }
]
```

### Configuration Required
Add to `hooks.py`:
```python
fixtures = [
    {"dt": "Role Template", "filters": []}
]
```

---

## 2. Conditional Field Visibility (depends_on)

### Decision
Use `depends_on` attribute with `eval:doc.applies_to_org_type=='Company'` for `default_hourly_rate` field.

### Rationale
- Standard Frappe pattern for conditional fields
- Works in both Desk UI and API responses
- No custom JavaScript required

### Alternatives Considered

| Approach | Pros | Cons | Rejected Because |
|----------|------|------|------------------|
| Custom JS form script | Full control | Maintenance overhead | Standard pattern exists |
| Separate DocType for Company roles | Clean separation | Violates single source of truth | Constitution principle #1 |
| Always show field | Simple | Poor UX for non-Company roles | User confusion |

### Implementation Pattern

```json
{
  "fieldname": "default_hourly_rate",
  "fieldtype": "Currency",
  "label": "Default Hourly Rate",
  "depends_on": "eval:doc.applies_to_org_type=='Company'",
  "description": "Default hourly rate for Company roles"
}
```

---

## 3. Link Field Filtering

### Decision
Use `get_query` in Org Member form to filter Role Template by organization's `org_type`.

### Rationale
- Org Member will have a Link field to Role Template
- The filter must be dynamic based on the selected organization
- Frappe's `get_query` allows server-side filtering with context

### Alternatives Considered

| Approach | Pros | Cons | Rejected Because |
|----------|------|------|------------------|
| Client-side filter only | Simple | Bypassed via API | Security concern |
| Hardcoded filters | Simple | Can't adapt to org context | Need dynamic filtering |
| Pre-filter all roles | Performance | Loads unnecessary data | Poor UX |

### Implementation Pattern (for Org Member, Feature 3)

In `org_member.js`:
```javascript
frappe.ui.form.on('Org Member', {
    organization: function(frm) {
        frm.set_query('role', function() {
            return {
                filters: {
                    applies_to_org_type: frm.doc.organization_type
                }
            };
        });
    }
});
```

Note: This implementation is documented here but will be implemented in Feature 3 (Org Member DocType).

---

## 4. Deletion Prevention Hook

### Decision
Implement `on_trash` hook in `role_template.py` that checks for linked Org Member records.

### Rationale
- FR-008 requires preventing deletion of in-use Role Templates
- `on_trash` is the standard Frappe hook for deletion validation
- Should fail gracefully if Org Member DocType doesn't exist yet

### Alternatives Considered

| Approach | Pros | Cons | Rejected Because |
|----------|------|------|------------------|
| Database foreign key | Enforced at DB level | Hard to customize error message | Poor UX on error |
| Soft delete only | Never lose data | Complexity for reference data | Overkill |
| No prevention | Simple | Data integrity risk | Spec requirement |

### Implementation Pattern

```python
class RoleTemplate(Document):
    def on_trash(self):
        # Check if Org Member DocType exists (Feature 3)
        if frappe.db.exists("DocType", "Org Member"):
            linked_members = frappe.db.count("Org Member", {"role": self.name})
            if linked_members > 0:
                frappe.throw(
                    f"Cannot delete Role Template '{self.role_name}': "
                    f"{linked_members} Org Member(s) are using this role."
                )
```

---

## 5. Permission Configuration

### Decision
- System Manager: Full CRUD access
- All authenticated users (Dartwing User): Read-only access

### Rationale
- Role Templates are system-wide reference data
- Only administrators should create/modify roles
- All users need to read roles for assignment UI

### Implementation Pattern

```json
"permissions": [
  {
    "role": "System Manager",
    "read": 1, "write": 1, "create": 1, "delete": 1,
    "export": 1, "report": 1
  },
  {
    "role": "Dartwing User",
    "read": 1,
    "export": 0, "report": 0
  }
]
```

---

## 6. Organization org_type Update

### Decision
Update Organization DocType's `org_type` options from "Club" to "Association".

### Rationale
- Clarification session confirmed "Association" is the canonical type
- Club is a subtype of Association
- Role Template filtering depends on matching org_type values

### Migration Approach
1. Update `organization.json` field options: `"Family\nCompany\nAssociation\nNonprofit"`
2. Create data migration to update existing "Club" records to "Association"
3. Include migration in this feature's tasks

### Impact Assessment
- Low risk: Limited existing data in development
- If production data exists, migration required before Role Template deployment

---

## Summary

All research topics resolved. No NEEDS CLARIFICATION items remain.

| Topic | Decision | Confidence |
|-------|----------|------------|
| Fixtures | JSON in dartwing/fixtures | HIGH |
| Conditional fields | `depends_on` attribute | HIGH |
| Link filtering | `get_query` (in Org Member) | HIGH |
| Deletion prevention | `on_trash` hook with graceful fallback | HIGH |
| Permissions | System Manager write, Dartwing User read | HIGH |
| org_type update | "Club" → "Association" migration | HIGH |
