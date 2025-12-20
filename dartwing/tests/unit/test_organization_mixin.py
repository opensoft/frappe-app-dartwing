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
        """Remove test Organization, Family, and Company records."""
        # Delete test families first (due to foreign key)
        family_names = frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Test Mixin%"]},
            pluck="name",
        )
        for name in family_names:
            frappe.delete_doc("Family", name, force=True)

        # Delete test companies (due to foreign key)
        company_names = frappe.get_all(
            "Company",
            filters={"legal_name": ["like", "Test Mixin%"]},
            pluck="name",
        )
        for name in company_names:
            frappe.delete_doc("Company", name, force=True)

        # Delete test organizations (specific patterns to avoid interfering with other tests)
        org_patterns = ["Test Mixin%", "Test Company%"]
        for pattern in org_patterns:
            org_names = frappe.get_all(
                "Organization",
                filters={"org_name": ["like", pattern]},
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

    # T021: Test update_org_name with unicode characters
    def test_update_org_name_with_unicode_characters(self):
        """Verify update_org_name() handles unicode characters correctly."""
        family = frappe.get_doc("Family", self.family.name)

        # Test various unicode characters
        unicode_names = [
            "日本語組織",  # Japanese
            "Société Française",  # French with accents
            "Компания России",  # Russian
            "公司名称 🏢",  # Chinese with emoji
            "Ñoño & Compañía",  # Spanish with ñ
        ]

        for unicode_name in unicode_names:
            family.update_org_name(unicode_name)
            # Verify it was saved correctly in database
            saved_name = frappe.db.get_value("Organization", self.org.name, "org_name")
            self.assertEqual(saved_name, unicode_name, f"Failed for: {unicode_name}")
            # Verify mixin property returns correct unicode value
            self.assertEqual(family.org_name, unicode_name, f"Mixin property failed for: {unicode_name}")
            # Clear cache for next iteration
            family._clear_organization_cache()

    # T022: Test update_org_name is SQL injection safe
    def test_update_org_name_sql_injection_safe(self):
        """Verify update_org_name() is safe from SQL injection attempts.

        Note: SQL injection safety comes from Frappe's ORM using parameterized
        queries. This test verifies the integration works correctly - malicious
        strings are stored as literals without being executed as SQL.
        """
        family = frappe.get_doc("Family", self.family.name)

        # Common SQL injection patterns - should be saved as literal strings
        injection_attempts = [
            "'; DROP TABLE tabOrganization; --",
            "Robert'); DROP TABLE Students;--",
            "1' OR '1'='1",
            "1; DELETE FROM tabOrganization WHERE 1=1;--",
            "' UNION SELECT * FROM tabUser --",
        ]

        # Get initial Organization count to verify no records created/deleted
        initial_org_count = frappe.db.count("Organization")

        for injection in injection_attempts:
            family.update_org_name(injection)
            # Verify it was saved as literal string (not executed)
            saved_name = frappe.db.get_value("Organization", self.org.name, "org_name")
            self.assertEqual(saved_name, injection)
            # Verify Organization table still exists and has our record
            self.assertTrue(frappe.db.exists("Organization", self.org.name))
            # Verify Organization count hasn't changed (no INSERT/DELETE executed)
            current_count = frappe.db.count("Organization")
            self.assertEqual(current_count, initial_org_count,
                f"Organization count changed after injection: {injection}")
            family._clear_organization_cache()

    # T023: Test input trimming preserves internal whitespace
    def test_update_org_name_trims_only_edges(self):
        """Verify update_org_name() trims edges but preserves internal whitespace."""
        family = frappe.get_doc("Family", self.family.name)

        # Leading/trailing whitespace should be stripped
        family.update_org_name("  Acme Corporation  ")
        saved_name = frappe.db.get_value("Organization", self.org.name, "org_name")
        self.assertEqual(saved_name, "Acme Corporation")

        # Internal whitespace should be preserved
        family._clear_organization_cache()
        family.update_org_name("Acme  Double  Space  Corp")
        saved_name = frappe.db.get_value("Organization", self.org.name, "org_name")
        self.assertEqual(saved_name, "Acme  Double  Space  Corp")

    # T024: Test mixin properties work on Company doctype (User Story 3)
    def test_mixin_properties_on_company(self):
        """Verify OrganizationMixin works identically on Company doctype.

        User Story 3: Consistent API Across All Concrete Types
        Tests that org_name, logo, org_status, get_organization_doc(), and
        update_org_name() work the same on Company as they do on Family.
        """
        # Create a Company-specific Organization
        company_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Company Organization",
            "org_type": "Company",
            "status": "Active",
            "logo": "/files/company-logo.png"
        })
        # Skip auto-creation of Company record and field validation for test setup
        company_org.flags.skip_concrete_type = True  # Prevent auto-creation despite org_type='Company'
        company_org.flags.ignore_validate = True      # Skip ORG_FIELD_MAP validation
        company_org.insert(ignore_permissions=True)

        try:
            # Create a Company linked to the Organization
            company = frappe.get_doc({
                "doctype": "Company",
                "legal_name": "Test Mixin Company LLC",
                "organization": company_org.name,
                "status": "Active"
            })
            company.insert(ignore_permissions=True)

            # Test 1: org_name property returns Organization name
            self.assertEqual(company.org_name, "Test Company Organization")

            # Test 2: logo property returns Organization logo
            self.assertEqual(company.logo, "/files/company-logo.png")

            # Test 3: org_status property returns Organization status
            self.assertEqual(company.org_status, "Active")

            # Test 4: get_organization_doc() returns Organization document
            org_doc = company.get_organization_doc()
            self.assertIsNotNone(org_doc)
            self.assertEqual(org_doc.name, company_org.name)
            self.assertEqual(org_doc.org_name, "Test Company Organization")

            # Test 5: update_org_name() updates Organization name
            company.update_org_name("Updated Company Name")
            company._clear_organization_cache()
            self.assertEqual(company.org_name, "Updated Company Name")

            # Verify database was updated
            saved_name = frappe.db.get_value("Organization", company_org.name, "org_name")
            self.assertEqual(saved_name, "Updated Company Name")

            # Clean up Company
            frappe.delete_doc("Company", company.name, force=True)

        finally:
            # Clean up Organization
            if frappe.db.exists("Organization", company_org.name):
                frappe.delete_doc("Organization", company_org.name, force=True)
