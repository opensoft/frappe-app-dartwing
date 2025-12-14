# FIX PLAN: 009-api-helpers

**Created By:** Director of Engineering
**Date:** 2025-12-14
**Branch:** `009-api-helpers`
**Module:** `dartwing_core`
**Source:** MASTER_REVIEW.md

---

## Executive Summary

This fix plan addresses **6 P1 Critical issues** identified in MASTER_REVIEW.md. All fixes have been cross-referenced against `dartwing_core_arch.md` and `dartwing_core_prd.md` for compliance.

**Status:** P1 IMPLEMENTATION COMPLETE

---

## 1. Master Fix Plan (P1 Critical Only)

### Task 1: P1-001 — Fix Undefined Exception Variable

| Attribute | Value |
|:----------|:------|
| **Issue ID** | P1-001 |
| **Type** | Runtime Bug |
| **File** | `dartwing/dartwing_core/doctype/organization/organization.py` |
| **Line** | 383 |
| **Problem** | `except frappe.LinkExistsError:` references `str(e)` on line 387 but `e` is never captured. Causes `NameError` at runtime. |
| **Fix** | Change `except frappe.LinkExistsError:` to `except frappe.LinkExistsError as e:` |
| **Compliance** | No architectural conflict. Required for runtime stability. |

**Before:**
```python
except frappe.LinkExistsError:
    logger.error(
        f"Cannot delete {self.linked_doctype} {self.linked_name}: "
        f"Other records still reference it. {str(e)}"
    )
```

**After:**
```python
except frappe.LinkExistsError as e:
    logger.error(
        f"Cannot delete {self.linked_doctype} {self.linked_name}: "
        f"Other records still reference it. {str(e)}"
    )
```

---

### Task 2: P1-002 — Fix Function Signature Mismatch

| Attribute | Value |
|:----------|:------|
| **Issue ID** | P1-002 |
| **Type** | Runtime Bug |
| **File** | `dartwing/permissions/helpers.py` |
| **Line** | 125 |
| **Problem** | `_cleanup_orphaned_permissions(user, doc)` called with 2 args but function defined with 3: `(user, org_name, doc)`. Causes `TypeError`. |
| **Fix** | Change call to `_cleanup_orphaned_permissions(user, doc.organization, doc)` |
| **Compliance** | No architectural conflict. Required for runtime stability. |

**Before:**
```python
_cleanup_orphaned_permissions(user, doc)
```

**After:**
```python
_cleanup_orphaned_permissions(user, doc.organization, doc)
```

---

### Task 3: P1-003 — Clean Malformed Docstring

| Attribute | Value |
|:----------|:------|
| **Issue ID** | P1-003 |
| **Type** | Code Corruption |
| **File** | `dartwing/dartwing_core/doctype/organization/organization.py` |
| **Lines** | 339-347 |
| **Problem** | `_delete_concrete_type()` docstring contains orphaned code fragments referencing undefined `concrete_doctype` and `e`. |
| **Fix** | Remove embedded code fragments, keep only method description and implementation notes. |
| **Compliance** | Code quality per project constitution. No architectural conflict. |

**Before:**
```python
def _delete_concrete_type(self):
    """
    Delete the linked concrete type document (cascade delete).
        frappe.log_error(f"Error creating concrete type {concrete_doctype}: {str(e)}")
        frappe.throw(
            _("Failed to create {0} record. Please try again or contact support.").format(
                concrete_doctype
            )
        )

    Implements FR-005, FR-006, FR-012, FR-013.
    ...
```

**After:**
```python
def _delete_concrete_type(self):
    """
    Delete the linked concrete type document (cascade delete).

    Implements FR-005, FR-006, FR-012, FR-013.
    ...
```

---

### Task 4: P1-004 — Fix Method Naming/Body Confusion

| Attribute | Value |
|:----------|:------|
| **Issue ID** | P1-004 |
| **Type** | Code Structure |
| **File** | `dartwing/dartwing_core/doctype/organization/organization.py` |
| **Lines** | 234-257 |
| **Problem** | `_create_concrete_type()` (line 234) has docstring but no body. `create_concrete_type()` (line 257) has the implementation. Hook at line 228 calls `self._create_concrete_type()` which is empty. |
| **Fix** | Merge docstring into implementation, rename `create_concrete_type()` to `_create_concrete_type()` (private). Update test file if needed. |
| **Compliance** | Per `dartwing_core_arch.md` Section 3.6: hook methods should be private. Matches `_delete_concrete_type()` pattern. |

**Before:**
```python
def _create_concrete_type(self):
    """
    Create the concrete type document and establish bidirectional link.
    ... (docstring only, no implementation)
    """
def create_concrete_type(self):
    """Create the concrete type document..."""
    # actual implementation here
```

**After:**
```python
def _create_concrete_type(self):
    """
    Create the concrete type document and establish bidirectional link.

    Implements FR-001 through FR-004, FR-011, FR-012, FR-013.
    ... (merged docstring)
    """
    # actual implementation moved here
```

---

### Task 5: P1-005 — Fix Authorization Model Inconsistency

| Attribute | Value |
|:----------|:------|
| **Issue ID** | P1-005 |
| **Type** | Security/Design |
| **File** | `dartwing/dartwing_core/api/organization_api.py` |
| **Lines** | 86-100 |
| **Problem** | `get_user_organizations()` derives access from Org Member table, but detail endpoints use `frappe.has_permission()`. Can cause "phantom orgs" visible but inaccessible. |
| **Fix** | Add `has_access: bool` field to each organization in response by calling `frappe.has_permission("Organization", "read", org_name)`. |
| **Compliance** | Per `dartwing_core_arch.md` Section 8.2.1: consistent permission model via User Permission. Non-breaking additive change. |

**Before:**
```python
data.append({
    "name": m.organization,
    "org_name": m.org_name,
    # ... other fields
    "is_supervisor": m.is_supervisor or 0,
})
```

**After:**
```python
data.append({
    "name": m.organization,
    "org_name": m.org_name,
    # ... other fields
    "is_supervisor": m.is_supervisor or 0,
    "has_access": frappe.has_permission("Organization", "read", m.organization),
})
```

---

### Task 6: P1-006 — Add Parameter Validation

| Attribute | Value |
|:----------|:------|
| **Issue ID** | P1-006 |
| **Type** | Input Validation |
| **File** | `dartwing/dartwing_core/api/organization_api.py` |
| **Lines** | 141-155 |
| **Problem** | Missing validation: (1) Guest check for 401, (2) Empty organization, (3) Limit ≤0 allowed, (4) Status not validated against enum, (5) Non-int limit causes ValueError. |
| **Fix** | Add comprehensive validation block at start of `get_org_members()`. |
| **Compliance** | Per `dartwing_core_prd.md` API design: proper error semantics (401/403/404). |

**After (new validation block):**
```python
@frappe.whitelist()
def get_org_members(
    organization: str,
    limit: int = 20,
    offset: int = 0,
    status: Optional[str] = None,
) -> dict:
    # Validation constants
    VALID_STATUSES = {"Active", "Inactive", "Pending"}

    # Authentication check (401)
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    # Required parameter check
    if not organization:
        frappe.throw(_("Organization parameter is required"), frappe.ValidationError)

    # Organization existence check (404)
    if not frappe.db.exists("Organization", organization):
        frappe.throw(_("Organization {0} not found").format(organization), frappe.DoesNotExistError)

    # Permission check (403)
    if not frappe.has_permission("Organization", "read", organization):
        logger.warning(f"API: get_org_members - Permission denied for '{organization}'")
        frappe.throw(_("Not permitted to access this organization"), frappe.PermissionError)

    # Validate and clamp limit
    try:
        limit = max(1, min(int(limit), 100))
    except (ValueError, TypeError):
        limit = 20

    # Validate and clamp offset
    try:
        offset = max(0, int(offset))
    except (ValueError, TypeError):
        offset = 0

    # Validate status enum
    if status and status not in VALID_STATUSES:
        frappe.throw(
            _("Invalid status: {0}. Must be one of: {1}").format(status, ", ".join(VALID_STATUSES)),
            frappe.ValidationError
        )

    # ... rest of implementation
```

---

## 2. Summary of High-Impact Decisions

### Architectural Changes

| Issue | Change Type | Decision | Rationale |
|:------|:------------|:---------|:----------|
| **P1-004** | Method Refactoring | Rename `create_concrete_type()` → `_create_concrete_type()` | Per `dartwing_core_arch.md` Section 3.6, hook-called methods should be private. Matches existing `_delete_concrete_type()` pattern. |
| **P1-005** | API Response Change | Add `has_access: bool` field (additive) | Non-breaking change. Preserves list completeness while indicating access state. |

### Judgment Calls vs MASTER_REVIEW.md

| Issue | MASTER_REVIEW Recommendation | Decision Made | Reason |
|:------|:-----------------------------|:--------------|:-------|
| **P1-005** | Filter by `has_permission` OR add `has_access` field | **Add `has_access` field** | Filtering would hide orgs with pending User Permission propagation. Adding field preserves visibility while informing clients. |
| **P1-006** | Add Guest check | **Add Guest check + existence check** | Added `frappe.db.exists()` before `has_permission` for proper 404 vs 403 semantics per API contract. |

---

## 3. Test Impact Assessment

| Task | Test File Impact | Action Required |
|:-----|:-----------------|:----------------|
| P1-004 | `test_organization_api.py:283` | Update test to call `org._create_concrete_type()` if directly testing, or rely on hooks |
| P1-005 | `test_organization_api.py` | Add assertion for `has_access` field in `test_get_user_organizations_returns_all_memberships` |
| P1-006 | `test_organization_api.py` | Existing `test_get_org_members_permission_denied` should still pass; may add validation tests |

---

## 4. Execution Checklist

- [x] Task 1: Fix P1-001 (exception variable)
- [x] Task 2: Fix P1-002 (function signature)
- [x] Task 3: Fix P1-003 (malformed docstring)
- [x] Task 4: Fix P1-004 (method naming)
- [x] Task 5: Fix P1-005 (has_access field)
- [x] Task 6: Fix P1-006 (parameter validation)
- [x] Run test suite to verify fixes (13/13 passed)
- [ ] Stage all changes for commit

---

## 5. Implementation Results

**Date Completed:** 2025-12-14
**Tests Passed:** 13/13 (dartwing.tests.test_organization_api)

### Files Modified

| File | Changes |
|:-----|:--------|
| `dartwing/dartwing_core/doctype/organization/organization.py` | P1-001 (line 383), P1-003 (lines 339-347), P1-004 (lines 234-257) |
| `dartwing/permissions/helpers.py` | P1-002 (line 125) |
| `dartwing/dartwing_core/api/organization_api.py` | P1-005 (line 101), P1-006 (lines 112-187) |
| `dartwing/tests/test_organization_api.py` | Updated to use `_create_concrete_type()` (line 283) |

### Summary of Changes

1. **P1-001:** Added `as e` to capture exception in `LinkExistsError` handler
2. **P1-002:** Fixed function call to pass 3 arguments instead of 2
3. **P1-003:** Removed orphaned code fragments from docstring
4. **P1-004:** Merged docstring and implementation into single `_create_concrete_type()` method
5. **P1-005:** Added `has_access` boolean field to organization list response
6. **P1-006:** Added comprehensive parameter validation with proper 401/403/404 error semantics

---

**STATUS: P1 IMPLEMENTATION COMPLETE - READY FOR STAGING**
