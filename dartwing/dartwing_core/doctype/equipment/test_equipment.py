# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Test cases for Equipment DocType.

Run tests with:
    bench --site <site> run-tests --app dartwing --module dartwing.dartwing_core.doctype.equipment.test_equipment
"""

import frappe
from frappe.tests import IntegrationTestCase


class TestEquipment(IntegrationTestCase):
    """Test cases for Equipment DocType."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures that are shared across all tests."""
        super().setUpClass()

        # Create test organization
        cls.test_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Equipment Org",
            "org_type": "Company"
        })
        cls.test_org.insert()
        cls.test_org.reload()

        # Create test person
        cls.test_person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Test",
            "last_name": "EquipmentUser"
        })
        cls.test_person.insert()

        # Create org member to link person to org
        cls.test_member = frappe.get_doc({
            "doctype": "Org Member",
            "organization": cls.test_org.name,
            "person": cls.test_person.name,
            "status": "Active"
        })
        cls.test_member.insert()

        # Create user permission for Administrator
        frappe.get_doc({
            "doctype": "User Permission",
            "user": "Administrator",
            "allow": "Organization",
            "for_value": cls.test_org.name
        }).insert(ignore_if_duplicate=True)

    @classmethod
    def tearDownClass(cls):
        """Clean up test fixtures."""
        # Clean up equipment
        for eq in frappe.get_all(
            "Equipment",
            filters={"owner_organization": cls.test_org.name},
            pluck="name"
        ):
            frappe.delete_doc("Equipment", eq, force=True)

        # Clean up org member
        if frappe.db.exists("Org Member", cls.test_member.name):
            frappe.delete_doc("Org Member", cls.test_member.name, force=True)

        # Clean up person
        if frappe.db.exists("Person", cls.test_person.name):
            frappe.delete_doc("Person", cls.test_person.name, force=True)

        # Clean up organization (will cascade delete linked Company)
        if frappe.db.exists("Organization", cls.test_org.name):
            frappe.delete_doc("Organization", cls.test_org.name, force=True)

        # Clean up user permissions
        for up in frappe.get_all(
            "User Permission",
            filters={"for_value": cls.test_org.name},
            pluck="name"
        ):
            frappe.delete_doc("User Permission", up, force=True)

        super().tearDownClass()

    def tearDown(self):
        """Clean up equipment created during individual tests."""
        for eq in frappe.get_all(
            "Equipment",
            filters={"equipment_name": ["like", "Test Eq%"]},
            pluck="name"
        ):
            frappe.delete_doc("Equipment", eq, force=True)

    def test_equipment_creation(self):
        """Test basic equipment creation (FR-001)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": "Test Eq Basic",
            "owner_organization": self.test_org.name
        })
        equipment.insert()

        self.assertEqual(equipment.equipment_name, "Test Eq Basic")
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
            "equipment_name": "Test Eq Serial 1",
            "owner_organization": self.test_org.name,
            "serial_number": "SN-UNIQUE-TEST-001"
        })
        eq1.insert()

        # Try to create second with same serial - should fail
        eq2 = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": "Test Eq Serial 2",
            "owner_organization": self.test_org.name,
            "serial_number": "SN-UNIQUE-TEST-001"
        })

        with self.assertRaises(frappe.exceptions.ValidationError):
            eq2.insert()

    def test_assignment_requires_org_membership(self):
        """Test assigned person must be org member (FR-010)."""
        # Create a person NOT in the test org
        other_person = frappe.get_doc({
            "doctype": "Person",
            "first_name": "Other",
            "last_name": "Person"
        })
        other_person.insert()

        try:
            equipment = frappe.get_doc({
                "doctype": "Equipment",
                "equipment_name": "Test Eq Assignment",
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
            "equipment_name": "Test Eq Valid Assignment",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        equipment.insert()

        self.assertEqual(equipment.assigned_to, self.test_person.name)

    def test_organization_immutable(self):
        """Test owner_organization cannot change after creation (P2-05)."""
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": "Test Eq Immutable Org",
            "owner_organization": self.test_org.name
        })
        equipment.insert()

        # Create second org
        other_org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": "Test Equipment Other Org",
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
            "equipment_name": "Test Eq Block Delete",
            "owner_organization": self.test_org.name
        })
        equipment.insert()

        # Try to delete organization - should fail
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.delete_doc("Organization", self.test_org.name)

        # Clean up
        frappe.delete_doc("Equipment", equipment.name, force=True)

    def test_member_removal_blocked_with_equipment(self):
        """Test org member cannot be removed with assigned equipment (FR-013)."""
        # Create equipment assigned to the test person
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": "Test Eq Block Member Delete",
            "owner_organization": self.test_org.name,
            "assigned_to": self.test_person.name
        })
        equipment.insert()

        # Try to delete org member - should fail
        with self.assertRaises(frappe.exceptions.ValidationError):
            frappe.delete_doc("Org Member", self.test_member.name)

        # Clean up
        frappe.delete_doc("Equipment", equipment.name, force=True)

    def test_member_deactivation_blocked_with_equipment(self):
        """Test org member cannot be deactivated with assigned equipment (P1-03)."""
        # Create equipment assigned to the test person
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": "Test Eq Block Deactivation",
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

        # Clean up
        frappe.delete_doc("Equipment", equipment.name, force=True)

    def test_assignment_change_creates_comment(self):
        """Test assignment changes create audit comment (P2-06)."""
        # Create equipment with assignment
        equipment = frappe.get_doc({
            "doctype": "Equipment",
            "equipment_name": "Test Eq Audit Trail",
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
                "equipment_name": f"Test Eq Status {status}",
                "owner_organization": self.test_org.name,
                "status": status
            })
            equipment.insert()
            self.assertEqual(equipment.status, status)
            frappe.delete_doc("Equipment", equipment.name, force=True)
