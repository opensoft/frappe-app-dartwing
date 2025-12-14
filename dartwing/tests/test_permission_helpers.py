# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for permission helpers module.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_helpers
"""

import frappe
from frappe.tests.utils import FrappeTestCase
from unittest.mock import patch, MagicMock

from dartwing.permissions.helpers import (
    _cleanup_orphaned_permissions,
    ORGANIZATION_DOCTYPES,
)


class TestPermissionHelpers(FrappeTestCase):
    """Test cases for permission helper functions."""

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
        
        # Create test user
        if not frappe.db.exists("User", "test_perm_helper@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test_perm_helper@example.com",
                "first_name": "Test",
                "last_name": "Perm Helper",
                "send_welcome_email": 0,
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
        
        if not frappe.db.exists("Person", {"frappe_user": "test_perm_helper@example.com"}):
            person = frappe.get_doc({
                "doctype": "Person",
                "first_name": "Test",
                "last_name": "Helper",
                "frappe_user": "test_perm_helper@example.com",
            })
            person.insert(ignore_permissions=True)
            cls.test_person = person.name
        else:
            cls.test_person = frappe.db.get_value(
                "Person", {"frappe_user": "test_perm_helper@example.com"}, "name"
            )

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        super().tearDownClass()

        # Delete test Person
        if frappe.db.exists("Person", cls.test_person):
            frappe.delete_doc("Person", cls.test_person, force=True, ignore_permissions=True)

        # Delete test user
        if frappe.db.exists("User", "test_perm_helper@example.com"):
            frappe.delete_doc("User", "test_perm_helper@example.com", force=True, ignore_permissions=True)

    def setUp(self):
        """Set up test data for each test."""
        # Clean up any test organizations
        for org_name in frappe.get_all(
            "Organization",
            filters={"name": ["like", "Test Perm Org%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)

        # Clean up any test org members
        for member_name in frappe.get_all(
            "Org Member",
            filters={"person": self.test_person},
            pluck="name"
        ):
            frappe.delete_doc("Org Member", member_name, force=True, ignore_permissions=True)

        # Clean up user permissions for test user
        for perm_name in frappe.get_all(
            "User Permission",
            filters={"user": "test_perm_helper@example.com"},
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
        _cleanup_orphaned_permissions("test_perm_user@example.com", org_name, org_member)

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
        _cleanup_orphaned_permissions("test_perm_user@example.com", org.name, org_member)

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
        _cleanup_orphaned_permissions("test_perm_user@example.com", org.name, org_member)

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
        _cleanup_orphaned_permissions("test_perm_user@example.com", org.name, org_member)

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
        _cleanup_orphaned_permissions("test_perm_user@example.com", org_name, org_member)

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

    def _create_mock_org_member(self, member_name, org_name):
        """Helper to create a mock Org Member doc."""
        mock_doc = MagicMock()
        mock_doc.name = member_name
        mock_doc.organization = org_name
        return mock_doc

    def _create_user_permission(self, user_email, allow_doctype, for_value):
        """Helper to create a User Permission."""
        perm = frappe.get_doc({
            "doctype": "User Permission",
            "user": user_email,
            "allow": allow_doctype,
            "for_value": for_value,
            "apply_to_all_doctypes": 0,
        })
        perm.insert(ignore_permissions=True)
        return perm

    def _mock_logger_and_log_event(self):
        """Helper to set up mocks for logger and log_permission_event."""
        mock_logger = patch('dartwing.permissions.helpers.frappe.logger')
        mock_log_event = patch('dartwing.permissions.helpers.log_permission_event')
        return mock_logger, mock_log_event

    def test_cleanup_orphaned_permissions_removes_all_related_perms(self):
        """Test that _cleanup_orphaned_permissions removes both Organization and concrete type permissions."""
        org_name = "Test Perm Org Cleanup All"
        user_email = "test_perm_helper@example.com"

        # Create User Permissions manually (simulating orphaned state)
        self._create_user_permission(user_email, "Organization", org_name)
        self._create_user_permission(user_email, "Family", org_name)
        self._create_user_permission(user_email, "Company", org_name)

        # Verify permissions exist
        self.assertEqual(
            frappe.db.count("User Permission", {
                "user": user_email,
                "for_value": org_name
            }),
            3
        )

        # Create a mock Org Member doc and call cleanup function
        mock_doc = self._create_mock_org_member("Test Member 001", org_name)
        _cleanup_orphaned_permissions(user_email, org_name, mock_doc)

        # Verify all permissions are removed
        self.assertEqual(
            frappe.db.count("User Permission", {
                "user": user_email,
                "for_value": org_name
            }),
            0
        )

    def test_cleanup_orphaned_permissions_logs_each_removal(self):
        """Test that proper audit logging occurs for each removed permission."""
        org_name = "Test Perm Org Logging"
        user_email = "test_perm_helper@example.com"

        # Create User Permissions
        self._create_user_permission(user_email, "Organization", org_name)
        self._create_user_permission(user_email, "Family", org_name)

        # Create a mock Org Member doc
        mock_doc = self._create_mock_org_member("Test Member 002", org_name)

        # Mock the log_permission_event to capture calls
        with patch('dartwing.permissions.helpers.log_permission_event') as mock_log:
            _cleanup_orphaned_permissions(user_email, org_name, mock_doc)

            # Verify log_permission_event was called for each permission removal
            # Should be called twice (once for Organization, once for Family)
            self.assertEqual(mock_log.call_count, 2)

            # Verify the calls included "remove" action
            calls = mock_log.call_args_list
            for call in calls:
                args, kwargs = call
                self.assertEqual(args[0], "remove")
                self.assertEqual(kwargs["user"], user_email)
                self.assertIn(kwargs["doctype"], ["Organization", "Family"])
                self.assertEqual(kwargs["for_value"], org_name)

    def test_cleanup_orphaned_permissions_logs_when_no_perms_found(self):
        """Test that the function logs appropriately when no permissions are found."""
        org_name = "Test Perm Org No Perms"
        user_email = "test_perm_helper@example.com"

        # Create a mock Org Member doc
        mock_doc = self._create_mock_org_member("Test Member 003", org_name)

        # Mock the logger and log_permission_event
        mock_logger_patch, mock_log_event_patch = self._mock_logger_and_log_event()
        with mock_logger_patch as mock_logger, mock_log_event_patch as mock_log_event:
            mock_logger_instance = MagicMock()
            mock_logger.return_value = mock_logger_instance

            _cleanup_orphaned_permissions(user_email, org_name, mock_doc)

            # Verify logger.info was called with appropriate message
            mock_logger_instance.info.assert_called_once()
            info_message = mock_logger_instance.info.call_args[0][0]
            self.assertIn(org_name, info_message)
            self.assertIn("no User Permissions found", info_message)

            # Verify log_permission_event was called with "skip"
            mock_log_event.assert_called_once()
            args, kwargs = mock_log_event.call_args
            self.assertEqual(args[0], "skip")
            self.assertIn("Organization not found", kwargs["reason"])

    def test_cleanup_orphaned_permissions_only_org_related_doctypes(self):
        """Test that only organization-related DocTypes are queried and removed."""
        org_name = "Test Perm Org Filtered"
        user_email = "test_perm_helper@example.com"

        # Create Organization permission
        self._create_user_permission(user_email, "Organization", org_name)

        # Create a User Permission for a non-organization DocType with same for_value
        # This should NOT be removed
        self._create_user_permission(user_email, "Person", org_name)

        # Create a mock Org Member doc
        mock_doc = self._create_mock_org_member("Test Member 004", org_name)

        # Call cleanup function
        _cleanup_orphaned_permissions(user_email, org_name, mock_doc)

        # Verify Organization permission is removed
        self.assertFalse(
            frappe.db.exists("User Permission", {
                "user": user_email,
                "allow": "Organization",
                "for_value": org_name
            })
        )

        # Verify Person permission still exists (not removed)
        self.assertTrue(
            frappe.db.exists("User Permission", {
                "user": user_email,
                "allow": "Person",
                "for_value": org_name
            })
        )

    def test_cleanup_orphaned_permissions_respects_organization_doctypes_constant(self):
        """Test that cleanup uses ORGANIZATION_DOCTYPES constant for filtering."""
        org_name = "Test Perm Org Constant"
        user_email = "test_perm_helper@example.com"

        # Create permissions for all DocTypes in ORGANIZATION_DOCTYPES
        for doctype in ORGANIZATION_DOCTYPES:
            self._create_user_permission(user_email, doctype, org_name)

        # Verify all permissions were created
        initial_count = frappe.db.count("User Permission", {
            "user": user_email,
            "for_value": org_name,
            "allow": ["in", ORGANIZATION_DOCTYPES]
        })
        self.assertEqual(initial_count, len(ORGANIZATION_DOCTYPES))

        # Create a mock Org Member doc and call cleanup function
        mock_doc = self._create_mock_org_member("Test Member 005", org_name)
        _cleanup_orphaned_permissions(user_email, org_name, mock_doc)

        # Verify all organization-related permissions are removed
        final_count = frappe.db.count("User Permission", {
            "user": user_email,
            "for_value": org_name,
            "allow": ["in", ORGANIZATION_DOCTYPES]
        })
        self.assertEqual(final_count, 0)

    def test_cleanup_orphaned_permissions_logs_summary(self):
        """Test that cleanup logs a summary with permission types removed."""
        org_name = "Test Perm Org Summary"
        user_email = "test_perm_helper@example.com"

        # Create multiple permission types
        for doctype in ["Organization", "Family", "Company"]:
            self._create_user_permission(user_email, doctype, org_name)

        # Create a mock Org Member doc
        mock_doc = self._create_mock_org_member("Test Member 006", org_name)

        # Mock the logger
        mock_logger_patch, _ = self._mock_logger_and_log_event()
        with mock_logger_patch as mock_logger:
            mock_logger_instance = MagicMock()
            mock_logger.return_value = mock_logger_instance

            _cleanup_orphaned_permissions(user_email, org_name, mock_doc)

            # Verify logger.info was called once for the summary
            self.assertEqual(mock_logger_instance.info.call_count, 1)
            
            # Check the summary message
            summary_message = mock_logger_instance.info.call_args[0][0]
            self.assertIn("Successfully removed 3", summary_message)
            self.assertIn(org_name, summary_message)
            # Should mention the permission types (in sorted order)
            self.assertIn("Company", summary_message)
            self.assertIn("Family", summary_message)
            self.assertIn("Organization", summary_message)
