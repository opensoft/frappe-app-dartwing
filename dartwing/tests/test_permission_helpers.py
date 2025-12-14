# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for permission helpers module.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_helpers
"""

import frappe
from frappe.tests import IntegrationTestCase
from unittest.mock import patch, MagicMock

from dartwing.permissions.helpers import (
    create_user_permissions,
    remove_user_permissions,
    _cleanup_orphaned_permissions,
    ORGANIZATION_DOCTYPES,
)


class TestPermissionHelpers(IntegrationTestCase):
    """Test cases for permission helper functions."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        super().setUpClass()

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
            frappe.delete_doc("User Permission", perm_name, force=True, ignore_permissions=True)

    def tearDown(self):
        """Clean up test data after each test."""
        self.setUp()  # Reuse cleanup logic

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
        with patch('dartwing.permissions.helpers.frappe.logger') as mock_logger, \
                patch('dartwing.permissions.helpers.log_permission_event') as mock_log_event:
            
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
        with patch('dartwing.permissions.helpers.frappe.logger') as mock_logger:
            mock_logger_instance = MagicMock()
            mock_logger.return_value = mock_logger_instance

            _cleanup_orphaned_permissions(user_email, org_name, mock_doc)

            # Verify logger.info was called twice (once for summary)
            # The second call should be the summary
            self.assertEqual(mock_logger_instance.info.call_count, 1)
            
            # Check the summary message
            summary_message = mock_logger_instance.info.call_args[0][0]
            self.assertIn("Successfully removed 3", summary_message)
            self.assertIn(org_name, summary_message)
            # Should mention the permission types (in sorted order)
            self.assertIn("Company", summary_message)
            self.assertIn("Family", summary_message)
            self.assertIn("Organization", summary_message)
