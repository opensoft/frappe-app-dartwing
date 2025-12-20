# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Test cases for Family permission system.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_family_permissions
"""

import frappe
from frappe.tests.utils import FrappeTestCase

from dartwing.permissions.family import (
    get_user_organizations,
    has_org_access,
    add_org_user_permission,
    remove_org_user_permission,
    get_permission_query_conditions,
    has_permission,
)


class TestFamilyPermissions(FrappeTestCase):
    """Test cases for Family permission system."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        super().setUpClass()

        # Create test user
        if not frappe.db.exists("User", "test_family_user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test_family_user@example.com",
                "first_name": "Test",
                "last_name": "Family User",
                "roles": [{"role": "Family Manager"}]
            })
            user.insert(ignore_permissions=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        super().tearDownClass()

        # Delete test user
        if frappe.db.exists("User", "test_family_user@example.com"):
            frappe.delete_doc("User", "test_family_user@example.com", force=True)

    def setUp(self):
        """Set up test data for each test."""
        # Clean up test organizations and families
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Perm Test%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org_name, force=True)

        for family_name in frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Perm Test%"]},
            pluck="name"
        ):
            frappe.delete_doc("Family", family_name, force=True)

        # Clean up user permissions for test user
        for perm_name in frappe.get_all(
            "User Permission",
            filters={
                "user": "test_family_user@example.com",
                "allow": "Organization"
            },
            pluck="name"
        ):
            frappe.delete_doc("User Permission", perm_name, force=True)

    def tearDown(self):
        """Clean up test data after each test."""
        self.setUp()  # Reuse cleanup logic

    def test_get_user_organizations_empty(self):
        """Test get_user_organizations returns empty for user with no permissions."""
        orgs = get_user_organizations("test_family_user@example.com")
        self.assertEqual(orgs, [])

    def test_add_org_user_permission(self):
        """Test adding organization permission for user."""
        # Create an organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Perm Test Org Add",
            "org_type": "Family"
        })
        org.insert()

        # Add permission
        perm_name = add_org_user_permission("test_family_user@example.com", org.name)
        self.assertIsNotNone(perm_name)

        # Verify user has access
        self.assertTrue(has_org_access("test_family_user@example.com", org.name))

        # Verify get_user_organizations returns the org
        orgs = get_user_organizations("test_family_user@example.com")
        self.assertIn(org.name, orgs)

    def test_remove_org_user_permission(self):
        """Test removing organization permission for user."""
        # Create an organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Perm Test Org Remove",
            "org_type": "Family"
        })
        org.insert()

        # Add then remove permission
        add_org_user_permission("test_family_user@example.com", org.name)
        self.assertTrue(has_org_access("test_family_user@example.com", org.name))

        remove_org_user_permission("test_family_user@example.com", org.name)
        self.assertFalse(has_org_access("test_family_user@example.com", org.name))

    def test_has_org_access(self):
        """Test has_org_access function."""
        # Create an organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Perm Test Org Access",
            "org_type": "Family"
        })
        org.insert()

        # Initially no access
        self.assertFalse(has_org_access("test_family_user@example.com", org.name))

        # After adding permission, has access
        add_org_user_permission("test_family_user@example.com", org.name)
        self.assertTrue(has_org_access("test_family_user@example.com", org.name))

    def test_permission_query_conditions_admin(self):
        """Test that Administrator sees all families."""
        conditions = get_permission_query_conditions("Administrator")
        self.assertEqual(conditions, "")

    def test_permission_query_conditions_no_access(self):
        """Test that user with no org access sees nothing."""
        conditions = get_permission_query_conditions("test_family_user@example.com")
        self.assertEqual(conditions, "1=0")

    def test_permission_query_conditions_with_access(self):
        """Test that user with org access sees filtered results."""
        # Create an organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Perm Test Org Query",
            "org_type": "Family"
        })
        org.insert()

        # Add permission
        add_org_user_permission("test_family_user@example.com", org.name)

        # Get query conditions
        conditions = get_permission_query_conditions("test_family_user@example.com")

        # Should contain the organization name in the IN clause
        self.assertIn(org.name, conditions)
        self.assertIn("IN", conditions)

    def test_has_permission_admin(self):
        """Test that Administrator has permission on any family."""
        # Create a family
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Perm Test Family Admin"
        })
        family.insert()
        family.reload()

        # Administrator should have permission
        self.assertTrue(has_permission(family, "read", "Administrator"))

    def test_has_permission_with_org_access(self):
        """Test that user with org access has permission on family."""
        # Create a family (which creates an organization)
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Perm Test Family Access"
        })
        family.insert()
        family.reload()

        # Add permission for the organization
        add_org_user_permission("test_family_user@example.com", family.organization)

        # User should have permission
        self.assertTrue(has_permission(family, "read", "test_family_user@example.com"))

    def test_has_permission_without_org_access(self):
        """Test that user without org access doesn't have permission."""
        # Create a family (which creates an organization)
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Perm Test Family No Access"
        })
        family.insert()
        family.reload()

        # User should NOT have permission (no org access granted)
        self.assertFalse(has_permission(family, "read", "test_family_user@example.com"))
