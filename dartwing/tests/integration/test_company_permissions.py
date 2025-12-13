# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Integration tests for Company permission enforcement (SC-006 / CR-012).

Tests verify that:
1. Users with Organization User Permission can access linked Company
2. Users without permission cannot access Company
3. API endpoints respect permissions
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompanyPermissions(FrappeTestCase):
    """Test Company permission inheritance from Organization."""

    TEST_USER_EMAIL = "__testcompanyperms@test.local"
    TEST_PREFIX = "__PermTest_"

    @classmethod
    def setUpClass(cls):
        """Create test user and data."""
        super().setUpClass()

        # Create test user if not exists
        if not frappe.db.exists("User", cls.TEST_USER_EMAIL):
            user = frappe.get_doc({
                "doctype": "User",
                "email": cls.TEST_USER_EMAIL,
                "first_name": "Test",
                "last_name": "CompanyPermUser",
                "enabled": 1,
                "new_password": "testpassword123"
            })
            user.insert(ignore_permissions=True)
            user.add_roles("Dartwing User")
            frappe.db.commit()

    @classmethod
    def tearDownClass(cls):
        """Clean up test data."""
        super().tearDownClass()

        # Ensure we're admin for cleanup
        frappe.set_user("Administrator")

        # Delete test user permissions
        frappe.db.delete("User Permission", {
            "user": cls.TEST_USER_EMAIL
        })

        # Delete test organizations and companies
        for org in frappe.get_all("Organization", filters={"org_name": ["like", f"{cls.TEST_PREFIX}%"]}):
            frappe.delete_doc("Organization", org.name, force=True, ignore_permissions=True)

        # Delete test user
        if frappe.db.exists("User", cls.TEST_USER_EMAIL):
            frappe.delete_doc("User", cls.TEST_USER_EMAIL, force=True, ignore_permissions=True)

        frappe.db.commit()

    def setUp(self):
        """Ensure admin user for setup."""
        frappe.set_user("Administrator")

    def tearDown(self):
        """Reset to admin user."""
        frappe.set_user("Administrator")

    def test_user_can_access_company_with_user_permission(self):
        """User with Organization User Permission can access linked Company."""
        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Accessible Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert(ignore_permissions=True)
        frappe.db.commit()

        # Grant User Permission
        frappe.get_doc({
            "doctype": "User Permission",
            "user": self.TEST_USER_EMAIL,
            "allow": "Organization",
            "for_value": org.name
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        # Test permission as test user
        frappe.set_user(self.TEST_USER_EMAIL)

        try:
            # Should be able to read Company via has_permission check
            has_perm = frappe.has_permission("Company", doc=org.linked_name, ptype="read")
            self.assertTrue(has_perm, "User should have permission to access Company")

            # Should be able to get Company
            company = frappe.get_doc("Company", org.linked_name)
            self.assertEqual(company.organization, org.name)
        finally:
            frappe.set_user("Administrator")
            # Cleanup
            frappe.db.delete("User Permission", {
                "user": self.TEST_USER_EMAIL,
                "for_value": org.name
            })

    def test_user_cannot_access_company_without_user_permission(self):
        """User without Organization User Permission cannot access Company."""
        # Create Organization and Company (no User Permission granted)
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Inaccessible Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert(ignore_permissions=True)
        frappe.db.commit()

        # Test permission as test user (no permission granted)
        frappe.set_user(self.TEST_USER_EMAIL)

        try:
            # Should NOT have permission
            has_perm = frappe.has_permission("Company", doc=org.linked_name, ptype="read")
            self.assertFalse(has_perm, "User should NOT have permission to access Company")
        finally:
            frappe.set_user("Administrator")

    def test_permission_query_conditions_filter_companies(self):
        """Permission query conditions should filter companies correctly."""
        # Create two Organizations
        org1 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Permitted Company",
            "org_type": "Company",
            "status": "Active"
        })
        org1.insert(ignore_permissions=True)

        org2 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}NotPermitted Company",
            "org_type": "Company",
            "status": "Active"
        })
        org2.insert(ignore_permissions=True)
        frappe.db.commit()

        # Grant permission only for org1
        frappe.get_doc({
            "doctype": "User Permission",
            "user": self.TEST_USER_EMAIL,
            "allow": "Organization",
            "for_value": org1.name
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        # Test as test user
        frappe.set_user(self.TEST_USER_EMAIL)

        try:
            # Get all companies user can see
            # Note: Use get_list instead of get_all to apply permission hooks
            companies = frappe.get_list(
                "Company",
                filters={"legal_name": ["like", f"{self.TEST_PREFIX}%"]},
                pluck="name"
            )

            # Should only see org1's company
            self.assertIn(org1.linked_name, companies)
            self.assertNotIn(org2.linked_name, companies)
        finally:
            frappe.set_user("Administrator")
            frappe.db.delete("User Permission", {
                "user": self.TEST_USER_EMAIL,
                "for_value": org1.name
            })

    def test_api_respects_permissions(self):
        """API endpoints should respect user permissions."""
        from dartwing.dartwing_company.api import get_company_with_org_details

        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}API Test Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert(ignore_permissions=True)
        frappe.db.commit()

        # Test WITHOUT permission - should raise error
        frappe.set_user(self.TEST_USER_EMAIL)

        try:
            with self.assertRaises(frappe.PermissionError):
                get_company_with_org_details(org.linked_name)
        finally:
            frappe.set_user("Administrator")

        # Grant permission
        frappe.get_doc({
            "doctype": "User Permission",
            "user": self.TEST_USER_EMAIL,
            "allow": "Organization",
            "for_value": org.name
        }).insert(ignore_permissions=True)
        frappe.db.commit()

        # Test WITH permission - should succeed
        frappe.set_user(self.TEST_USER_EMAIL)

        try:
            result = get_company_with_org_details(org.linked_name)
            self.assertIsNotNone(result)
            self.assertEqual(result.get("message"), "success")
            self.assertEqual(result.get("org_details", {}).get("name"), org.name)
        finally:
            frappe.set_user("Administrator")
            frappe.db.delete("User Permission", {
                "user": self.TEST_USER_EMAIL,
                "for_value": org.name
            })
