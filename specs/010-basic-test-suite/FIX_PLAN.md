# FIX PLAN: 010-basic-test-suite (P1-Critical Issues)

**Branch:** 010-basic-test-suite
**Module:** dartwing_core
**Date:** 2025-12-16
**Status:** APPROVED - Ready for Execution
**Scope:** P1-Critical Issues Only (8 tasks)

---

## Executive Summary

This fix plan addresses **8 P1-Critical issues** identified in MASTER_REVIEW.md that prevent merge of the Basic Test Suite branch. All fixes align with architectural constraints from `dartwing_core_arch.md` and `dartwing_core_prd.md`.

**Estimated Execution Time:** 4-6 hours
**Risk Level:** Medium (involves test refactoring and schema changes)
**Dependencies:** None (all tasks can be executed sequentially)

---

## Task Breakdown

### TASK 1: Remove "Club" from ORG_TYPE_MAP ✅
**Issue ID:** P1-007
**Priority:** Critical
**Complexity:** Low

**Files to Modify:**
- `dartwing/dartwing_core/doctype/organization/organization.py` (line 26)

**Changes:**
```python
# BEFORE:
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Club": "Club",  # ← REMOVE THIS LINE
    "Association": "Association",
    "Nonprofit": "Nonprofit",
}

# AFTER:
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Association": "Association",
    "Nonprofit": "Nonprofit",
}
```

**Rationale:** Per PRD Section 3.4, Association type covers clubs via `association_type` field. "Club" should not be a root organization type.

**Validation:**
```bash
python -m py_compile dartwing/dartwing_core/doctype/organization/organization.py
```

---

### TASK 2: Implement fetch_from for Company Synced Fields ✅
**Issue ID:** P1-003
**Priority:** Critical
**Complexity:** Medium

**Files to Modify:**
1. `dartwing/dartwing_company/doctype/company/company.json` (lines 42-49, 61-69)
2. `dartwing/dartwing_core/doctype/organization/organization.py` (lines 33-38)

**Changes to company.json:**
```json
// Field: company_name (line 42-49)
{
  "fieldname": "company_name",
  "fieldtype": "Data",
  "label": "Company Name",
  "reqd": 1,
  "in_list_view": 1,
  "in_standard_filter": 1,
  "fetch_from": "organization.org_name",  // ← ADD THIS
  "read_only": 1,  // ← ADD THIS
  "description": "Display name of the company (synced from Organization)"
}

// Field: status (line 61-69)
{
  "fieldname": "status",
  "fieldtype": "Select",
  "label": "Status",
  "options": "Active\\nInactive",
  "default": "Active",
  "in_list_view": 1,
  "in_standard_filter": 1,
  "fetch_from": "organization.status",  // ← ADD THIS
  "read_only": 1,  // ← ADD THIS
  "description": "Company status (synced from Organization)"
}
```

**Changes to organization.py:**
```python
# BEFORE:
ORG_FIELD_MAP = {
    "Family": {"name_field": "family_name", "status_field": "status"},
    "Company": {"name_field": "company_name", "status_field": "status"},  # ← REMOVE THIS LINE
    "Association": {"name_field": "association_name", "status_field": "status"},
    "Nonprofit": {"name_field": "nonprofit_name", "status_field": "status"},
}

# AFTER:
ORG_FIELD_MAP = {
    "Family": {"name_field": "family_name", "status_field": "status"},
    "Association": {"name_field": "association_name", "status_field": "status"},
    "Nonprofit": {"name_field": "nonprofit_name", "status_field": "status"},
}
```

**Rationale:** Frappe's native `fetch_from` mechanism automatically propagates changes from Organization to Company, preventing data drift. Aligns with Single Source of Truth principle (constitution.md Section 1).

**Validation:**
```bash
python -m json.tool dartwing/dartwing_company/doctype/company/company.json
python -m py_compile dartwing/dartwing_core/doctype/organization/organization.py
```

---

### TASK 3: Fix Test Helper Creation Flow to Organization-First ✅
**Issue ID:** P1-001
**Priority:** Critical
**Complexity:** High

**Files to Modify:**
- `dartwing/tests/integration/test_full_workflow.py` (lines 138-152)

**Changes:**
```python
# BEFORE (concrete-first - WRONG):
def _create_test_organization(self, name_suffix, org_type="Family"):
    """Helper to create a test Organization with concrete type."""
    # Create concrete type first which triggers Organization creation
    concrete_doctype = org_type
    name_field = f"{org_type.lower()}_name"

    concrete = frappe.get_doc({
        "doctype": concrete_doctype,
        name_field: f"{TEST_PREFIX}{org_type} {name_suffix}"
    })
    concrete.insert(ignore_permissions=True)
    concrete.reload()

    org = frappe.get_doc("Organization", concrete.organization)
    return org, concrete

# AFTER (Organization-first - CORRECT):
def _create_test_organization(self, name_suffix, org_type="Family"):
    """Helper to create a test Organization with concrete type.

    Creates Organization first, which triggers hook to create concrete type.
    This matches production behavior and tests the bidirectional linking hooks.
    """
    # Step 1: Create Organization with org_type
    org = frappe.get_doc({
        "doctype": "Organization",
        "org_name": f"{TEST_PREFIX}{org_type} {name_suffix}",
        "org_type": org_type,
        "status": "Active"
    })
    org.insert(ignore_permissions=True)

    # Step 2: Reload to get hook-populated linked_doctype and linked_name
    org.reload()

    # Step 3: Fetch the concrete type created by hooks
    if not org.linked_doctype or not org.linked_name:
        raise ValueError(f"Organization hook failed to create concrete type for {org.name}")

    concrete = frappe.get_doc(org.linked_doctype, org.linked_name)

    return org, concrete
```

**Rationale:** Per dartwing_core_arch.md Section 3.2, Organization MUST be created first. Hooks automatically create and link the concrete type. This change:
1. Matches production behavior users will encounter
2. Enforces schema constraints (Company.organization is mandatory)
3. Tests the actual hook logic critical to data integrity
4. Prevents architectural drift

**Validation:**
```bash
bench --site <site> run-tests --app dartwing --module dartwing.tests.integration.test_full_workflow
```

---

### TASK 4: Remove OrganizationMixin Tests (Out of Scope) ✅
**Issue ID:** P1-004
**Priority:** Critical
**Complexity:** Low

**Files to Remove:**
- `dartwing/dartwing_core/mixins/test_organization_mixin.py` (327 lines)

**Command:**
```bash
git rm dartwing/dartwing_core/mixins/test_organization_mixin.py
```

**Rationale:** Feature 8 (OrganizationMixin) is sequenced AFTER Feature 10 (Basic Test Suite) per dartwing_core_features_priority.md. Tests should not precede implementation. This prevents:
1. False test coverage (tests for unimplemented features)
2. Scope creep into this branch
3. Confusion about what's actually implemented

Feature 8 should be its own branch with: spec → implementation → tests.

**Validation:**
```bash
# Verify file is staged for deletion
git status
# Verify tests still run without errors
bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.mixins
```

---

### TASK 5: Change Test Users from System Manager to Dartwing User ✅
**Issue ID:** P1-005
**Priority:** Critical
**Complexity:** Medium

**Files to Modify:**
- `dartwing/tests/integration/test_full_workflow.py` (line 119)

**Changes:**
```python
# BEFORE:
def _create_test_user(self, name_suffix):
    """Helper to create a test Frappe User."""
    email = f"{TEST_PREFIX}{name_suffix}@workflow.test"
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": "Workflow",
            "last_name": f"Test {name_suffix}",
            "enabled": 1,
            "user_type": "System User",
            "roles": [{"role": "System Manager"}]  # ← CHANGE THIS
        })
        user.flags.ignore_permissions = True
        user.insert(ignore_permissions=True)
    return email

# AFTER:
def _create_test_user(self, name_suffix):
    """Helper to create a test Frappe User.

    Creates user with Dartwing User role to properly test permission enforcement.
    System Manager role bypasses all User Permission checks, which defeats the
    purpose of testing Feature 5 (User Permission Propagation).
    """
    email = f"{TEST_PREFIX}{name_suffix}@workflow.test"
    if not frappe.db.exists("User", email):
        user = frappe.get_doc({
            "doctype": "User",
            "email": email,
            "first_name": "Workflow",
            "last_name": f"Test {name_suffix}",
            "enabled": 1,
            "user_type": "System User",
            "roles": [{"role": "Dartwing User"}]  # Standard member role
        })
        user.flags.ignore_permissions = True
        user.insert(ignore_permissions=True)
    return email
```

**Additional Changes Required:**
Update test assertions in workflow tests to explicitly verify permission enforcement. Tests should verify:
1. User CAN access organizations they're members of
2. User CANNOT access other organizations (expect `frappe.PermissionError`)

**Rationale:** Per dartwing_core_arch.md Section 8.2.2, Dartwing User is the standard member role. System Manager bypasses all User Permission checks. Tests must use realistic roles to properly validate Feature 5 (User Permission Propagation).

**Validation:**
```bash
bench --site <site> run-tests --app dartwing --module dartwing.tests.integration.test_full_workflow
```

---

### TASK 6: Refactor Test Cleanup to Surface Real Bugs ✅
**Issue ID:** P1-008
**Priority:** Critical
**Complexity:** Medium

**Files to Modify:**
- `dartwing/tests/test_permission_api.py` (lines 67-106)

**Changes:**
```python
# BEFORE (broad exception handling - masks bugs):
def _cleanup_test_data(self):
    """Helper to clean up all test data."""
    # ... cleanup logic with:
    except (frappe.DoesNotExistError, frappe.LinkExistsError):
        # Concrete type may have already been deleted or has links
        pass  # ← WRONG: silently swallows bugs

# AFTER (selective exception handling - surfaces bugs):
def _cleanup_test_data(self):
    """Helper to clean up all test data in reverse dependency order."""

    # 1. Clean up User Permissions first (no dependencies)
    for perm_name in frappe.get_all(
        "User Permission",
        filters={"user": ["like", f"%{TEST_PREFIX}%"]},
        pluck="name"
    ):
        try:
            frappe.delete_doc("User Permission", perm_name, force=True, ignore_permissions=True)
        except frappe.DoesNotExistError:
            pass  # Already deleted - this is expected

    # 2. Clean up Org Members (depends on Person and Organization)
    test_person_names = frappe.get_all(
        "Person",
        filters={"primary_email": ["like", f"%{TEST_PREFIX}%"]},
        pluck="name"
    )
    if test_person_names:
        for member_name in frappe.get_all(
            "Org Member",
            filters={"person": ["in", test_person_names]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Org Member", member_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass

    # 3. Clean up Organizations (will cascade to concrete types via hooks)
    for org_name in frappe.get_all(
        "Organization",
        filters={"org_name": ["like", f"{TEST_PREFIX}%"]},
        pluck="name"
    ):
        try:
            frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
        except frappe.DoesNotExistError:
            pass
        except frappe.LinkExistsError as e:
            # This should NOT happen - log it as potential bug
            frappe.log_error(
                f"LinkExistsError during test cleanup for {org_name}: {str(e)}",
                "Test Cleanup Error"
            )
            # Force delete blocking links then retry
            frappe.db.sql("DELETE FROM `tabOrg Member` WHERE organization = %s", org_name)
            frappe.db.commit()
            frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)

    # 4. Clean up Persons (no longer referenced by Org Members)
    for person_name in frappe.get_all(
        "Person",
        filters={"primary_email": ["like", f"%{TEST_PREFIX}%"]},
        pluck="name"
    ):
        try:
            frappe.delete_doc("Person", person_name, force=True, ignore_permissions=True)
        except frappe.DoesNotExistError:
            pass
```

**Rationale:** Per SC-005 requirement (zero test flakiness), cleanup must not mask deletion hook bugs. Proper cleanup order prevents LinkExistsError cascades. Selective exception handling surfaces real bugs during test development.

**Validation:**
```bash
bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_api
```

---

### TASK 7: Verify and Fix Duplicate Dictionary Keys ⚠️
**Issue ID:** P1-002
**Priority:** Critical
**Complexity:** Low
**Status:** VERIFICATION NEEDED

**Files to Check:**
- `dartwing/hooks.py` (lines 121-136)

**Investigation Plan:**
1. Read complete hooks.py file
2. Verify no duplicate keys in `permission_query_conditions` and `has_permission` dictionaries
3. If duplicates found: remove duplicates and consolidate to single entry per DocType
4. Run `python -m py_compile dartwing/hooks.py`

**Note:** Initial file read showed NO duplicates. This task may be marked as already-fixed/non-issue after comprehensive verification.

**Rationale:** Python silently overwrites duplicate dictionary keys, breaking permission system integrity.

**Validation:**
```bash
python -m py_compile dartwing/hooks.py
# Check for duplicate keys programmatically
python -c "import ast; ast.parse(open('dartwing/hooks.py').read())"
```

---

### TASK 8: Verify Organization.py Code Structure ⚠️
**Issue ID:** P1-006
**Priority:** Critical
**Complexity:** Low
**Status:** VERIFICATION NEEDED

**Files to Check:**
- `dartwing/dartwing_core/doctype/organization/organization.py` (reported issues at lines 257-258, 339-346)

**Investigation Plan:**
1. Read complete organization.py file
2. Verify all methods have proper docstrings
3. Verify all exception handlers are complete
4. Verify no orphaned documentation
5. Run `python -m py_compile` on the file

**Rationale:** Code structure integrity is fundamental to maintainability. Orphaned docstrings and incomplete exception handlers indicate failed refactoring.

**Validation:**
```bash
python -m py_compile dartwing/dartwing_core/doctype/organization/organization.py
bench --site <site> run-tests --module dartwing.dartwing_core.doctype.organization.test_organization
```

---

## Validation Checklist (Post-Execution)

After completing all tasks, verify:

```bash
# 1. Python syntax validation (no compilation errors)
python -m py_compile dartwing/hooks.py
python -m py_compile dartwing/dartwing_core/doctype/organization/organization.py
python -m json.tool dartwing/dartwing_company/doctype/company/company.json

# 2. Git status check
git status  # Should show modified files, one deleted file

# 3. Run full test suite (all tests pass or skip gracefully)
bench --site <site> run-tests --app dartwing

# 4. Verify zero flakiness (run 3 times, all pass)
for i in {1..3}; do
    echo "Run $i/3"
    bench --site <site> run-tests --app dartwing || exit 1
done

# 5. Check for leftover test data (clean slate)
bench --site <site> console
>>> frappe.db.count("Organization", {"org_name": ["like", "%Test%"]})
# Should be 0
```

---

## Risk Assessment

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Tests fail after Organization-first refactor | Medium | High | Comprehensive testing after TASK 3; may reveal hook issues |
| fetch_from breaks existing Company records | Low | Medium | Test on dev site first; migration may be needed |
| Removing mixin tests causes import errors | Low | Low | Git rm ensures clean removal; verify imports |
| Dartwing User role doesn't exist on test site | Medium | High | Check fixtures loaded; add programmatic role creation |

---

## Architectural Compliance Summary

All fixes comply with:
- ✅ `dartwing_core_arch.md` Section 3.2 (Organization-first lifecycle)
- ✅ `dartwing_core_arch.md` Section 8.2.2 (Role hierarchy)
- ✅ `dartwing_core_prd.md` Section 3.4 (Organization types)
- ✅ `constitution.md` Section 1 (Single Source of Truth)
- ✅ `constitution.md` Section 5 (Role-based access control)
- ✅ `dartwing_core_features_priority.md` (Feature sequencing)

---

**End of Fix Plan**

**Next Step:** Execute tasks sequentially, validate after each task, and prepare final commit message.
