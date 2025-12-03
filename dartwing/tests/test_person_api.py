# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Integration tests for Person API endpoints.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_person_api
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestPersonAPI(FrappeTestCase):
    """Integration tests for Person API endpoints."""

    def setUp(self):
        """Set up test fixtures."""
        # Clean up any existing test persons
        for person_name in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@api-test.example.com"]},
            pluck="name"
        ):
            frappe.delete_doc("Person", person_name, force=True)

    def tearDown(self):
        """Clean up test data."""
        for person_name in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@api-test.example.com"]},
            pluck="name"
        ):
            frappe.delete_doc("Person", person_name, force=True)

    def _create_test_person(self, email_prefix, **kwargs):
        """Helper to create a test person."""
        defaults = {
            "doctype": "Person",
            "primary_email": f"{email_prefix}@api-test.example.com",
            "first_name": "Test",
            "last_name": "Person",
            "source": "signup"
        }
        defaults.update(kwargs)
        person = frappe.get_doc(defaults)
        person.insert()
        return person

    # =========================================================================
    # CRUD Cycle Tests
    # =========================================================================

    def test_person_create_read_update_delete(self):
        """Test full CRUD cycle via REST API patterns."""
        # CREATE
        person = self._create_test_person("crud")
        self.assertTrue(person.name)
        self.assertEqual(person.status, "Active")

        # READ
        fetched = frappe.get_doc("Person", person.name)
        self.assertEqual(fetched.primary_email, "crud@api-test.example.com")

        # UPDATE
        fetched.last_name = "Updated"
        fetched.save()
        refetched = frappe.get_doc("Person", person.name)
        self.assertEqual(refetched.last_name, "Updated")
        self.assertEqual(refetched.full_name, "Test Updated")

        # DELETE
        frappe.delete_doc("Person", person.name)
        self.assertFalse(frappe.db.exists("Person", person.name))

    def test_person_list_filter_by_status(self):
        """Test listing Persons with status filter."""
        # Create active and inactive persons
        active = self._create_test_person("active")
        inactive = self._create_test_person("inactive", status="Inactive")

        # Query active only
        active_persons = frappe.get_all(
            "Person",
            filters={"status": "Active", "primary_email": ["like", "%@api-test.example.com"]},
            pluck="name"
        )
        self.assertIn(active.name, active_persons)
        self.assertNotIn(inactive.name, active_persons)

    # =========================================================================
    # capture_consent API Tests
    # =========================================================================

    def test_capture_consent_success(self):
        """Test successful consent capture for minor."""
        person = self._create_test_person("minor", is_minor=1, consent_captured=0)

        result = frappe.call(
            "dartwing.api.person.capture_consent",
            person_name=person.name
        )

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["consent_timestamp"])

        # Verify person was updated
        person.reload()
        self.assertEqual(person.consent_captured, 1)
        self.assertIsNotNone(person.consent_timestamp)

    def test_capture_consent_not_minor(self):
        """Test capture_consent fails for non-minor."""
        person = self._create_test_person("adult", is_minor=0)

        with self.assertRaises(frappe.ValidationError):
            frappe.call(
                "dartwing.api.person.capture_consent",
                person_name=person.name
            )

    def test_capture_consent_already_captured(self):
        """Test capture_consent fails if already captured."""
        person = self._create_test_person("minor-consent", is_minor=1, consent_captured=1)

        with self.assertRaises(frappe.ValidationError):
            frappe.call(
                "dartwing.api.person.capture_consent",
                person_name=person.name
            )

    def test_capture_consent_self_capture_denied_integration(self):
        """Integration test: Verify minors cannot capture their own consent (full flow without mocks)."""
        # Create a real user with System Manager role
        test_user = frappe.get_doc({
            "doctype": "User",
            "email": "integration.minor@api-test.example.com",
            "first_name": "Integration",
            "last_name": "Minor",
            "enabled": 1,
            "user_type": "System User",
            "roles": [{"role": "System Manager"}]  # Ensure authorized role
        })
        test_user.flags.ignore_permissions = True
        test_user.insert()

        try:
            # Create a minor linked to this user
            person = self._create_test_person(
                "integration-minor",
                is_minor=1,
                consent_captured=0,
                frappe_user=test_user.name
            )

            # Switch to the minor's user session
            original_user = frappe.session.user
            try:
                frappe.set_user(test_user.name)

                # Attempt to capture own consent - should fail with PermissionError
                with self.assertRaises(frappe.PermissionError) as context:
                    frappe.call(
                        "dartwing.api.person.capture_consent",
                        person_name=person.name
                    )

                self.assertIn("Minors cannot capture their own consent", str(context.exception))

            finally:
                frappe.set_user(original_user)
                frappe.delete_doc("Person", person.name, force=True)

        finally:
            frappe.delete_doc("User", test_user.name, force=True)

    def test_capture_consent_permission_denied_integration(self):
        """Integration test: Verify users without write permission cannot capture consent."""
        # Create a user with only basic Website User role (no write permission on Person)
        test_user = frappe.get_doc({
            "doctype": "User",
            "email": "unauthorized.user@api-test.example.com",
            "first_name": "Unauthorized",
            "last_name": "User",
            "enabled": 1,
            "user_type": "Website User",
            "roles": [{"role": "Guest"}]  # No write permission on Person
        })
        test_user.flags.ignore_permissions = True
        test_user.insert()

        try:
            # Create a minor (not linked to test_user)
            person = self._create_test_person(
                "permission-denied-minor",
                is_minor=1,
                consent_captured=0
            )

            # Switch to the unauthorized user
            original_user = frappe.session.user
            try:
                frappe.set_user(test_user.name)

                # Attempt to capture consent - should fail with PermissionError
                # due to lack of write permission on Person document
                with self.assertRaises(frappe.PermissionError):
                    frappe.call(
                        "dartwing.api.person.capture_consent",
                        person_name=person.name
                    )

            finally:
                frappe.set_user(original_user)
                frappe.delete_doc("Person", person.name, force=True)

        finally:
            frappe.delete_doc("User", test_user.name, force=True)

    # =========================================================================
    # get_sync_status API Tests
    # =========================================================================

    def test_get_sync_status(self):
        """Test get_sync_status returns correct fields."""
        person = self._create_test_person("sync-status")

        result = frappe.call(
            "dartwing.api.person.get_sync_status",
            person_name=person.name
        )

        self.assertEqual(result["person_name"], person.name)
        self.assertIn("user_sync_status", result)
        self.assertIn("frappe_user", result)
        self.assertIn("sync_error_message", result)
        self.assertIn("last_sync_at", result)

    def test_get_sync_status_not_found(self):
        """Test get_sync_status fails for non-existent person."""
        with self.assertRaises(frappe.DoesNotExistError):
            frappe.call(
                "dartwing.api.person.get_sync_status",
                person_name="NONEXISTENT-PERSON-12345"
            )

    # =========================================================================
    # retry_sync API Tests
    # =========================================================================

    def test_retry_sync_no_keycloak_id(self):
        """Test retry_sync fails without keycloak_user_id."""
        person = self._create_test_person("no-keycloak")

        with self.assertRaises(frappe.ValidationError):
            frappe.call(
                "dartwing.api.person.retry_sync",
                person_name=person.name
            )

    def test_retry_sync_already_synced(self):
        """Test retry_sync fails if already synced."""
        person = self._create_test_person(
            "synced",
            keycloak_user_id="kc-test-123",
            user_sync_status="synced"
        )

        with self.assertRaises(frappe.ValidationError):
            frappe.call(
                "dartwing.api.person.retry_sync",
                person_name=person.name
            )

    # =========================================================================
    # merge_persons API Tests
    # =========================================================================

    def test_merge_persons_success(self):
        """Test successful merge of two persons."""
        source = self._create_test_person("merge-source")
        target = self._create_test_person("merge-target")

        result = frappe.call(
            "dartwing.api.person.merge_persons",
            source_person=source.name,
            target_person=target.name,
            notes="Test merge"
        )

        self.assertTrue(result["success"])
        self.assertEqual(result["source"], source.name)
        self.assertEqual(result["target"], target.name)

        # Verify source is now Merged
        source.reload()
        self.assertEqual(source.status, "Merged")

        # Verify merge log was created on target
        target.reload()
        self.assertEqual(len(target.merge_logs), 1)
        self.assertEqual(target.merge_logs[0].source_person, source.name)
        self.assertEqual(target.merge_logs[0].notes, "Test merge")

    def test_merge_persons_same_person(self):
        """Test merge fails when source equals target."""
        person = self._create_test_person("self-merge")

        with self.assertRaises(frappe.ValidationError):
            frappe.call(
                "dartwing.api.person.merge_persons",
                source_person=person.name,
                target_person=person.name
            )

    def test_merge_persons_already_merged(self):
        """Test merge fails if source already merged."""
        source = self._create_test_person("already-merged", status="Merged")
        target = self._create_test_person("merge-target2")

        with self.assertRaises(frappe.ValidationError):
            frappe.call(
                "dartwing.api.person.merge_persons",
                source_person=source.name,
                target_person=target.name
            )

    def test_merge_persons_not_found(self):
        """Test merge fails for non-existent person."""
        target = self._create_test_person("merge-target3")

        with self.assertRaises(frappe.DoesNotExistError):
            frappe.call(
                "dartwing.api.person.merge_persons",
                source_person="NONEXISTENT-PERSON-12345",
                target_person=target.name
            )
