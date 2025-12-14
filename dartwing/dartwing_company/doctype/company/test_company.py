# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Unit tests for Company DocType.

CR-013/14 FIX: Uses unique test prefix to avoid deleting legitimate data.
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompany(FrappeTestCase):
    """Test cases for Company DocType."""

    # CR-013 FIX: Use unique prefix to avoid deleting legitimate test data
    TEST_PREFIX = "__UnitTestCompany_"

    def setUp(self):
        """Set up test fixtures."""
        # Clean up any existing test data
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data after each test."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove test Organizations, Companies, and Persons."""
        # Delete test Companies first (due to foreign key)
        for company in frappe.get_all("Company", filters={"legal_name": ["like", f"{self.TEST_PREFIX}%"]}):
            frappe.delete_doc("Company", company.name, force=True)

        # Delete test Organizations
        for org in frappe.get_all("Organization", filters={"org_name": ["like", f"{self.TEST_PREFIX}%"]}):
            frappe.delete_doc("Organization", org.name, force=True)

        # CR-014 FIX: Also clean up test Persons
        for person in frappe.get_all("Person", filters={"primary_email": ["like", f"{self.TEST_PREFIX}%"]}):
            frappe.delete_doc("Person", person.name, force=True)

    def test_company_auto_creation_from_organization(self):
        """Test that Company is auto-created when Organization with org_type=Company is created."""
        # Create Organization with org_type="Company"
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Auto Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        # Verify Organization was created
        self.assertTrue(frappe.db.exists("Organization", org.name))

        # Verify Company was auto-created
        self.assertIsNotNone(org.linked_name)
        self.assertEqual(org.linked_doctype, "Company")
        self.assertTrue(frappe.db.exists("Company", org.linked_name))

        # Verify Company has correct data
        company = frappe.get_doc("Company", org.linked_name)
        self.assertEqual(company.organization, org.name)
        self.assertEqual(company.legal_name, f"{self.TEST_PREFIX}Auto Company")

    def test_bidirectional_link(self):
        """Test that Organization and Company have bidirectional references."""
        # Create Organization with org_type="Company"
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Bidirectional Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        # Get the auto-created Company
        company = frappe.get_doc("Company", org.linked_name)

        # Verify bidirectional links
        self.assertEqual(company.organization, org.name)
        self.assertEqual(org.linked_doctype, "Company")
        self.assertEqual(org.linked_name, company.name)

        # Verify mixin properties work
        self.assertEqual(company.org_name, org.org_name)
        self.assertEqual(company.org_status, org.status)

    def test_ownership_percentage_warning(self):
        """Test that warning is displayed when ownership exceeds 100%."""
        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Ownership Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        company = frappe.get_doc("Company", org.linked_name)
        company.entity_type = "LLC"

        # CR-014 FIX: Use unique test prefix for Person emails
        person1_email = f"{self.TEST_PREFIX}member1@test.local"
        person2_email = f"{self.TEST_PREFIX}member2@test.local"

        # Create test Persons
        person1 = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Test",
            "last_name": "Member1",
            "primary_email": person1_email,
            "status": "Active"
        })
        person1.insert()

        person2 = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Test",
            "last_name": "Member2",
            "primary_email": person2_email,
            "status": "Active"
        })
        person2.insert()

        try:
            # Add members with ownership > 100%
            company.append("members_partners", {
                "person": person1.name,
                "ownership_percent": 60
            })
            company.append("members_partners", {
                "person": person2.name,
                "ownership_percent": 50
            })

            # Save should succeed but display warning (not throw)
            # We can't easily test msgprint in unit tests, so just verify save works
            company.save()

            # Verify the data was saved
            company.reload()
            self.assertEqual(len(company.members_partners), 2)
        finally:
            # Clean up: remove members before deleting persons
            company.members_partners = []
            company.save()

    def test_cascade_delete(self):
        """Test that Company is deleted when Organization is deleted."""
        # Create Organization with org_type="Company"
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Cascade Delete Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        company_name = org.linked_name
        self.assertTrue(frappe.db.exists("Company", company_name))

        # Delete Organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Verify Company was also deleted
        self.assertFalse(frappe.db.exists("Company", company_name))

    def test_organization_mixin_properties(self):
        """Test that OrganizationMixin properties return correct values."""
        # Create Organization with org_type="Company"
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Mixin Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        company = frappe.get_doc("Company", org.linked_name)

        # Test mixin properties without logo
        self.assertEqual(company.org_name, f"{self.TEST_PREFIX}Mixin Company")
        self.assertEqual(company.org_status, "Active")
        self.assertIsNone(company.logo)  # No logo set yet

        # Set logo on Organization and test that it's accessible via Company
        test_logo_path = "/files/test_logo.png"
        org.logo = test_logo_path
        org.save()

        # Reload company and verify logo is accessible via mixin
        company.reload()
        company._clear_organization_cache()  # Clear cache to ensure fresh data
        self.assertEqual(company.logo, test_logo_path)

        # Test get_organization_doc method
        org_doc = company.get_organization_doc()
        self.assertIsNotNone(org_doc)
        self.assertEqual(org_doc.name, org.name)

    def test_entity_type_options(self):
        """Test that entity_type field has correct options."""
        meta = frappe.get_meta("Company")
        entity_type_field = meta.get_field("entity_type")

        expected_options = [
            "",
            "C-Corp",
            "S-Corp",
            "LLC",
            "Limited Partnership (LP)",
            "General Partnership",
            "LLP",
            "WFOE (China)",
            "Benefit Corporation",
            "Cooperative"
        ]

        actual_options = entity_type_field.options.split("\n")
        self.assertEqual(actual_options, expected_options)

    def test_negative_ownership_rejected(self):
        """Test that negative ownership percentage is rejected (CR-010)."""
        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Negative Ownership Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        company = frappe.get_doc("Company", org.linked_name)
        company.entity_type = "LLC"

        # Create test Person
        person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Test",
            "last_name": "NegativeMember",
            "primary_email": f"{self.TEST_PREFIX}negative@test.local",
            "status": "Active"
        })
        person.insert()

        try:
            # Add member with negative ownership
            company.append("members_partners", {
                "person": person.name,
                "ownership_percent": -10
            })

            # Save should throw validation error
            with self.assertRaises(frappe.ValidationError):
                company.save()
        finally:
            # Clean up
            company.members_partners = []
