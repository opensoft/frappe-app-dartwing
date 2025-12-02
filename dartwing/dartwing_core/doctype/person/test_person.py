# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for Person DocType.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.person.test_person
"""

import frappe
from frappe.tests.utils import FrappeTestCase


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

    def test_user_sync_status_synced_on_success(self):
        """T018: Verify frappe_user link and user_sync_status='synced' when auto-creation succeeds."""
        # This test will be implemented when User sync functionality is added
        pass

    def test_user_sync_status_pending_on_failure(self):
        """T019: Verify Person saved with user_sync_status='pending' when User creation fails."""
        # This test will be implemented when User sync functionality is added
        pass

    # =========================================================================
    # User Story 3: Prevent Deletion of Linked Person - Tests (T026-T027)
    # =========================================================================

    def test_deletion_blocked_with_org_member(self):
        """T026: Verify LinkExistsError when deleting Person linked to Org Member."""
        # This test will be implemented when Org Member exists
        pass

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

    # =========================================================================
    # User Story 4: Merge Duplicate Persons - Tests (T030-T031)
    # =========================================================================

    def test_merge_operation(self):
        """T030: Verify source Person status='Merged', merge log entry created on target."""
        # This test will be implemented when merge functionality is added
        pass

    def test_merge_with_org_members(self):
        """T031: Verify Org Member links transferred to target Person."""
        # This test will be implemented when Org Member exists and merge is implemented
        pass
