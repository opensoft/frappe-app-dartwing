# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for org-level user permission propagation and lifecycle.

This module tests the automatic creation and removal of User Permissions
when Org Member records are created, deleted, or have status changes.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_propagation
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPermissionPropagation(FrappeTestCase):
    """Test cases for permission propagation lifecycle."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        super().setUpClass()

        # Skip all tests if Org Member DocType doesn't exist yet
        if not frappe.db.exists("DocType", "Org Member"):
            import unittest
            raise unittest.SkipTest("Org Member DocType not available - skipping permission propagation tests")

        # Create test user with basic role
        if not frappe.db.exists("User", "test_perm_user@example.com"):
            user = frappe.get_doc({
                "doctype": "User",
                "email": "test_perm_user@example.com",
                "first_name": "Test",
                "last_name": "Permission User",
                "enabled": 1,
                "user_type": "System User",
                "roles": [{"role": "System Manager"}]  # Basic role for testing
            })
            user.flags.ignore_permissions = True
            user.insert(ignore_permissions=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        super().tearDownClass()

        # Delete test user
        if frappe.db.exists("User", "test_perm_user@example.com"):
            frappe.delete_doc("User", "test_perm_user@example.com", force=True)

    def setUp(self):
        """Set up test data for each test."""
        # Clean up test data from previous runs
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data after each test."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Helper to clean up all test data."""
        # Clean up Org Members
        for member_name in frappe.get_all(
            "Org Member",
            filters={"person": ["like", "PERM-TEST-%"]},
            pluck="name"
        ):
            frappe.delete_doc("Org Member", member_name, force=True, ignore_permissions=True)

        # Clean up Persons
        for person_name in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@perm-test.example.com"]},
            pluck="name"
        ):
            frappe.delete_doc("Person", person_name, force=True, ignore_permissions=True)

        # Clean up Organizations and concrete types
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Perm Test %"]},
            pluck="name"
        ):
            org = frappe.get_doc("Organization", org_name)
            # Delete concrete type first if exists
            if org.linked_doctype and org.linked_name:
                try:
                    frappe.delete_doc(org.linked_doctype, org.linked_name, force=True, ignore_permissions=True)
                except (frappe.DoesNotExistError, frappe.LinkExistsError):
                    # Concrete type may have already been deleted or has links
                    pass
            frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)

        # Clean up User Permissions for test user
        for perm_name in frappe.get_all(
            "User Permission",
            filters={"user": "test_perm_user@example.com"},
            pluck="name"
        ):
            frappe.delete_doc("User Permission", perm_name, force=True, ignore_permissions=True)

    def _create_test_person(self, name_suffix, with_user=True):
        """Helper to create a test Person."""
        person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Test",
            "last_name": f"Perm User {name_suffix}",
            "primary_email": f"test.perm.{name_suffix}@perm-test.example.com",
            "source": "manual",
            "frappe_user": "test_perm_user@example.com" if with_user else None
        })
        person.insert(ignore_permissions=True)
        return person

    def _create_test_organization(self, name_suffix, org_type="Family", with_concrete=True):
        """Helper to create a test Organization with optional concrete type."""
        # Create concrete type first if requested
        concrete_name = None
        if with_concrete:
            concrete = frappe.get_doc({
                "doctype": org_type,
                f"{org_type.lower()}_name": f"Perm Test {org_type} {name_suffix}"
            })
            concrete.insert(ignore_permissions=True)
            concrete.reload()
            # Get the auto-created organization
            org = frappe.get_doc("Organization", concrete.organization)
            return org, concrete
        else:
            # Create standalone Organization
            org = frappe.get_doc({
                "doctype": "Organization",
                "org_name": f"Perm Test Org {name_suffix}",
                "org_type": org_type
            })
            org.insert(ignore_permissions=True)
            return org, None

    def _get_user_permissions(self, user, allow=None, for_value=None):
        """Helper to get User Permissions for a user."""
        filters = {"user": user}
        if allow:
            filters["allow"] = allow
        if for_value:
            filters["for_value"] = for_value
        return frappe.get_all("User Permission", filters=filters, fields=["name", "allow", "for_value"])

    # =========================================================================
    # Test Permission Creation on Org Member Insert
    # =========================================================================

    def test_create_permissions_active_member(self):
        """Test that permissions are created when Active Org Member is inserted."""
        person = self._create_test_person("active1")
        org, family = self._create_test_organization("active1", "Family")

        # Create Active Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify Organization permission created
        org_perms = self._get_user_permissions("test_perm_user@example.com", "Organization", org.name)
        self.assertEqual(len(org_perms), 1, "Organization permission should be created")

        # Verify Family permission created
        family_perms = self._get_user_permissions("test_perm_user@example.com", "Family", family.name)
        self.assertEqual(len(family_perms), 1, "Family (concrete type) permission should be created")

    def test_skip_permissions_pending_member(self):
        """Test that permissions are NOT created for Pending Org Member."""
        person = self._create_test_person("pending1")
        org, _ = self._create_test_organization("pending1", "Company")

        # Create Pending Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Pending",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify NO permissions created
        perms = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms), 0, "No permissions should be created for Pending member")

    def test_skip_permissions_inactive_member(self):
        """Test that permissions are NOT created for Inactive Org Member on insert."""
        person = self._create_test_person("inactive1")
        org, _ = self._create_test_organization("inactive1", "Nonprofit")

        # Create Inactive Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Inactive",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify NO permissions created
        perms = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms), 0, "No permissions should be created for Inactive member on insert")

    def test_skip_permissions_person_without_user(self):
        """Test that permissions are skipped gracefully when Person has no Frappe User."""
        person = self._create_test_person("nouser1", with_user=False)
        org, _ = self._create_test_organization("nouser1", "Association")

        # Create Active Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify NO permissions created (but no error raised)
        perms = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms), 0, "No permissions should be created when Person has no frappe_user")

    def test_create_permissions_organization_only(self):
        """Test permission creation when Organization has no concrete type."""
        person = self._create_test_person("orgonly1")
        org, _ = self._create_test_organization("orgonly1", "Family", with_concrete=False)

        # Create Active Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify Organization permission created
        org_perms = self._get_user_permissions("test_perm_user@example.com", "Organization", org.name)
        self.assertEqual(len(org_perms), 1, "Organization permission should be created")

        # Verify NO concrete type permission (since none exists)
        all_perms = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(all_perms), 1, "Only Organization permission should exist")

    def test_create_permissions_multiple_org_types(self):
        """Test permission creation works for all concrete types."""
        person = self._create_test_person("multi1")
        
        for org_type in ["Family", "Company", "Nonprofit", "Association"]:
            org, concrete = self._create_test_organization(f"multi-{org_type}", org_type)
            
            member = frappe.get_doc({
                "doctype": "Org Member",
                "person": person.name,
                "organization": org.name,
                "status": "Active",
                "start_date": frappe.utils.today()
            })
            member.insert(ignore_permissions=True)

            # Verify both Organization and concrete type permissions
            org_perms = self._get_user_permissions("test_perm_user@example.com", "Organization", org.name)
            self.assertEqual(len(org_perms), 1, f"{org_type} Organization permission should exist")
            
            concrete_perms = self._get_user_permissions("test_perm_user@example.com", org_type, concrete.name)
            self.assertEqual(len(concrete_perms), 1, f"{org_type} concrete type permission should exist")

    # =========================================================================
    # Test Permission Removal on Org Member Delete
    # =========================================================================

    def test_remove_permissions_on_delete(self):
        """Test that permissions are removed when Org Member is deleted."""
        person = self._create_test_person("delete1")
        org, family = self._create_test_organization("delete1", "Family")

        # Create Active Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify permissions created
        perms_before = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_before), 2, "Should have 2 permissions (Org + Family)")

        # Delete Org Member
        frappe.delete_doc("Org Member", member.name, ignore_permissions=True)

        # Verify permissions removed
        perms_after = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_after), 0, "All permissions should be removed on delete")

    def test_remove_permissions_person_without_user(self):
        """Test that deletion handles Person without Frappe User gracefully."""
        person = self._create_test_person("delete-nouser1", with_user=False)
        org, _ = self._create_test_organization("delete-nouser1", "Company")

        # Create Active Org Member (no permissions will be created)
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Delete should not raise error
        frappe.delete_doc("Org Member", member.name, ignore_permissions=True)
        
        # Test passes if no exception raised

    # =========================================================================
    # Test Status Change Handling
    # =========================================================================

    def test_status_change_active_to_inactive(self):
        """Test that permissions are removed when status changes to Inactive."""
        person = self._create_test_person("status1")
        org, family = self._create_test_organization("status1", "Family")

        # Create Active Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify permissions created
        perms_before = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_before), 2, "Should have 2 permissions initially")

        # Change status to Inactive
        member.status = "Inactive"
        member.save(ignore_permissions=True)

        # Verify permissions removed
        perms_after = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_after), 0, "Permissions should be removed when status becomes Inactive")

    def test_status_change_inactive_to_active(self):
        """Test that permissions are created when status changes from Inactive to Active."""
        person = self._create_test_person("status2")
        org, family = self._create_test_organization("status2", "Family")

        # Create Inactive Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Inactive",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify no permissions initially
        perms_before = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_before), 0, "Should have no permissions initially")

        # Change status to Active
        member.status = "Active"
        member.save(ignore_permissions=True)

        # Verify permissions created
        perms_after = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_after), 2, "Permissions should be created when status becomes Active")

    def test_status_change_pending_to_active(self):
        """Test that permissions are created when status changes from Pending to Active."""
        person = self._create_test_person("status3")
        org, company = self._create_test_organization("status3", "Company")

        # Create Pending Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Pending",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify no permissions initially
        perms_before = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_before), 0, "Should have no permissions for Pending member")

        # Change status to Active
        member.status = "Active"
        member.save(ignore_permissions=True)

        # Verify permissions created
        perms_after = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_after), 2, "Permissions should be created when status becomes Active from Pending")

    def test_status_change_active_to_pending(self):
        """Test that status change from Active to Pending does not remove permissions."""
        person = self._create_test_person("status4")
        org, _ = self._create_test_organization("status4", "Nonprofit")

        # Create Active Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify permissions created
        perms_before = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_before), 2, "Should have 2 permissions initially")

        # Change status to Pending (should not trigger permission removal)
        member.status = "Pending"
        member.save(ignore_permissions=True)

        # Verify permissions still exist
        perms_after = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_after), 2, "Permissions should remain when changing to Pending")

    def test_no_status_change_no_action(self):
        """Test that updating other fields doesn't trigger permission changes."""
        person = self._create_test_person("status5")
        org, _ = self._create_test_organization("status5", "Association")

        # Create Active Org Member
        member = frappe.get_doc({
            "doctype": "Org Member",
            "person": person.name,
            "organization": org.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member.insert(ignore_permissions=True)

        # Verify permissions created
        perms_before = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_before), 2, "Should have 2 permissions initially")

        # Update end_date (not status)
        member.end_date = frappe.utils.add_days(frappe.utils.today(), 30)
        member.save(ignore_permissions=True)

        # Verify permissions unchanged
        perms_after = self._get_user_permissions("test_perm_user@example.com")
        self.assertEqual(len(perms_after), 2, "Permissions should remain unchanged")
