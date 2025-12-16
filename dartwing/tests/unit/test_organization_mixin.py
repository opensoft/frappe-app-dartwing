# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Unit tests for OrganizationMixin.

Tests verify the mixin provides correct access to parent Organization
properties and methods from concrete types (Family, Company).
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestOrganizationMixin(FrappeTestCase):
    """Test cases for OrganizationMixin functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures once for all tests."""
        super().setUpClass()
        # Clean up any existing test data
        cls._cleanup_test_data()

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures after all tests."""
        cls._cleanup_test_data()
        super().tearDownClass()

    @classmethod
    def _cleanup_test_data(cls):
        """Remove test Organization and Family records."""
        # Delete test families first (due to foreign key)
        family_names = frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Test Mixin%"]},
            pluck="name",
        )
        for name in family_names:
            frappe.delete_doc("Family", name, force=True)
        # Delete test organizations
        org_names = frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Mixin%"]},
            pluck="name",
        )
        for name in org_names:
            frappe.delete_doc("Organization", name, force=True)

    def setUp(self):
        """Set up test data for each test."""
        # Create a test Organization
        self.org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Mixin Organization",
            "org_type": "Family",
            "status": "Active",
            "logo": "/files/test-logo.png"
        })
        self.org.flags.skip_concrete_type = True  # Don't auto-create Family
        self.org.flags.ignore_validate = True  # Skip ORG_FIELD_MAP validation
        self.org.insert(ignore_permissions=True)

        # Create a test Family linked to the Organization
        self.family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Mixin Family",
            "organization": self.org.name,
            "status": "Active"
        })
        self.family.insert(ignore_permissions=True)

    def tearDown(self):
        """Clean up test data after each test."""
        if hasattr(self, "family") and frappe.db.exists("Family", self.family.name):
            frappe.delete_doc("Family", self.family.name, force=True)
        if hasattr(self, "org") and frappe.db.exists("Organization", self.org.name):
            frappe.delete_doc("Organization", self.org.name, force=True)

    # T012: Test org_name property
    def test_org_name_returns_organization_name(self):
        """Verify org_name property returns correct value from linked Organization."""
        # Reload to ensure fresh data
        family = frappe.get_doc("Family", self.family.name)
        self.assertEqual(family.org_name, "Test Mixin Organization")

    # T013: Test logo property
    def test_logo_returns_organization_logo(self):
        """Verify logo property returns correct value from linked Organization."""
        family = frappe.get_doc("Family", self.family.name)
        self.assertEqual(family.logo, "/files/test-logo.png")

    def test_logo_returns_none_when_empty(self):
        """Verify logo property returns None when Organization has no logo."""
        # Update org to have no logo
        frappe.db.set_value("Organization", self.org.name, "logo", None)

        family = frappe.get_doc("Family", self.family.name)
        self.assertIsNone(family.logo)

    # T014: Test org_status property
    def test_org_status_returns_organization_status(self):
        """Verify org_status property returns correct value from linked Organization."""
        family = frappe.get_doc("Family", self.family.name)
        self.assertEqual(family.org_status, "Active")

    # T015: Test get_organization_doc method
    def test_get_organization_doc_returns_document(self):
        """Verify get_organization_doc() returns full Organization document."""
        family = frappe.get_doc("Family", self.family.name)
        org_doc = family.get_organization_doc()

        self.assertIsNotNone(org_doc)
        self.assertEqual(org_doc.doctype, "Organization")
        self.assertEqual(org_doc.name, self.org.name)
        self.assertEqual(org_doc.org_name, "Test Mixin Organization")

    # T016: Test update_org_name method
    def test_update_org_name_updates_organization(self):
        """Verify update_org_name() changes org_name in database."""
        family = frappe.get_doc("Family", self.family.name)
        family.update_org_name("Updated Organization Name")

        # Verify the Organization was updated in database
        updated_name = frappe.db.get_value("Organization", self.org.name, "org_name")
        self.assertEqual(updated_name, "Updated Organization Name")

        # Verify the property reflects the change (cache cleared)
        self.assertEqual(family.org_name, "Updated Organization Name")

    # T017: Test update_org_name validation
    def test_update_org_name_empty_raises_error(self):
        """Verify update_org_name('') raises ValidationError."""
        family = frappe.get_doc("Family", self.family.name)

        with self.assertRaises(frappe.ValidationError) as context:
            family.update_org_name("")

        self.assertIn("Organization name cannot be empty", str(context.exception))

    def test_update_org_name_whitespace_raises_error(self):
        """Verify update_org_name('   ') raises ValidationError."""
        family = frappe.get_doc("Family", self.family.name)

        with self.assertRaises(frappe.ValidationError) as context:
            family.update_org_name("   ")

        self.assertIn("Organization name cannot be empty", str(context.exception))

    # T018: Test properties return None when organization is null
    def test_properties_return_none_when_organization_null(self):
        """Verify all properties return None when organization field is None."""
        # Create a Family without organization link
        orphan_family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Mixin Orphan Family",
            "organization": None,
            "status": "Active"
        })
        orphan_family.insert(ignore_permissions=True)

        try:
            family = frappe.get_doc("Family", orphan_family.name)
            self.assertIsNone(family.org_name)
            self.assertIsNone(family.logo)
            self.assertIsNone(family.org_status)
            self.assertIsNone(family.get_organization_doc())
        finally:
            frappe.delete_doc("Family", orphan_family.name, force=True)

    # T019: Test properties return None when Organization is deleted
    def test_properties_return_none_when_organization_deleted(self):
        """Verify all properties return None when linked Organization is deleted."""
        # Get the family first
        family = frappe.get_doc("Family", self.family.name)

        # Delete the Organization (without cascade to simulate orphan)
        frappe.db.delete("Organization", self.org.name)

        # Clear cache and reload
        family._clear_organization_cache()

        # All properties should return None
        self.assertIsNone(family.org_name)
        self.assertIsNone(family.logo)
        self.assertIsNone(family.org_status)

        # Mark org as deleted so tearDown doesn't fail
        delattr(self, "org")

    # T020: Test update_org_name raises when no organization
    def test_update_org_name_raises_when_no_organization(self):
        """Verify update_org_name() raises error when organization field is None."""
        # Create a Family without organization link
        orphan_family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Mixin Update Orphan",
            "organization": None,
            "status": "Active"
        })
        orphan_family.insert(ignore_permissions=True)

        try:
            family = frappe.get_doc("Family", orphan_family.name)

            with self.assertRaises(frappe.ValidationError) as context:
                family.update_org_name("New Name")

            expected_msg = "Cannot update organization name: No organization linked"
            self.assertIn(expected_msg, str(context.exception))
        finally:
            frappe.delete_doc("Family", orphan_family.name, force=True)
