# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for permission API endpoints.

This module tests the API endpoints in dartwing.permissions.api that provide
helpers for querying permission state.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_permission_api
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPermissionAPI(FrappeTestCase):
    """Test cases for permission API endpoints."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        super().setUpClass()

        # Skip all tests if Org Member DocType doesn't exist yet
        if not frappe.db.exists("DocType", "Org Member"):
            import unittest
            raise unittest.SkipTest("Org Member DocType not available - skipping permission API tests")

        # Create test users
        for email in ["test_api_user1@example.com", "test_api_user2@example.com", "test_api_guest@example.com"]:
            if not frappe.db.exists("User", email):
                user = frappe.get_doc({
                    "doctype": "User",
                    "email": email,
                    "first_name": "Test",
                    "last_name": "API User",
                    "enabled": 1,
                    "user_type": "System User",
                    "roles": [{"role": "System Manager"}]
                })
                user.flags.ignore_permissions = True
                user.insert(ignore_permissions=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        super().tearDownClass()

        # Delete test users
        for email in ["test_api_user1@example.com", "test_api_user2@example.com", "test_api_guest@example.com"]:
            if frappe.db.exists("User", email):
                frappe.delete_doc("User", email, force=True)

    def setUp(self):
        """Set up test data for each test."""
        self._cleanup_test_data()
        self.original_user = frappe.session.user

    def tearDown(self):
        """Clean up test data after each test."""
        # Restore original user
        frappe.set_user(self.original_user)
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Helper to clean up all test data in reverse dependency order.

        Cleanup occurs in reverse dependency order with selective exception handling.
        Only catches expected DoesNotExistError. Logs LinkExistsError as potential
        bugs instead of silently swallowing them, which prevents test flakiness.
        """
        # 1. Clean up User Permissions first (no dependencies)
        for email in ["test_api_user1@example.com", "test_api_user2@example.com"]:
            for perm_name in frappe.get_all(
                "User Permission",
                filters={"user": email},
                pluck="name"
            ):
                try:
                    frappe.delete_doc("User Permission", perm_name, force=True, ignore_permissions=True)
                except frappe.DoesNotExistError:
                    pass  # Already deleted - this is expected

        # 2. Clean up Org Members (depends on Person and Organization)
        test_person_names = frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@api-test.example.com"]},
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
            filters={"org_name": ["like", "API Test %"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass
            except frappe.LinkExistsError as e:
                # CR-010-106 FIX: Use Frappe's delete API instead of raw SQL.
                # This should NOT happen in normal test execution - indicates a bug.
                frappe.log_error(
                    f"LinkExistsError during test cleanup for {org_name}: {str(e)}",
                    "Test Cleanup Error"
                )
                # Find and delete blocking Org Members using Frappe API
                blocking_members = frappe.get_all(
                    "Org Member",
                    filters={"organization": org_name},
                    pluck="name"
                )
                for member_name in blocking_members:
                    try:
                        frappe.delete_doc("Org Member", member_name, force=True, ignore_permissions=True)
                    except (frappe.DoesNotExistError, frappe.LinkExistsError):
                        pass  # Already deleted or still has dependencies - expected in cleanup
                    except Exception as ex:
                        frappe.log_error(f"Unexpected error deleting Org Member {member_name}: {str(ex)}", "Test Cleanup Error")

                # Retry Organization deletion
                try:
                    frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
                except (frappe.DoesNotExistError, frappe.LinkExistsError):
                    pass  # Already deleted or still has dependencies - expected in cleanup
                except Exception as ex:
                    frappe.log_error(f"Unexpected error deleting Organization {org_name}: {str(ex)}", "Test Cleanup Error")

        # 4. Clean up Persons (no longer referenced by Org Members)
        for person_name in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@api-test.example.com"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Person", person_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass

    def _create_test_person(self, name_suffix, user_email):
        """Helper to create a test Person."""
        person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "API",
            "last_name": f"Test {name_suffix}",
            "primary_email": f"api.test.{name_suffix}@api-test.example.com",
            "source": "manual",
            "frappe_user": user_email
        })
        person.insert(ignore_permissions=True)
        return person

    def _create_test_organization(self, name_suffix, org_type="Family"):
        """Helper to create a test Organization with concrete type."""
        concrete = frappe.get_doc({
            "doctype": org_type,
            f"{org_type.lower()}_name": f"API Test {org_type} {name_suffix}"
        })
        concrete.insert(ignore_permissions=True)
        concrete.reload()
        org = frappe.get_doc("Organization", concrete.organization)
        return org, concrete

    def _add_user_permission(self, user, allow, for_value):
        """Helper to manually add a User Permission."""
        if not frappe.db.exists("User Permission", {"user": user, "allow": allow, "for_value": for_value}):
            perm = frappe.get_doc({
                "doctype": "User Permission",
                "user": user,
                "allow": allow,
                "for_value": for_value,
                "apply_to_all_doctypes": 0
            })
            perm.insert(ignore_permissions=True)

    def _create_restricted_user(self, email, first_name, last_name):
        """Helper to create a test user without System Manager role."""
        if not frappe.db.exists("User", email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "enabled": 1,
                "user_type": "System User",
                "roles": [{"role": "Guest"}]  # No real permissions
            })
            user.flags.ignore_permissions = True
            user.insert(ignore_permissions=True)
        return email

    # =========================================================================
    # Test get_user_organizations API
    # =========================================================================

    def test_get_user_organizations_guest(self):
        """Test that Guest user cannot access get_user_organizations."""
        frappe.set_user("Guest")
        
        with self.assertRaises(frappe.PermissionError):
            frappe.call("dartwing.permissions.api.get_user_organizations")

    def test_get_user_organizations_no_test_orgs_exist(self):
        """Test that System Manager sees no API Test orgs when none exist yet."""
        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.get_user_organizations")
        
        self.assertIsInstance(result, list)
        # Note: System Manager sees all orgs, so filter for API Test orgs only
        api_test_orgs = [org for org in result if "API Test" in org.get("org_name", "")]
        self.assertEqual(len(api_test_orgs), 0, "Should have no API Test organizations")

    def test_get_user_organizations_with_permissions(self):
        """Test that user gets organizations they have permission to."""
        self._create_test_person("user1org", "test_api_user1@example.com")
        org1, family1 = self._create_test_organization("1", "Family")
        org2, company2 = self._create_test_organization("2", "Company")

        # Add permissions manually
        self._add_user_permission("test_api_user1@example.com", "Organization", org1.name)
        self._add_user_permission("test_api_user1@example.com", "Organization", org2.name)

        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.get_user_organizations")
        
        self.assertIsInstance(result, list)
        org_names = [org["name"] for org in result]
        self.assertIn(org1.name, org_names, "Should include org1")
        self.assertIn(org2.name, org_names, "Should include org2")

    def test_get_user_organizations_administrator(self):
        """Test that Administrator sees all organizations."""
        org1, _ = self._create_test_organization("admin1", "Family")
        org2, _ = self._create_test_organization("admin2", "Company")

        frappe.set_user("Administrator")
        
        result = frappe.call("dartwing.permissions.api.get_user_organizations")
        
        self.assertIsInstance(result, list)
        org_names = [org["name"] for org in result]
        self.assertIn(org1.name, org_names, "Administrator should see org1")
        self.assertIn(org2.name, org_names, "Administrator should see org2")

    def test_get_user_organizations_system_manager(self):
        """Test that System Manager sees all organizations."""
        org1, _ = self._create_test_organization("sysmgr1", "Nonprofit")

        # test_api_user1 has System Manager role
        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.get_user_organizations")
        
        self.assertIsInstance(result, list)
        org_names = [org["name"] for org in result]
        self.assertIn(org1.name, org_names, "System Manager should see all orgs")

    def test_get_user_organizations_fields(self):
        """Test that get_user_organizations returns correct fields."""
        org1, _ = self._create_test_organization("fields1", "Association")
        self._add_user_permission("test_api_user1@example.com", "Organization", org1.name)

        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.get_user_organizations")
        
        api_test_orgs = [org for org in result if org.get("name") == org1.name]
        self.assertEqual(len(api_test_orgs), 1)
        
        org = api_test_orgs[0]
        self.assertIn("name", org)
        self.assertIn("org_name", org)
        self.assertIn("org_type", org)
        # logo is optional, so we don't assert its presence

    # =========================================================================
    # Test check_organization_access API
    # =========================================================================

    def test_check_organization_access_guest(self):
        """Test that Guest user cannot access check_organization_access."""
        org1, _ = self._create_test_organization("checkaccess1", "Family")
        
        frappe.set_user("Guest")
        
        with self.assertRaises(frappe.PermissionError):
            frappe.call("dartwing.permissions.api.check_organization_access", organization=org1.name)

    def test_check_organization_access_no_permission(self):
        """Test that user without permission gets has_access=False."""
        org1, _ = self._create_test_organization("checkaccess2", "Company")
        
        # Create a user without System Manager role for this test
        test_user_email = self._create_restricted_user("test_noperm@example.com", "No", "Permission")
        
        try:
            frappe.set_user(test_user_email)
            
            result = frappe.call("dartwing.permissions.api.check_organization_access", organization=org1.name)
            
            self.assertIsInstance(result, dict)
            self.assertFalse(result.get("has_access"), "User should not have access")
        finally:
            frappe.set_user("Administrator")
            if frappe.db.exists("User", test_user_email):
                frappe.delete_doc("User", test_user_email, force=True)

    def test_check_organization_access_with_permission(self):
        """Test that user with permission gets has_access=True."""
        org1, family1 = self._create_test_organization("checkaccess3", "Family")
        self._add_user_permission("test_api_user1@example.com", "Organization", org1.name)

        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.check_organization_access", organization=org1.name)
        
        self.assertIsInstance(result, dict)
        self.assertTrue(result.get("has_access"), "User should have access")
        self.assertEqual(result.get("org_type"), "Family")
        self.assertEqual(result.get("concrete_type"), family1.name)

    def test_check_organization_access_administrator(self):
        """Test that Administrator always has access."""
        org1, _ = self._create_test_organization("checkaccess4", "Nonprofit")

        frappe.set_user("Administrator")
        
        result = frappe.call("dartwing.permissions.api.check_organization_access", organization=org1.name)
        
        self.assertTrue(result.get("has_access"), "Administrator should have access")

    def test_check_organization_access_nonexistent(self):
        """Test that nonexistent organization returns has_access=False."""
        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.check_organization_access", organization="NONEXISTENT-ORG-12345")
        
        self.assertFalse(result.get("has_access"), "Should not have access to nonexistent org")

    def test_check_organization_access_no_org_param(self):
        """Test that missing organization parameter raises error."""
        frappe.set_user("test_api_user1@example.com")
        
        with self.assertRaises(Exception):  # Should throw validation error
            frappe.call("dartwing.permissions.api.check_organization_access")

    # =========================================================================
    # Test get_organization_members API
    # =========================================================================

    def test_get_organization_members_guest(self):
        """Test that Guest user cannot access get_organization_members."""
        org1, _ = self._create_test_organization("members1", "Family")
        
        frappe.set_user("Guest")
        
        with self.assertRaises(frappe.PermissionError):
            frappe.call("dartwing.permissions.api.get_organization_members", organization=org1.name)

    def test_get_organization_members_no_access(self):
        """Test that user without org access gets permission error."""
        org1, _ = self._create_test_organization("members2", "Company")
        
        # Create user without System Manager
        test_user_email = self._create_restricted_user("test_nomember@example.com", "No", "Member")
        
        try:
            frappe.set_user(test_user_email)
            
            with self.assertRaises(frappe.PermissionError):
                frappe.call("dartwing.permissions.api.get_organization_members", organization=org1.name)
        finally:
            frappe.set_user("Administrator")
            if frappe.db.exists("User", test_user_email):
                frappe.delete_doc("User", test_user_email, force=True)

    def test_get_organization_members_with_access(self):
        """Test that user with access gets member list."""
        org1, _ = self._create_test_organization("members3", "Family")
        person1 = self._create_test_person("member1", "test_api_user1@example.com")
        person2 = self._create_test_person("member2", "test_api_user2@example.com")

        # Create Org Members
        member1 = frappe.get_doc({
            "doctype": "Org Member",
            "person": person1.name,
            "organization": org1.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member1.insert(ignore_permissions=True)

        member2 = frappe.get_doc({
            "doctype": "Org Member",
            "person": person2.name,
            "organization": org1.name,
            "status": "Inactive",
            "start_date": frappe.utils.today()
        })
        member2.insert(ignore_permissions=True)

        # Give user1 access to org
        self._add_user_permission("test_api_user1@example.com", "Organization", org1.name)

        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.get_organization_members", organization=org1.name)
        
        self.assertIsInstance(result, list)
        # By default, inactive members are excluded
        self.assertEqual(len(result), 1, "Should only include active member by default")
        self.assertEqual(result[0]["person"], person1.name)

    def test_get_organization_members_include_inactive(self):
        """Test that include_inactive parameter works."""
        org1, _ = self._create_test_organization("members4", "Nonprofit")
        person1 = self._create_test_person("member3", "test_api_user1@example.com")
        person2 = self._create_test_person("member4", "test_api_user2@example.com")

        # Create Org Members
        member1 = frappe.get_doc({
            "doctype": "Org Member",
            "person": person1.name,
            "organization": org1.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member1.insert(ignore_permissions=True)

        member2 = frappe.get_doc({
            "doctype": "Org Member",
            "person": person2.name,
            "organization": org1.name,
            "status": "Inactive",
            "start_date": frappe.utils.today()
        })
        member2.insert(ignore_permissions=True)

        self._add_user_permission("test_api_user1@example.com", "Organization", org1.name)

        frappe.set_user("test_api_user1@example.com")
        
        # Request with include_inactive=True
        result = frappe.call("dartwing.permissions.api.get_organization_members", 
                           organization=org1.name, 
                           include_inactive=True)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 2, "Should include both active and inactive members")

    def test_get_organization_members_fields(self):
        """Test that get_organization_members returns correct fields."""
        org1, _ = self._create_test_organization("members5", "Association")
        person1 = self._create_test_person("member5", "test_api_user1@example.com")

        member1 = frappe.get_doc({
            "doctype": "Org Member",
            "person": person1.name,
            "organization": org1.name,
            "status": "Active",
            "start_date": frappe.utils.today()
        })
        member1.insert(ignore_permissions=True)

        self._add_user_permission("test_api_user1@example.com", "Organization", org1.name)

        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call("dartwing.permissions.api.get_organization_members", organization=org1.name)
        
        self.assertEqual(len(result), 1)
        member = result[0]
        
        self.assertIn("name", member)
        self.assertIn("person", member)
        self.assertIn("person_name", member)
        self.assertIn("status", member)
        self.assertIn("start_date", member)
        self.assertIn("is_supervisor", member)

    # =========================================================================
    # Test get_permission_audit_log API
    # =========================================================================

    def test_get_permission_audit_log_guest(self):
        """Test that Guest user cannot access audit log."""
        frappe.set_user("Guest")
        
        with self.assertRaises(frappe.PermissionError):
            frappe.call("dartwing.permissions.api.get_permission_audit_log")

    def test_get_permission_audit_log_non_system_manager(self):
        """Test that non-System Manager cannot access audit log."""
        # Create user without System Manager
        test_user_email = self._create_restricted_user("test_noaudit@example.com", "No", "Audit")
        
        try:
            frappe.set_user(test_user_email)
            
            with self.assertRaises(frappe.PermissionError):
                frappe.call("dartwing.permissions.api.get_permission_audit_log")
        finally:
            frappe.set_user("Administrator")
            if frappe.db.exists("User", test_user_email):
                frappe.delete_doc("User", test_user_email, force=True)

    def test_get_permission_audit_log_system_manager(self):
        """Test that System Manager can access audit log."""
        frappe.set_user("test_api_user1@example.com")  # Has System Manager role
        
        result = frappe.call("dartwing.permissions.api.get_permission_audit_log")
        
        self.assertIsInstance(result, dict)
        self.assertIn("message", result)
        self.assertIn("log_path", result)
        self.assertIn("filters_applied", result)

    def test_get_permission_audit_log_administrator(self):
        """Test that Administrator can access audit log."""
        frappe.set_user("Administrator")
        
        result = frappe.call("dartwing.permissions.api.get_permission_audit_log")
        
        self.assertIsInstance(result, dict)
        self.assertIn("log_path", result)

    def test_get_permission_audit_log_with_filters(self):
        """Test that audit log accepts filter parameters."""
        frappe.set_user("test_api_user1@example.com")
        
        result = frappe.call(
            "dartwing.permissions.api.get_permission_audit_log",
            organization="ORG-001",
            user="test@example.com",
            event_type="create",
            from_date="2025-01-01",
            to_date="2025-12-31",
            limit=50
        )
        
        self.assertIsInstance(result, dict)
        self.assertIn("filters_applied", result)
        filters = result["filters_applied"]
        self.assertEqual(filters["organization"], "ORG-001")
        self.assertEqual(filters["user"], "test@example.com")
        self.assertEqual(filters["event_type"], "create")
        self.assertEqual(filters["limit"], 50)
