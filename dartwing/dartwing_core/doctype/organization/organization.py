# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


# Mapping from org_type to concrete DocType
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Club": "Club",
    "Nonprofit": "Nonprofit",
}


class Organization(Document):
    def validate(self):
        """Validate organization before save."""
        if not self.org_name:
            frappe.throw(_("Organization Name is required"))

        if not self.status:
            self.status = "Active"

    def after_insert(self):
        """Create concrete type document after organization is created."""
        # Skip if this was created by Family (to prevent recursion)
        if getattr(self.flags, "skip_concrete_type", False):
            return
        self.create_concrete_type()

    def on_trash(self):
        """Delete linked concrete type when organization is deleted."""
        self.delete_concrete_type()

    def create_concrete_type(self):
        """Create the concrete type document (e.g., Family) and link it back."""
        concrete_doctype = ORG_TYPE_MAP.get(self.org_type)

        if not concrete_doctype:
            return

        # Check if concrete type already exists
        if self.linked_name and frappe.db.exists(concrete_doctype, self.linked_name):
            return

        # Only create Family for now (other types not implemented yet)
        if concrete_doctype != "Family":
            return

        try:
            concrete = frappe.new_doc(concrete_doctype)
            concrete.family_name = self.org_name
            concrete.organization = self.name
            concrete.status = self.status
            concrete.flags.ignore_permissions = True
            concrete.flags.from_organization = True  # Prevent recursion
            concrete.insert()

            # Update organization with linked info
            self.db_set("linked_doctype", concrete_doctype, update_modified=False)
            self.db_set("linked_name", concrete.name, update_modified=False)

            frappe.msgprint(
                _("Created {0}: {1}").format(concrete_doctype, concrete.name),
                alert=True
            )
        except Exception as e:
            frappe.log_error(f"Error creating concrete type {concrete_doctype}: {str(e)}")
            # Don't throw - organization can exist without concrete type

    def delete_concrete_type(self):
        """Delete the linked concrete type document."""
        if not self.linked_doctype or not self.linked_name:
            return

        if frappe.db.exists(self.linked_doctype, self.linked_name):
            try:
                frappe.delete_doc(
                    self.linked_doctype,
                    self.linked_name,
                    force=True,
                    ignore_permissions=True
                )
            except Exception as e:
                frappe.log_error(f"Error deleting {self.linked_doctype} {self.linked_name}: {str(e)}")


def get_organization_for_family(family_name):
    """Get the Organization linked to a Family."""
    org = frappe.db.get_value(
        "Organization",
        {"linked_doctype": "Family", "linked_name": family_name},
        "name"
    )
    return org


def create_organization_for_family(family_doc):
    """Create an Organization for an existing Family that doesn't have one."""
    if family_doc.organization:
        return family_doc.organization

    org = frappe.new_doc("Organization")
    org.org_name = family_doc.family_name
    org.org_type = "Family"
    org.status = family_doc.status or "Active"
    org.linked_doctype = "Family"
    org.linked_name = family_doc.name
    org.flags.ignore_permissions = True
    org.flags.skip_concrete_type = True  # Don't create another Family
    org.insert()

    return org.name
