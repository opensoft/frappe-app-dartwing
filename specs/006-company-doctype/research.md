# Research: Company DocType

**Feature**: 006-company-doctype
**Date**: 2025-12-13

## Overview

This document consolidates research findings for implementing the Company DocType as a concrete organization type in Dartwing's hybrid organization model.

---

## 1. Frappe Module Structure for New Modules

### Decision
Create `dartwing_company` as a new Frappe module within the existing `dartwing` app, not as a separate Frappe app.

### Rationale
- The existing codebase has `dartwing_core` as a module inside the `dartwing` app directory
- Module-level separation allows logical grouping while sharing app infrastructure
- Frappe 15.x supports multiple modules within a single app via the module manifest

### Alternatives Considered
1. **Separate Frappe app** - Rejected: Adds deployment complexity, cross-app imports are fragile
2. **Add to dartwing_core** - Rejected: Would grow core module too large; Company has distinct concerns

### Implementation
```
dartwing/
├── dartwing_core/        # Existing
├── dartwing_company/     # NEW
│   ├── __init__.py
│   └── doctype/
│       └── company/
├── modules.txt           # App-level module registration
```

Register in `dartwing/modules.txt` (app-level, not per-module):
```
Dartwing Core
Dartwing Company
```

---

## 2. Child Table Placement (Organization Officer, Organization Member Partner)

### Decision
Place both child tables in `dartwing_core` module, not `dartwing_company`.

### Rationale
- Per architecture doc (Section 3.5), Organization Officer is "shared child table also used by Nonprofit for board members"
- Organization Member Partner may be used by future Association type for membership
- Placing in core prevents circular dependencies between modules

### Alternatives Considered
1. **In dartwing_company** - Rejected: Would create dependency when Nonprofit needs officers
2. **Duplicate in each module** - Rejected: Violates DRY, creates sync issues

### Implementation
Child tables in `dartwing_core/doctype/`:
- `organization_officer/` - Links Person with title and dates
- `organization_member_partner/` - Links Person with ownership/voting data

---

## 3. Organization Hook Extension Pattern

### Decision
Extend existing `after_insert` hook in Organization to handle Company type alongside Family.

### Rationale
- Organization.py already has the pattern: `ORG_TYPE_MAP` + `create_concrete_type()`
- Current code explicitly skips Company: `if concrete_doctype != "Family": return`
- Removing this guard and adding Company-specific field mapping is minimal change

### Alternatives Considered
1. **Separate hook file** - Rejected: Fragmenting hook logic makes debugging harder
2. **Event-driven (signals)** - Rejected: Frappe doesn't have Django-style signals; doc_events are the pattern

### Implementation
Update `organization.py`:
```python
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",  # Already present
    "Club": "Club",
    "Nonprofit": "Nonprofit",
}

def create_concrete_type(self):
    # Remove the "if != Family: return" guard
    # Add type-specific field mapping:
    if concrete_doctype == "Family":
        concrete.family_name = self.org_name
    elif concrete_doctype == "Company":
        concrete.legal_name = self.org_name  # Map to legal_name
```

---

## 4. Naming Series Pattern

### Decision
Use `CO-.#####` naming series for Company, consistent with architecture doc Section 3.4.

### Rationale
- Architecture specifies this exact format
- Aligns with Family (`FAM-.#####`) and Organization (`ORG-.YYYY.-`) patterns
- Five-digit suffix supports up to 99,999 companies per instance

### Alternatives Considered
1. **Field-based autoname** - Rejected: Legal names aren't unique (multiple "Acme Inc")
2. **Hash autoname** - Rejected: Less human-readable for support/debugging

### Implementation
In `company.json`:
```json
{
  "autoname": "naming_series:",
  "fields": [
    {
      "fieldname": "naming_series",
      "fieldtype": "Select",
      "options": "CO-.#####",
      "default": "CO-.#####",
      "hidden": 1
    }
  ]
}
```

---

## 5. Entity Type Conditional Visibility

### Decision
Use Frappe's `depends_on` with `eval:` syntax to show/hide ownership section based on entity type.

### Rationale
- Frappe natively supports `depends_on` for field visibility
- The `eval:` prefix allows JavaScript expressions in the desk form
- Matching the exact entity types from spec (LLC, LP, GP, LLP)

### Alternatives Considered
1. **Custom script (.js)** - Rejected: Adds complexity; `depends_on` is cleaner
2. **Server-side hide** - Rejected: Doesn't provide dynamic UX feedback

### Implementation
In `company.json`:
```json
{
  "fieldname": "section_ownership",
  "fieldtype": "Section Break",
  "label": "Ownership / Members / Partners",
  "depends_on": "eval:['LLC','Limited Partnership (LP)','LLP','General Partnership'].includes(doc.entity_type)"
}
```

---

## 6. Permission Inheritance Strategy

### Decision
Use `user_permission_dependant_doctype` on Company pointing to Organization for automatic permission inheritance.

### Rationale
- Architecture doc (Section 8.2.1) specifies this exact pattern
- Frappe's built-in User Permission system handles filtering automatically
- No custom permission hooks needed if this setting is configured correctly

### Alternatives Considered
1. **Custom permission_query_conditions** - Still add as defense-in-depth
2. **Role-based only** - Rejected: Doesn't provide org-level isolation

### Implementation
In `company.json`:
```json
{
  "permissions": [
    {"role": "System Manager", "read": 1, "write": 1, "create": 1, "delete": 1},
    {"role": "Dartwing User", "read": 1, "write": 1, "if_owner": 0}
  ],
  "user_permission_dependant_doctype": "Organization"
}
```

Plus permission hook in `dartwing_company/permissions.py`:
```python
def get_permission_query_conditions_company(user):
    # Filter Company list by user's accessible Organizations
```

---

## 7. OrganizationMixin Implementation

### Decision
Create a mixin class in `dartwing_core/mixins/` that Company (and other concrete types) inherit.

### Rationale
- Architecture doc (Section 3.6) defines the mixin pattern with properties like `org_name`, `logo`, `org_status`
- DRY principle - avoids duplicating Organization access logic
- Existing Family controller doesn't yet use a mixin; Company can be the first

### Alternatives Considered
1. **Composition over inheritance** - Consider for future; mixin is simpler for now
2. **No mixin** - Rejected: Would duplicate property logic across concrete types

### Implementation
Create `dartwing_core/mixins/organization_mixin.py`:
```python
class OrganizationMixin:
    @property
    def org_name(self):
        return frappe.db.get_value("Organization", self.organization, "org_name")

    @property
    def logo(self):
        return frappe.db.get_value("Organization", self.organization, "logo")

    @property
    def org_status(self):
        return frappe.db.get_value("Organization", self.organization, "status")
```

Then in `company.py`:
```python
from dartwing_core.mixins.organization_mixin import OrganizationMixin

class Company(Document, OrganizationMixin):
    ...
```

---

## 8. Address DocType Integration

### Decision
Use standard Frappe `Link` field to the existing `Address` DocType.

### Rationale
- Frappe ships with a built-in Address DocType
- The spec requires two address links: registered and physical
- Person as registered agent also uses standard Link field

### Alternatives Considered
1. **Dynamic Link (like ERPNext)** - Rejected: Overkill for two fixed address fields
2. **Embedded address fields** - Rejected: Violates normalization, harder to reuse

### Implementation
In `company.json`:
```json
{
  "fieldname": "registered_address",
  "fieldtype": "Link",
  "options": "Address",
  "label": "Registered Address"
},
{
  "fieldname": "physical_address",
  "fieldtype": "Link",
  "options": "Address",
  "label": "Principal / Physical Address"
}
```

---

## 9. Country/State Fields for Jurisdiction

### Decision
Use `Link` to Frappe's built-in Country DocType for country, and `Data` field for state/province.

### Rationale
- Frappe has a Countries fixture with ISO codes
- State/province varies too much by country for a global list
- Matches architecture doc's Company JSON in Section 3.4

### Alternatives Considered
1. **Both as Data fields** - Rejected: Country standardization benefits from link
2. **State as Link to custom DocType** - Rejected: Maintenance burden, data entry friction

### Implementation
```json
{
  "fieldname": "jurisdiction_country",
  "fieldtype": "Link",
  "options": "Country",
  "label": "Country of Formation"
},
{
  "fieldname": "jurisdiction_state",
  "fieldtype": "Data",
  "label": "State / Province"
}
```

---

## 10. Ownership Percentage Validation

### Decision
Implement a soft validation that warns (but doesn't block) when ownership percentages exceed 100%.

### Rationale
- Spec states: "System should display a warning but not prevent saving"
- Partial ownership records may be entered incrementally
- Hard block would frustrate users during data entry

### Alternatives Considered
1. **Hard block at 100%** - Rejected per spec
2. **No validation** - Rejected: Silent data quality issues

### Implementation
In `company.py` validate method:
```python
def validate(self):
    total_ownership = sum(
        (m.ownership_percent or 0) for m in self.members_partners
    )
    if total_ownership > 100:
        frappe.msgprint(
            _("Warning: Total ownership ({0}%) exceeds 100%").format(total_ownership),
            indicator="orange",
            alert=True
        )
```

---

## Summary of Key Decisions

| Topic | Decision |
|-------|----------|
| Module location | New `dartwing_company` module in `dartwing` app |
| Child tables | In `dartwing_core` (shared with future Nonprofit) |
| Hook pattern | Extend existing `Organization.create_concrete_type()` |
| Naming | `CO-.#####` series |
| Conditional fields | `depends_on` with `eval:` JavaScript |
| Permissions | `user_permission_dependant_doctype` + permission hook |
| Mixin | New `OrganizationMixin` in `dartwing_core/mixins/` |
| Addresses | Link to standard Frappe Address DocType |
| Jurisdiction | Link to Country, Data for state |
| Ownership validation | Soft warning via `frappe.msgprint` |
