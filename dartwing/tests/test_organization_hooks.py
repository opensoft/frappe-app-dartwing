# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Test cases for Organization Bidirectional Hooks.

Feature: 004-org-bidirectional-hooks
Tests: FR-001 through FR-013

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.tests.test_organization_hooks
"""

import time
import frappe
from frappe.tests.utils import FrappeTestCase

from dartwing.dartwing_core.doctype.organization.organization import (
    ORG_TYPE_MAP,
    get_concrete_doc,
    get_organization_with_details,
)


class TestOrganizationBidirectionalHooks(FrappeTestCase):
    """
    Test cases for Organization Bidirectional Hooks feature.

    Covers all four user stories:
    - US1: Automatic Concrete Type Creation (P1)
    - US2: Organization Retrieval with Concrete Details (P1)
    - US3: Cascade Delete to Concrete Type (P2)
    - US4: Organization Type Immutability (P2)
    """

    def setUp(self):
        """Set up test fixtures before each test."""
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data after each test."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Clean up all test organizations and families."""
        # Clean up test organizations
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Hook%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
            except Exception:
                pass

        # Clean up test families
        for family_name in frappe.get_all(
            "Family",
            filters={"family_name": ["like", "Test Hook%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Family", family_name, force=True, ignore_permissions=True)
            except Exception:
                pass

        # Clean up test companies
        for company_name in frappe.get_all(
            "Company",
            filters={"company_name": ["like", "Test Hook%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Company", company_name, force=True, ignore_permissions=True)
            except Exception:
                pass

        # Clean up test associations
        for assoc_name in frappe.get_all(
            "Association",
            filters={"association_name": ["like", "Test Hook%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Association", assoc_name, force=True, ignore_permissions=True)
            except Exception:
                pass

        # Clean up test nonprofits
        for nonprofit_name in frappe.get_all(
            "Nonprofit",
            filters={"nonprofit_name": ["like", "Test Hook%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Nonprofit", nonprofit_name, force=True, ignore_permissions=True)
            except Exception:
                pass

        frappe.db.commit()

    # =========================================================================
    # User Story 1: Automatic Concrete Type Creation (P1)
    # =========================================================================

    def test_us1_org_type_family_creates_family_record(self):
        """T008: Test Organization with org_type Family creates Family record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Family",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        # Verify Family was created
        self.assertEqual(org.linked_doctype, "Family")
        self.assertIsNotNone(org.linked_name)
        self.assertTrue(frappe.db.exists("Family", org.linked_name))

    def test_us1_linked_doctype_populated(self):
        """T012: Test linked_doctype is populated correctly."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Linked DocType",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        self.assertEqual(org.linked_doctype, "Family")

    def test_us1_linked_name_populated(self):
        """T012: Test linked_name is populated correctly."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Linked Name",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        self.assertIsNotNone(org.linked_name)
        # Verify the linked name points to an actual record
        self.assertTrue(frappe.db.exists("Family", org.linked_name))

    def test_us1_concrete_type_organization_field_points_back(self):
        """T013: Test concrete type's organization field points back to Organization."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Backlink",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        family = frappe.get_doc("Family", org.linked_name)
        self.assertEqual(family.organization, org.name)

    def test_us1_invalid_org_type_rejected(self):
        """T014: Test invalid org_type is rejected with ValidationError."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Invalid Type",
            "org_type": "InvalidType"
        })

        with self.assertRaises(frappe.exceptions.ValidationError) as context:
            org.insert()

        self.assertIn("Invalid org_type", str(context.exception))
        self.assertIn("Family, Company, Association, Nonprofit", str(context.exception))

    def test_us1_org_type_map_contains_expected_types(self):
        """Verify ORG_TYPE_MAP contains all four expected types."""
        expected_types = {"Family", "Company", "Association", "Nonprofit"}
        self.assertEqual(set(ORG_TYPE_MAP.keys()), expected_types)

    def test_us1_org_type_company_creates_company_record(self):
        """T009: Test Organization with org_type Company creates Company record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Company",
            "org_type": "Company"
        })
        org.insert()
        org.reload()

        # Verify Company was created
        self.assertEqual(org.linked_doctype, "Company")
        self.assertIsNotNone(org.linked_name)
        self.assertTrue(frappe.db.exists("Company", org.linked_name))

        # Verify Company has correct field values
        company = frappe.get_doc("Company", org.linked_name)
        self.assertEqual(company.company_name, "Test Hook Company")
        self.assertEqual(company.organization, org.name)

    def test_us1_org_type_association_creates_association_record(self):
        """T010: Test Organization with org_type Association creates Association record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Association",
            "org_type": "Association"
        })
        org.insert()
        org.reload()

        # Verify Association was created
        self.assertEqual(org.linked_doctype, "Association")
        self.assertIsNotNone(org.linked_name)
        self.assertTrue(frappe.db.exists("Association", org.linked_name))

        # Verify Association has correct field values
        association = frappe.get_doc("Association", org.linked_name)
        self.assertEqual(association.association_name, "Test Hook Association")
        self.assertEqual(association.organization, org.name)

    def test_us1_org_type_nonprofit_creates_nonprofit_record(self):
        """T011: Test Organization with org_type Nonprofit creates Nonprofit record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Nonprofit",
            "org_type": "Nonprofit"
        })
        org.insert()
        org.reload()

        # Verify Nonprofit was created
        self.assertEqual(org.linked_doctype, "Nonprofit")
        self.assertIsNotNone(org.linked_name)
        self.assertTrue(frappe.db.exists("Nonprofit", org.linked_name))

        # Verify Nonprofit has correct field values
        nonprofit = frappe.get_doc("Nonprofit", org.linked_name)
        self.assertEqual(nonprofit.nonprofit_name, "Test Hook Nonprofit")
        self.assertEqual(nonprofit.organization, org.name)

    # =========================================================================
    # User Story 2: Organization Retrieval with Concrete Details (P1)
    # =========================================================================

    def test_us2_get_concrete_doc_returns_document(self):
        """T022: Test get_concrete_doc returns concrete type document."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Get Concrete",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        concrete = get_concrete_doc(org.name)

        self.assertIsNotNone(concrete)
        self.assertEqual(concrete["doctype"], "Family")
        self.assertEqual(concrete["name"], org.linked_name)
        self.assertEqual(concrete["organization"], org.name)

    def test_us2_get_concrete_doc_returns_none_when_no_link(self):
        """T023: Test get_concrete_doc returns None when no linked concrete type."""
        # Create org with skip_concrete_type flag to avoid auto-creation
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook No Concrete",
            "org_type": "Family"
        })
        org.flags.skip_concrete_type = True
        org.insert()

        concrete = get_concrete_doc(org.name)
        self.assertIsNone(concrete)

    def test_us2_get_organization_with_details_returns_merged_data(self):
        """T024: Test get_organization_with_details returns merged data."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook With Details",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        result = get_organization_with_details(org.name)

        # Verify Organization fields
        self.assertEqual(result["name"], org.name)
        self.assertEqual(result["org_name"], "Test Hook With Details")
        self.assertEqual(result["org_type"], "Family")

        # Verify concrete_type is present
        self.assertIn("concrete_type", result)
        self.assertIsNotNone(result["concrete_type"])

    def test_us2_get_organization_with_details_includes_nested_object(self):
        """T025: Test get_organization_with_details includes concrete_type nested object."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Nested",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        result = get_organization_with_details(org.name)

        # Verify concrete_type structure
        concrete = result["concrete_type"]
        self.assertEqual(concrete["doctype"], "Family")
        self.assertEqual(concrete["family_name"], "Test Hook Nested")
        self.assertEqual(concrete["organization"], org.name)

    def test_us2_retrieval_performance(self):
        """T026: Test retrieval completes within 500ms."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Performance",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        start_time = time.time()
        result = get_organization_with_details(org.name)
        elapsed_ms = (time.time() - start_time) * 1000

        self.assertIsNotNone(result)
        self.assertLess(elapsed_ms, 500, f"Retrieval took {elapsed_ms:.2f}ms, expected < 500ms")

    # =========================================================================
    # User Story 3: Cascade Delete to Concrete Type (P2)
    # =========================================================================

    def test_us3_delete_org_cascades_to_family(self):
        """T030: Test deleting Organization cascades to delete Family record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Cascade Delete",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        family_name = org.linked_name
        self.assertTrue(frappe.db.exists("Family", family_name))

        # Delete organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Verify Family was also deleted
        self.assertFalse(frappe.db.exists("Family", family_name))

    def test_us3_deletion_succeeds_when_concrete_missing(self):
        """T032: Test deletion succeeds when concrete type already missing."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Missing Concrete",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        family_name = org.linked_name

        # Manually delete the Family first
        frappe.delete_doc("Family", family_name, force=True, ignore_permissions=True)
        frappe.db.commit()

        # Now delete Organization - should not raise error
        try:
            frappe.delete_doc("Organization", org.name, force=True)
        except Exception as e:
            self.fail(f"Deletion should succeed even when concrete type is missing: {e}")

    def test_us3_other_orgs_unaffected(self):
        """T033: Test other Organizations unaffected by single deletion."""
        # Create two organizations
        org1 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Org One",
            "org_type": "Family"
        })
        org1.insert()
        org1.reload()

        org2 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Org Two",
            "org_type": "Family"
        })
        org2.insert()
        org2.reload()

        org2_name = org2.name
        family2_name = org2.linked_name

        # Delete first organization
        frappe.delete_doc("Organization", org1.name, force=True)

        # Second organization and its Family should still exist
        self.assertTrue(frappe.db.exists("Organization", org2_name))
        self.assertTrue(frappe.db.exists("Family", family2_name))

    # =========================================================================
    # User Story 4: Organization Type Immutability (P2)
    # =========================================================================

    def test_us4_changing_org_type_raises_error(self):
        """T039: Test changing org_type raises ValidationError."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Immutable",
            "org_type": "Family"
        })
        org.insert()

        # Attempt to change org_type via direct assignment
        # Note: set_only_once attribute should prevent this at form level
        # Server-side validation provides defense in depth
        org.org_type = "Company"

        with self.assertRaises(frappe.exceptions.ValidationError) as context:
            org.save()

        self.assertIn("cannot be changed", str(context.exception))

    def test_us4_modifying_other_fields_succeeds(self):
        """T040: Test modifying other fields (org_name, status) succeeds."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Modify Other",
            "org_type": "Family"
        })
        org.insert()

        # Change other fields
        org.org_name = "Test Hook Modified Name"
        org.status = "Inactive"
        org.save()
        org.reload()

        self.assertEqual(org.org_name, "Test Hook Modified Name")
        self.assertEqual(org.status, "Inactive")
        self.assertEqual(org.org_type, "Family")  # Unchanged

    def test_us4_error_message_is_clear(self):
        """T041: Test error message is clear and user-friendly."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Hook Clear Error",
            "org_type": "Family"
        })
        org.insert()

        org.org_type = "Company"

        with self.assertRaises(frappe.exceptions.ValidationError) as context:
            org.save()

        error_message = str(context.exception)
        self.assertIn("Organization type", error_message)
        self.assertIn("cannot be changed", error_message)


class TestOrganizationHooksEdgeCases(FrappeTestCase):
    """Test edge cases and error handling for Organization hooks."""

    def setUp(self):
        """Set up test fixtures."""
        frappe.set_user("Administrator")
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Clean up all test data."""
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Edge%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
            except Exception:
                pass

        # Clean up all concrete types for edge case tests
        for doctype, name_field in [("Family", "family_name"), ("Company", "company_name"),
                                      ("Association", "association_name"), ("Nonprofit", "nonprofit_name")]:
            for doc_name in frappe.get_all(
                doctype,
                filters={name_field: ["like", "Test Edge%"]},
                pluck="name"
            ):
                try:
                    frappe.delete_doc(doctype, doc_name, force=True, ignore_permissions=True)
                except Exception:
                    pass

        frappe.db.commit()

    def test_organization_without_name_fails(self):
        """Test that Organization without org_name fails validation."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_type": "Family"
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            org.insert()

    def test_skip_concrete_type_flag_works(self):
        """Test that skip_concrete_type flag prevents concrete creation."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Edge Skip Concrete",
            "org_type": "Family"
        })
        org.flags.skip_concrete_type = True
        org.insert()

        self.assertIsNone(org.linked_doctype)
        self.assertIsNone(org.linked_name)

    def test_default_status_is_active(self):
        """Test that default status is 'Active'."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Edge Default Status",
            "org_type": "Family"
        })
        org.insert()

        self.assertEqual(org.status, "Active")

    def test_naming_series_applied(self):
        """Test that naming series is applied correctly."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Edge Naming",
            "org_type": "Family"
        })
        org.insert()

        self.assertTrue(org.name.startswith("ORG-"))

    def test_duplicate_family_names_allowed(self):
        """Test that multiple families can have the same family_name (Issue #2)."""
        # Create first organization with family
        org1 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Edge Duplicate Name Org1",
            "org_type": "Family"
        })
        org1.insert()
        org1.reload()

        family1_name = org1.linked_name
        family1 = frappe.get_doc("Family", family1_name)

        # Create second organization with family using same family_name
        org2 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Edge Duplicate Name Org2",
            "org_type": "Family"
        })
        org2.insert()
        org2.reload()

        family2_name = org2.linked_name
        family2 = frappe.get_doc("Family", family2_name)

        # Manually update family2 to have same family_name as family1
        # This should succeed without unique constraint violation
        try:
            family2.family_name = family1.family_name
            family2.save()

            # Verify both families exist with same name but different IDs
            families = frappe.get_all(
                "Family",
                filters={"family_name": family1.family_name},
                pluck="name"
            )
            self.assertEqual(len(families), 2, "Should allow duplicate family names")
            self.assertIn(family1_name, families)
            self.assertIn(family2_name, families)
        except frappe.exceptions.DuplicateEntryError:
            self.fail("Duplicate family names should be allowed (unique constraint removed)")


class TestOrganizationConcurrency(FrappeTestCase):
    """Test concurrent Organization creation (SC-006)."""

    def setUp(self):
        """Set up test fixtures."""
        frappe.set_user("Administrator")
        self._cleanup_test_data()

    def tearDown(self):
        """Clean up test data."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Clean up all test data."""
        for org_name in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", "Test Concurrent%"]},
            pluck="name"
        ):
            try:
                frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
            except Exception:
                pass

        # Clean up all concrete types for concurrency tests
        for doctype, name_field in [("Family", "family_name"), ("Company", "company_name"),
                                      ("Association", "association_name"), ("Nonprofit", "nonprofit_name")]:
            for doc_name in frappe.get_all(
                doctype,
                filters={name_field: ["like", "Test Concurrent%"]},
                pluck="name"
            ):
                try:
                    frappe.delete_doc(doctype, doc_name, force=True, ignore_permissions=True)
                except Exception:
                    pass

        frappe.db.commit()

    def test_sc006_concurrent_organization_creation(self):
        """T049: Test 100 concurrent Organization creations without data corruption.

        SC-006: System handles 100 concurrent Organization creations without
        data corruption or link inconsistencies.

        Note: This is a simplified sequential test since Frappe tests run in a
        single thread. True concurrent testing would require external load testing.
        """
        num_orgs = 100
        created_orgs = []

        # Create 100 organizations rapidly
        for i in range(num_orgs):
            org = frappe.get_doc({
                "doctype": "Organization",
                "org_name": f"Test Concurrent Org {i:03d}",
                "org_type": "Family"
            })
            org.insert()
            created_orgs.append(org.name)

        frappe.db.commit()

        # Verify all organizations have proper bidirectional links
        corrupted = []
        for org_name in created_orgs:
            org = frappe.get_doc("Organization", org_name)

            # Verify linked_doctype and linked_name are set
            if not org.linked_doctype or not org.linked_name:
                corrupted.append(f"{org_name}: missing linked fields")
                continue

            # Verify concrete type exists
            if not frappe.db.exists(org.linked_doctype, org.linked_name):
                corrupted.append(f"{org_name}: concrete type missing")
                continue

            # Verify bidirectional link
            family = frappe.get_doc("Family", org.linked_name)
            if family.organization != org_name:
                corrupted.append(f"{org_name}: bidirectional link broken")

        self.assertEqual(
            len(corrupted), 0,
            f"Found {len(corrupted)} corrupted organizations:\n" + "\n".join(corrupted[:10])
        )
        self.assertEqual(len(created_orgs), num_orgs)
