"""
Shared test fixtures for Dartwing test suite.

P2-001 FIX: Centralized test fixture helpers to eliminate code duplication
across test_permission_api.py, test_full_workflow.py, and other test files.

Provides reusable helpers for creating test data with automatic cleanup tracking.
"""

import frappe


class DartwingTestFixtures:
    """Base class for test fixtures with automatic cleanup tracking.

    Usage:
        def setUp(self):
            self.fixtures = DartwingTestFixtures(prefix="_Test_")

        def tearDown(self):
            self.fixtures.cleanup_all()

        def test_something(self):
            user = self.fixtures.create_test_user("user1")
            person = self.fixtures.create_test_person("person1", frappe_user=user)
            org, concrete = self.fixtures.create_test_organization("org1", "Family")
    """

    def __init__(self, prefix="_Test_"):
        """Initialize fixtures with a test data prefix.

        Args:
            prefix: String prefix for all test data (default: "_Test_")
        """
        self.prefix = prefix
        self.created_records = {
            "User": [],
            "Person": [],
            "Organization": [],
            "Org Member": [],
            "User Permission": []
        }

    def create_test_user(self, name_suffix, roles=None):
        """Create a test Frappe User with automatic cleanup tracking.

        Args:
            name_suffix: Suffix to append to test prefix for unique identification
            roles: List of role names (default: ["Dartwing User"])

        Returns:
            str: Email address of created user
        """
        if roles is None:
            roles = ["Dartwing User"]

        email = f"{self.prefix}{name_suffix}@test.example.com"

        if not frappe.db.exists("User", email):
            user = frappe.get_doc({
                "doctype": "User",
                "email": email,
                "first_name": "Test",
                "last_name": name_suffix,
                "enabled": 1,
                "user_type": "System User",
                "roles": [{"role": role} for role in roles]
            })
            user.flags.ignore_permissions = True
            user.insert(ignore_permissions=True)
            self.created_records["User"].append(email)

        return email

    def create_test_person(self, name_suffix, frappe_user=None, **kwargs):
        """Create a test Person with automatic cleanup tracking.

        Args:
            name_suffix: Suffix to append to test prefix for unique identification
            frappe_user: Optional Frappe User email to link to this Person
            **kwargs: Additional fields to set on the Person document

        Returns:
            Document: Created Person document
        """
        person_data = {
            "doctype": "Person",
            "first_name": "Test",
            "last_name": name_suffix,
            "primary_email": f"{self.prefix}{name_suffix}@test.example.com",
            "source": "manual"
        }

        if frappe_user:
            person_data["frappe_user"] = frappe_user

        person_data.update(kwargs)

        person = frappe.get_doc(person_data)
        person.insert(ignore_permissions=True)
        self.created_records["Person"].append(person.name)

        return person

    def create_test_organization(self, name_suffix, org_type="Family", **org_kwargs):
        """Create a test Organization with concrete type and automatic cleanup tracking.

        Creates Organization first (not concrete type), which triggers hook to create
        concrete type. This matches production behavior per dartwing_core_arch.md.

        Args:
            name_suffix: Suffix to append to test prefix for unique identification
            org_type: Type of organization ("Family", "Company", "Association", "Nonprofit")
            **org_kwargs: Additional fields to set on the Organization document

        Returns:
            tuple: (Organization document, Concrete type document)

        Raises:
            ValueError: If Organization hook fails to create concrete type
        """
        # Step 1: Create Organization with org_type
        org = frappe.get_doc({
            "doctype": "Organization",
            "org_name": f"{self.prefix}{org_type} {name_suffix}",
            "org_type": org_type,
            "status": "Active"
        })
        org.insert(ignore_permissions=True)

        # Step 2: Reload to get hook-populated linked_doctype and linked_name
        org.reload()

        # Step 3: Fetch the concrete type created by hooks
        if not org.linked_doctype or not org.linked_name:
            raise ValueError(f"Organization hook failed to create concrete type for {org.name}")

        concrete = frappe.get_doc(org.linked_doctype, org.linked_name)
        self.created_records["Organization"].append(org.name)

        # Apply any additional org kwargs
        if org_kwargs:
            for key, value in org_kwargs.items():
                setattr(org, key, value)
            org.save(ignore_permissions=True)
            org.reload()

        return org, concrete

    def create_test_org_member(self, person, organization, **kwargs):
        """Create a test Org Member with automatic cleanup tracking.

        Args:
            person: Person document or name
            organization: Organization document or name
            **kwargs: Additional fields to set on Org Member

        Returns:
            Document: Created Org Member document
        """
        person_name = person.name if hasattr(person, 'name') else person
        org_name = organization.name if hasattr(organization, 'name') else organization

        member_data = {
            "doctype": "Org Member",
            "person": person_name,
            "organization": org_name,
            "status": "Active",
            "start_date": frappe.utils.today()
        }
        member_data.update(kwargs)

        member = frappe.get_doc(member_data)
        member.insert(ignore_permissions=True)
        self.created_records["Org Member"].append(member.name)

        return member

    def cleanup_all(self):
        """Clean up all created test records in reverse dependency order.

        Cleanup order: User Permissions → Org Members → Organizations → Persons → Users
        This prevents LinkExistsError cascades and surfaces deletion hook bugs.
        """
        # 1. User Permissions (no dependencies)
        for perm_name in self.created_records.get("User Permission", []):
            try:
                frappe.delete_doc("User Permission", perm_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass

        # 2. Org Members (depends on Person and Organization)
        for member_name in self.created_records.get("Org Member", []):
            try:
                frappe.delete_doc("Org Member", member_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass

        # 3. Organizations (cascades to concrete types via hooks)
        for org_name in self.created_records.get("Organization", []):
            try:
                frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass
            except frappe.LinkExistsError as e:
                # Log unexpected link errors
                frappe.log_error(
                    f"LinkExistsError during fixture cleanup for {org_name}: {str(e)}",
                    "Test Fixture Cleanup Error"
                )
                # Force delete blocking links
                frappe.db.sql("DELETE FROM `tabOrg Member` WHERE organization = %s", org_name)
                frappe.db.commit()
                frappe.delete_doc("Organization", org_name, force=True, ignore_permissions=True)

        # 4. Persons (no longer referenced by Org Members)
        for person_name in self.created_records.get("Person", []):
            try:
                frappe.delete_doc("Person", person_name, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass

        # 5. Users (at the end, after Person deletion)
        for user_email in self.created_records.get("User", []):
            try:
                frappe.delete_doc("User", user_email, force=True, ignore_permissions=True)
            except frappe.DoesNotExistError:
                pass

        # Clear tracking
        self.created_records = {
            "User": [],
            "Person": [],
            "Organization": [],
            "Org Member": [],
            "User Permission": []
        }
