# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

import frappe
from frappe.tests import IntegrationTestCase
from frappe.utils import today


class TestOrgMember(IntegrationTestCase):
    """Test cases for Org Member DocType."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures: Organization and Person records."""
        super().setUpClass()

        # Create test Organization (Company type)
        if not frappe.db.exists("Organization", {"org_name": "Test Company Org"}):
            cls.test_org = frappe.get_doc(
                {
                    "doctype": "Organization",
                    "org_name": "Test Company Org",
                    "org_type": "Company",
                }
            )
            cls.test_org.insert()
        else:
            cls.test_org = frappe.get_doc(
                "Organization", {"org_name": "Test Company Org"}
            )

        # Create test Organization (Family type)
        if not frappe.db.exists("Organization", {"org_name": "Test Family Org"}):
            cls.test_family_org = frappe.get_doc(
                {
                    "doctype": "Organization",
                    "org_name": "Test Family Org",
                    "org_type": "Family",
                }
            )
            cls.test_family_org.insert()
        else:
            cls.test_family_org = frappe.get_doc(
                "Organization", {"org_name": "Test Family Org"}
            )

        # Create test Person
        if not frappe.db.exists("Person", {"primary_email": "testmember@example.com"}):
            cls.test_person = frappe.get_doc(
                {
                    "doctype": "Person",
                    "first_name": "Test",
                    "last_name": "Member",
                    "primary_email": "testmember@example.com",
                }
            )
            cls.test_person.insert()
        else:
            cls.test_person = frappe.get_doc(
                "Person", {"primary_email": "testmember@example.com"}
            )

        # Create second test Person
        if not frappe.db.exists("Person", {"primary_email": "testmember2@example.com"}):
            cls.test_person2 = frappe.get_doc(
                {
                    "doctype": "Person",
                    "first_name": "Test2",
                    "last_name": "Member2",
                    "primary_email": "testmember2@example.com",
                }
            )
            cls.test_person2.insert()
        else:
            cls.test_person2 = frappe.get_doc(
                "Person", {"primary_email": "testmember2@example.com"}
            )

    def tearDown(self):
        """Clean up Org Member records after each test."""
        # Delete any Org Member records created during tests
        for member in frappe.get_all("Org Member"):
            try:
                frappe.delete_doc("Org Member", member.name)
            except Exception as e:
                # Log the exception and attempt force delete as a last resort
                frappe.logger().warning(
                    "Could not delete Org Member during tearDown. Attempting force delete.",
                    exc_info=True
                )
                frappe.delete_doc("Org Member", member.name, force=True)
        frappe.db.commit()

    # =========================================================================
    # User Story 1: Add Member to Organization (T006-T010)
    # =========================================================================

    def test_create_basic_membership(self):
        """T006a: Verify basic Org Member creation works."""
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",  # Company role
            }
        )
        member.insert()

        self.assertIsNotNone(member.name, "Org Member should be created")
        self.assertEqual(member.person, self.test_person.name)
        self.assertEqual(member.organization, self.test_org.name)
        self.assertEqual(member.role, "Employee")

    def test_default_status_is_active(self):
        """T008a: Verify status defaults to Active (FR-005)."""
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                # status not specified
            }
        )
        member.insert()

        self.assertEqual(member.status, "Active", "Status should default to Active")

    def test_default_start_date_is_today(self):
        """T008b: Verify start_date defaults to today (FR-004)."""
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                # start_date not specified
            }
        )
        member.insert()

        self.assertEqual(
            str(member.start_date), today(), "Start date should default to today"
        )

    def test_unique_membership_constraint(self):
        """T006b: Verify duplicate (Person, Organization) is rejected (FR-002)."""
        # Create first membership
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
            }
        )
        member1.insert()

        # Try to create duplicate membership
        with self.assertRaises(frappe.ValidationError) as context:
            member2 = frappe.get_doc(
                {
                    "doctype": "Org Member",
                    "person": self.test_person.name,
                    "organization": self.test_org.name,
                    "role": "Manager",  # Different role, same person+org
                }
            )
            member2.insert()

        self.assertIn(
            "already a member",
            str(context.exception).lower(),
            "Error should mention duplicate membership",
        )

    def test_role_validation_for_org_type(self):
        """T007a: Verify role must match organization type (FR-003)."""
        # Try to assign Company role to Family organization
        with self.assertRaises(frappe.ValidationError) as context:
            member = frappe.get_doc(
                {
                    "doctype": "Org Member",
                    "person": self.test_person.name,
                    "organization": self.test_family_org.name,  # Family org
                    "role": "Employee",  # Company role
                }
            )
            member.insert()

        self.assertIn(
            "not valid for",
            str(context.exception).lower(),
            "Error should mention invalid role for org type",
        )

    def test_role_validation_accepts_matching_type(self):
        """T007b: Verify valid role for org type is accepted."""
        # Assign Family role to Family organization
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_family_org.name,  # Family org
                "role": "Parent",  # Family role
            }
        )
        member.insert()

        self.assertEqual(member.role, "Parent", "Family role should be accepted")

    def test_add_member_api_creates_new(self):
        """T009a: Verify add_member_to_organization creates new membership."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            add_member_to_organization,
        )

        result = add_member_to_organization(
            person=self.test_person.name,
            organization=self.test_org.name,
            role="Employee",
        )

        self.assertEqual(result["action"], "created")
        self.assertEqual(result["person"], self.test_person.name)
        self.assertEqual(result["organization"], self.test_org.name)
        self.assertEqual(result["role"], "Employee")
        self.assertEqual(result["status"], "Active")

    def test_add_member_api_reactivates_inactive(self):
        """T009b: Verify add_member_to_organization reactivates inactive membership."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            add_member_to_organization,
        )

        # Create initial membership
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Inactive",
                "end_date": "2025-01-01",
            }
        )
        member.insert()

        # Reactivate via API
        result = add_member_to_organization(
            person=self.test_person.name,
            organization=self.test_org.name,
            role="Manager",  # Can change role on reactivation
        )

        self.assertEqual(result["action"], "reactivated")
        self.assertEqual(result["previous_status"], "Inactive")
        self.assertEqual(result["status"], "Active")
        self.assertEqual(result["role"], "Manager")

        # Verify end_date was cleared
        member.reload()
        self.assertIsNone(member.end_date, "End date should be cleared on reactivation")

    def test_add_member_api_rejects_active_duplicate(self):
        """T009c: Verify add_member_to_organization rejects active duplicate."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            add_member_to_organization,
        )

        # Create active membership
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Try to add again
        with self.assertRaises(frappe.ValidationError) as context:
            add_member_to_organization(
                person=self.test_person.name,
                organization=self.test_org.name,
                role="Manager",
            )

        self.assertIn(
            "already an active member",
            str(context.exception).lower(),
            "Error should mention already active member",
        )

    def test_fetched_fields_populated(self):
        """T003a: Verify fetched fields are populated correctly."""
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
            }
        )
        member.insert()

        # Reload to get fetched values
        member.reload()

        self.assertIsNotNone(member.member_name, "member_name should be populated")
        self.assertIsNotNone(
            member.organization_name, "organization_name should be populated"
        )
        self.assertEqual(
            member.organization_type, "Company", "organization_type should be Company"
        )

    # =========================================================================
    # User Story 2: View Organization Members (T011-T013)
    # =========================================================================

    def test_get_members_for_organization(self):
        """T011a: Verify get_members_for_organization returns all members."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            get_members_for_organization,
        )

        # Create multiple members
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        member1.insert()

        member2 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person2.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member2.insert()

        # Get members
        members = get_members_for_organization(self.test_org.name)

        self.assertEqual(len(members), 2, "Should return 2 members")
        member_names = {m["person"] for m in members}
        self.assertIn(self.test_person.name, member_names)
        self.assertIn(self.test_person2.name, member_names)

    def test_get_members_includes_supervisor_flag(self):
        """T011b: Verify is_supervisor flag is included in response."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            get_members_for_organization,
        )

        # Create member with supervisor role (Manager is_supervisor=1)
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        member.insert()

        members = get_members_for_organization(self.test_org.name)

        self.assertEqual(len(members), 1)
        self.assertEqual(members[0]["is_supervisor"], 1, "Manager should be supervisor")

    def test_get_members_filters_by_status(self):
        """T011c: Verify status filter works correctly."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            get_members_for_organization,
        )

        # Create active member
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        member1.insert()

        # Create inactive member
        member2 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person2.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Inactive",
            }
        )
        member2.insert()

        # Get only active members (default excludes inactive)
        active_members = get_members_for_organization(self.test_org.name)
        self.assertEqual(len(active_members), 1, "Should return only active member")

        # Get all members including inactive
        all_members = get_members_for_organization(
            self.test_org.name, include_inactive=True
        )
        self.assertEqual(len(all_members), 2, "Should return all members")

        # Get only inactive members
        inactive_members = get_members_for_organization(
            self.test_org.name, status="Inactive"
        )
        self.assertEqual(len(inactive_members), 1, "Should return only inactive member")

    def test_get_organizations_for_person(self):
        """T012a: Verify get_organizations_for_person returns all memberships."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            get_organizations_for_person,
        )

        # Create membership in Company org
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member1.insert()

        # Create membership in Family org
        member2 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_family_org.name,
                "role": "Parent",
                "status": "Active",
            }
        )
        member2.insert()

        # Get organizations
        orgs = get_organizations_for_person(self.test_person.name)

        self.assertEqual(len(orgs), 2, "Should return 2 organizations")
        org_names = {o["organization"] for o in orgs}
        self.assertIn(self.test_org.name, org_names)
        self.assertIn(self.test_family_org.name, org_names)

    def test_get_organizations_includes_supervisor_flag(self):
        """T012b: Verify is_supervisor flag is included in response."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            get_organizations_for_person,
        )

        # Create membership with supervisor role
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_family_org.name,
                "role": "Parent",  # Parent is_supervisor=1
                "status": "Active",
            }
        )
        member.insert()

        orgs = get_organizations_for_person(self.test_person.name)

        self.assertEqual(len(orgs), 1)
        self.assertEqual(orgs[0]["is_supervisor"], 1, "Parent should be supervisor")

    def test_get_organizations_filters_by_status(self):
        """T012c: Verify status filter works correctly."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            get_organizations_for_person,
        )

        # Create active membership
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member1.insert()

        # Create inactive membership
        member2 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_family_org.name,
                "role": "Parent",
                "status": "Inactive",
            }
        )
        member2.insert()

        # Get only active (default)
        active_orgs = get_organizations_for_person(self.test_person.name)
        self.assertEqual(len(active_orgs), 1, "Should return only active membership")

        # Get inactive
        inactive_orgs = get_organizations_for_person(
            self.test_person.name, status="Inactive"
        )
        self.assertEqual(
            len(inactive_orgs), 1, "Should return only inactive membership"
        )

    # =========================================================================
    # User Story 3: Manage Member Status (T014-T016)
    # =========================================================================

    def test_end_date_validation(self):
        """T014a: Verify end_date must be >= start_date (V-005)."""
        # Try to set end_date before start_date
        with self.assertRaises(frappe.ValidationError) as context:
            member = frappe.get_doc(
                {
                    "doctype": "Org Member",
                    "person": self.test_person.name,
                    "organization": self.test_org.name,
                    "role": "Employee",
                    "start_date": "2025-06-01",
                    "end_date": "2025-01-01",  # Before start_date
                }
            )
            member.insert()

        self.assertIn(
            "end date",
            str(context.exception).lower(),
            "Error should mention end date",
        )

    def test_end_date_same_as_start_allowed(self):
        """T014b: Verify end_date same as start_date is allowed."""
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "start_date": "2025-06-01",
                "end_date": "2025-06-01",  # Same as start_date
            }
        )
        member.insert()

        self.assertEqual(str(member.end_date), "2025-06-01")

    def test_deactivate_member_api(self):
        """T015a: Verify deactivate_member sets status to Inactive."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            deactivate_member,
        )

        # Create active member
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Deactivate
        result = deactivate_member(member.name)

        self.assertEqual(result["status"], "Inactive")
        self.assertIsNotNone(result["end_date"])

        # Verify in database
        member.reload()
        self.assertEqual(member.status, "Inactive")

    def test_deactivate_member_with_custom_end_date(self):
        """T015b: Verify deactivate_member accepts custom end_date."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            deactivate_member,
        )

        # Create active member
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Deactivate with custom end date
        result = deactivate_member(member.name, end_date="2025-12-31")

        self.assertEqual(result["end_date"], "2025-12-31")

    def test_deactivate_already_inactive_rejected(self):
        """T015c: Verify deactivating already inactive member is rejected."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            deactivate_member,
        )

        # Create inactive member
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Inactive",
            }
        )
        member.insert()

        # Try to deactivate again
        with self.assertRaises(frappe.ValidationError) as context:
            deactivate_member(member.name)

        self.assertIn(
            "already inactive",
            str(context.exception).lower(),
            "Error should mention already inactive",
        )

    def test_status_change_direct_save(self):
        """T016a: Verify status can be changed via direct save."""
        # Create active member
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Change to Pending via direct save
        member.status = "Pending"
        member.save()

        member.reload()
        self.assertEqual(member.status, "Pending")

        # Change back to Active
        member.status = "Active"
        member.save()

        member.reload()
        self.assertEqual(member.status, "Active")

    # =========================================================================
    # User Story 4: Change Member Role (T017-T018)
    # =========================================================================

    def test_change_member_role_api(self):
        """T017a: Verify change_member_role changes the role."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            change_member_role,
        )

        # Create member with Employee role
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Change to Manager
        result = change_member_role(member.name, "Manager")

        self.assertEqual(result["previous_role"], "Employee")
        self.assertEqual(result["role"], "Manager")

        # Verify in database
        member.reload()
        self.assertEqual(member.role, "Manager")

    def test_change_role_validates_org_type(self):
        """T017b: Verify role change validates against org type."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            change_member_role,
        )

        # Create member in Company org
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Try to change to Family role
        with self.assertRaises(frappe.ValidationError) as context:
            change_member_role(member.name, "Parent")  # Family role

        self.assertIn(
            "not valid for",
            str(context.exception).lower(),
            "Error should mention invalid role",
        )

    def test_change_to_same_role_rejected(self):
        """T017c: Verify changing to same role is rejected."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            change_member_role,
        )

        # Create member
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Try to change to same role
        with self.assertRaises(frappe.ValidationError) as context:
            change_member_role(member.name, "Employee")

        self.assertIn(
            "already has this role",
            str(context.exception).lower(),
            "Error should mention same role",
        )

    def test_change_role_direct_save(self):
        """T018a: Verify role can be changed via direct save."""
        # Create member
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Change role via direct save
        member.role = "Manager"
        member.save()

        member.reload()
        self.assertEqual(member.role, "Manager")

    # =========================================================================
    # User Story 5: Remove Member with Supervisor Protection (T019-T022)
    # =========================================================================

    def test_last_supervisor_cannot_be_deactivated(self):
        """T020a: Verify last supervisor cannot be deactivated (FR-015)."""
        # Create single supervisor member
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",  # Manager is_supervisor=1
                "status": "Active",
            }
        )
        member.insert()

        # Try to deactivate
        with self.assertRaises(frappe.ValidationError) as context:
            member.status = "Inactive"
            member.save()

        self.assertIn(
            "supervisor must remain",
            str(context.exception).lower(),
            "Error should mention supervisor protection",
        )

    def test_supervisor_can_be_deactivated_if_others_remain(self):
        """T020b: Verify supervisor can be deactivated if other supervisors remain."""
        # Create two supervisor members
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        member1.insert()

        member2 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person2.name,
                "organization": self.test_org.name,
                "role": "Owner",  # Owner is_supervisor=1
                "status": "Active",
            }
        )
        member2.insert()

        # Deactivate first member - should succeed
        member1.status = "Inactive"
        member1.save()

        member1.reload()
        self.assertEqual(member1.status, "Inactive")

    def test_non_supervisor_can_always_be_deactivated(self):
        """T020c: Verify non-supervisor can be deactivated even if last."""
        # Create supervisor member
        supervisor = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        supervisor.insert()

        # Create non-supervisor member
        employee = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person2.name,
                "organization": self.test_org.name,
                "role": "Employee",  # Employee is_supervisor=0
                "status": "Active",
            }
        )
        employee.insert()

        # Deactivate non-supervisor - should succeed
        employee.status = "Inactive"
        employee.save()

        employee.reload()
        self.assertEqual(employee.status, "Inactive")

    def test_role_change_from_supervisor_to_non_supervisor_blocked(self):
        """T020d: Verify role change from supervisor to non-supervisor is blocked if last."""
        # Create single supervisor
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        member.insert()

        # Try to change to non-supervisor role
        with self.assertRaises(frappe.ValidationError) as context:
            member.role = "Employee"
            member.save()

        self.assertIn(
            "supervisor must remain",
            str(context.exception).lower(),
            "Error should mention supervisor protection",
        )

    def test_check_is_last_supervisor_api(self):
        """T021a: Verify check_is_last_supervisor returns correct info."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            check_is_last_supervisor,
        )

        # Create single supervisor
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        member.insert()

        result = check_is_last_supervisor(member.name)

        self.assertTrue(result["is_last_supervisor"])
        self.assertEqual(result["supervisor_count"], 1)
        self.assertTrue(result["member_role_is_supervisor"])

    def test_check_is_last_supervisor_with_multiple(self):
        """T021b: Verify check_is_last_supervisor with multiple supervisors."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            check_is_last_supervisor,
        )

        # Create two supervisors
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Manager",
                "status": "Active",
            }
        )
        member1.insert()

        member2 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person2.name,
                "organization": self.test_org.name,
                "role": "Owner",
                "status": "Active",
            }
        )
        member2.insert()

        result = check_is_last_supervisor(member1.name)

        self.assertFalse(result["is_last_supervisor"])
        self.assertEqual(result["supervisor_count"], 2)

    def test_check_is_last_supervisor_for_non_supervisor(self):
        """T021c: Verify check_is_last_supervisor returns False for non-supervisor."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            check_is_last_supervisor,
        )

        # Create non-supervisor
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        result = check_is_last_supervisor(member.name)

        self.assertFalse(result["is_last_supervisor"])
        self.assertFalse(result["member_role_is_supervisor"])

    # =========================================================================
    # Phase 8: Edge Cases & Cascade Handling (T023-T026)
    # =========================================================================

    def test_person_deletion_soft_cascade(self):
        """T024a: Verify Person deletion soft-cascades Org Member to Inactive (FR-010).

        Note: This test requires the Person on_trash hook to be triggered.
        We test the handler function directly.
        """
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            handle_person_deletion,
        )

        # Create a new person for this test
        test_person = frappe.get_doc(
            {
                "doctype": "Person",
                "first_name": "Cascade",
                "last_name": "Test",
                "primary_email": "cascadetest@example.com",
            }
        )
        test_person.insert()

        # Create membership for this person
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()

        # Simulate Person deletion by calling the handler directly
        handle_person_deletion(test_person, "on_trash")

        # Verify Org Member was soft-cascaded
        member.reload()
        self.assertEqual(member.status, "Inactive")
        self.assertIsNotNone(member.end_date)

        # Clean up
        frappe.delete_doc("Person", test_person.name, force=True)

    def test_person_deletion_soft_cascade_multiple_members(self):
        """T024b: Verify Person deletion soft-cascades multiple Org Members."""
        from dartwing.dartwing_core.doctype.org_member.org_member import (
            handle_person_deletion,
        )

        # Create a new person for this test
        test_person = frappe.get_doc(
            {
                "doctype": "Person",
                "first_name": "Multi",
                "last_name": "Cascade",
                "primary_email": "multicascade@example.com",
            }
        )
        test_person.insert()

        # Create memberships in both organizations
        member1 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": test_person.name,
                "organization": self.test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member1.insert()

        member2 = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": test_person.name,
                "organization": self.test_family_org.name,
                "role": "Parent",
                "status": "Active",
            }
        )
        member2.insert()

        # Simulate Person deletion
        handle_person_deletion(test_person, "on_trash")

        # Verify both Org Members were soft-cascaded
        member1.reload()
        member2.reload()
        self.assertEqual(member1.status, "Inactive")
        self.assertEqual(member2.status, "Inactive")

        # Clean up
        frappe.delete_doc("Person", test_person.name, force=True)

    def test_organization_deletion_cascade(self):
        """T025: Verify Organization deletion cascades Org Members (FR-012).

        Note: Frappe's standard Link cascade behavior deletes linked records.
        This test verifies that behavior.
        """
        # Create a test organization specifically for deletion
        test_org = frappe.get_doc(
            {
                "doctype": "Organization",
                "org_name": "Test Delete Org",
                "org_type": "Company",
            }
        )
        test_org.insert()

        # Create membership
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": test_org.name,
                "role": "Employee",
                "status": "Active",
            }
        )
        member.insert()
        member_name = member.name

        # Delete the organization
        frappe.delete_doc("Organization", test_org.name, force=True)

        # Verify Org Member was also deleted (standard Frappe cascade)
        self.assertFalse(
            frappe.db.exists("Org Member", member_name),
            "Org Member should be deleted when Organization is deleted",
        )

    def test_role_template_deletion_prevented_when_linked(self):
        """T026: Verify Role Template deletion is prevented when linked (FR-011).

        Note: This test verifies the existing Role Template on_trash hook
        works with Org Member.
        """
        # Create test role
        test_role = frappe.get_doc(
            {
                "doctype": "Role Template",
                "role_name": "Test Delete Role",
                "applies_to_org_type": "Company",
            }
        )
        test_role.insert()

        # Create membership using this role
        member = frappe.get_doc(
            {
                "doctype": "Org Member",
                "person": self.test_person.name,
                "organization": self.test_org.name,
                "role": test_role.name,
                "status": "Active",
            }
        )
        member.insert()

        # Try to delete the role - should fail
        with self.assertRaises(frappe.exceptions.LinkExistsError):
            frappe.delete_doc("Role Template", test_role.name)

        # Clean up
        frappe.delete_doc("Org Member", member.name, force=True)
        frappe.delete_doc("Role Template", test_role.name, force=True)
