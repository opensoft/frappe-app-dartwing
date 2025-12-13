# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Integration tests for Company DocType.

These tests verify cross-doctype interactions and cascade behaviors
as specified in SC-007 and related success criteria.
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestCompanyIntegration(FrappeTestCase):
    """Integration tests for Company DocType interactions."""

    def setUp(self):
        """Set up test fixtures."""
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data after each test."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove test data created during tests."""
        # Delete test Companies first
        for company in frappe.get_all("Company", filters={"legal_name": ["like", "Integration Test%"]}):
            frappe.delete_doc("Company", company.name, force=True)

        # Delete test Organizations
        for org in frappe.get_all("Organization", filters={"org_name": ["like", "Integration Test%"]}):
            frappe.delete_doc("Organization", org.name, force=True)

        # Delete test Persons
        for person in frappe.get_all("Person", filters={"primary_email": ["like", "%integrationtest%"]}):
            frappe.delete_doc("Person", person.name, force=True)

    def test_sc007_cascade_delete_organization_to_company(self):
        """
        SC-007: Verify cascade delete from Organization to Company.

        When an Organization is deleted, its linked Company should also be deleted.
        """
        # Create Organization with org_type="Company"
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Integration Test Cascade Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()
        frappe.db.commit()

        # Verify both records exist
        self.assertTrue(frappe.db.exists("Organization", org.name))
        company_name = org.linked_name
        self.assertTrue(frappe.db.exists("Company", company_name))

        # Delete Organization
        frappe.delete_doc("Organization", org.name, force=True)
        frappe.db.commit()

        # Verify both are deleted
        self.assertFalse(frappe.db.exists("Organization", org.name))
        self.assertFalse(frappe.db.exists("Company", company_name))

    def test_person_deletion_blocked_when_officer(self):
        """
        Test that Person cannot be deleted when linked as Company officer.
        """
        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Integration Test Officer Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        # Create test Person
        person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "IntegrationTestOfficer",
            "last_name": "Person",
            "primary_email": "integrationtestofficer@test.local",
            "status": "Active"
        })
        person.insert()

        # Add Person as officer to Company
        company = frappe.get_doc("Company", org.linked_name)
        company.append("officers", {
            "person": person.name,
            "title": "CEO"
        })
        company.save()

        # Attempt to delete Person should fail
        with self.assertRaises(frappe.LinkExistsError):
            frappe.delete_doc("Person", person.name)

        # Clean up: remove officer link first
        company.officers = []
        company.save()

        # Now deletion should succeed
        frappe.delete_doc("Person", person.name, force=True)
        self.assertFalse(frappe.db.exists("Person", person.name))

    def test_person_deletion_blocked_when_member_partner(self):
        """
        Test that Person cannot be deleted when linked as Company member/partner.
        """
        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Integration Test Member Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        # Create test Person
        person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "IntegrationTestMember",
            "last_name": "Person",
            "primary_email": "integrationtestmember@test.local",
            "status": "Active"
        })
        person.insert()

        # Add Person as member to Company
        company = frappe.get_doc("Company", org.linked_name)
        company.entity_type = "LLC"
        company.append("members_partners", {
            "person": person.name,
            "ownership_percent": 50
        })
        company.save()

        # Attempt to delete Person should fail
        with self.assertRaises(frappe.LinkExistsError):
            frappe.delete_doc("Person", person.name)

        # Clean up: remove member link first
        company.members_partners = []
        company.save()

        # Now deletion should succeed
        frappe.delete_doc("Person", person.name, force=True)
        self.assertFalse(frappe.db.exists("Person", person.name))

    def test_person_deletion_blocked_when_registered_agent(self):
        """
        Test that Person cannot be deleted when set as Company registered agent.
        """
        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Integration Test Agent Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        # Create test Person
        person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "IntegrationTestAgent",
            "last_name": "Person",
            "primary_email": "integrationtestagent@test.local",
            "status": "Active"
        })
        person.insert()

        # Set Person as registered agent
        company = frappe.get_doc("Company", org.linked_name)
        company.registered_agent = person.name
        company.save()

        # Attempt to delete Person should fail
        with self.assertRaises(frappe.LinkExistsError):
            frappe.delete_doc("Person", person.name)

        # Clean up: remove registered agent link first
        company.registered_agent = None
        company.save()

        # Now deletion should succeed
        frappe.delete_doc("Person", person.name, force=True)
        self.assertFalse(frappe.db.exists("Person", person.name))

    def test_company_inherits_organization_status_via_mixin(self):
        """
        Test that Company accesses Organization status through OrganizationMixin.
        """
        # Create Organization
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Integration Test Status Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        company = frappe.get_doc("Company", org.linked_name)

        # Verify initial status
        self.assertEqual(company.org_status, "Active")

        # Update Organization status
        org.status = "Inactive"
        org.save()

        # Reload company and clear the mixin cache to reflect the change
        company.reload()
        company._clear_organization_cache()
        self.assertEqual(company.org_status, "Inactive")

    def test_api_get_company_with_org_details(self):
        """
        Test the get_company_with_org_details API endpoint.
        """
        from dartwing.dartwing_company.api import get_company_with_org_details

        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Integration Test API Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        company = frappe.get_doc("Company", org.linked_name)
        company.legal_name = "Integration Test API Inc."
        company.entity_type = "C-Corp"
        company.save()

        # Call API
        result = get_company_with_org_details(company.name)

        # Verify response (CR-007 FIX: Updated response structure)
        self.assertEqual(result["message"], "success")
        self.assertEqual(result["company"]["name"], company.name)
        self.assertEqual(result["company"]["legal_name"], "Integration Test API Inc.")
        self.assertEqual(result["company"]["entity_type"], "C-Corp")
        self.assertEqual(result["org_details"]["org_name"], "Integration Test API Company")
        self.assertEqual(result["org_details"]["status"], "Active")

    def test_api_validate_ownership(self):
        """
        Test the validate_ownership API endpoint.
        """
        from dartwing.dartwing_company.api import validate_ownership

        # Create Organization and Company
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Integration Test Ownership Company",
            "org_type": "Company",
            "status": "Active"
        })
        org.insert()

        # Create test Persons
        person1 = frappe.get_doc({
            "doctype": "Person",
            "first_name": "IntegrationTestOwner1",
            "last_name": "Person",
            "primary_email": "integrationtestowner1@test.local",
            "status": "Active"
        })
        person1.insert()

        person2 = frappe.get_doc({
            "doctype": "Person",
            "first_name": "IntegrationTestOwner2",
            "last_name": "Person",
            "primary_email": "integrationtestowner2@test.local",
            "status": "Active"
        })
        person2.insert()

        company = frappe.get_doc("Company", org.linked_name)
        company.entity_type = "LLC"
        company.append("members_partners", {
            "person": person1.name,
            "ownership_percent": 60
        })
        company.append("members_partners", {
            "person": person2.name,
            "ownership_percent": 50
        })
        company.save()

        # Call API
        result = validate_ownership(company.name)

        # Verify response (CR-007 FIX: key renamed to total_ownership)
        self.assertFalse(result["valid"])
        self.assertEqual(result["total_ownership"], 110)
        self.assertEqual(result["member_count"], 2)
        self.assertTrue(len(result["warnings"]) > 0)

        # Clean up
        company.members_partners = []
        company.save()
        frappe.delete_doc("Person", person1.name, force=True)
        frappe.delete_doc("Person", person2.name, force=True)
