# Research: OrganizationMixin Base Class

**Feature**: 008-organization-mixin
**Date**: 2025-12-14

## Research Summary

This feature enhances an existing implementation. The OrganizationMixin already exists with core functionality. Research focuses on best practices for the new `update_org_name()` method and confirming Frappe patterns.

---

## Research Item 1: Frappe Single-Field Update Pattern

**Question**: What is the most efficient way to update a single field on a related document in Frappe?

**Decision**: Use `frappe.get_doc().save()` for permission-enforced updates

**Rationale**:
- `frappe.db.set_value()` performs a direct SQL UPDATE but does NOT enforce permissions
- For multi-tenant security (Organization is the permission boundary per Architecture Section 8.2.1),
  we must explicitly check permissions before updating
- `get_doc()` + `check_permission()` + `save()` ensures proper access control and audit logging
- Trade-off: Less efficient but necessary for security

**Alternatives Considered**:
1. `frappe.db.set_value()` - Rejected: Bypasses Frappe's permission system (security vulnerability)
2. Raw SQL - Rejected: Bypasses permissions and audit trail
3. `doc.db_set()` - Rejected: Also bypasses permissions

**Implementation Pattern**:
```python
org = frappe.get_doc("Organization", self.organization)
org.check_permission("write")
org.org_name = new_name
org.save()
```

---

## Research Item 2: Validation Error Pattern in Frappe

**Question**: How should validation errors be raised in Frappe methods?

**Decision**: Use `frappe.throw()` with translatable message

**Rationale**:
- `frappe.throw()` raises `frappe.ValidationError` with proper UI handling
- `_()` wrapper enables translation/localization
- Consistent with existing codebase patterns (see Organization.validate())

**Alternatives Considered**:
1. `raise ValueError` - Rejected: Not translated, no Frappe UI integration
2. `frappe.msgprint()` + return - Rejected: Doesn't halt execution

**Implementation Pattern**:
```python
from frappe import _

def update_org_name(self, new_name: str):
    if not new_name or not new_name.strip():
        frappe.throw(_("Organization name cannot be empty"))
```

---

## Research Item 3: Python Mixin Multiple Inheritance with Frappe Document

**Question**: Does Python's MRO (Method Resolution Order) cause issues when mixing Document with OrganizationMixin?

**Decision**: Use `class ConcreteType(Document, OrganizationMixin)` order

**Rationale**:
- Document must come first to be the primary class
- Mixin provides additional methods/properties that don't override Document methods
- Company already uses this pattern successfully
- Python's C3 linearization handles MRO correctly

**Evidence**:
```python
# Existing working pattern in dartwing_company/doctype/company/company.py:
class Company(Document, OrganizationMixin):
    pass
```

**Alternatives Considered**:
1. Mixin first `(OrganizationMixin, Document)` - Rejected: Document should be primary base
2. Composition over inheritance - Rejected: Less ergonomic API, more boilerplate

---

## Research Item 4: Cache Invalidation After Update

**Question**: Should `update_org_name()` invalidate the mixin's internal cache?

**Decision**: Yes, call `_clear_organization_cache()` after update

**Rationale**:
- The mixin caches Organization data in `_org_cache`
- After updating `org_name`, the cache would be stale
- Calling `_clear_organization_cache()` ensures subsequent `org_name` access returns fresh data
- Pattern already exists in mixin for this purpose

**Implementation Pattern**:
```python
def update_org_name(self, new_name: str):
    # ... validation and update ...
    self._clear_organization_cache()  # Invalidate cache
```

---

## Research Item 5: Error Handling for Missing Organization

**Question**: What error should be raised when `update_org_name()` is called on a concrete type without a linked Organization?

**Decision**: Raise `frappe.throw()` with descriptive error

**Rationale**:
- Unlike read properties (which return None silently per FR-007), write operations should fail explicitly
- Prevents silent failures that could confuse developers
- Matches clarification: "update_org_name() raises an error since there is no target to update"

**Implementation Pattern**:
```python
def update_org_name(self, new_name: str):
    if not self.organization:
        frappe.throw(_("Cannot update organization name: No organization linked"))
```

---

## Research Item 6: Permission Handling

**Question**: Should the mixin check permissions before updating?

**Decision**: Yes, explicitly check write permission before updating

**Rationale**:
- **CORRECTION**: `frappe.db.set_value()` does NOT enforce permissions - it performs direct SQL
- Per PRD REQ-ORG-002: "Complete data isolation between Organizations"
- Per Architecture Section 8.2.1: "Organization is the permission boundary"
- Must use `doc.check_permission("write")` before modifying Organization data
- `doc.save()` also runs document hooks and audit logging

**Implementation Pattern**:
```python
org = frappe.get_doc("Organization", self.organization)
org.check_permission("write")  # Raises PermissionError if denied
org.org_name = new_name
org.save()  # Runs validations, hooks, audit logging
```

**Security Note**: Be cautious when using `frappe.db.set_value()` for cross-document
updates in multi-tenant contexts. It bypasses Frappe's permission system, validation
hooks, and audit logging. Consider the security implications - use `frappe.get_doc()` +
`doc.save()` instead when permission enforcement, validations, or audit trails are required.
Valid use cases for `frappe.db.set_value()` exist in internal/system operations where
permissions are pre-verified.

---

## Resolved NEEDS CLARIFICATION Items

All technical context items resolved. No NEEDS CLARIFICATION markers remain.

| Item | Resolution | Source |
|------|------------|--------|
| Update method pattern | `get_doc()` + `check_permission()` + `save()` | Security requirement (PRD REQ-ORG-002) |
| Validation approach | `frappe.throw()` | Existing codebase patterns |
| Inheritance order | Document first | Working Company implementation |
| Cache invalidation | Call `_clear_organization_cache()` | Existing mixin pattern |
| Missing org error | `frappe.throw()` | Spec clarification |
| Permission handling | Explicit `check_permission("write")` | Architecture Section 8.2.1 |
