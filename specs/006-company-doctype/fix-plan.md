# Implementation Plan: Fix Code Review Issues (Branch 006)

**Created**: 2025-12-13
**Branch**: `006-company-doctype`
**Reference**: [code-review.md](code-review.md)

---

## Overview

This plan addresses all 16 issues identified in the consolidated code review. Issues are grouped into phases by priority, with each phase building on the previous.

**Estimated Effort**: 4-6 hours total
**Risk Level**: Medium (security fixes required)

---

## Phase 1: Critical Security & Blocking Issues (Must Fix)

### Task 1.1: Fix SQL Injection (CR-001)
**File**: `dartwing/dartwing_company/permissions.py`
**Line**: 33
**Effort**: 5 minutes

**Current Code**:
```python
org_list = ", ".join(f"'{org}'" for org in permitted_orgs)
return f"`tabCompany`.`organization` in ({org_list})"
```

**Fix**:
```python
org_list = ", ".join(frappe.db.escape(org) for org in permitted_orgs)
return f"`tabCompany`.`organization` in ({org_list})"
```

**Verification**:
- Manual test with Organization name containing `'` or `"` characters
- Ensure query still works with normal names

---

### Task 1.2: Fix Permission Enforcement (CR-002)
**File**: `dartwing/dartwing_company/permissions.py`
**Line**: 37-48
**Effort**: 15 minutes

**Current Code**:
```python
def has_permission_company(doc, ptype, user):
    if not user:
        user = frappe.session.user

    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return True

    return frappe.has_permission("Organization", ptype=ptype, doc=doc.organization, user=user)
```

**Fix**:
```python
def has_permission_company(doc, ptype, user):
    """
    Check if user has permission to access a specific Company document.

    Permission is granted if:
    1. User is Administrator or System Manager
    2. User has a User Permission for the linked Organization
    """
    if not user:
        user = frappe.session.user

    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return True

    # Check if user has User Permission for this Organization
    # This allows Company access without requiring direct Organization read permission
    return bool(frappe.db.exists("User Permission", {
        "user": user,
        "allow": "Organization",
        "for_value": doc.organization
    }))
```

**Verification**:
- Create test user with "Dartwing User" role
- Grant User Permission for specific Organization
- Verify user can access linked Company
- Verify user cannot access other Companies

---

### Task 1.3: Fix API PermissionError (CR-003)
**File**: `dartwing/dartwing_company/api.py`
**Line**: 27
**Effort**: 10 minutes

**Current Code**:
```python
company = frappe.get_doc("Company", company_name)
org = frappe.get_doc("Organization", company.organization)

return {
    # ... uses org.org_name, org.org_type, org.status
}
```

**Fix**:
```python
company = frappe.get_doc("Company", company_name)

# Use db.get_value to avoid permission check on Organization
# Users with Company access should see basic org info
org_data = frappe.db.get_value(
    "Organization",
    company.organization,
    ["name", "org_name", "org_type", "status"],
    as_dict=True
)

return {
    "name": company.name,
    "legal_name": company.legal_name,
    "tax_id": company.tax_id,
    "entity_type": company.entity_type,
    "formation_date": company.formation_date,
    "jurisdiction_country": company.jurisdiction_country,
    "jurisdiction_state": company.jurisdiction_state,
    "registered_address": company.registered_address,
    "physical_address": company.physical_address,
    "registered_agent": company.registered_agent,
    "organization": {
        "name": org_data.name if org_data else None,
        "org_name": org_data.org_name if org_data else None,
        "org_type": org_data.org_type if org_data else None,
        "status": org_data.status if org_data else None
    }
}
```

**Verification**:
- Test API as non-admin user with Company User Permission
- Verify org details are returned without PermissionError

---

### Task 1.4: Commit Untracked Files (CR-004)
**Effort**: 5 minutes

**Commands**:
```bash
cd /workspace/bench/apps/dartwing

# Add all new implementation files
git add dartwing/dartwing_company/
git add dartwing/dartwing_core/doctype/organization_officer/
git add dartwing/dartwing_core/doctype/organization_member_partner/
git add dartwing/dartwing_core/mixins/
git add dartwing/tests/

# Add modified files
git add dartwing/dartwing_core/doctype/organization/organization.py
git add dartwing/dartwing_core/doctype/person/person.py
git add dartwing/hooks.py
git add dartwing/modules.txt
git add dartwing/fixtures/role_template.json

# Commit
git commit -m "feat: implement Company DocType with Organization integration

- Add Company DocType with legal entity fields
- Add Organization Officer child table
- Add Organization Member Partner child table
- Add OrganizationMixin for shared properties
- Extend Organization to auto-create Company records
- Add Person deletion protection for Company links
- Add Company permissions module
- Add Company API endpoints
- Add unit and integration tests

🤖 Generated with Claude Code"
```

**Verification**:
- `git status` shows clean working directory
- `git log` shows new commit with all files

---

## Phase 2: High Priority Fixes

### Task 2.1: Make Organization Creation Atomic (CR-005)
**File**: `dartwing/dartwing_core/doctype/organization/organization.py`
**Line**: 72-74
**Effort**: 10 minutes

**Decision Required**: Should Organization creation fail if Company creation fails?

**Option A - Atomic (Recommended)**:
```python
try:
    concrete = frappe.new_doc(concrete_doctype)
    concrete.organization = self.name
    concrete.flags.ignore_permissions = True
    concrete.flags.from_organization = True

    if concrete_doctype == "Family":
        concrete.family_name = self.org_name
        concrete.status = self.status
    elif concrete_doctype == "Company":
        concrete.legal_name = self.org_name

    concrete.insert()

    self.db_set("linked_doctype", concrete_doctype, update_modified=False)
    self.db_set("linked_name", concrete.name, update_modified=False)

    frappe.msgprint(
        _("Created {0}: {1}").format(concrete_doctype, concrete.name),
        alert=True
    )
except Exception as e:
    frappe.log_error(f"Error creating concrete type {concrete_doctype}: {str(e)}")
    frappe.throw(
        _("Failed to create {0} record. Please try again or contact support.").format(concrete_doctype)
    )
```

**Option B - Graceful Degradation** (update spec instead):
- Keep current behavior
- Update spec FR-001 to say "SHOULD" instead of "MUST"
- Add admin tool to create missing concrete records

---

### Task 2.2: Fix ORG_TYPE_MAP Inconsistency (CR-006)
**File**: `dartwing/dartwing_core/doctype/organization/organization.py`
**Line**: 9-15
**Effort**: 5 minutes

**Current Code**:
```python
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Club": "Club",
    "Nonprofit": "Nonprofit",
}
```

**Fix** (add Association):
```python
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Club": "Club",
    "Association": "Association",  # Added for consistency with fixtures
    "Nonprofit": "Nonprofit",
}
```

**Alternative** (if Association should map to Club):
```python
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Club": "Club",
    "Association": "Club",  # Association uses Club DocType
    "Nonprofit": "Nonprofit",
}
```

**Verification**:
- Check Organization.org_type field options
- Check Role Template fixtures for org types
- Ensure consistency across codebase

---

### Task 2.3: Reconcile API Contract Mismatches (CR-007)
**File**: `dartwing/dartwing_company/api.py`
**Effort**: 20 minutes

**Changes Required**:

| Function | Change |
|----------|--------|
| `get_company_with_org_details` | Rename param `company_name` → `company` |
| `get_company_with_org_details` | Update response to match contract structure |
| `validate_ownership` | Rename key `total_ownership_percent` → `total_ownership` |

**Updated `get_company_with_org_details`**:
```python
@frappe.whitelist()
def get_company_with_org_details(company: str) -> dict:
    """
    Get Company record with parent Organization details.

    Args:
        company: The name of the Company document

    Returns:
        dict: Company data with embedded Organization details
    """
    if not frappe.has_permission("Company", doc=company, ptype="read"):
        frappe.throw(_("Not permitted to access this Company"), frappe.PermissionError)

    doc = frappe.get_doc("Company", company)
    org_data = frappe.db.get_value(
        "Organization",
        doc.organization,
        ["name", "org_name", "org_type", "status"],
        as_dict=True
    )

    # Get officers list
    officers = []
    for officer in doc.officers or []:
        person_name = frappe.db.get_value("Person", officer.person, "full_name")
        officers.append({
            "person": officer.person,
            "person_name": person_name,
            "title": officer.title,
            "start_date": str(officer.start_date) if officer.start_date else None,
            "end_date": str(officer.end_date) if officer.end_date else None
        })

    # Get members list
    members = []
    for member in doc.members_partners or []:
        person_name = frappe.db.get_value("Person", member.person, "full_name")
        members.append({
            "person": member.person,
            "person_name": person_name,
            "ownership_percent": member.ownership_percent,
            "capital_contribution": member.capital_contribution,
            "voting_rights": member.voting_rights
        })

    return {
        "message": "success",
        "company": {
            "name": doc.name,
            "legal_name": doc.legal_name,
            "tax_id": doc.tax_id,
            "entity_type": doc.entity_type,
            "formation_date": str(doc.formation_date) if doc.formation_date else None,
            "jurisdiction_country": doc.jurisdiction_country,
            "jurisdiction_state": doc.jurisdiction_state,
            "registered_address": doc.registered_address,
            "physical_address": doc.physical_address,
            "registered_agent": doc.registered_agent
        },
        "org_details": {
            "name": org_data.name if org_data else None,
            "org_name": org_data.org_name if org_data else None,
            "org_type": org_data.org_type if org_data else None,
            "status": org_data.status if org_data else None
        },
        "officers": officers,
        "members": members
    }
```

**Updated `validate_ownership`**:
```python
return {
    "valid": len(warnings) == 0,
    "total_ownership": total_ownership,  # Changed from total_ownership_percent
    "total_voting_rights": total_voting,
    "member_count": len(company.members_partners),
    "warnings": warnings
}
```

**Also update contract** if implementation is preferred:
- Update `specs/006-company-doctype/contracts/api.md` to match implementation

---

## Phase 3: Medium Priority Fixes

### Task 3.1: Remove Audit Logging (CR-008)
**File**: `dartwing/dartwing_company/doctype/company/company.py`
**Effort**: 5 minutes

**Remove these methods entirely** (Frappe's `track_changes: 1` handles this):

```python
# DELETE these methods:
def after_insert(self):
    """Log company creation."""
    self._log_audit_event("Created")

def on_update(self):
    """Log company updates."""
    if not self.is_new():
        self._log_audit_event("Updated")

def on_trash(self):
    """Log company deletion."""
    self._log_audit_event("Deleted")

def _log_audit_event(self, action):
    """Log audit event for company operations."""
    frappe.log_error(...)
```

**Keep only**:
```python
class Company(Document, OrganizationMixin):
    """Company DocType - represents a business entity."""

    def validate(self):
        """Validate company before save."""
        self.validate_ownership_percentage()

    def validate_ownership_percentage(self):
        """Warn if total ownership percentage exceeds 100%."""
        # ... existing code ...
```

---

### Task 3.2: Fix OrganizationMixin N+1 Queries (CR-009)
**File**: `dartwing/dartwing_core/mixins/organization_mixin.py`
**Effort**: 15 minutes

**Replace entire file**:
```python
# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
OrganizationMixin provides access to parent Organization properties
for concrete organization types (Company, Family, Nonprofit, Club).
"""

import frappe


class OrganizationMixin:
    """
    Mixin class that provides access to parent Organization's properties.

    Concrete organization types (Company, Family, etc.) should inherit from
    both Document and OrganizationMixin to get access to org_name, logo,
    and org_status properties.

    Usage:
        class Company(Document, OrganizationMixin):
            pass

    The concrete type must have an 'organization' field linking to Organization.
    """

    def _get_organization_cache(self):
        """
        Lazy-load and cache Organization data.

        Single DB query fetches all needed fields, cached for the request lifetime.
        """
        if not hasattr(self, "_org_cache"):
            if not self.organization:
                self._org_cache = None
            else:
                self._org_cache = frappe.db.get_value(
                    "Organization",
                    self.organization,
                    ["org_name", "logo", "status"],
                    as_dict=True
                )
        return self._org_cache

    def _clear_organization_cache(self):
        """Clear the cached Organization data (call after Organization updates)."""
        if hasattr(self, "_org_cache"):
            delattr(self, "_org_cache")

    @property
    def org_name(self):
        """Get the organization name from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("org_name") if cache else None

    @property
    def logo(self):
        """Get the logo from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("logo") if cache else None

    @property
    def org_status(self):
        """Get the status from the parent Organization."""
        cache = self._get_organization_cache()
        return cache.get("status") if cache else None

    def get_organization_doc(self):
        """Get the full Organization document."""
        if not self.organization:
            return None
        return frappe.get_doc("Organization", self.organization)
```

---

### Task 3.3: Add Percentage Validation (CR-010)
**File**: `dartwing/dartwing_core/doctype/organization_member_partner/organization_member_partner.py`
**Effort**: 10 minutes

**Replace file**:
```python
# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class OrganizationMemberPartner(Document):
    """Child table for LLC members or partnership partners."""

    def validate(self):
        """Validate member/partner record."""
        self.validate_percentages()

    def validate_percentages(self):
        """Ensure percentages are within valid range (0-100)."""
        if self.ownership_percent is not None:
            if self.ownership_percent < 0:
                frappe.throw(
                    _("Ownership percentage cannot be negative"),
                    title=_("Invalid Percentage")
                )
            if self.ownership_percent > 100:
                frappe.throw(
                    _("Ownership percentage cannot exceed 100%"),
                    title=_("Invalid Percentage")
                )

        if self.voting_rights is not None:
            if self.voting_rights < 0:
                frappe.throw(
                    _("Voting rights percentage cannot be negative"),
                    title=_("Invalid Percentage")
                )
            if self.voting_rights > 100:
                frappe.throw(
                    _("Voting rights percentage cannot exceed 100%"),
                    title=_("Invalid Percentage")
                )
```

---

### Task 3.4: Add Permission Integration Tests (CR-012)
**File**: `dartwing/tests/integration/test_company_permissions.py` (new file)
**Effort**: 30 minutes

```python
# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Integration tests for Company permission enforcement (SC-006).
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompanyPermissions(FrappeTestCase):
    """Test Company permission inheritance from Organization."""

    @classmethod
    def setUpClass(cls):
        """Create test user and data."""
        super().setUpClass()

        # Create test user if not exists
        if not frappe.db.exists("User", "testcompanyuser@test.local"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "testcompanyuser@test.local",
                "first_name": "Test",
                "last_name": "CompanyUser",
                "enabled": 1,
                "new_password": "testpassword123"
            })
            user.insert(ignore_permissions=True)
            user.add_roles("Dartwing User")

    @classmethod
    def tearDownClass(cls):
        """Clean up test data."""
        super().tearDownClass()

        # Delete test user permissions
        frappe.db.delete("User Permission", {
            "user": "testcompanyuser@test.local"
        })

        # Delete test organizations and companies
        for org in frappe.get_all("Organization", filters={"org_name": ["like", "__PermTest%"]}):
            frappe.delete_doc("Organization", org.name, force=True, ignore_permissions=True)

    def test_user_can_access_company_with_user_permission(self):
        """User with Organization User Permission can access linked Company."""
        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "__PermTest Accessible Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert(ignore_permissions=True)

        # Grant User Permission
        frappe.get_doc({
            "doctype": "User Permission",
            "user": "testcompanyuser@test.local",
            "allow": "Organization",
            "for_value": org.name
        }).insert(ignore_permissions=True)

        # Test permission as test user
        frappe.set_user("testcompanyuser@test.local")

        try:
            # Should be able to read Company
            company = frappe.get_doc("Company", org.linked_name)
            self.assertEqual(company.organization, org.name)
        finally:
            frappe.set_user("Administrator")

    def test_user_cannot_access_company_without_user_permission(self):
        """User without Organization User Permission cannot access Company."""
        # Create Organization and Company (no User Permission granted)
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "__PermTest Inaccessible Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert(ignore_permissions=True)

        # Test permission as test user
        frappe.set_user("testcompanyuser@test.local")

        try:
            # Should NOT be able to read Company
            with self.assertRaises(frappe.PermissionError):
                frappe.get_doc("Company", org.linked_name)
        finally:
            frappe.set_user("Administrator")

    def test_api_works_with_user_permission(self):
        """API endpoint works for user with appropriate permission."""
        from dartwing.dartwing_company.api import get_company_with_org_details

        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "__PermTest API Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert(ignore_permissions=True)

        # Grant User Permission
        frappe.get_doc({
            "doctype": "User Permission",
            "user": "testcompanyuser@test.local",
            "allow": "Organization",
            "for_value": org.name
        }).insert(ignore_permissions=True)

        # Test API as test user
        frappe.set_user("testcompanyuser@test.local")

        try:
            result = get_company_with_org_details(org.linked_name)
            self.assertIsNotNone(result)
            self.assertEqual(result.get("organization", {}).get("name"), org.name)
        finally:
            frappe.set_user("Administrator")
```

---

## Phase 4: Low Priority Fixes

### Task 4.1: Address Deletion Protection (CR-011)
**File**: `dartwing/hooks.py`
**Effort**: 15 minutes

**Add to doc_events**:
```python
doc_events = {
    # ... existing entries ...
    "Address": {
        "before_delete": "dartwing.dartwing_company.utils.check_address_company_links"
    }
}
```

**Create file** `dartwing/dartwing_company/utils.py`:
```python
# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def check_address_company_links(doc, method):
    """Prevent deletion of Address linked to Company."""
    if not frappe.db.exists("DocType", "Company"):
        return

    links = frappe.get_all(
        "Company",
        filters={
            "registered_address": doc.name
        },
        limit=1
    )

    if links:
        frappe.throw(
            _("Cannot delete Address '{0}' - it is linked as registered address to Company").format(doc.name),
            frappe.LinkExistsError
        )

    links = frappe.get_all(
        "Company",
        filters={
            "physical_address": doc.name
        },
        limit=1
    )

    if links:
        frappe.throw(
            _("Cannot delete Address '{0}' - it is linked as physical address to Company").format(doc.name),
            frappe.LinkExistsError
        )
```

---

### Task 4.2: Improve Test Cleanup Patterns (CR-013, CR-014)
**File**: `dartwing/dartwing_company/doctype/company/test_company.py`
**Effort**: 15 minutes

**Update cleanup to use unique prefix**:
```python
import uuid

class TestCompany(FrappeTestCase):
    TEST_PREFIX = f"__Test_{uuid.uuid4().hex[:8]}_"

    def _cleanup_test_data(self):
        """Remove test Organizations and Companies."""
        # Use unique prefix to avoid deleting real data
        for company in frappe.get_all("Company", filters={"legal_name": ["like", f"{self.TEST_PREFIX}%"]}):
            frappe.delete_doc("Company", company.name, force=True)

        for org in frappe.get_all("Organization", filters={"org_name": ["like", f"{self.TEST_PREFIX}%"]}):
            frappe.delete_doc("Organization", org.name, force=True)

        for person in frappe.get_all("Person", filters={"primary_email": ["like", f"{self.TEST_PREFIX}%"]}):
            frappe.delete_doc("Person", person.name, force=True)

    def test_company_auto_creation_from_organization(self):
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Auto Company",
            "org_type": "Company",
            "status": "Active"
        })
        # ... rest of test
```

---

### Task 4.3: Add Type Hints (CR-015)
**File**: `dartwing/dartwing_company/api.py`
**Effort**: 10 minutes

**Update function signatures**:
```python
@frappe.whitelist()
def get_company_with_org_details(company: str) -> dict:
    ...

@frappe.whitelist()
def get_user_companies(user: str | None = None) -> list[dict]:
    ...

@frappe.whitelist()
def validate_ownership(company: str) -> dict:
    ...
```

---

### Task 4.4: Remove Redundant JS (CR-016)
**File**: `dartwing/dartwing_company/doctype/company/company.js`
**Effort**: 2 minutes

**Remove redundant refresh handler** (already set in JSON):
```javascript
frappe.ui.form.on("Company", {
    entity_type: function(frm) {
        if (!frm.is_new() && frm.doc.members_partners && frm.doc.members_partners.length > 0) {
            frappe.msgprint({
                title: __("Warning"),
                indicator: "orange",
                message: __(
                    "Changing the entity type may affect the ownership section visibility. " +
                    "The ownership section is only visible for LLC, Limited Partnership (LP), LLP, and General Partnership entity types."
                )
            });
        }
    }
    // Removed: refresh handler that set organization read_only (already in JSON)
});
```

---

## Execution Order

```
Phase 1 (Critical - Block merge without these)
├── Task 1.1: Fix SQL Injection
├── Task 1.2: Fix Permission Enforcement
├── Task 1.3: Fix API PermissionError
└── Task 1.4: Commit Untracked Files

Phase 2 (High - Should fix before merge)
├── Task 2.1: Make Organization Creation Atomic
├── Task 2.2: Fix ORG_TYPE_MAP
└── Task 2.3: Reconcile API Contract

Phase 3 (Medium - Recommended)
├── Task 3.1: Remove Audit Logging
├── Task 3.2: Fix N+1 Queries
├── Task 3.3: Add Percentage Validation
└── Task 3.4: Add Permission Tests

Phase 4 (Low - Nice to have)
├── Task 4.1: Address Deletion Protection
├── Task 4.2: Improve Test Cleanup
├── Task 4.3: Add Type Hints
└── Task 4.4: Remove Redundant JS
```

---

## Verification Checklist

After all fixes:

- [ ] `bench --site [site] migrate` succeeds
- [ ] `bench --site [site] run-tests --app dartwing` passes
- [ ] Manual test: Create Organization with org_type="Company"
- [ ] Manual test: Non-admin user can access Company with User Permission
- [ ] Manual test: Non-admin user cannot access Company without permission
- [ ] Manual test: API endpoints work for authorized users
- [ ] Manual test: Ownership >100% shows warning but saves
- [ ] Manual test: Negative ownership throws error
- [ ] `git status` shows clean working directory
- [ ] `git log` shows all implementation commits

---

## Commit Strategy

**Option A: Single fix commit**
```bash
git add -A
git commit -m "fix: address code review issues for Company DocType

- Fix SQL injection in permissions.py (CR-001)
- Fix permission enforcement for non-admin users (CR-002)
- Fix API PermissionError when fetching Organization (CR-003)
- Make Organization creation atomic (CR-005)
- Fix ORG_TYPE_MAP inconsistency (CR-006)
- Reconcile API contract mismatches (CR-007)
- Remove inappropriate audit logging (CR-008)
- Fix OrganizationMixin N+1 queries (CR-009)
- Add percentage validation (CR-010)
- Add permission integration tests (CR-012)
- Minor test and code quality improvements

🤖 Generated with Claude Code"
```

**Option B: Separate commits per phase** (preferred for code review)
- Phase 1: "fix: critical security and blocking issues"
- Phase 2: "fix: high priority spec compliance issues"
- Phase 3: "fix: medium priority improvements"
- Phase 4: "chore: low priority cleanup"
