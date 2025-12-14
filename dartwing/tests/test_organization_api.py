# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Tests for Organization API helpers.

This module tests the whitelisted API methods for organization data access:
- get_user_organizations()
- get_organization_with_details()
- get_concrete_doc()
- get_org_members()
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestOrganizationAPI(FrappeTestCase):
    """Test cases for Organization API methods."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        super().setUpClass()

        # Create test user for permission tests
        if not frappe.db.exists("User", "apitest@example.com"):
            cls.test_user = frappe.get_doc({
                "doctype": "User",
                "email": "apitest@example.com",
                "first_name": "API",
                "last_name": "Test",
                "enabled": 1,
                "user_type": "System User",
            })
            cls.test_user.insert(ignore_permissions=True)
        else:
            cls.test_user = frappe.get_doc("User", "apitest@example.com")

        # Create test user without any permissions
        if not frappe.db.exists("User", "noperm@example.com"):
            cls.no_perm_user = frappe.get_doc({
                "doctype": "User",
                "email": "noperm@example.com",
                "first_name": "No",
                "last_name": "Permission",
                "enabled": 1,
                "user_type": "System User",
            })
            cls.no_perm_user.insert(ignore_permissions=True)
        else:
            cls.no_perm_user = frappe.get_doc("User", "noperm@example.com")

        # Create test Person linked to test user
        if not frappe.db.exists("Person", {"frappe_user": "apitest@example.com"}):
            cls.test_person = frappe.get_doc({
                "doctype": "Person",
                "first_name": "API",
                "last_name": "Tester",
                "primary_email": "apitest@example.com",
                "frappe_user": "apitest@example.com",
            })
            cls.test_person.insert(ignore_permissions=True)
        else:
            cls.test_person = frappe.get_doc(
                "Person", {"frappe_user": "apitest@example.com"}
            )

        # Create a second Person linked to no_perm_user
        if not frappe.db.exists("Person", {"frappe_user": "noperm@example.com"}):
            cls.no_perm_person = frappe.get_doc({
                "doctype": "Person",
                "first_name": "No",
                "last_name": "Permission",
                "primary_email": "noperm@example.com",
                "frappe_user": "noperm@example.com",
            })
            cls.no_perm_person.insert(ignore_permissions=True)
        else:
            cls.no_perm_person = frappe.get_doc(
                "Person", {"frappe_user": "noperm@example.com"}
            )

        # Create test Organization (Company type) - auto-creates linked Company
        if not frappe.db.exists("Organization", {"org_name": "API Test Company"}):
            cls.test_company_org = frappe.get_doc({
                "doctype": "Organization",
                "org_name": "API Test Company",
                "org_type": "Company",
            })
            cls.test_company_org.insert(ignore_permissions=True)
        else:
            cls.test_company_org = frappe.get_doc(
                "Organization", {"org_name": "API Test Company"}
            )

        # Create test Organization (Family type) - auto-creates linked Family
        if not frappe.db.exists("Organization", {"org_name": "API Test Family"}):
            cls.test_family_org = frappe.get_doc({
                "doctype": "Organization",
                "org_name": "API Test Family",
                "org_type": "Family",
            })
            cls.test_family_org.insert(ignore_permissions=True)
        else:
            cls.test_family_org = frappe.get_doc(
                "Organization", {"org_name": "API Test Family"}
            )

        # Create Organization with no linked concrete type for testing
        if not frappe.db.exists("Organization", {"org_name": "API Test Unlinked"}):
            cls.unlinked_org = frappe.get_doc({
                "doctype": "Organization",
                "org_name": "API Test Unlinked",
                "org_type": "Company",
            })
            cls.unlinked_org.flags.skip_concrete_type = True
            cls.unlinked_org.insert(ignore_permissions=True)
        else:
            cls.unlinked_org = frappe.get_doc(
                "Organization", {"org_name": "API Test Unlinked"}
            )

    def setUp(self):
        """Set up before each test."""
        super().setUp()
        frappe.set_user("Administrator")

    def tearDown(self):
        """Clean up after each test."""
        super().tearDown()
        frappe.set_user("Administrator")
        # Clean up Org Member records created during tests
        for member in frappe.get_all(
            "Org Member",
            filters={"person": ["in", [self.test_person.name, self.no_perm_person.name]]},
        ):
            try:
                frappe.delete_doc("Org Member", member.name, force=True)
            except Exception:
                pass
        frappe.db.commit()

    # =========================================================================
    # User Story 1: get_user_organizations tests
    # =========================================================================

    def test_get_user_organizations_returns_all_memberships(self):
        """Test that get_user_organizations returns all organizations user belongs to."""
        from dartwing.dartwing_core.api.organization_api import get_user_organizations

        # Create memberships for test_person in both organizations
        member1 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": self.test_company_org.name,
            "role": "Employee",
            "status": "Active",
        })
        member1.insert(ignore_permissions=True)

        member2 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": self.test_family_org.name,
            "role": "Parent",
            "status": "Active",
        })
        member2.insert(ignore_permissions=True)

        # Switch to test user and call API
        frappe.set_user("apitest@example.com")
        result = get_user_organizations()

        # Verify response structure
        self.assertIn("data", result)
        self.assertIn("total_count", result)
        self.assertEqual(result["total_count"], 2)
        self.assertEqual(len(result["data"]), 2)

        # Verify organization data is returned
        org_names = {org["name"] for org in result["data"]}
        self.assertIn(self.test_company_org.name, org_names)
        self.assertIn(self.test_family_org.name, org_names)

        # Verify expected fields are present
        for org in result["data"]:
            self.assertIn("name", org)
            self.assertIn("org_name", org)
            self.assertIn("org_type", org)
            self.assertIn("status", org)
            self.assertIn("role", org)
            self.assertIn("membership_status", org)
            self.assertIn("is_supervisor", org)

    def test_get_user_organizations_empty_for_no_memberships(self):
        """Test that get_user_organizations returns empty list for user with no memberships."""
        from dartwing.dartwing_core.api.organization_api import get_user_organizations

        # Use no_perm_user who has no memberships
        frappe.set_user("noperm@example.com")
        result = get_user_organizations()

        # Verify empty response
        self.assertEqual(result["data"], [])
        self.assertEqual(result["total_count"], 0)

    def test_get_user_organizations_requires_authentication(self):
        """Test that get_user_organizations requires authentication."""
        from dartwing.dartwing_core.api.organization_api import get_user_organizations

        # Switch to Guest user
        frappe.set_user("Guest")

        # Should raise AuthenticationError
        with self.assertRaises(frappe.AuthenticationError):
            get_user_organizations()

    # =========================================================================
    # User Story 2: get_organization_with_details tests
    # =========================================================================

    def test_get_organization_with_details_returns_concrete_type(self):
        """Test that get_organization_with_details returns Organization with nested concrete_type."""
        from dartwing.dartwing_core.doctype.organization.organization import (
            get_organization_with_details,
        )

        # Call API as Administrator (has full permissions)
        result = get_organization_with_details(self.test_company_org.name)

        # Verify Organization fields
        self.assertEqual(result["name"], self.test_company_org.name)
        self.assertEqual(result["org_name"], "API Test Company")
        self.assertEqual(result["org_type"], "Company")

        # Verify concrete_type is nested
        self.assertIn("concrete_type", result)
        if result["concrete_type"]:
            self.assertIn("doctype", result["concrete_type"])
            self.assertEqual(result["concrete_type"]["doctype"], "Company")

    def test_get_organization_with_details_permission_denied(self):
        """Test that get_organization_with_details returns PermissionError for unauthorized access."""
        from dartwing.dartwing_core.doctype.organization.organization import (
            get_organization_with_details,
        )

        # Switch to user with no permissions
        frappe.set_user("noperm@example.com")

        # Should raise PermissionError
        with self.assertRaises(frappe.PermissionError):
            get_organization_with_details(self.test_company_org.name)

    def test_get_organization_with_details_not_found(self):
        """Test that get_organization_with_details returns DoesNotExistError for missing org."""
        from dartwing.dartwing_core.doctype.organization.organization import (
            get_organization_with_details,
        )

        # Should raise DoesNotExistError
        with self.assertRaises(frappe.DoesNotExistError):
            get_organization_with_details("NonExistent-Organization-12345")

    # =========================================================================
    # User Story 3: get_concrete_doc tests
    # =========================================================================

    def test_get_concrete_doc_returns_family_fields(self):
        """Test that get_concrete_doc returns only concrete type fields."""
        from dartwing.dartwing_core.doctype.organization.organization import (
            get_concrete_doc,
        )

        # Reload the org to ensure we have fresh data
        self.test_family_org.reload()

        # Ensure the organization has a linked concrete type
        # (may not exist if created in previous test run)
        if not self.test_family_org.linked_name:
            # Create the concrete type if missing
            self.test_family_org._create_concrete_type()
            self.test_family_org.reload()

        # Call API for Family organization
        result = get_concrete_doc(self.test_family_org.name)

        # Verify it returns the Family document
        self.assertIsNotNone(result, "Expected concrete doc but got None. linked_name: %s, linked_doctype: %s" % (
            self.test_family_org.linked_name, self.test_family_org.linked_doctype
        ))
        self.assertEqual(result["doctype"], "Family")
        self.assertIn("family_name", result)

        # Verify Organization-specific fields are NOT in the result
        # (the result should be just the Family doc, not wrapped)
        self.assertNotIn("org_type", result)

    def test_get_concrete_doc_returns_null_when_unlinked(self):
        """Test that get_concrete_doc returns None when org has no linked concrete type."""
        from dartwing.dartwing_core.doctype.organization.organization import (
            get_concrete_doc,
        )

        # Clear the linked_name to simulate unlinked org
        frappe.db.set_value(
            "Organization", self.unlinked_org.name, "linked_name", None
        )
        frappe.db.commit()

        # Call API
        result = get_concrete_doc(self.unlinked_org.name)

        # Verify null is returned
        self.assertIsNone(result)

    def test_get_concrete_doc_permission_check(self):
        """Test that get_concrete_doc enforces permission checks."""
        from dartwing.dartwing_core.doctype.organization.organization import (
            get_concrete_doc,
        )

        # Switch to user with no permissions
        frappe.set_user("noperm@example.com")

        # Should raise PermissionError
        with self.assertRaises(frappe.PermissionError):
            get_concrete_doc(self.test_family_org.name)

    # =========================================================================
    # User Story 4: get_org_members tests
    # =========================================================================

    def test_get_org_members_returns_all_members(self):
        """Test that get_org_members returns all members of an organization."""
        from dartwing.dartwing_core.api.organization_api import get_org_members

        # Create multiple members
        member1 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": self.test_company_org.name,
            "role": "Manager",
            "status": "Active",
        })
        member1.insert(ignore_permissions=True)

        member2 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.no_perm_person.name,
            "organization": self.test_company_org.name,
            "role": "Employee",
            "status": "Active",
        })
        member2.insert(ignore_permissions=True)

        # Call API as Administrator
        result = get_org_members(self.test_company_org.name)

        # Verify response structure
        self.assertIn("data", result)
        self.assertIn("total_count", result)
        self.assertIn("limit", result)
        self.assertIn("offset", result)
        self.assertEqual(result["total_count"], 2)
        self.assertEqual(len(result["data"]), 2)

        # Verify expected fields in member data
        for member in result["data"]:
            self.assertIn("name", member)
            self.assertIn("person", member)
            self.assertIn("member_name", member)
            self.assertIn("role", member)
            self.assertIn("status", member)
            self.assertIn("is_supervisor", member)

    def test_get_org_members_pagination(self):
        """Test that get_org_members supports pagination via limit/offset."""
        from dartwing.dartwing_core.api.organization_api import get_org_members

        # Create 3 members
        member1 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": self.test_company_org.name,
            "role": "Manager",
            "status": "Active",
        })
        member1.insert(ignore_permissions=True)

        member2 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.no_perm_person.name,
            "organization": self.test_company_org.name,
            "role": "Employee",
            "status": "Active",
        })
        member2.insert(ignore_permissions=True)

        # Test limit
        result = get_org_members(self.test_company_org.name, limit=1)
        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(result["total_count"], 2)
        self.assertEqual(result["limit"], 1)

        # Test offset
        result = get_org_members(self.test_company_org.name, limit=1, offset=1)
        self.assertEqual(len(result["data"]), 1)
        self.assertEqual(result["offset"], 1)

        # Test limit capping (max 100)
        result = get_org_members(self.test_company_org.name, limit=200)
        self.assertEqual(result["limit"], 100)

    def test_get_org_members_status_filter(self):
        """Test that get_org_members filters by member status."""
        from dartwing.dartwing_core.api.organization_api import get_org_members

        # Create active member
        member1 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": self.test_company_org.name,
            "role": "Manager",
            "status": "Active",
        })
        member1.insert(ignore_permissions=True)

        # Create inactive member
        member2 = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.no_perm_person.name,
            "organization": self.test_company_org.name,
            "role": "Employee",
            "status": "Inactive",
        })
        member2.insert(ignore_permissions=True)

        # Get only active members
        result = get_org_members(self.test_company_org.name, status="Active")
        self.assertEqual(result["total_count"], 1)
        self.assertEqual(result["data"][0]["status"], "Active")

        # Get only inactive members
        result = get_org_members(self.test_company_org.name, status="Inactive")
        self.assertEqual(result["total_count"], 1)
        self.assertEqual(result["data"][0]["status"], "Inactive")

        # Get all members (no filter)
        result = get_org_members(self.test_company_org.name)
        self.assertEqual(result["total_count"], 2)

    def test_get_org_members_permission_denied(self):
        """Test that get_org_members returns PermissionError for unauthorized access."""
        from dartwing.dartwing_core.api.organization_api import get_org_members

        # Switch to user with no permissions
        frappe.set_user("noperm@example.com")

        # Should raise PermissionError
        with self.assertRaises(frappe.PermissionError):
            get_org_members(self.test_company_org.name)
