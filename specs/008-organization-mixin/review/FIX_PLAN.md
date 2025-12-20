# FIX PLAN: 008-organization-mixin

**Branch:** `008-organization-mixin`
**Module:** `dartwing_core`
**Created:** 2025-12-14
**Status:** PENDING APPROVAL

---

## Executive Summary

This plan addresses all issues identified in `MASTER_REVIEW.md` for the OrganizationMixin feature. The implementation is currently **incomplete** - the `update_org_name()` method is missing entirely, and Family does not inherit the mixin despite tests expecting it to.

**Critical Finding:** 6 P1 issues must be fixed before merge, including a security vulnerability (permission bypass) and broken hooks.py syntax.

---

## Cross-Reference Verification

All fixes have been verified against:
- `docs/dartwing_core/dartwing_core_arch.md` (Architecture constraints)
- `docs/dartwing_core/dartwing_core_prd.md` (Product requirements)

| Issue | Architecture/PRD Reference | Compliance Status |
|-------|---------------------------|-------------------|
| Permission enforcement | Section 8.2.1: "Organization is the permission boundary" | Fix aligns with requirement |
| Mixin inheritance | Section 3.6: All concrete types inherit OrganizationMixin | Fix aligns with requirement |
| `user_permission_dependant_doctype` | Section 8.2.1, PRD Section 3.7 | Fix aligns with requirement |
| Family fields (`family_name` vs `family_nickname`) | Section 3.4 shows `family_nickname` | **DEFERRED** - would break autoname |

---

## P1: CRITICAL (Before Merge - MUST FIX)

### P1-1: Add `update_org_name()` Method with Permission Enforcement

**Original Issue:** Permission Bypass in `update_org_name()` Method (jeni52, gemi30, opus45, sonn4p5)

**Current State:** Method is completely missing from `organization_mixin.py` (file ends at line 76)

**Files Affected:**
- `dartwing/dartwing_core/mixins/organization_mixin.py`

**Plan:**
Add the `update_org_name()` method with full permission enforcement:

```python
def update_org_name(self, new_name: str) -> None:
    """
    Update the organization name on the linked Organization record.

    Args:
        new_name: The new organization name to set.

    Raises:
        frappe.ValidationError: If new_name is empty/whitespace or no organization is linked.
        frappe.PermissionError: If user lacks write permission on Organization.
    """
    from frappe import _

    # Normalize and validate input
    org_name = (new_name or "").strip()
    if not org_name:
        frappe.throw(_("Organization name cannot be empty"))

    # Validate organization link exists
    if not self.organization:
        frappe.throw(_("Cannot update organization name: No organization linked"))

    # Load Organization document (checks read permission)
    org = frappe.get_doc("Organization", self.organization)

    # Check write permission explicitly
    org.check_permission("write")

    # Update and save (runs validations, hooks, and audit logging)
    org.org_name = org_name
    org.save()

    # Clear cache so subsequent property access returns fresh data
    self._clear_organization_cache()
```

**Compliance Note:** PRD REQ-ORG-002 requires "complete data isolation"; Architecture Section 8.2.1 states "Organization is the permission boundary."

---

### P1-2: Fix Duplicate Dictionary Keys and Broken Syntax in hooks.py

**Original Issue:** Duplicate Dictionary Keys in `hooks.py` (sonn4p5)

**Current State:**
- Lines 125-126: Duplicate "Company" key in `permission_query_conditions`
- Lines 134-135: Duplicate "Company" key in `has_permission`
- Lines 176-187: Broken syntax with two `doc_events = {` definitions

**Files Affected:**
- `dartwing/dartwing/hooks.py`

**Plan:**
1. Remove duplicate "Company" entries, keeping `dartwing.permissions.company.*` (consistent with other org types)
2. Fix `doc_events` syntax to have single properly-formed dictionary

**Before (broken):**
```python
permission_query_conditions = {
    ...
    "Company": "dartwing.dartwing_company.permissions.get_permission_query_conditions_company",
    "Company": "dartwing.permissions.company.get_permission_query_conditions",  # DUPLICATE
    ...
}
```

**After (fixed):**
```python
permission_query_conditions = {
    ...
    "Company": "dartwing.permissions.company.get_permission_query_conditions",
    ...
}
```

**Compliance Note:** Architecture Section 8.2.1 requires proper permission hook registration.

---

### P1-3: Add Negative Ownership Validation in Company Controller

**Original Issue:** Missing Negative Ownership Validation (opus45)

**Current State:** `validate_ownership_percentage()` only warns when >100%, no validation for negative values

**Files Affected:**
- `dartwing/dartwing_company/doctype/company/company.py`

**Plan:**
Add validation loop before sum calculation:

```python
def validate_ownership_percentage(self):
    """Validate ownership percentages and warn if total exceeds 100%."""
    if not self.members_partners:
        return

    # Validate no negative ownership
    for mp in self.members_partners:
        if mp.ownership_percent is not None and mp.ownership_percent < 0:
            frappe.throw(
                _("Ownership percentage cannot be negative for {0}").format(
                    mp.person
                )
            )

    # Calculate total ownership
    total_ownership = sum(
        (mp.ownership_percent or 0) for mp in self.members_partners
    )

    # Warn if exceeds 100%
    if total_ownership > 100:
        frappe.msgprint(
            _("Total ownership percentage ({0}%) exceeds 100%").format(
                total_ownership
            ),
            indicator="orange",
            alert=True
        )
```

**Compliance Note:** Ensures data integrity; test `test_negative_ownership_rejected` expects this validation.

---

### P1-4: Remove `__pycache__` from Git and Update .gitignore

**Original Issue:** `__pycache__` Directories Committed (jeni52)

**Current State:** 47+ `__pycache__` files tracked in git

**Files Affected:**
- All `__pycache__/` directories
- `.gitignore`

**Plan:**
```bash
# Remove from git tracking (keeps local files)
git rm -r --cached **/__pycache__/

# Ensure .gitignore includes:
__pycache__/
*.pyc
*.pyo
```

**Compliance Note:** Standard hygiene; prevents CI "clean tree" failures.

---

### P1-5: Move Tests to Discoverable Location

**Original Issue:** Test File Location Won't Be Discovered (jeni52, opus45, sonn4p5)

**Current State:** Tests at `dartwing/dartwing_core/tests/test_organization_mixin.py`

**Files Affected:**
- `dartwing/dartwing_core/tests/test_organization_mixin.py` (source)
- `dartwing/tests/unit/test_organization_mixin.py` (destination)

**Plan:**
1. Create `dartwing/tests/unit/` directory if it doesn't exist
2. Move test file to `dartwing/tests/unit/test_organization_mixin.py`
3. Remove empty `dartwing/dartwing_core/tests/` directory if no other files remain

**Compliance Note:** Aligns with project convention (`dartwing/tests/integration/` exists).

---

### P1-6: Make Family Inherit OrganizationMixin

**Original Issue:** Discovered during analysis - Family does NOT inherit mixin

**Current State:** `class Family(Document):` without mixin

**Files Affected:**
- `dartwing/dartwing_core/doctype/family/family.py`

**Plan:**
```python
from dartwing.dartwing_core.mixins import OrganizationMixin

class Family(Document, OrganizationMixin):
    """
    Family DocType - represents a household unit.

    Inherits from OrganizationMixin to provide access to parent Organization
    properties (org_name, logo, org_status) and methods (get_organization_doc,
    update_org_name).
    """
```

**Compliance Note:** Architecture Section 3.6 requires all concrete types to inherit mixin.

---

## P2: MEDIUM (Should Fix Soon)

### P2-1: Add `user_permission_dependant_doctype` to Family.json

**Original Issue:** Family DocType Missing Permission Configuration (opus45)

**Files Affected:**
- `dartwing/dartwing_core/doctype/family/family.json`

**Plan:**
Add at root level of JSON:
```json
{
  "user_permission_dependant_doctype": "Organization",
  ...
}
```

Add "Dartwing User" role to permissions array:
```json
{
  "email": 1,
  "export": 1,
  "print": 1,
  "read": 1,
  "report": 1,
  "role": "Dartwing User",
  "share": 1,
  "write": 1
}
```

**Compliance Note:** Required by Architecture Section 8.2.1 for multi-tenant isolation.

---

### P2-2: Add OrganizationMixin to Association and Nonprofit

**Original Issue:** Inconsistent Mixin Adoption (sonn4p5)

**Files Affected:**
- `dartwing/dartwing_core/doctype/association/association.py`
- `dartwing/dartwing_core/doctype/nonprofit/nonprofit.py`

**Plan:**
Update both files to inherit from OrganizationMixin:

```python
from dartwing.dartwing_core.mixins import OrganizationMixin

class Association(Document, OrganizationMixin):
    """
    Association DocType - represents member-based organizations.

    Inherits from OrganizationMixin to provide access to parent Organization
    properties (org_name, logo, org_status) and methods.
    """
```

(Same pattern for Nonprofit)

**Compliance Note:** Architecture Section 3.6 (FR-006/SC-004) requires all concrete types inherit mixin.

---

### P2-3: Add Type Hints to Mixin Properties/Methods

**Original Issue:** Missing Type Hints (opus45, sonn4p5)

**Files Affected:**
- `dartwing/dartwing_core/mixins/organization_mixin.py`

**Plan:**
```python
from typing import Optional, Dict, Any

def _get_organization_cache(self) -> Optional[Dict[str, Any]]:
    ...

@property
def org_name(self) -> Optional[str]:
    ...

@property
def logo(self) -> Optional[str]:
    ...

@property
def org_status(self) -> Optional[str]:
    ...

def get_organization_doc(self) -> Optional["Document"]:
    ...

def update_org_name(self, new_name: str) -> None:
    ...
```

**Compliance Note:** Python 3.11+ per PRD Section 1.4.

---

### P2-4: Remove Excessive `frappe.db.commit()` from Tests

**Original Issue:** Test Quality (jeni52, opus45, sonn4p5)

**Files Affected:**
- `dartwing/tests/unit/test_organization_mixin.py` (after move)

**Plan:**
Remove all manual `frappe.db.commit()` calls from:
- `setUp()` (line 64)
- `tearDown()` (line 72)
- `_cleanup_test_data()` (line 40)
- Individual test methods (lines 91, 174)

**Compliance Note:** Frappe test framework manages transactions automatically.

---

### P2-5: Add CACHED_ORG_FIELDS Constant

**Original Issue:** Hardcoded Field Names (sonn4p5)

**Files Affected:**
- `dartwing/dartwing_core/mixins/organization_mixin.py`

**Plan:**
```python
# At module level
CACHED_ORG_FIELDS = ["org_name", "logo", "status"]

# In _get_organization_cache():
self._org_cache = frappe.db.get_value(
    "Organization",
    self.organization,
    CACHED_ORG_FIELDS,
    as_dict=True
)
```

**Compliance Note:** Improves maintainability; single point of change if schema evolves.

---

### P2-6: Correct research.md Incorrect Statement

**Original Issue:** Documentation Error (gemi30, sonn4p5)

**Files Affected:**
- `specs/008-organization-mixin/research.md`

**Plan:**
Update Research Item 6 (lines 129-144):

**Before:**
> `frappe.db.set_value()` respects permissions by default

**After:**
> `frappe.db.set_value()` performs a direct SQL UPDATE and does NOT enforce Frappe's permission system or run document hooks. For permission-enforced writes, use `doc.check_permission("write")` followed by `doc.save()`.

**Compliance Note:** Prevents future security vulnerabilities from copied patterns.

---

## P3: LOW (Post-Merge Improvements)

### P3-1: Remove Hardcoded Status Default from Family Controller

**Original Issue:** Code Style (gemi30)

**Files Affected:**
- `dartwing/dartwing_core/doctype/family/family.py`

**Plan:**
Remove from `validate()`:
```python
# Remove this line - default is already in family.json
if not self.status:
    self.status = "Active"
```

**Compliance Note:** Follows "Metadata-as-Data" principle; `family.json` already has `"default": "Active"`.

---

## Deferred Items (Not In Scope)

| Item | Reason for Deferral |
|------|---------------------|
| Family fields (`family_name` → `family_nickname`) | Would break `autoname: field:family_name` and existing data. Requires separate migration. |
| Additional test cases (permissions, unicode, Company) | Can be added post-merge as enhancement. |
| Standardize mixin API documentation across doctypes | Low priority cosmetic improvement. |

---

## Execution Order

1. **P1-4**: Remove `__pycache__` first (clean working tree)
2. **P1-2**: Fix hooks.py (enables app to load without syntax errors)
3. **P1-1**: Add `update_org_name()` to mixin (core functionality)
4. **P1-6**: Add mixin to Family (enables tests to pass)
5. **P1-3**: Add negative ownership validation
6. **P1-5**: Move tests to correct location
7. **P2-1 through P2-6**: Medium priority fixes
8. **P3-1**: Low priority cleanup

---

## Approval Checklist

- [ ] P1 fixes reviewed and approved
- [ ] P2 fixes reviewed and approved
- [ ] P3 fixes reviewed and approved
- [ ] Deferred items acknowledged

**Approver:** __________________ **Date:** __________________

---

## Post-Implementation Verification

After implementation, verify:
1. `bench --site <site> run-tests --app dartwing` discovers and runs all tests
2. `python3 -c "import dartwing.hooks"` succeeds without errors
3. All `test_organization_mixin.py` tests pass
4. `test_negative_ownership_rejected` test passes
5. No `__pycache__` files in git status

---

*Generated from MASTER_REVIEW.md analysis*
*Reference Documents: dartwing_core_arch.md, dartwing_core_prd.md*
