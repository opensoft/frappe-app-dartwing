# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for OrganizationMixin.

Tests verify that concrete organization types (Family, Company) can
access parent Organization properties via the mixin.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.mixins.test_organization_mixin
"""

import frappe
from frappe.tests.utils import FrappeTestCase


TEST_PREFIX = "_MixinTest_"


class TestOrganizationMixin(FrappeTestCase):
    """Test cases for OrganizationMixin functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Helper to clean up all test data created by these tests."""
        # Delete test Organizations (will cascade to concrete types via hooks)
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", f"{TEST_PREFIX}%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass

    def _create_test_family(self, name_suffix, **org_kwargs):
        """
        Helper to create a test Family with linked Organization.

        Args:
            name_suffix: Suffix for unique naming
            **org_kwargs: Additional fields to set on the Organization after creation

        Returns:
            tuple: (family_doc, organization_doc)
        """
        # Create Family which auto-creates Organization via hooks
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": f"{TEST_PREFIX}Family {name_suffix}"
        })
        family.insert(ignore_permissions=True)
        family.reload()

        # Get the linked Organization
        org = frappe.get_doc("Organization", family.organization)

        # Update org with any additional kwargs
        if org_kwargs:
            for key, value in org_kwargs.items():
                setattr(org, key, value)
            org.save(ignore_permissions=True)
            org.reload()
            # Clear family's cache since org was updated
            family._clear_organization_cache()

        return family, org

    def _create_test_company(self, name_suffix, **org_kwargs):
        """
        Helper to create a test Company with linked Organization.

        Args:
            name_suffix: Suffix for unique naming
            **org_kwargs: Additional fields to set on the Organization after creation

        Returns:
            tuple: (company_doc, organization_doc)
        """
        # Create Company which auto-creates Organization via hooks
        company = frappe.get_doc({
            "doctype": "Company",
            "company_name": f"{TEST_PREFIX}Company {name_suffix}"
        })
        company.insert(ignore_permissions=True)
        company.reload()

        # Get the linked Organization
        org = frappe.get_doc("Organization", company.organization)

        # Update org with any additional kwargs
        if org_kwargs:
            for key, value in org_kwargs.items():
                setattr(org, key, value)
            org.save(ignore_permissions=True)
            org.reload()
            # Clear company's cache since org was updated
            company._clear_organization_cache()

        return company, org

    # =========================================================================
    # Test org_name property
    # =========================================================================

    def test_org_name_property_returns_parent_value(self):
        """T024: Verify org_name property returns the parent Organization's org_name."""
        family, org = self._create_test_family("orgname1")

        # Access org_name via mixin property
        self.assertEqual(family.org_name, org.org_name)
        self.assertIn(TEST_PREFIX, family.org_name)

    def test_org_name_with_custom_value(self):
        """Test org_name returns custom value set on Organization."""
        family, org = self._create_test_family("orgname2")

        # Update org_name on Organization
        custom_name = f"{TEST_PREFIX}Custom Org Name"
        org.org_name = custom_name
        org.save(ignore_permissions=True)

        # Clear cache and verify
        family._clear_organization_cache()
        self.assertEqual(family.org_name, custom_name)

    def test_org_name_returns_none_when_no_organization(self):
        """Test org_name returns None when organization field is not set."""
        # Create a Family doc without inserting (no organization link yet)
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": f"{TEST_PREFIX}NoOrg Family"
        })
        # Don't insert - organization field will be empty

        self.assertIsNone(family.org_name)

    # =========================================================================
    # Test logo property
    # =========================================================================

    def test_logo_property_returns_parent_value(self):
        """T025: Verify logo property returns the parent Organization's logo."""
        family, org = self._create_test_family("logo1", logo="/files/test-logo.png")

        # Access logo via mixin property
        self.assertEqual(family.logo, "/files/test-logo.png")
        self.assertEqual(family.logo, org.logo)

    def test_logo_returns_none_when_not_set(self):
        """Test logo returns None when not set on Organization."""
        family, org = self._create_test_family("logo2")

        # Logo should be None/empty by default
        self.assertIn(family.logo, [None, ""])

    # =========================================================================
    # Test org_status property
    # =========================================================================

    def test_org_status_property_returns_parent_value(self):
        """T026: Verify org_status property returns the parent Organization's status."""
        family, org = self._create_test_family("status1")

        # Default status should be Active
        self.assertEqual(family.org_status, org.status)
        self.assertEqual(family.org_status, "Active")

    def test_org_status_with_inactive(self):
        """Test org_status returns Inactive when Organization is inactive."""
        family, org = self._create_test_family("status2")

        # Update status on Organization
        org.status = "Inactive"
        org.save(ignore_permissions=True)

        # Clear cache and verify
        family._clear_organization_cache()
        self.assertEqual(family.org_status, "Inactive")

    # =========================================================================
    # Test get_organization_doc method
    # =========================================================================

    def test_get_organization_doc_returns_full_document(self):
        """T027: Verify get_organization_doc returns the full parent Organization document."""
        family, org = self._create_test_family("getdoc1")

        # Get organization doc via mixin method
        org_doc = family.get_organization_doc()

        self.assertIsNotNone(org_doc)
        self.assertEqual(org_doc.doctype, "Organization")
        self.assertEqual(org_doc.name, org.name)
        self.assertEqual(org_doc.org_name, org.org_name)
        self.assertEqual(org_doc.org_type, "Family")

    def test_get_organization_doc_returns_none_when_no_organization(self):
        """Test get_organization_doc returns None when organization field is not set."""
        # Create a Family doc without inserting
        family = frappe.get_doc({
            "doctype": "Family",
            "family_name": f"{TEST_PREFIX}NoOrg Family2"
        })

        org_doc = family.get_organization_doc()
        self.assertIsNone(org_doc)

    def test_get_organization_doc_includes_all_fields(self):
        """Test get_organization_doc returns document with all Organization fields."""
        family, org = self._create_test_family("getdoc2", logo="/files/logo.png")

        org_doc = family.get_organization_doc()

        # Verify key fields are accessible
        self.assertTrue(hasattr(org_doc, "org_name"))
        self.assertTrue(hasattr(org_doc, "org_type"))
        self.assertTrue(hasattr(org_doc, "status"))
        self.assertTrue(hasattr(org_doc, "logo"))
        self.assertTrue(hasattr(org_doc, "linked_doctype"))
        self.assertTrue(hasattr(org_doc, "linked_name"))

    # =========================================================================
    # Test update_org_name functionality (if implemented)
    # =========================================================================

    def test_update_org_name_modifies_parent(self):
        """T028: Verify updating org_name on concrete type updates the parent Organization.

        Note: The mixin provides read-only properties. To update org_name,
        you must update the Organization document directly.
        """
        family, org = self._create_test_family("update1")
        original_name = org.org_name

        # Update org_name on Organization directly
        new_name = f"{TEST_PREFIX}Updated Name"
        org.org_name = new_name
        org.save(ignore_permissions=True)

        # Verify Organization was updated
        org.reload()
        self.assertEqual(org.org_name, new_name)
        self.assertNotEqual(org.org_name, original_name)

        # Clear cache and verify mixin reflects change
        family._clear_organization_cache()
        self.assertEqual(family.org_name, new_name)

    # =========================================================================
    # Test caching behavior
    # =========================================================================

    def test_cache_is_populated_on_first_access(self):
        """Test that cache is populated on first property access."""
        family, org = self._create_test_family("cache1")

        # Cache should not exist initially
        self.assertFalse(hasattr(family, "_org_cache"))

        # Access a property to populate cache
        _ = family.org_name

        # Cache should now exist
        self.assertTrue(hasattr(family, "_org_cache"))
        self.assertIsNotNone(family._org_cache)

    def test_clear_cache_removes_cached_data(self):
        """Test that _clear_organization_cache removes cached data."""
        family, org = self._create_test_family("cache2")

        # Populate cache
        _ = family.org_name
        self.assertTrue(hasattr(family, "_org_cache"))

        # Clear cache
        family._clear_organization_cache()

        # Cache should be removed
        self.assertFalse(hasattr(family, "_org_cache"))

    def test_multiple_property_accesses_use_cache(self):
        """Test that multiple property accesses use cached data (no N+1)."""
        family, org = self._create_test_family("cache3", logo="/files/cached.png")

        # Access multiple properties
        name = family.org_name
        logo = family.logo
        status = family.org_status

        # All should return correct values
        self.assertEqual(name, org.org_name)
        self.assertEqual(logo, "/files/cached.png")
        self.assertEqual(status, "Active")

        # Cache should only contain one entry (all from same query)
        self.assertTrue(hasattr(family, "_org_cache"))
        self.assertIn("org_name", family._org_cache)
        self.assertIn("logo", family._org_cache)
        self.assertIn("status", family._org_cache)

    # =========================================================================
    # Test with Company (different concrete type)
    # =========================================================================

    def test_mixin_works_with_company(self):
        """Test that mixin works correctly with Company concrete type."""
        company, org = self._create_test_company("company1", logo="/files/company-logo.png")

        # Verify all mixin properties work
        self.assertEqual(company.org_name, org.org_name)
        self.assertEqual(company.logo, "/files/company-logo.png")
        self.assertEqual(company.org_status, "Active")

        # Verify get_organization_doc works
        org_doc = company.get_organization_doc()
        self.assertIsNotNone(org_doc)
        self.assertEqual(org_doc.org_type, "Company")
