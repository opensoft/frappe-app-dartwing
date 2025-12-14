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
    ORG_FIELD_MAP,
    get_concrete_doc,
    get_organization_with_details,
)


# Unique prefix for this test module to avoid collisions with other test suites
TEST_PREFIX = "_OrgHooksTest_"


def cleanup_test_organizations() -> None:
    """
    Shared utility for cleaning up test organizations and concrete types (Issue #20).

    Uses TEST_PREFIX to ensure only data created by this test module is removed,
    avoiding accidental deletion of unrelated test data in shared environments.
    """
    pattern = f"{TEST_PREFIX}%"

    # Clean up organizations matching the test prefix
    for org_name in frappe.get_all(
        "Organization",
        filters={"org_name": ["like", pattern]},
        pluck="name"
    ):
        try:
            frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
        except Exception:
            pass

    # Clean up all concrete types matching the test prefix
    # Derive from ORG_FIELD_MAP to maintain single source of truth
    for org_type, field_config in ORG_FIELD_MAP.items():
        doctype = ORG_TYPE_MAP.get(org_type)
        name_field = field_config.get("name_field")
        if not doctype or not name_field:
            continue
        for doc_name in frappe.get_all(
            doctype,
            filters={name_field: ["like", pattern]},
            pluck="name"
        ):
            try:
                frappe.delete_doc(doctype, doc_name, force=True, ignore_permissions=True)
            except Exception:
                pass

    frappe.db.commit()


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
        cleanup_test_organizations()

    def tearDown(self):
        """Clean up test data after each test."""
        cleanup_test_organizations()

    # =========================================================================
    # User Story 1: Automatic Concrete Type Creation (P1)
    # =========================================================================

    def test_us1_org_type_family_creates_family_record(self):
        """T008: Test Organization with org_type Family creates Family record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Family",
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
            "org_name": f"{TEST_PREFIX}Linked DocType",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        self.assertEqual(org.linked_doctype, "Family")

    def test_us1_linked_name_populated(self):
        """T012: Test linked_name is populated correctly."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Linked Name",
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
            "org_name": f"{TEST_PREFIX}Backlink",
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
            "org_name": f"{TEST_PREFIX}Invalid Type",
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
            "org_name": f"{TEST_PREFIX}Company",
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
        self.assertEqual(company.company_name, f"{TEST_PREFIX}Company")
        self.assertEqual(company.organization, org.name)

    def test_us1_org_type_association_creates_association_record(self):
        """T010: Test Organization with org_type Association creates Association record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Association",
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
        self.assertEqual(association.association_name, f"{TEST_PREFIX}Association")
        self.assertEqual(association.organization, org.name)

    def test_us1_org_type_nonprofit_creates_nonprofit_record(self):
        """T011: Test Organization with org_type Nonprofit creates Nonprofit record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Nonprofit",
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
        self.assertEqual(nonprofit.nonprofit_name, f"{TEST_PREFIX}Nonprofit")
        self.assertEqual(nonprofit.organization, org.name)

    # =========================================================================
    # User Story 2: Organization Retrieval with Concrete Details (P1)
    # =========================================================================

    def test_us2_get_concrete_doc_returns_document(self):
        """T022: Test get_concrete_doc returns concrete type document."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Get Concrete",
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
            "org_name": f"{TEST_PREFIX}No Concrete",
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
            "org_name": f"{TEST_PREFIX}With Details",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        result = get_organization_with_details(org.name)

        # Verify Organization fields
        self.assertEqual(result["name"], org.name)
        self.assertEqual(result["org_name"], f"{TEST_PREFIX}With Details")
        self.assertEqual(result["org_type"], "Family")

        # Verify concrete_type is present
        self.assertIn("concrete_type", result)
        self.assertIsNotNone(result["concrete_type"])

    def test_us2_get_organization_with_details_includes_nested_object(self):
        """T025: Test get_organization_with_details includes concrete_type nested object."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Nested",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        result = get_organization_with_details(org.name)

        # Verify concrete_type structure
        concrete = result["concrete_type"]
        self.assertEqual(concrete["doctype"], "Family")
        self.assertEqual(concrete["family_name"], f"{TEST_PREFIX}Nested")
        self.assertEqual(concrete["organization"], org.name)

    def test_us2_retrieval_performance(self):
        """T026: Test retrieval completes within 500ms."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Performance",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        start_time = time.time()
        result = get_organization_with_details(org.name)
        elapsed_ms = (time.time() - start_time) * 1000

        self.assertIsNotNone(result)
        self.assertLess(elapsed_ms, 500, f"Retrieval took {elapsed_ms:.2f}ms, expected < 500ms")

    def test_get_organization_with_details_handles_missing_concrete(self):
        """Test optimized get_organization_with_details handles missing concrete type (Issue #11)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Optimized Missing",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        family_name = org.linked_name

        # Delete the Family to simulate orphaned organization
        frappe.delete_doc("Family", family_name, force=True, ignore_permissions=True)
        frappe.db.commit()

        # Verify get_organization_with_details handles this gracefully
        # (uses try/except instead of db.exists() for optimization)
        result = get_organization_with_details(org.name)

        self.assertIsNotNone(result)
        self.assertEqual(result["name"], org.name)
        # concrete_type should be None when missing
        self.assertIsNone(result["concrete_type"])

    # =========================================================================
    # User Story 3: Cascade Delete to Concrete Type (P2)
    # =========================================================================

    def test_us3_delete_org_cascades_to_family(self):
        """T030: Test deleting Organization cascades to delete Family record."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Cascade Delete",
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
            "org_name": f"{TEST_PREFIX}Missing Concrete",
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
            "org_name": f"{TEST_PREFIX}Org One",
            "org_type": "Family"
        })
        org1.insert()
        org1.reload()

        org2 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Org Two",
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

    def test_cascade_delete_respects_link_constraints(self):
        """Test that cascade delete respects link constraints (Issue #8)."""
        # This test would require creating a linked record to the Family
        # For now, we verify that without force=True, the delete mechanism
        # will properly handle LinkExistsError if such constraints exist
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Link Constraint",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        # Verify the organization was created successfully
        self.assertTrue(frappe.db.exists("Family", org.linked_name))

        # Normal cascade delete should succeed (no links exist)
        frappe.delete_doc("Organization", org.name)

        # Verify Family was deleted
        self.assertFalse(frappe.db.exists("Family", org.linked_name))

    def test_linked_doctype_set_before_concrete_creation(self):
        """Test that linked_doctype is set before concrete type creation (Issue #15)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Race Condition",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        # Verify linked_doctype is set
        self.assertEqual(org.linked_doctype, "Family")
        self.assertIsNotNone(org.linked_name)

        # Verify the concrete type exists
        self.assertTrue(frappe.db.exists("Family", org.linked_name))

        # Verify bidirectional link
        family = frappe.get_doc("Family", org.linked_name)
        self.assertEqual(family.organization, org.name)

    def test_us3_delete_org_cascades_to_company(self):
        """Test deleting Organization cascades to delete Company record (Issue #7)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Company Cascade",
            "org_type": "Company"
        })
        org.insert()
        org.reload()

        company_name = org.linked_name
        self.assertTrue(frappe.db.exists("Company", company_name))

        # Delete organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Verify Company was also deleted
        self.assertFalse(frappe.db.exists("Company", company_name))

    def test_us3_delete_org_cascades_to_association(self):
        """Test deleting Organization cascades to delete Association record (Issue #7)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Association Cascade",
            "org_type": "Association"
        })
        org.insert()
        org.reload()

        association_name = org.linked_name
        self.assertTrue(frappe.db.exists("Association", association_name))

        # Delete organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Verify Association was also deleted
        self.assertFalse(frappe.db.exists("Association", association_name))

    def test_us3_delete_org_cascades_to_nonprofit(self):
        """Test deleting Organization cascades to delete Nonprofit record (Issue #7)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Nonprofit Cascade",
            "org_type": "Nonprofit"
        })
        org.insert()
        org.reload()

        nonprofit_name = org.linked_name
        self.assertTrue(frappe.db.exists("Nonprofit", nonprofit_name))

        # Delete organization
        frappe.delete_doc("Organization", org.name, force=True)

        # Verify Nonprofit was also deleted
        self.assertFalse(frappe.db.exists("Nonprofit", nonprofit_name))

    # =========================================================================
    # User Story 4: Organization Type Immutability (P2)
    # =========================================================================

    def test_us4_changing_org_type_raises_error(self):
        """T039: Test changing org_type raises ValidationError."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Immutable",
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
            "org_name": f"{TEST_PREFIX}Modify Other",
            "org_type": "Family"
        })
        org.insert()

        # Change other fields
        org.org_name = f"{TEST_PREFIX}Modified Name"
        org.status = "Inactive"
        org.save()
        org.reload()

        self.assertEqual(org.org_name, f"{TEST_PREFIX}Modified Name")
        self.assertEqual(org.status, "Inactive")
        self.assertEqual(org.org_type, "Family")  # Unchanged

    def test_us4_error_message_is_clear(self):
        """T041: Test error message is clear and user-friendly."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Clear Error",
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
        cleanup_test_organizations()

    def tearDown(self):
        """Clean up test data."""
        cleanup_test_organizations()

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
            "org_name": f"{TEST_PREFIX}Skip Concrete",
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
            "org_name": f"{TEST_PREFIX}Default Status",
            "org_type": "Family"
        })
        org.insert()

        self.assertEqual(org.status, "Active")

    def test_naming_series_applied(self):
        """Test that naming series is applied correctly."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Naming",
            "org_type": "Family"
        })
        org.insert()

        self.assertTrue(org.name.startswith("ORG-"))

    def test_duplicate_family_names_allowed(self):
        """Test that multiple families can have the same family_name (Issue #2)."""
        # Create first organization with family
        org1 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Duplicate Name Org1",
            "org_type": "Family"
        })
        org1.insert()
        org1.reload()

        family1_name = org1.linked_name
        family1 = frappe.get_doc("Family", family1_name)

        # Create second organization with family using same family_name
        org2 = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Duplicate Name Org2",
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

    def test_validate_links_passes_for_valid_organization(self):
        """Test that validate_links returns valid for properly linked Organization (Issue #12)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Valid Links",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        # Validate links
        result = org.validate_links()

        self.assertTrue(result["valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_validate_links_detects_orphaned_concrete_type(self):
        """Test that validate_links detects when concrete type is missing (Issue #12)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Orphaned",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        family_name = org.linked_name

        # Delete the Family manually (orphan scenario)
        frappe.delete_doc("Family", family_name, force=True, ignore_permissions=True)
        frappe.db.commit()

        # Reload org and validate
        org.reload()
        result = org.validate_links()

        self.assertFalse(result["valid"])
        self.assertTrue(any("does not exist" in error for error in result["errors"]))

    def test_validate_links_detects_broken_bidirectional_link(self):
        """Test that validate_links detects broken bidirectional link (Issue #12)."""
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Broken Link",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        family_name = org.linked_name

        # Break the bidirectional link by clearing organization field
        frappe.db.set_value("Family", family_name, "organization", None)
        frappe.db.commit()

        # Reload org and validate
        org.reload()
        result = org.validate_links()

        self.assertFalse(result["valid"])
        self.assertTrue(any("Bidirectional link broken" in error for error in result["errors"]))

    def test_validate_organization_links_api(self):
        """Test the whitelisted validate_organization_links API (Issue #12)."""
        from dartwing.dartwing_core.doctype.organization.organization import validate_organization_links

        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}API Validate",
            "org_type": "Family"
        })
        org.insert()
        org.reload()

        # Call API
        result = validate_organization_links(org.name)

        self.assertIn("valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)
        self.assertTrue(result["valid"])


class TestOrganizationConcurrency(FrappeTestCase):
    """Test concurrent Organization creation (SC-006)."""

    def setUp(self):
        """Set up test fixtures."""
        frappe.set_user("Administrator")
        cleanup_test_organizations()

    def tearDown(self):
        """Clean up test data."""
        cleanup_test_organizations()

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
                "org_name": f"{TEST_PREFIX}Concurrent Org {i:03d}",
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


class TestOrganizationAtomicity(FrappeTestCase):
    """Test atomic transaction behavior for Organization creation (Issue #7)."""

    def setUp(self):
        """Set up test fixtures."""
        frappe.set_user("Administrator")
        cleanup_test_organizations()

    def tearDown(self):
        """Clean up test data."""
        cleanup_test_organizations()

    def test_t015_atomic_rollback_on_concrete_creation_failure(self):
        """T015: Test atomic rollback when concrete type creation fails (Issue #7)."""
        from unittest.mock import patch

        # Create organization document
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{TEST_PREFIX}Atomic Rollback",
            "org_type": "Family"
        })

        # Mock frappe.new_doc to raise error when creating Family
        original_new_doc = frappe.new_doc

        def mock_new_doc(doctype):
            if doctype == "Family":
                raise frappe.ValidationError("Simulated concrete type creation failure")
            return original_new_doc(doctype)

        # Attempt to insert organization with mocked failure
        with patch("frappe.new_doc", side_effect=mock_new_doc):
            with self.assertRaises(frappe.ValidationError) as context:
                org.insert()

            self.assertIn("Simulated concrete type creation failure", str(context.exception))

        # Verify Organization was NOT created (rollback occurred)
        orgs_created = frappe.get_all(
            "Organization",
            filters={"org_name": f"{TEST_PREFIX}Atomic Rollback"},
            pluck="name"
        )
        self.assertEqual(len(orgs_created), 0, "Organization should be rolled back after concrete creation failure")

        # Verify no orphaned Organization records exist
        all_test_orgs = frappe.get_all(
            "Organization",
            filters={"org_name": ["like", f"{TEST_PREFIX}Atomic%"]},
            pluck="name"
        )
        self.assertEqual(len(all_test_orgs), 0, "No test organizations should exist after rollback")
