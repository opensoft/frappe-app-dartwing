# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for permission helper functions.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_helpers
"""

import frappe
from frappe.tests import IntegrationTestCase

from dartwing.permissions.helpers import (
    create_user_permissions,
    remove_user_permissions,
    _cleanup_orphaned_permissions,
)


class TestPermissionHelpers(IntegrationTestCase):
    """Test cases for permission propagation helpers."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        super().setUpClass()

        # Create test user with Frappe User link
        if not frappe.db.exists("User", "test_perm_user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test_perm_user@example.com",
                "first_name": "Test",
                "last_name": "Permission User",
                "roles": [{"role": "System Manager"}]
            })
            user.insert(ignore_permissions=True)

        # Create test Person linked to User
        if not frappe.db.exists("Person", {"primary_email": "test_perm_user@example.com"}):
            cls.test_person = frappe.get_doc({
                "doctype": "Person",
                "first_name": "Test",
                "last_name": "Permission User",
                "primary_email": "test_perm_user@example.com",
                "frappe_user": "test_perm_user@example.com"
            })
            cls.test_person.insert(ignore_permissions=True)
        else:
            cls.test_person = frappe.get_doc(
                "Person", {"primary_email": "test_perm_user@example.com"}
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        super().tearDownClass()

        # Delete test person
        if frappe.db.exists("Person", cls.test_person.name):
            frappe.delete_doc("Person", cls.test_person.name, force=True)

        # Delete test user
        if frappe.db.exists("User", "test_perm_user@example.com"):
            frappe.delete_doc("User", "test_perm_user@example.com", force=True)

    def setUp(self):
        """Set up test data for each test."""
        # Clean up any existing test data
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data after each test."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Helper to clean up test organizations, families, and permissions."""
        # Clean up user permissions for test user
        for perm_name in frappe.get_all(
            "User Permission",
            filters={"user": "test_perm_user@example.com"},
            pluck="name"
        ):
            frappe.delete_doc("User Permission", perm_name, force=True)

        # Clean up org members
        for member_name in frappe.get_all(
            "Org Member",
            filters={"person": self.test_person.name},
            pluck="name"
        ):
            frappe.delete_doc("Org Member", member_name, force=True)

        # Clean up families
        for family_name in frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Test Perm%"]},
            pluck="name"
        ):
            frappe.delete_doc("Family", family_name, force=True)

        # Clean up organizations
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Perm%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org_name, force=True)

        frappe.db.commit()

    def test_cleanup_orphaned_permissions_with_valid_org_type(self):
        """Test cleanup when Organization is deleted but org_type is cached."""
        # Create a Family (which creates Organization automatically)
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Perm Family Valid"
        })
        family.insert(ignore_permissions=True)
        family.reload()

        # Get the organization name
        org_name = family.organization

        # Create Org Member with Active status
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": org_name,
            "role": "Parent",
            "status": "Active"
        })
        org_member.insert(ignore_permissions=True)
        org_member.reload()

        # Verify User Permissions were created
        org_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Organization",
            "for_value": org_name
        })
        self.assertTrue(org_perm_exists, "Organization permission should be created")

        family_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Family",
            "for_value": family.name
        })
        self.assertTrue(family_perm_exists, "Family permission should be created")

        # Store organization_type before deleting Organization
        org_type = org_member.organization_type
        self.assertEqual(org_type, "Family", "Organization type should be Family")

        # Delete the Organization document (simulating cascade issue)
        frappe.delete_doc("Organization", org_name, force=True)

        # Now call _cleanup_orphaned_permissions directly
        _cleanup_orphaned_permissions("test_perm_user@example.com", org_member)

        # Verify Organization permission was removed
        org_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Organization",
            "for_value": org_name
        })
        self.assertFalse(org_perm_exists, "Organization permission should be removed")

        # Verify Family permission was also removed
        family_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Family",
            "for_value": family.name
        })
        self.assertFalse(family_perm_exists, "Family permission should be removed")

    def test_cleanup_orphaned_permissions_with_invalid_org_type(self):
        """Test cleanup when org_type is not in VALID_ORG_TYPES."""
        # Create an Organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Perm Org Invalid",
            "org_type": "Family"
        })
        org.insert(ignore_permissions=True)

        # Create Org Member
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": org.name,
            "role": "Parent",
            "status": "Active"
        })
        org_member.insert(ignore_permissions=True)
        org_member.reload()

        # Manually set an invalid organization_type
        org_member.organization_type = "InvalidType"

        # Delete the Organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Call cleanup - should log warning but not crash
        _cleanup_orphaned_permissions("test_perm_user@example.com", org_member)

        # Should still remove Organization permission
        org_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Organization",
            "for_value": org.name
        })
        self.assertFalse(org_perm_exists, "Organization permission should be removed")

    def test_cleanup_orphaned_permissions_with_no_cached_org_type(self):
        """Test cleanup when organization_type is None."""
        # Create an Organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Perm Org No Type",
            "org_type": "Family"
        })
        org.insert(ignore_permissions=True)

        # Create Org Member
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": org.name,
            "role": "Parent",
            "status": "Active"
        })
        org_member.insert(ignore_permissions=True)
        org_member.reload()

        # Manually set organization_type to None
        org_member.organization_type = None

        # Delete the Organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Call cleanup - should log warning but not crash
        _cleanup_orphaned_permissions("test_perm_user@example.com", org_member)

        # Should still remove Organization permission
        org_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Organization",
            "for_value": org.name
        })
        self.assertFalse(org_perm_exists, "Organization permission should be removed")

    def test_cleanup_orphaned_permissions_concrete_type_does_not_exist(self):
        """Test cleanup when concrete document doesn't exist."""
        # Create an Organization without a linked concrete type
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Perm Org No Concrete",
            "org_type": "Family"
        })
        org.insert(ignore_permissions=True)

        # Create Org Member
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": org.name,
            "role": "Parent",
            "status": "Active"
        })
        org_member.insert(ignore_permissions=True)
        org_member.reload()

        # Delete the Organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Call cleanup - should handle gracefully when no concrete doc exists
        _cleanup_orphaned_permissions("test_perm_user@example.com", org_member)

        # Should still remove Organization permission
        org_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Organization",
            "for_value": org.name
        })
        self.assertFalse(org_perm_exists, "Organization permission should be removed")

    def test_cleanup_orphaned_permissions_multiple_concrete_docs(self):
        """Test cleanup when multiple concrete documents exist for same organization."""
        # Create a Family
        family1 = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Perm Family Multi 1"
        })
        family1.insert(ignore_permissions=True)
        family1.reload()

        org_name = family1.organization

        # Create another Family with same organization (data integrity issue)
        family2 = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Perm Family Multi 2"
        })
        family2.insert(ignore_permissions=True)
        # Manually set the same organization
        frappe.db.set_value("Family", family2.name, "organization", org_name)
        family2.reload()

        # Create Org Member
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": org_name,
            "role": "Parent",
            "status": "Active"
        })
        org_member.insert(ignore_permissions=True)
        org_member.reload()

        # Manually create User Permissions for both families
        for family in [family1, family2]:
            if not frappe.db.exists("User Permission", {
                "user": "test_perm_user@example.com",
                "allow": "Family",
                "for_value": family.name
            }):
                perm = frappe.get_doc({
                    "doctype": "User Permission",
                    "user": "test_perm_user@example.com",
                    "allow": "Family",
                    "for_value": family.name,
                    "apply_to_all_doctypes": 0
                })
                perm.insert(ignore_permissions=True)

        # Delete the Organization
        frappe.delete_doc("Organization", org_name, force=True)

        # Call cleanup - should remove permissions for BOTH families
        _cleanup_orphaned_permissions("test_perm_user@example.com", org_member)

        # Verify both Family permissions were removed
        family1_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Family",
            "for_value": family1.name
        })
        self.assertFalse(family1_perm_exists, "Family 1 permission should be removed")

        family2_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Family",
            "for_value": family2.name
        })
        self.assertFalse(family2_perm_exists, "Family 2 permission should be removed")

    def test_remove_user_permissions_normal_flow(self):
        """Test remove_user_permissions when Organization exists (normal flow)."""
        # Create a Family
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Perm Family Normal"
        })
        family.insert(ignore_permissions=True)
        family.reload()

        # Create Org Member
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": family.organization,
            "role": "Parent",
            "status": "Active"
        })
        org_member.insert(ignore_permissions=True)
        org_member.reload()

        # Verify permissions were created
        org_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Organization",
            "for_value": family.organization
        })
        self.assertTrue(org_perm_exists, "Organization permission should exist")

        family_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Family",
            "for_value": family.name
        })
        self.assertTrue(family_perm_exists, "Family permission should exist")

        # Call remove_user_permissions (simulates on_trash hook)
        remove_user_permissions(org_member, "on_trash")

        # Verify permissions were removed
        org_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Organization",
            "for_value": family.organization
        })
        self.assertFalse(org_perm_exists, "Organization permission should be removed")

        family_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Family",
            "for_value": family.name
        })
        self.assertFalse(family_perm_exists, "Family permission should be removed")

    def test_remove_user_permissions_org_already_deleted(self):
        """Test remove_user_permissions calls cleanup when Organization is deleted."""
        # Create a Family
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Perm Family Deleted"
        })
        family.insert(ignore_permissions=True)
        family.reload()

        org_name = family.organization

        # Create Org Member
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "person": self.test_person.name,
            "organization": org_name,
            "role": "Parent",
            "status": "Active"
        })
        org_member.insert(ignore_permissions=True)
        org_member.reload()

        # Delete Organization first
        frappe.delete_doc("Organization", org_name, force=True)

        # Call remove_user_permissions - should call cleanup logic
        remove_user_permissions(org_member, "on_trash")

        # Verify permissions were removed
        family_perm_exists = frappe.db.exists("User Permission", {
            "user": "test_perm_user@example.com",
            "allow": "Family",
            "for_value": family.name
        })
        self.assertFalse(family_perm_exists, "Family permission should be removed via cleanup")
