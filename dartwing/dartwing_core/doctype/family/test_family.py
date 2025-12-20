# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Test cases for Family DocType.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.family.test_family
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestFamily(FrappeTestCase):
    """Test cases for Family DocType."""

    def setUp(self):
        """Set up test fixtures."""
        # Clean up any existing test families
        for family_name in frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Test Family%"]},
            pluck="name"
        ):
            frappe.delete_doc("Family", family_name, force=True)

    def tearDown(self):
        """Clean up test data."""
        # Clean up test families
        for family_name in frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Test Family%"]},
            pluck="name"
        ):
            frappe.delete_doc("Family", family_name, force=True)

        # Clean up test organizations
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Family%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org_name, force=True)

    def test_family_creation(self):
        """Test basic family creation."""
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Family Basic"
        })
        family.insert()

        self.assertEqual(family.family_name, "Test Family Basic")
        self.assertEqual(family.status, "Active")
        self.assertIsNotNone(family.slug)
        self.assertTrue(family.slug.startswith("test-family"))

    def test_family_slug_generation(self):
        """Test slug generation and uniqueness."""
        # Create first family
        family1 = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Family Slug"
        })
        family1.insert()
        self.assertEqual(family1.slug, "test-family-slug")

        # Create second family with same name prefix
        family2 = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Family Slug 2"
        })
        family2.insert()
        self.assertEqual(family2.slug, "test-family-slug-2")

    def test_family_organization_linking(self):
        """Test that creating a Family auto-creates an Organization."""
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Family Org Link"
        })
        family.insert()

        # Reload to get organization link
        family.reload()

        # Check organization was created
        self.assertIsNotNone(family.organization)
        self.assertTrue(frappe.db.exists("Organization", family.organization))

        # Verify organization details
        org = frappe.get_doc("Organization", family.organization)
        self.assertEqual(org.org_name, "Test Family Org Link")
        self.assertEqual(org.org_type, "Family")
        self.assertEqual(org.linked_doctype, "Family")
        self.assertEqual(org.linked_name, family.name)

    def test_family_with_members(self):
        """Test creating family with members."""
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Family Members",
            "members": [
                {
                    "full_name": "John Doe",
                    "relationship": "Parent",
                    "email": "john@example.com"
                },
                {
                    "full_name": "Jane Doe",
                    "relationship": "Parent",
                    "email": "jane@example.com"
                }
            ]
        })
        family.insert()

        self.assertEqual(len(family.members), 2)
        self.assertEqual(family.members[0].full_name, "John Doe")
        self.assertEqual(family.members[1].full_name, "Jane Doe")

    def test_family_member_age_calculation(self):
        """Test that member ages are calculated correctly."""
        from datetime import date
        from dateutil.relativedelta import relativedelta

        # Create a member who is exactly 10 years old
        dob_10_years = date.today() - relativedelta(years=10)

        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Family Age",
            "members": [
                {
                    "full_name": "Child Ten",
                    "relationship": "Child",
                    "date_of_birth": dob_10_years.isoformat()
                }
            ]
        })
        family.insert()

        member = family.members[0]
        self.assertEqual(member.age, 10)
        self.assertEqual(member.age_category, "Child")
        self.assertEqual(member.is_minor, 1)
        self.assertEqual(member.is_coppa_protected, 1)

    def test_family_required_fields(self):
        """Test that family_name is required."""
        family = frappe.get_doc({
            "doctype": "Family"
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            family.insert()

    def test_family_status_default(self):
        """Test default status is Active."""
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": "Test Family Status"
        })
        family.insert()

        self.assertEqual(family.status, "Active")
