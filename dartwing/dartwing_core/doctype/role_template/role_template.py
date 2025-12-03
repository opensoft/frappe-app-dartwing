# Copyright (c) 2025, Dartwing and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RoleTemplate(Document):
    """Role Template DocType controller.

    Role Templates define organization-type-specific roles that can be assigned
    to members of an organization. Each role belongs to a specific org_type
    (Family, Company, Nonprofit, Association) and may have supervisor privileges.
    """

    def validate(self):
        """Validate role template before save."""
        self.validate_hourly_rate()

    def validate_hourly_rate(self):
        """Validate hourly rate field.

        - Clears hourly rate for Family roles (non-employment relationships)
        - Rejects negative hourly rates for all other org types
        """
        if self.applies_to_org_type == "Family":
            self.default_hourly_rate = 0
        elif self.default_hourly_rate and self.default_hourly_rate < 0:
            frappe.throw(
                "Hourly rate cannot be negative.",
                frappe.ValidationError,
            )

    def on_trash(self):
        """Prevent deletion if role is in use by Org Members."""
        self.check_linked_org_members()

    def check_linked_org_members(self):
        """Check if any Org Members reference this role."""
        # Graceful fallback when Org Member DocType doesn't exist yet (Feature 3)
        if not frappe.db.exists("DocType", "Org Member"):
            return

        linked_count = frappe.db.count("Org Member", {"role": self.name})
        if linked_count > 0:
            frappe.throw(
                f"Cannot delete Role Template '{self.role_name}': "
                f"{linked_count} Org Member(s) are using this role.",
                frappe.LinkExistsError,
            )


@frappe.whitelist()
def get_roles_for_org_type(org_type: str) -> list:
    """Get all Role Templates for a specific organization type.

    This API method is used by Org Member forms to filter available roles
    based on the parent organization's type.

    Args:
        org_type: Organization type (Family, Company, Nonprofit, Association)

    Returns:
        List of Role Template documents matching the org_type
    """
    return frappe.get_all(
        "Role Template",
        filters={"applies_to_org_type": org_type},
        fields=[
            "name",
            "role_name",
            "applies_to_org_type",
            "is_supervisor",
            "default_hourly_rate",
        ],
        order_by="role_name asc",
    )


@frappe.whitelist()
def is_supervisor_role(role_name: str) -> bool:
    """Check if a role has supervisor privileges.

    Args:
        role_name: Name of the Role Template to check

    Returns:
        True if the role is a supervisor role, False otherwise

    Raises:
        frappe.ValidationError: If the role_name does not exist
    """
    try:
        role = frappe.get_doc("Role Template", role_name)
        return bool(role.is_supervisor)
    except frappe.DoesNotExistError:
        frappe.throw(
            f"Role Template '{role_name}' does not exist.",
            frappe.ValidationError,
        )
