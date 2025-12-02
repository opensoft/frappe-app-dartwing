# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for Person DocType.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.person.test_person
"""

import frappe
from frappe.tests.utils import FrappeTestCase
from unittest.mock import patch, MagicMock
from frappe.utils import now


class TestPerson(FrappeTestCase):
    """Test cases for Person DocType."""

    def setUp(self):
        """Set up test fixtures."""
        # Clean up any existing test persons
        for person_name in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@test.example.com"]},
            pluck="name"
        ):
            frappe.delete_doc("Person", person_name, force=True)

    def tearDown(self):
        """Clean up test data."""
        # Clean up test persons
        for person_name in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", "%@test.example.com"]},
            pluck="name"
        ):
            frappe.delete_doc("Person", person_name, force=True)

        # Clean up test organizations created for tests
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Org%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org_name, force=True)

    # =========================================================================
    # User Story 1: Create Person Record - Tests (T010-T012a)
    # =========================================================================

    def test_person_creation(self):
        """Test basic person creation with required fields."""
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "john.doe@test.example.com",
            "first_name": "John",
            "last_name": "Doe",
            "source": "signup"
        })
        person.insert()

        self.assertEqual(person.primary_email, "john.doe@test.example.com")
        self.assertEqual(person.first_name, "John")
        self.assertEqual(person.last_name, "Doe")
        self.assertEqual(person.status, "Active")
        self.assertEqual(person.source, "signup")

    def test_duplicate_email_rejected(self):
        """T010: Verify UniqueValidationError thrown when creating Person with existing primary_email."""
        # Create first person
        person1 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "duplicate@test.example.com",
            "first_name": "First",
            "last_name": "Person",
            "source": "signup"
        })
        person1.insert()

        # Attempt to create second person with same email
        person2 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "duplicate@test.example.com",
            "first_name": "Second",
            "last_name": "Person",
            "source": "invite"
        })

        with self.assertRaises(frappe.UniqueValidationError):
            person2.insert()

    def test_nullable_unique_keycloak_user_id_multiple_nulls(self):
        """T011: Verify multiple NULLs allowed for keycloak_user_id."""
        # Create first person without keycloak_user_id
        person1 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "null1@test.example.com",
            "first_name": "Null",
            "last_name": "One",
            "source": "signup"
        })
        person1.insert()
        self.assertIsNone(person1.keycloak_user_id)

        # Create second person without keycloak_user_id - should succeed
        person2 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "null2@test.example.com",
            "first_name": "Null",
            "last_name": "Two",
            "source": "signup"
        })
        person2.insert()
        self.assertIsNone(person2.keycloak_user_id)

    def test_nullable_unique_keycloak_user_id_duplicate_rejected(self):
        """T011: Verify duplicate non-null keycloak_user_id values rejected."""
        # Create first person with keycloak_user_id
        person1 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "keycloak1@test.example.com",
            "first_name": "Keycloak",
            "last_name": "One",
            "source": "signup",
            "keycloak_user_id": "kc-user-12345"
        })
        person1.insert()

        # Attempt to create second person with same keycloak_user_id
        person2 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "keycloak2@test.example.com",
            "first_name": "Keycloak",
            "last_name": "Two",
            "source": "signup",
            "keycloak_user_id": "kc-user-12345"
        })

        with self.assertRaises(frappe.DuplicateEntryError):
            person2.insert()

    def test_mobile_validation_valid_e164(self):
        """T012: Verify E.164 format validation and normalization."""
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "mobile.valid@test.example.com",
            "first_name": "Mobile",
            "last_name": "Valid",
            "source": "signup",
            "mobile_no": "+1 (212) 555-1234"  # Valid NYC area code
        })
        person.insert()

        # Should be normalized to E.164 format
        self.assertEqual(person.mobile_no, "+12125551234")

    def test_mobile_validation_invalid_rejected(self):
        """T012: Verify invalid mobile numbers are rejected."""
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "mobile.invalid@test.example.com",
            "first_name": "Mobile",
            "last_name": "Invalid",
            "source": "signup",
            "mobile_no": "not-a-phone-number"
        })

        with self.assertRaises(frappe.ValidationError):
            person.insert()

    def test_mobile_validation_empty_allowed(self):
        """T012: Verify empty mobile_no is allowed."""
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "mobile.empty@test.example.com",
            "first_name": "Mobile",
            "last_name": "Empty",
            "source": "signup"
        })
        person.insert()

        self.assertFalse(person.mobile_no)

    def test_personal_org_link_valid(self):
        """T012a: Verify Link to Organization works."""
        # Create an organization first
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Personal",
            "org_type": "Family"
        })
        org.insert()

        # Create person linked to the organization
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "org.link@test.example.com",
            "first_name": "Org",
            "last_name": "Link",
            "source": "signup",
            "personal_org": org.name
        })
        person.insert()

        self.assertEqual(person.personal_org, org.name)

    def test_personal_org_link_invalid_rejected(self):
        """T012a: Verify invalid org names are rejected (FR-009)."""
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "org.invalid@test.example.com",
            "first_name": "Org",
            "last_name": "Invalid",
            "source": "signup",
            "personal_org": "NONEXISTENT-ORG-12345"
        })

        with self.assertRaises(frappe.exceptions.LinkValidationError):
            person.insert()

    def test_full_name_computed(self):
        """Test that full_name is computed from first_name + last_name."""
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "fullname@test.example.com",
            "first_name": "Full",
            "last_name": "Name",
            "source": "signup"
        })
        person.insert()

        self.assertEqual(person.full_name, "Full Name")

    def test_minor_consent_blocking(self):
        """Test that writes are blocked for minors without consent (FR-013)."""
        # Create a minor without consent
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "minor@test.example.com",
            "first_name": "Minor",
            "last_name": "Child",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 0
        })
        person.insert()

        # Attempting to update should fail
        person.last_name = "Updated"
        with self.assertRaises(frappe.PermissionError):
            person.save()

    def test_minor_consent_allows_updates(self):
        """Test that minors with consent can be updated."""
        # Create a minor with consent
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "minor.consent@test.example.com",
            "first_name": "Minor",
            "last_name": "WithConsent",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 1
        })
        person.insert()

        # Update should succeed
        person.last_name = "Updated"
        person.save()

        self.assertEqual(person.last_name, "Updated")

    # =========================================================================
    # User Story 2: Link Person to Frappe User - Tests (T018-T019)
    # =========================================================================

    @patch("dartwing.utils.person_sync.is_auto_creation_enabled")
    @patch("dartwing.utils.person_sync.queue_user_sync")
    def test_user_sync_queued_on_person_creation(self, mock_queue_sync, mock_is_enabled):
        """T018: Verify user sync is queued when Person is created with keycloak_user_id."""
        # Enable auto-creation
        mock_is_enabled.return_value = True

        # Create person with keycloak_user_id
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "sync.test@test.example.com",
            "first_name": "Sync",
            "last_name": "Test",
            "source": "signup",
            "keycloak_user_id": "kc-sync-test-123"
        })
        person.insert()

        # Verify sync was queued
        mock_queue_sync.assert_called_once_with(person.name, attempt=1)
        self.assertEqual(person.user_sync_status, "pending")

    @patch("dartwing.utils.person_sync.is_auto_creation_enabled")
    @patch("dartwing.utils.person_sync.queue_user_sync")
    def test_user_sync_not_queued_when_disabled(self, mock_queue_sync, mock_is_enabled):
        """T018: Verify user sync is NOT queued when auto-creation is disabled."""
        # Disable auto-creation
        mock_is_enabled.return_value = False

        # Create person with keycloak_user_id
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "sync.disabled@test.example.com",
            "first_name": "Sync",
            "last_name": "Disabled",
            "source": "signup",
            "keycloak_user_id": "kc-sync-disabled-123"
        })
        person.insert()

        # Verify sync was NOT queued
        mock_queue_sync.assert_not_called()
        self.assertFalse(person.user_sync_status)  # Can be None or empty string

    @patch("dartwing.utils.person_sync.create_frappe_user")
    @patch("frappe.enqueue")
    def test_user_sync_status_synced_on_success(self, mock_enqueue, mock_create_user):
        """T018: Verify frappe_user link and user_sync_status='synced' when auto-creation succeeds."""
        from dartwing.utils.person_sync import sync_frappe_user

        # Clean up any existing test data
        if frappe.db.exists("User", "sync.success@test.example.com"):
            frappe.delete_doc("User", "sync.success@test.example.com", force=True)

        # Create person
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "sync.success@test.example.com",
            "first_name": "Sync",
            "last_name": "Success",
            "source": "signup",
            "keycloak_user_id": "kc-sync-success-123"
        })
        person.insert()

        # Create actual User document for link validation
        test_user = frappe.get_doc({
            "doctype": "User",
            "email": "sync.success@test.example.com",
            "first_name": "Sync",
            "last_name": "Success",
            "enabled": 1,
            "user_type": "Website User"
        })
        test_user.flags.ignore_permissions = True
        test_user.insert()

        try:
            # Mock create_frappe_user to return the actual user
            mock_create_user.return_value = test_user

            # Call sync directly (bypassing queue)
            sync_frappe_user(person.name, attempt=1)

            # Reload person and verify sync succeeded
            person.reload()
            self.assertEqual(person.frappe_user, "sync.success@test.example.com")
            self.assertEqual(person.user_sync_status, "synced")
            self.assertIsNotNone(person.last_sync_at)
            self.assertIsNone(person.sync_error_message)

        finally:
            # Cleanup
            frappe.delete_doc("Person", person.name, force=True)
            frappe.delete_doc("User", test_user.name, force=True)

    @patch("dartwing.utils.person_sync.create_frappe_user")
    @patch("frappe.enqueue")
    def test_user_sync_status_pending_on_retryable_failure(self, mock_enqueue, mock_create_user):
        """T019: Verify Person saved with user_sync_status='pending' when User creation fails with retryable error."""
        from dartwing.utils.person_sync import sync_frappe_user, RetryableError

        # Create person
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "sync.retry@test.example.com",
            "first_name": "Sync",
            "last_name": "Retry",
            "source": "signup",
            "keycloak_user_id": "kc-sync-retry-123"
        })
        person.insert()

        # Mock retryable error
        mock_create_user.side_effect = RetryableError("Database connection failed")

        # Call sync directly (bypassing queue)
        sync_frappe_user(person.name, attempt=1)

        # Reload person and verify status
        person.reload()
        self.assertEqual(person.user_sync_status, "pending")
        self.assertIsNotNone(person.sync_error_message)
        self.assertIn("Database connection failed", person.sync_error_message)

        # Verify retry was queued
        mock_enqueue.assert_called()

    @patch("dartwing.utils.person_sync.create_frappe_user")
    @patch("frappe.enqueue")
    def test_user_sync_status_failed_on_nonretryable_error(self, mock_enqueue, mock_create_user):
        """T019: Verify Person saved with user_sync_status='failed' when User creation fails with non-retryable error."""
        from dartwing.utils.person_sync import sync_frappe_user, NonRetryableError

        # Create person
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "sync.failed@test.example.com",
            "first_name": "Sync",
            "last_name": "Failed",
            "source": "signup",
            "keycloak_user_id": "kc-sync-failed-123"
        })
        person.insert()

        # Mock non-retryable error
        mock_create_user.side_effect = NonRetryableError("Invalid email format")

        # Call sync directly (bypassing queue)
        sync_frappe_user(person.name, attempt=1)

        # Reload person and verify status
        person.reload()
        self.assertEqual(person.user_sync_status, "failed")
        self.assertIsNotNone(person.sync_error_message)
        self.assertIn("Invalid email format", person.sync_error_message)

        # Verify retry was NOT queued
        mock_enqueue.assert_not_called()

    @patch("frappe.enqueue")
    def test_user_sync_exponential_backoff(self, mock_enqueue):
        """Verify exponential backoff is applied to retry attempts."""
        from dartwing.utils.person_sync import queue_user_sync, BASE_DELAY

        person_name = "test-person-backoff"

        # Test first attempt (immediate)
        queue_user_sync(person_name, attempt=1)
        call_kwargs = mock_enqueue.call_args[1]
        self.assertNotIn("enqueue_in", call_kwargs)

        # Test second attempt (2s delay)
        queue_user_sync(person_name, attempt=2)
        call_kwargs = mock_enqueue.call_args[1]
        self.assertEqual(call_kwargs["enqueue_in"], BASE_DELAY * 2)

        # Test third attempt (4s delay)
        queue_user_sync(person_name, attempt=3)
        call_kwargs = mock_enqueue.call_args[1]
        self.assertEqual(call_kwargs["enqueue_in"], BASE_DELAY * 4)

        # Test fourth attempt (8s delay)
        queue_user_sync(person_name, attempt=4)
        call_kwargs = mock_enqueue.call_args[1]
        self.assertEqual(call_kwargs["enqueue_in"], BASE_DELAY * 8)

    def test_minor_allows_system_sync_updates(self):
        """Test that minors without consent can receive system sync updates (FR-013 Exception 2)."""
        # Create a minor without consent
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "minor.sync@test.example.com",
            "first_name": "Minor",
            "last_name": "Sync",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 0,
            "keycloak_user_id": "kc-minor-sync-123"
        })
        person.insert()

        # Update sync fields - should succeed (not setting frappe_user to avoid link validation)
        person.user_sync_status = "synced"
        person.last_sync_at = now()
        person.sync_error_message = None
        person.save()

        # Reload and verify
        person.reload()
        self.assertEqual(person.user_sync_status, "synced")
        self.assertIsNotNone(person.last_sync_at)

    # =========================================================================
    # User Story 3: Prevent Deletion of Linked Person - Tests (T026-T027)
    # =========================================================================

    def test_deletion_blocked_with_org_member(self):
        """T026: Verify LinkExistsError when deleting Person linked to Org Member."""
        # Skip if Org Member DocType doesn't exist
        if not frappe.db.exists("DocType", "Org Member"):
            self.skipTest("Org Member DocType not available")

        # Create organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Deletion",
            "org_type": "Family"
        })
        org.insert()

        # Create person
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "delete.blocked@test.example.com",
            "first_name": "Delete",
            "last_name": "Blocked",
            "source": "signup"
        })
        person.insert()

        # Create Org Member link
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "organization": org.name,
            "person": person.name,
            "role": "Member"
        })
        org_member.insert()

        # Attempt to delete person - should fail
        with self.assertRaises(frappe.LinkExistsError):
            person.delete()

        # Cleanup
        org_member.delete()

    def test_deletion_allowed_without_org_member(self):
        """T027: Verify Person without Org Member links can be deleted."""
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "delete.me@test.example.com",
            "first_name": "Delete",
            "last_name": "Me",
            "source": "signup"
        })
        person.insert()
        person_name = person.name

        # Delete should succeed
        person.delete()

        self.assertFalse(frappe.db.exists("Person", person_name))

    def test_deletion_allowed_when_org_member_doctype_absent(self):
        """T027: Verify Person can be deleted when Org Member DocType doesn't exist."""
        # This test verifies graceful handling when Org Member DocType is absent
        # The _has_org_member_doctype() cache check should prevent errors

        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "delete.no.orgmember@test.example.com",
            "first_name": "Delete",
            "last_name": "NoOrgMember",
            "source": "signup"
        })
        person.insert()
        person_name = person.name

        # Mock the cache to simulate Org Member DocType not existing
        from dartwing.dartwing_core.doctype.person import person as person_module
        original_cache = person_module._org_member_doctype_exists_cache
        try:
            person_module._org_member_doctype_exists_cache = False

            # Delete should succeed without errors
            person.delete()
            self.assertFalse(frappe.db.exists("Person", person_name))

        finally:
            # Restore original cache state
            person_module._org_member_doctype_exists_cache = original_cache

    # =========================================================================
    # User Story 4: Merge Duplicate Persons - Tests (T030-T031)
    # =========================================================================

    def test_merge_operation(self):
        """T030: Verify source Person status='Merged', merge log entry created on target."""
        from dartwing.api.person import merge_persons

        # Create source person
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.source@test.example.com",
            "first_name": "Source",
            "last_name": "Person",
            "source": "signup"
        })
        source.insert()

        # Create target person
        target = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.target@test.example.com",
            "first_name": "Target",
            "last_name": "Person",
            "source": "invite"
        })
        target.insert()

        # Perform merge
        result = merge_persons(source.name, target.name, notes="Test merge")

        # Verify result
        self.assertTrue(result["success"])
        self.assertEqual(result["source"], source.name)
        self.assertEqual(result["target"], target.name)

        # Reload and verify source status
        source.reload()
        self.assertEqual(source.status, "Merged")

        # Reload and verify merge log entry on target
        target.reload()
        self.assertEqual(len(target.merge_logs), 1)
        merge_log = target.merge_logs[0]
        self.assertEqual(merge_log.source_person, source.name)
        self.assertEqual(merge_log.target_person, target.name)
        self.assertEqual(merge_log.notes, "Test merge")
        self.assertIsNotNone(merge_log.merged_at)
        self.assertEqual(merge_log.merged_by, frappe.session.user)

    def test_merge_prevents_duplicate_merge(self):
        """T030: Verify that already-merged Person cannot be merged again."""
        from dartwing.api.person import merge_persons

        # Create three persons
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.source2@test.example.com",
            "first_name": "Source",
            "last_name": "Two",
            "source": "signup"
        })
        source.insert()

        target1 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.target1@test.example.com",
            "first_name": "Target",
            "last_name": "One",
            "source": "invite"
        })
        target1.insert()

        target2 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.target2@test.example.com",
            "first_name": "Target",
            "last_name": "Two",
            "source": "invite"
        })
        target2.insert()

        # First merge
        merge_persons(source.name, target1.name)

        # Attempt second merge of already-merged source - should fail
        with self.assertRaises(frappe.ValidationError) as context:
            merge_persons(source.name, target2.name)

        self.assertIn("already been merged", str(context.exception))

    def test_merge_prevents_self_merge(self):
        """T030: Verify Person cannot be merged into itself."""
        from dartwing.api.person import merge_persons

        # Create person
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.self@test.example.com",
            "first_name": "Self",
            "last_name": "Merge",
            "source": "signup"
        })
        person.insert()

        # Attempt self-merge - should fail
        with self.assertRaises(frappe.ValidationError) as context:
            merge_persons(person.name, person.name)

        self.assertIn("Cannot merge a Person into itself", str(context.exception))

    def test_merge_with_org_members(self):
        """T031: Verify Org Member links transferred to target Person."""
        from dartwing.api.person import merge_persons

        # Skip if Org Member DocType doesn't exist
        if not frappe.db.exists("DocType", "Org Member"):
            self.skipTest("Org Member DocType not available")

        # Create organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Merge",
            "org_type": "Family"
        })
        org.insert()

        # Create source person
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.source.org@test.example.com",
            "first_name": "Source",
            "last_name": "WithOrg",
            "source": "signup"
        })
        source.insert()

        # Create target person
        target = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.target.org@test.example.com",
            "first_name": "Target",
            "last_name": "WithOrg",
            "source": "invite"
        })
        target.insert()

        # Create Org Member link to source
        org_member = frappe.get_doc({
            "doctype": "Org Member",
            "organization": org.name,
            "person": source.name,
            "role": "Member"
        })
        org_member.insert()

        # Perform merge
        result = merge_persons(source.name, target.name)

        # Verify Org Member was transferred
        self.assertEqual(result["org_members_transferred"], 1)

        # Reload Org Member and verify it now points to target
        org_member.reload()
        self.assertEqual(org_member.person, target.name)

        # Cleanup
        org_member.delete()

    def test_merge_without_org_members(self):
        """T031: Verify merge succeeds when source has no Org Member links."""
        from dartwing.api.person import merge_persons

        # Create source person
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.source.noorg@test.example.com",
            "first_name": "Source",
            "last_name": "NoOrg",
            "source": "signup"
        })
        source.insert()

        # Create target person
        target = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.target.noorg@test.example.com",
            "first_name": "Target",
            "last_name": "NoOrg",
            "source": "invite"
        })
        target.insert()

        # Perform merge (no Org Members to transfer)
        result = merge_persons(source.name, target.name)

        # Verify merge succeeded with 0 transfers
        self.assertTrue(result["success"])
        self.assertEqual(result["org_members_transferred"], 0)

    def test_merge_status_transition_validation(self):
        """Test that status transitions are validated correctly during merge."""
        # Test that Merged is a terminal state
        merged_person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merged.terminal@test.example.com",
            "first_name": "Merged",
            "last_name": "Terminal",
            "source": "signup",
            "status": "Active"
        })
        merged_person.insert()

        # Manually set status to Merged
        merged_person.status = "Merged"
        merged_person.save()

        # Attempt to change status - should fail
        merged_person.status = "Active"
        with self.assertRaises(frappe.ValidationError) as context:
            merged_person.save()

        self.assertIn("Cannot change status of a merged Person", str(context.exception))

    @patch("dartwing.api.person._has_org_member_doctype")
    def test_merge_when_org_member_doctype_absent(self, mock_has_org_member):
        """Test merge operation succeeds gracefully when Org Member DocType doesn't exist."""
        from dartwing.api.person import merge_persons

        # Mock Org Member DocType as absent
        mock_has_org_member.return_value = False

        # Create source person
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.source.absent@test.example.com",
            "first_name": "Source",
            "last_name": "Absent",
            "source": "signup"
        })
        source.insert()

        # Create target person
        target = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "merge.target.absent@test.example.com",
            "first_name": "Target",
            "last_name": "Absent",
            "source": "invite"
        })
        target.insert()

        # Perform merge - should succeed without attempting Org Member transfer
        result = merge_persons(source.name, target.name)

        # Verify merge succeeded with 0 transfers (since DocType doesn't exist)
        self.assertTrue(result["success"])
        self.assertEqual(result["org_members_transferred"], 0)

    # =========================================================================
    # API Permission Tests
    # =========================================================================

    def test_capture_consent_permission_denied(self):
        """Test that capture_consent rejects users without write permission."""
        from dartwing.api.person import capture_consent

        # Create a minor without consent
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.perm.minor@test.example.com",
            "first_name": "API",
            "last_name": "PermMinor",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 0
        })
        person.insert()

        # Mock the check_permission method to deny permission
        with patch.object(person.__class__, 'check_permission', side_effect=frappe.PermissionError):
            # Attempt to capture consent - should fail with PermissionError
            with self.assertRaises(frappe.PermissionError):
                capture_consent(person.name)

    @patch("frappe.get_roles")
    def test_capture_consent_self_capture_denied(self, mock_get_roles):
        """Test that minors cannot capture their own consent."""
        from dartwing.api.person import capture_consent
        from dartwing.dartwing_core.doctype.person.person import Person

        # Clean up any existing test data
        if frappe.db.exists("User", "minor.self@test.example.com"):
            frappe.delete_doc("User", "minor.self@test.example.com", force=True)

        # Create a user for the minor
        test_user = frappe.get_doc({
            "doctype": "User",
            "email": "minor.self@test.example.com",
            "first_name": "Minor",
            "last_name": "Self",
            "enabled": 1,
            "user_type": "Website User"
        })
        test_user.flags.ignore_permissions = True
        test_user.insert()

        # Create a minor linked to this user
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "minor.self@test.example.com",
            "first_name": "Minor",
            "last_name": "Self",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 0,
            "frappe_user": test_user.name
        })
        person.insert()

        # Set current user to the minor
        original_user = frappe.session.user
        try:
            frappe.set_user(test_user.name)

            # Mock user roles to include System Manager (passes role gate)
            mock_get_roles.return_value = ["System Manager"]

            # Mock check_permission to succeed (bypassing permission check)
            with patch.object(Person, 'check_permission'):
                # Attempt to capture own consent - should fail at self-capture check
                with self.assertRaises(frappe.PermissionError) as context:
                    capture_consent(person.name)

                self.assertIn("Minors cannot capture their own consent", str(context.exception))

        finally:
            frappe.set_user(original_user)
            # Cleanup - delete person first, then user
            frappe.delete_doc("Person", person.name, force=True)
            frappe.delete_doc("User", test_user.name, force=True)

    @patch("frappe.db.get_single_value")
    @patch("frappe.get_roles")
    def test_capture_consent_role_gate_denied(self, mock_get_roles, mock_get_single_value):
        """Test that capture_consent rejects users without authorized roles."""
        from dartwing.api.person import capture_consent

        # Create a minor without consent
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.role.minor@test.example.com",
            "first_name": "API",
            "last_name": "RoleMinor",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 0
        })
        person.insert()

        # Mock Settings to return "Guardian, Parent" as allowed roles
        mock_get_single_value.return_value = "Guardian, Parent"

        # Mock user having only basic roles (no guardian/parent/system manager)
        mock_get_roles.return_value = ["Website User", "Guest"]

        # Attempt to capture consent - should fail with PermissionError
        with self.assertRaises(frappe.PermissionError) as context:
            capture_consent(person.name)

        self.assertIn("authorized role for consent capture", str(context.exception))

    @patch("frappe.db.get_single_value")
    @patch("frappe.get_roles")
    def test_capture_consent_role_gate_allowed(self, mock_get_roles, mock_get_single_value):
        """Test that capture_consent allows users with authorized roles from Settings."""
        from dartwing.api.person import capture_consent

        # Create a minor without consent
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.guardian.minor@test.example.com",
            "first_name": "API",
            "last_name": "GuardianMinor",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 0
        })
        person.insert()

        # Mock Settings to return "Guardian, Parent" as allowed roles
        mock_get_single_value.return_value = "Guardian, Parent"

        # Mock user having Guardian role
        mock_get_roles.return_value = ["Website User", "Guardian"]

        # Attempt to capture consent - should succeed
        result = capture_consent(person.name)

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["consent_timestamp"])

        # Verify consent was captured
        person.reload()
        self.assertEqual(person.consent_captured, 1)

    @patch("frappe.db.get_single_value")
    @patch("frappe.get_roles")
    def test_capture_consent_system_manager_always_allowed(self, mock_get_roles, mock_get_single_value):
        """Test that System Manager is always allowed regardless of Settings configuration."""
        from dartwing.api.person import capture_consent

        # Create a minor without consent
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.sysmanager.minor@test.example.com",
            "first_name": "API",
            "last_name": "SysManagerMinor",
            "source": "signup",
            "is_minor": 1,
            "consent_captured": 0
        })
        person.insert()

        # Mock Settings to return empty (no custom roles configured)
        mock_get_single_value.return_value = None

        # Mock user having System Manager role
        mock_get_roles.return_value = ["System Manager"]

        # Attempt to capture consent - should succeed (System Manager always allowed)
        result = capture_consent(person.name)

        self.assertTrue(result["success"])
        self.assertIsNotNone(result["consent_timestamp"])

        # Verify consent was captured
        person.reload()
        self.assertEqual(person.consent_captured, 1)

    def test_get_sync_status_permission_denied(self):
        """Test that get_sync_status rejects users without read permission."""
        from dartwing.api.person import get_sync_status
        from dartwing.dartwing_core.doctype.person.person import Person

        # Create person
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.sync.status@test.example.com",
            "first_name": "API",
            "last_name": "SyncStatus",
            "source": "signup"
        })
        person.insert()

        # Mock check_permission to deny permission
        with patch.object(Person, 'check_permission', side_effect=frappe.PermissionError):
            # Attempt to get sync status - should fail with PermissionError
            with self.assertRaises(frappe.PermissionError):
                get_sync_status(person.name)

    def test_retry_sync_permission_denied(self):
        """Test that retry_sync rejects users without write permission."""
        from dartwing.api.person import retry_sync
        from dartwing.dartwing_core.doctype.person.person import Person

        # Create person with keycloak_user_id
        person = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.retry.sync@test.example.com",
            "first_name": "API",
            "last_name": "RetrySync",
            "source": "signup",
            "keycloak_user_id": "kc-retry-test",
            "user_sync_status": "failed"
        })
        person.insert()

        # Mock check_permission to deny permission
        with patch.object(Person, 'check_permission', side_effect=frappe.PermissionError):
            # Attempt to retry sync - should fail with PermissionError
            with self.assertRaises(frappe.PermissionError):
                retry_sync(person.name)

    def test_merge_persons_permission_denied_source(self):
        """Test that merge_persons rejects when user lacks permission on source."""
        from dartwing.api.person import merge_persons
        from dartwing.dartwing_core.doctype.person.person import Person

        # Create two persons
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.merge.source.perm@test.example.com",
            "first_name": "API",
            "last_name": "MergeSourcePerm",
            "source": "signup"
        })
        source.insert()

        target = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.merge.target.perm@test.example.com",
            "first_name": "API",
            "last_name": "MergeTargetPerm",
            "source": "invite"
        })
        target.insert()

        # Mock check_permission to deny permission on source only
        original_check = Person.check_permission
        def mock_check_permission(self, ptype=None, user=None):
            if self.name == source.name:
                raise frappe.PermissionError("No permission on source")
            return original_check(self, ptype, user)

        with patch.object(Person, 'check_permission', mock_check_permission):
            # Attempt to merge - should fail with PermissionError
            with self.assertRaises(frappe.PermissionError):
                merge_persons(source.name, target.name)

    def test_merge_persons_permission_denied_target(self):
        """Test that merge_persons rejects when user lacks permission on target."""
        from dartwing.api.person import merge_persons
        from dartwing.dartwing_core.doctype.person.person import Person

        # Create two persons
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.merge.source.perm2@test.example.com",
            "first_name": "API",
            "last_name": "MergeSourcePerm2",
            "source": "signup"
        })
        source.insert()

        target = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.merge.target.perm2@test.example.com",
            "first_name": "API",
            "last_name": "MergeTargetPerm2",
            "source": "invite"
        })
        target.insert()

        # Mock check_permission to deny permission on target only
        original_check = Person.check_permission
        def mock_check_permission(self, ptype=None, user=None):
            if self.name == target.name:
                raise frappe.PermissionError("No permission on target")
            return original_check(self, ptype, user)

        with patch.object(Person, 'check_permission', mock_check_permission):
            # Attempt to merge - should fail with PermissionError
            with self.assertRaises(frappe.PermissionError):
                merge_persons(source.name, target.name)

    def test_merge_persons_prevents_merge_into_merged_target(self):
        """Test that merge_persons rejects merging into an already-merged target."""
        from dartwing.api.person import merge_persons

        # Create three persons
        source = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.merge.source3@test.example.com",
            "first_name": "API",
            "last_name": "MergeSource3",
            "source": "signup"
        })
        source.insert()

        target1 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.merge.target3a@test.example.com",
            "first_name": "API",
            "last_name": "MergeTarget3a",
            "source": "invite"
        })
        target1.insert()

        target2 = frappe.get_doc({
            "doctype": "Person",
            "primary_email": "api.merge.target3b@test.example.com",
            "first_name": "API",
            "last_name": "MergeTarget3b",
            "source": "invite"
        })
        target2.insert()

        # First merge: target1 into target2
        merge_persons(target1.name, target2.name)

        # Attempt to merge source into already-merged target1 - should fail
        with self.assertRaises(frappe.ValidationError) as context:
            merge_persons(source.name, target1.name)

        self.assertIn("already been merged", str(context.exception))
