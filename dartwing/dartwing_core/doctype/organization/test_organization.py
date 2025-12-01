# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Test cases for Organization DocType.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.organization.test_organization
"""

import frappe
from frappe.tests import IntegrationTestCase


class TestOrganization(IntegrationTestCase):
    """Test cases for Organization DocType."""

    def setUp(self):
        """Set up test fixtures."""
        # Clean up any existing test organizations
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Org%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org_name, force=True)

    def tearDown(self):
        """Clean up test data."""
        # Clean up test organizations
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Org%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org_name, force=True)

        # Clean up test families created by organization
        for family_name in frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Test Org%"]},
            pluck="name"
        ):
            frappe.delete_doc("Family", family_name, force=True)

    def test_organization_creation(self):
        """Test basic organization creation."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Basic",
            "org_type": "Family"
        })
        org.insert()

        self.assertEqual(org.org_name, "Test Org Basic")
        self.assertEqual(org.org_type, "Family")
        self.assertEqual(org.status, "Active")
        self.assertTrue(org.name.startswith("ORG-"))

    def test_organization_creates_family(self):
        """Test that creating a Family-type Organization creates a Family."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Family Create",
            "org_type": "Family"
        })
        org.insert()

        # Reload to get linked info
        org.reload()

        # Check Family was created
        self.assertEqual(org.linked_doctype, "Family")
        self.assertIsNotNone(org.linked_name)
        self.assertTrue(frappe.db.exists("Family", org.linked_name))

        # Verify Family details
        family = frappe.get_doc("Family", org.linked_name)
        self.assertEqual(family.family_name, "Test Org Family Create")
        self.assertEqual(family.organization, org.name)

    def test_organization_required_fields(self):
        """Test that org_name and org_type are required."""
        org = frappe.get_doc({
            "doctype": "Organization"
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            org.insert()

    def test_organization_type_immutable(self):
        """Test that org_type cannot be changed after creation."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Immutable",
            "org_type": "Family"
        })
        org.insert()

        # Try to change org_type (should fail due to set_only_once)
        org.org_type = "Company"
        # Note: set_only_once prevents value change, not throws error
        # The value should remain "Family"
        org.save()
        org.reload()
        self.assertEqual(org.org_type, "Family")

    def test_organization_status_default(self):
        """Test default status is Active."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Status",
            "org_type": "Family"
        })
        org.insert()

        self.assertEqual(org.status, "Active")

    def test_organization_delete_cascades(self):
        """Test that deleting Organization deletes linked Family."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Org Cascade",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        family_name = org.linked_name
        self.assertTrue(frappe.db.exists("Family", family_name))

        # Delete organization
        frappe.delete_doc("Organization", org.name)

        # Family should also be deleted
        self.assertFalse(frappe.db.exists("Family", family_name))
