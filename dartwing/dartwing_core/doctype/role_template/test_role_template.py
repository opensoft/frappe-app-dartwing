# Copyright (c) 2025, Dartwing and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase


class TestRoleTemplate(IntegrationTestCase):
    """Test cases for Role Template DocType."""

    # =========================================================================
    # User Story 1: System Administrator Seeds Role Data (T008-T012)
    # =========================================================================

    def test_fixture_loads_all_roles(self):
        """T008: Verify all 14 roles are loaded from fixtures."""
        roles = frappe.get_all("Role Template", fields=["role_name"])
        self.assertEqual(len(roles), 14, "Expected 14 predefined roles")

    def test_family_roles_exist(self):
        """T009: Verify 4 Family roles exist."""
        family_roles = frappe.get_all(
            "Role Template",
            filters={"applies_to_org_type": "Family"},
            fields=["role_name"],
        )
        expected_roles = {"Parent", "Child", "Guardian", "Extended Family"}
        actual_roles = {r.role_name for r in family_roles}
        self.assertEqual(actual_roles, expected_roles, "Family roles mismatch")
        self.assertEqual(len(family_roles), 4, "Expected 4 Family roles")

    def test_company_roles_exist(self):
        """T010: Verify 4 Company roles exist."""
        company_roles = frappe.get_all(
            "Role Template",
            filters={"applies_to_org_type": "Company"},
            fields=["role_name"],
        )
        expected_roles = {"Owner", "Manager", "Employee", "Contractor"}
        actual_roles = {r.role_name for r in company_roles}
        self.assertEqual(actual_roles, expected_roles, "Company roles mismatch")
        self.assertEqual(len(company_roles), 4, "Expected 4 Company roles")

    def test_nonprofit_roles_exist(self):
        """T011: Verify 3 Nonprofit roles exist."""
        nonprofit_roles = frappe.get_all(
            "Role Template",
            filters={"applies_to_org_type": "Nonprofit"},
            fields=["role_name"],
        )
        expected_roles = {"Board Member", "Volunteer", "Staff"}
        actual_roles = {r.role_name for r in nonprofit_roles}
        self.assertEqual(actual_roles, expected_roles, "Nonprofit roles mismatch")
        self.assertEqual(len(nonprofit_roles), 3, "Expected 3 Nonprofit roles")

    def test_association_roles_exist(self):
        """T012: Verify 3 Association roles exist."""
        association_roles = frappe.get_all(
            "Role Template",
            filters={"applies_to_org_type": "Association"},
            fields=["role_name"],
        )
        expected_roles = {"President", "Member", "Honorary"}
        actual_roles = {r.role_name for r in association_roles}
        self.assertEqual(actual_roles, expected_roles, "Association roles mismatch")
        self.assertEqual(len(association_roles), 3, "Expected 3 Association roles")

    # =========================================================================
    # User Story 2: Organization Admin Assigns Roles to Members (T020-T023)
    # =========================================================================

    def test_filter_by_family_type(self):
        """T020: Verify filtering returns only Family roles."""
        from dartwing.dartwing_core.doctype.role_template.role_template import (
            get_roles_for_org_type,
        )

        roles = get_roles_for_org_type("Family")
        self.assertEqual(len(roles), 4, "Expected 4 Family roles")
        for role in roles:
            self.assertEqual(
                role.applies_to_org_type,
                "Family",
                f"Role {role.role_name} should be Family type",
            )

    def test_filter_by_company_type(self):
        """T021: Verify filtering returns only Company roles."""
        from dartwing.dartwing_core.doctype.role_template.role_template import (
            get_roles_for_org_type,
        )

        roles = get_roles_for_org_type("Company")
        self.assertEqual(len(roles), 4, "Expected 4 Company roles")
        for role in roles:
            self.assertEqual(
                role.applies_to_org_type,
                "Company",
                f"Role {role.role_name} should be Company type",
            )

    def test_filter_by_nonprofit_type(self):
        """T022: Verify filtering returns only Nonprofit roles."""
        from dartwing.dartwing_core.doctype.role_template.role_template import (
            get_roles_for_org_type,
        )

        roles = get_roles_for_org_type("Nonprofit")
        self.assertEqual(len(roles), 3, "Expected 3 Nonprofit roles")
        for role in roles:
            self.assertEqual(
                role.applies_to_org_type,
                "Nonprofit",
                f"Role {role.role_name} should be Nonprofit type",
            )

    def test_filter_by_association_type(self):
        """T023: Verify filtering returns only Association roles."""
        from dartwing.dartwing_core.doctype.role_template.role_template import (
            get_roles_for_org_type,
        )

        roles = get_roles_for_org_type("Association")
        self.assertEqual(len(roles), 3, "Expected 3 Association roles")
        for role in roles:
            self.assertEqual(
                role.applies_to_org_type,
                "Association",
                f"Role {role.role_name} should be Association type",
            )

    # =========================================================================
    # User Story 3: System Enforces Supervisor Hierarchy (T028-T031)
    # =========================================================================

    def test_supervisor_flags_family(self):
        """T028: Verify Family role supervisor flags match expected values."""
        expected_flags = {
            "Parent": 1,
            "Child": 0,
            "Guardian": 1,
            "Extended Family": 0,
        }
        for role_name, expected_supervisor in expected_flags.items():
            role = frappe.get_doc("Role Template", role_name)
            self.assertEqual(
                role.is_supervisor,
                expected_supervisor,
                f"{role_name} supervisor flag should be {expected_supervisor}",
            )

    def test_supervisor_flags_company(self):
        """T029: Verify Company role supervisor flags match expected values."""
        expected_flags = {
            "Owner": 1,
            "Manager": 1,
            "Employee": 0,
            "Contractor": 0,
        }
        for role_name, expected_supervisor in expected_flags.items():
            role = frappe.get_doc("Role Template", role_name)
            self.assertEqual(
                role.is_supervisor,
                expected_supervisor,
                f"{role_name} supervisor flag should be {expected_supervisor}",
            )

    def test_supervisor_flags_nonprofit(self):
        """T030: Verify Nonprofit role supervisor flags match expected values."""
        expected_flags = {
            "Board Member": 1,
            "Volunteer": 0,
            "Staff": 0,
        }
        for role_name, expected_supervisor in expected_flags.items():
            role = frappe.get_doc("Role Template", role_name)
            self.assertEqual(
                role.is_supervisor,
                expected_supervisor,
                f"{role_name} supervisor flag should be {expected_supervisor}",
            )

    def test_supervisor_flags_association(self):
        """T031: Verify Association role supervisor flags match expected values."""
        expected_flags = {
            "President": 1,
            "Member": 0,
            "Honorary": 0,
        }
        for role_name, expected_supervisor in expected_flags.items():
            role = frappe.get_doc("Role Template", role_name)
            self.assertEqual(
                role.is_supervisor,
                expected_supervisor,
                f"{role_name} supervisor flag should be {expected_supervisor}",
            )

    # =========================================================================
    # User Story 4: Paid Roles Include Hourly Rate (T036-T037)
    # Hourly rate visible for Company, Nonprofit, Association; hidden for Family
    # =========================================================================

    def test_hourly_rate_visible_for_paid_org_types(self):
        """T036: Verify hourly rate field is accessible on paid org types (Company, Nonprofit, Association)."""
        # Test Company roles
        company_roles = frappe.get_all(
            "Role Template",
            filters={"applies_to_org_type": "Company"},
            fields=["role_name", "default_hourly_rate"],
        )
        self.assertEqual(len(company_roles), 4, "Expected 4 Company roles")
        for role in company_roles:
            self.assertIsNotNone(
                role.default_hourly_rate,
                f"default_hourly_rate should be accessible for Company role {role.role_name}",
            )

        # Test Nonprofit roles (Staff can be paid)
        nonprofit_roles = frappe.get_all(
            "Role Template",
            filters={"applies_to_org_type": "Nonprofit"},
            fields=["role_name", "default_hourly_rate"],
        )
        self.assertEqual(len(nonprofit_roles), 3, "Expected 3 Nonprofit roles")
        for role in nonprofit_roles:
            self.assertIsNotNone(
                role.default_hourly_rate,
                f"default_hourly_rate should be accessible for Nonprofit role {role.role_name}",
            )

        # Test Association roles (may have paid staff)
        association_roles = frappe.get_all(
            "Role Template",
            filters={"applies_to_org_type": "Association"},
            fields=["role_name", "default_hourly_rate"],
        )
        self.assertEqual(len(association_roles), 3, "Expected 3 Association roles")
        for role in association_roles:
            self.assertIsNotNone(
                role.default_hourly_rate,
                f"default_hourly_rate should be accessible for Association role {role.role_name}",
            )

    def test_hourly_rate_conditional_visibility(self):
        """T036a: Verify hourly rate field is hidden for Family roles only."""
        meta = frappe.get_meta("Role Template")
        field = meta.get_field("default_hourly_rate")

        self.assertIsNotNone(field, "default_hourly_rate field should exist")
        self.assertIsNotNone(field.depends_on, "Field should have depends_on attribute")
        self.assertIn(
            "applies_to_org_type!='Family'",
            field.depends_on,
            "Field should be hidden for Family org type (depends_on should be \"eval:applies_to_org_type!='Family'\")",
        )

    def test_hourly_rate_cleared_for_family(self):
        """T037: Verify hourly rate is cleared for Family roles (non-employment)."""
        test_role = None
        try:
            # Create a test role with hourly rate, then change to Family
            test_role = frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Test Hourly Rate Role",
                    "applies_to_org_type": "Company",
                    "default_hourly_rate": 50.00,
                }
            )
            test_role.insert()

            # Change to Family type and save - should clear hourly rate
            test_role.applies_to_org_type = "Family"
            test_role.save()

            # Reload and verify hourly rate was cleared
            test_role.reload()
            self.assertEqual(
                test_role.default_hourly_rate,
                0,
                "Hourly rate should be cleared for Family roles",
            )
        finally:
            if test_role and frappe.db.exists("Role Template", test_role.name):
                test_role.delete()

    def test_hourly_rate_preserved_for_nonprofit(self):
        """T037a: Verify hourly rate is preserved when changing to Nonprofit (paid staff)."""
        test_role = None
        try:
            # Create a Company role with hourly rate
            test_role = frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Test Nonprofit Rate Role",
                    "applies_to_org_type": "Company",
                    "default_hourly_rate": 35.00,
                }
            )
            test_role.insert()

            # Change to Nonprofit type - should preserve hourly rate
            test_role.applies_to_org_type = "Nonprofit"
            test_role.save()

            # Reload and verify hourly rate was NOT cleared
            test_role.reload()
            self.assertEqual(
                test_role.default_hourly_rate,
                35.00,
                "Hourly rate should be preserved for Nonprofit roles (paid staff)",
            )
        finally:
            if test_role and frappe.db.exists("Role Template", test_role.name):
                test_role.delete()

    def test_negative_hourly_rate_rejected(self):
        """T037b: Verify negative hourly rates are rejected with proper error message."""
        with self.assertRaises(frappe.ValidationError) as context:
            frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Test Negative Rate Role",
                    "applies_to_org_type": "Company",
                    "default_hourly_rate": -25.00,
                }
            ).insert()
        self.assertIn(
            "negative",
            str(context.exception).lower(),
            "Error message should mention negative rate",
        )

    def test_zero_hourly_rate_allowed(self):
        """T037c: Verify zero hourly rate is allowed (valid default)."""
        test_role = None
        try:
            test_role = frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Test Zero Rate Role",
                    "applies_to_org_type": "Company",
                    "default_hourly_rate": 0.00,
                }
            )
            test_role.insert()  # Should not raise
            self.assertEqual(
                test_role.default_hourly_rate,
                0,
                "Zero hourly rate should be saved",
            )
        finally:
            if test_role and frappe.db.exists("Role Template", test_role.name):
                test_role.delete()

    def test_none_hourly_rate_allowed(self):
        """T037d: Verify None hourly rate is allowed (optional field)."""
        test_role = None
        try:
            test_role = frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Test None Rate Role",
                    "applies_to_org_type": "Company",
                    # default_hourly_rate not set (None)
                }
            )
            test_role.insert()  # Should not raise
            # Field defaults to 0 when not set
            self.assertIn(
                test_role.default_hourly_rate,
                [None, 0],
                "None or zero hourly rate should be accepted",
            )
        finally:
            if test_role and frappe.db.exists("Role Template", test_role.name):
                test_role.delete()

    # =========================================================================
    # Phase 7: Edge Cases & Deletion Prevention (T042-T044c)
    # =========================================================================

    def test_duplicate_role_name_rejected(self):
        """T042: Verify duplicate role names are rejected."""
        with self.assertRaises(frappe.DuplicateEntryError):
            frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Parent",  # Already exists in fixtures
                    "applies_to_org_type": "Family",
                }
            ).insert()

    def test_missing_org_type_rejected(self):
        """T043: Verify role creation fails without org_type."""
        with self.assertRaises(frappe.exceptions.MandatoryError):
            frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Test Missing Org Type",
                    # Missing applies_to_org_type
                }
            ).insert()

    def test_deletion_prevented_when_linked(self):
        """T044: Placeholder test for deletion prevention.

        This test will fully work when Org Member DocType (Feature 3) exists.
        For now, it verifies the on_trash hook exists and runs without error
        when no Org Member DocType exists.
        """
        test_role = None
        try:
            # Create a test role
            test_role = frappe.get_doc(
                {
                    "doctype": "Role Template",
                    "role_name": "Test Deletion Role",
                    "applies_to_org_type": "Family",
                }
            )
            test_role.insert()

            # Should be able to delete when no Org Members reference it
            # (and when Org Member DocType doesn't exist yet)
            test_role.delete()

            # Verify it was deleted
            self.assertFalse(
                frappe.db.exists("Role Template", "Test Deletion Role"),
                "Test role should be deleted",
            )
        finally:
            # Cleanup if test failed before delete or delete failed
            if test_role and frappe.db.exists("Role Template", "Test Deletion Role"):
                frappe.delete_doc("Role Template", "Test Deletion Role", force=True)

    def test_read_access_for_dartwing_user(self):
        """T044a: Verify Dartwing User role has read access to Role Templates."""
        # Check that the permission exists in DocType definition
        role_template_meta = frappe.get_meta("Role Template")
        dartwing_user_perms = [
            p for p in role_template_meta.permissions if p.role == "Dartwing User"
        ]
        self.assertEqual(
            len(dartwing_user_perms), 1, "Dartwing User should have permissions"
        )
        self.assertEqual(
            dartwing_user_perms[0].read, 1, "Dartwing User should have read access"
        )

    def test_create_restricted_to_system_manager(self):
        """T044b: Verify only System Manager can create Role Templates."""
        role_template_meta = frappe.get_meta("Role Template")

        # Check System Manager has create permission
        sys_manager_perms = [
            p for p in role_template_meta.permissions if p.role == "System Manager"
        ]
        self.assertEqual(
            len(sys_manager_perms), 1, "System Manager should have permissions"
        )
        self.assertEqual(
            sys_manager_perms[0].create, 1, "System Manager should have create access"
        )

        # Check Dartwing User does NOT have create permission
        dartwing_user_perms = [
            p for p in role_template_meta.permissions if p.role == "Dartwing User"
        ]
        self.assertEqual(
            dartwing_user_perms[0].get("create", 0),
            0,
            "Dartwing User should not have create access",
        )

    def test_invalid_org_type_rejected(self):
        """T044c: Verify invalid org_type raises ValidationError."""
        from dartwing.dartwing_core.doctype.role_template.role_template import (
            get_roles_for_org_type,
        )

        with self.assertRaises(frappe.ValidationError) as context:
            get_roles_for_org_type("InvalidType")

        self.assertIn(
            "Invalid organization type",
            str(context.exception),
            "Error should mention invalid org type",
        )
