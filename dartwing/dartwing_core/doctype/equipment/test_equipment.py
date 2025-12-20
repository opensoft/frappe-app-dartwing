# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for Equipment DocType.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.equipment.test_equipment
"""

import frappe
from frappe.tests.utils import FrappeTestCase


class TestEquipment(FrappeTestCase):
    """Test cases for Equipment DocType."""

    # Use unique prefix to avoid conflicts with other test data
    TEST_PREFIX = "__TestEquipment_"

    def setUp(self):
        """Set up test fixtures for each test."""
        self._cleanup_test_data()

        # Create test organization
        self.test_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}Org",
            "org_type": "Company"
        })
        self.test_org.insert()
        self.test_org.reload()

        # Create test role template (required for Org Member)
        self.test_role = frappe.get_doc({
            "doctype": "Role Template",
            "role_name": f"{self.TEST_PREFIX}Role_{frappe.generate_hash(length=6)}",
            "applies_to_org_type": "Company"
        })
        self.test_role.insert()

        # Create test person (P1-NEW-02: Add mandatory fields)
        self.test_person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Test",
            "last_name": "EquipmentUser",
            "primary_email": f"{self.TEST_PREFIX}{frappe.generate_hash(length=6)}@example.com",
            "source": "import"
        })
        self.test_person.insert()

        # Create org member to link person to org (P1-NEW-02: Add role)
        self.test_member = frappe.get_doc({
            "doctype": "Org Member",
            "organization": self.test_org.name,
            "person": self.test_person.name,
            "role": self.test_role.name,
            "status": "Active"
        })
        self.test_member.insert()

        # Create user permission for Administrator
        if not frappe.db.exists("User Permission", {
            "user": "Administrator",
            "allow": "Organization",
            "for_value": self.test_org.name
        }):
            frappe.get_doc({
                "doctype": "User Permission",
                "user": "Administrator",
                "allow": "Organization",
                "for_value": self.test_org.name
            }).insert(ignore_if_duplicate=True)

    def tearDown(self):
        """Clean up test fixtures after each test."""
        self._cleanup_test_data()

    def _cleanup_test_data(self):
        """Remove all test data with the test prefix."""
        # Clean up equipment
        for eq in frappe.get_all(
            "Equipment",
            filters={"equipment_name": ["like", f"{self.TEST_PREFIX}%"]},
            pluck="name"
        ):
            frappe.delete_doc("Equipment", eq, force=True)

        # Clean up equipment by org
        for org in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", f"{self.TEST_PREFIX}%"]},
            pluck="name"
        ):
            for eq in frappe.get_all("Equipment", filters={"owner_organization": org}, pluck="name"):
                frappe.delete_doc("Equipment", eq, force=True)

        # Clean up org members
        for om in frappe.get_all(
            "Org Member",
            filters={"organization": ["like", "ORG-%"]},
            pluck="name"
        ):
            try:
                org_member = frappe.get_doc("Org Member", om)
                if org_member.organization and frappe.db.exists("Organization", org_member.organization):
                    org = frappe.get_doc("Organization", org_member.organization)
                    if org.org_name and org.org_name.startswith(self.TEST_PREFIX):
                        frappe.delete_doc("Org Member", om, force=True)
            except Exception as e:
                # Ignore errors during cleanup (e.g., missing Org Member), as this is test teardown.
                frappe.log_error(f"Error deleting Org Member {om} during test cleanup: {e}")

        # Clean up persons
        for person in frappe.get_all(
            "Person",
            filters={"primary_email": ["like", f"{self.TEST_PREFIX}%"]},
            pluck="name"
        ):
            frappe.delete_doc("Person", person, force=True)

        # Clean up role templates
        for role in frappe.get_all(
            "Role Template",
            filters={"role_name": ["like", f"{self.TEST_PREFIX}%"]},
            pluck="name"
        ):
            frappe.delete_doc("Role Template", role, force=True)

        # Clean up organizations
        for org in frappe.get_all(
            "Organization",
            filters={"org_name": ["like", f"{self.TEST_PREFIX}%"]},
            pluck="name"
        ):
            frappe.delete_doc("Organization", org, force=True)

        # Clean up user permissions for test orgs
        for up in frappe.get_all(
            "User Permission",
            filters={"allow": "Organization"},
            pluck="name"
        ):
            try:
                perm = frappe.get_doc("User Permission", up)
                if perm.for_value and frappe.db.exists("Organization", perm.for_value):
                    org = frappe.get_doc("Organization", perm.for_value)
                    if org.org_name and org.org_name.startswith(self.TEST_PREFIX):
                        frappe.delete_doc("User Permission", up, force=True)
            except Exception:
                pass

    def test_equipment_creation(self):
        """Test basic equipment creation (FR-001)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}Basic",
            "owner_organization": self.test_org.name
        })
        equipment.insert()

        self.assertEqual(equipment.equipment_name, f"{self.TEST_PREFIX}Basic")
        self.assertEqual(equipment.owner_organization, self.test_org.name)
        self.assertEqual(equipment.status, "Active")
        self.assertTrue(equipment.name.startswith("EQ-"))

    def test_equipment_name_required(self):
        """Test that equipment_name is required (FR-001)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "owner_organization": self.test_org.name
        })

        with self.assertRaises(frappe.exceptions.MandatoryError):
            equipment.insert()

    def test_serial_number_unique(self):
        """Test serial number uniqueness (FR-002)."""
        # Create first equipment with serial
        eq1 = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}Serial1",
            "owner_organization": self.test_org.name,
            "serial_number": f"{self.TEST_PREFIX}SN001"
        })
        eq1.insert()

        # Try to create second with same serial - should fail
        eq2 = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}Serial2",
            "owner_organization": self.test_org.name,
            "serial_number": f"{self.TEST_PREFIX}SN001"
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            eq2.insert()

    def test_assignment_requires_org_membership(self):
        """Test assigned person must be org member (FR-010)."""
        # Create a person NOT in the test org (P1-NEW-02: Add mandatory fields)
        other_person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Other",
            "last_name": "Person",
            "primary_email": f"{self.TEST_PREFIX}other_{frappe.generate_hash(length=6)}@example.com",
            "source": "import"
        })
        other_person.insert()

        try:
            equipment = frappe.get_doc({
                "doctype": "Equipment",
                "equipment_name": f"{self.TEST_PREFIX}Assignment",
                "owner_organization": self.test_org.name,
                "assigned_to": other_person.name
            })

            with self.assertRaises(frappe.exceptions.ValidationError):
                equipment.insert()
        finally:
            frappe.delete_doc("Person", other_person.name, force=True)

    def test_valid_assignment(self):
        """Test equipment can be assigned to valid org member (FR-010)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}ValidAssign",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        equipment.insert()

        self.assertEqual(equipment.assigned_to, self.test_person.name)

    def test_organization_immutable(self):
        """Test owner_organization cannot change after creation (P2-05)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}ImmutableOrg",
            "owner_organization": self.test_org.name
        })
        equipment.insert()

        # Create second org
        other_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}OtherOrg",
            "org_type": "Company"
        })
        other_org.insert()

        try:
            # Try to change organization - should fail
            equipment.owner_organization = other_org.name
            with self.assertRaises(frappe.exceptions.ValidationError):
                equipment.save()
        finally:
            frappe.delete_doc("Organization", other_org.name, force=True)

    def test_org_deletion_blocked_with_equipment(self):
        """Test organization cannot be deleted with equipment (FR-012)."""
        # Create equipment for the test org
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}BlockDelete",
            "owner_organization": self.test_org.name
        })
        equipment.insert()

        # Try to delete organization - should fail
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.delete_doc("Organization", self.test_org.name)

    def test_member_removal_blocked_with_equipment(self):
        """Test org member cannot be removed with assigned equipment (FR-013)."""
        # Create equipment assigned to the test person
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}BlockMemberDelete",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        equipment.insert()

        # Try to delete org member - should fail
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.delete_doc("Org Member", self.test_member.name)

    def test_member_deactivation_blocked_with_equipment(self):
        """Test org member cannot be deactivated with assigned equipment (P1-03)."""
        # Create equipment assigned to the test person
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}BlockDeactivation",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        equipment.insert()

        # Try to deactivate org member - should fail
        self.test_member.reload()
        self.test_member.status = "Inactive"

        with self.assertRaises(frappe.exceptions.ValidationError):
            self.test_member.save()

        # Restore member status
        self.test_member.reload()

    def test_assignment_change_creates_comment(self):
        """Test assignment changes create audit comment (P2-06)."""
        # Create equipment with assignment
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}AuditTrail",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        equipment.insert()

        # Clear assignment
        equipment.assigned_to = None
        equipment.save()

        # Check for comment
        comments = frappe.get_all(
            "Comment",
            filters={
                "reference_doctype": "Equipment",
                "reference_name": equipment.name,
                "comment_type": "Info"
            },
            pluck="content"
        )

        self.assertTrue(any("assignment changed" in c.lower() for c in comments))

    def test_status_options(self):
        """Test all status options are valid (P2-09)."""
        valid_statuses = ["Active", "In Repair", "Retired", "Lost", "Stolen"]

        for status in valid_statuses:
            equipment = frappe.get_doc({
                "doctype": "Equipment",
                "equipment_name": f"{self.TEST_PREFIX}Status_{status}",
                "owner_organization": self.test_org.name,
                "status": status
            })
            equipment.insert()
            self.assertEqual(equipment.status, status)

    def test_assignment_blocked_for_lost_status(self):
        """Test equipment with Lost status cannot be assigned (P1-NEW-04)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}LostAssign",
            "owner_organization": self.test_org.name,
            "status": "Lost",
            "assigned_to": self.test_person.name
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            equipment.insert()

    def test_assignment_blocked_for_stolen_status(self):
        """Test equipment with Stolen status cannot be assigned (P1-NEW-04)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}StolenAssign",
            "owner_organization": self.test_org.name,
            "status": "Stolen",
            "assigned_to": self.test_person.name
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            equipment.insert()

    def test_assignment_blocked_for_retired_status(self):
        """Test equipment with Retired status cannot be assigned (P1-NEW-04)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}RetiredAssign",
            "owner_organization": self.test_org.name,
            "status": "Retired",
            "assigned_to": self.test_person.name
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            equipment.insert()

    def test_initial_assignment_creates_comment(self):
        """Test initial assignment creates audit comment (P1-NEW-03)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}InitialAssign",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        equipment.insert()

        # Check for initial assignment comment
        comments = frappe.get_all(
            "Comment",
            filters={
                "reference_doctype": "Equipment",
                "reference_name": equipment.name,
                "comment_type": "Info"
            },
            pluck="content"
        )

        self.assertTrue(any("initially assigned" in c.lower() for c in comments))

    def test_get_equipment_by_organization_permission_check(self):
        """Test get_equipment_by_organization enforces organization permissions (P3-01)."""
        from dartwing.dartwing_core.doctype.equipment.equipment import get_equipment_by_organization

        # Create a second org that user won't have permission for
        other_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}OtherOrg",
            "org_type": "Company"
        })
        other_org.insert()

        # Create equipment in both orgs
        eq1 = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}Eq1",
            "owner_organization": self.test_org.name
        })
        eq1.insert()

        eq2 = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}Eq2",
            "owner_organization": other_org.name
        })
        eq2.insert()

        # Create a non-admin test user with Dartwing User role
        test_user_email = f"{self.TEST_PREFIX}user@example.com"
        if not frappe.db.exists("User", test_user_email):
            test_user = frappe.get_doc({
                "doctype": "User",
                "email": test_user_email,
                "first_name": "Test",
                "last_name": "EquipmentUser",
                "enabled": 1,
                "user_type": "System User",
                "roles": [{"role": "Dartwing User"}]
            })
            test_user.insert()

        # Give user permission only for test_org
        frappe.get_doc({
            "doctype": "User Permission",
            "user": test_user_email,
            "allow": "Organization",
            "for_value": self.test_org.name
        }).insert(ignore_if_duplicate=True)

        try:
            # Test as the restricted user
            frappe.set_user(test_user_email)

            # Should succeed for org user has permission for
            result = get_equipment_by_organization(self.test_org.name)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], eq1.name)

            # Should raise permission error for org user doesn't have access to
            with self.assertRaises(frappe.PermissionError):
                get_equipment_by_organization(other_org.name)

        finally:
            # Restore admin user
            frappe.set_user("Administrator")
            # Cleanup
            frappe.delete_doc("Equipment", eq2.name, force=True)
            frappe.delete_doc("Organization", other_org.name, force=True)
            frappe.db.delete("User Permission", {"user": test_user_email})
            frappe.delete_doc("User", test_user_email, force=True)

    def test_get_equipment_by_person_filters_by_org(self):
        """Test get_equipment_by_person filters by user's accessible orgs (P3-01)."""
        from dartwing.dartwing_core.doctype.equipment.equipment import get_equipment_by_person

        # Create second org
        other_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.TEST_PREFIX}OtherOrg2",
            "org_type": "Company"
        })
        other_org.insert()

        # Create another role template for the other org
        other_role = frappe.get_doc({
            "doctype": "Role Template",
            "role_name": f"{self.TEST_PREFIX}OtherRole_{frappe.generate_hash(length=6)}",
            "applies_to_org_type": "Company"
        })
        other_role.insert()

        # Add test person to other org as well
        other_member = frappe.get_doc({
            "doctype": "Org Member",
            "organization": other_org.name,
            "person": self.test_person.name,
            "role": other_role.name,
            "status": "Active"
        })
        other_member.insert()

        # Create equipment in both orgs assigned to same person
        eq1 = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}EqOrg1",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        eq1.insert()

        eq2 = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": f"{self.TEST_PREFIX}EqOrg2",
            "owner_organization": other_org.name,
            "assigned_to": self.test_person.name
        })
        eq2.insert()

        # Create restricted user with access only to test_org and Dartwing User role
        test_user_email = f"{self.TEST_PREFIX}user2@example.com"
        if not frappe.db.exists("User", test_user_email):
            frappe.get_doc({
                "doctype": "User",
                "email": test_user_email,
                "first_name": "Test",
                "last_name": "User2",
                "enabled": 1,
                "user_type": "System User",
                "roles": [{"role": "Dartwing User"}]
            }).insert()

        frappe.get_doc({
            "doctype": "User Permission",
            "user": test_user_email,
            "allow": "Organization",
            "for_value": self.test_org.name
        }).insert(ignore_if_duplicate=True)

        # Link user to Person for Person permission
        self.test_person.frappe_user = test_user_email
        self.test_person.save()

        try:
            frappe.set_user(test_user_email)

            # Should only return equipment from test_org, not other_org
            result = get_equipment_by_person(self.test_person.name)
            equipment_names = [r["name"] for r in result]

            self.assertIn(eq1.name, equipment_names)
            self.assertNotIn(eq2.name, equipment_names)

        finally:
            frappe.set_user("Administrator")
            # Cleanup
            self.test_person.frappe_user = None
            self.test_person.save()
            frappe.delete_doc("Equipment", eq1.name, force=True)
            frappe.delete_doc("Equipment", eq2.name, force=True)
            frappe.delete_doc("Org Member", other_member.name, force=True)
            frappe.delete_doc("Role Template", other_role.name, force=True)
            frappe.delete_doc("Organization", other_org.name, force=True)
            frappe.db.delete("User Permission", {"user": test_user_email})
            frappe.delete_doc("User", test_user_email, force=True)

    def test_get_org_members_permission_check(self):
        """Test get_org_members enforces organization permissions (P3-01)."""
        from dartwing.dartwing_core.doctype.equipment.equipment import get_org_members

        # Create restricted user without org permission
        test_user_email = f"{self.TEST_PREFIX}user3@example.com"
        if not frappe.db.exists("User", test_user_email):
            frappe.get_doc({
                "doctype": "User",
                "email": test_user_email,
                "first_name": "Test",
                "last_name": "User3",
                "enabled": 1,
                "user_type": "System User"
            }).insert()

        try:
            frappe.set_user(test_user_email)

            # Should raise permission error - user has no org permission
            with self.assertRaises(frappe.PermissionError):
                get_org_members(
                    doctype="Person",
                    txt="",
                    searchfield="name",
                    start=0,
                    page_len=20,
                    filters={"organization": self.test_org.name}
                )

        finally:
            frappe.set_user("Administrator")
            frappe.delete_doc("User", test_user_email, force=True)
