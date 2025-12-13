# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

# Configure logger for audit trail
logger = frappe.logger("dartwing_core.hooks", allow_site=True, file_count=10)

# Mapping from org_type to concrete DocType (FR-010)
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Association": "Association",
    "Nonprofit": "Nonprofit",
}

# Mapping from org_type to field names for concrete type initialization
# Each entry defines which fields to copy from Organization to the concrete type
ORG_FIELD_MAP = {
    "Family": {"name_field": "family_name", "status_field": "status"},
    "Company": {"name_field": "company_name", "status_field": "status"},
    "Association": {"name_field": "association_name", "status_field": "status"},
    "Nonprofit": {"name_field": "nonprofit_name", "status_field": "status"},
}


class Organization(Document):
    def validate(self):
        """Validate organization before save."""
        self._validate_org_name()
        self._validate_org_type()
        self._validate_org_type_immutability()
        self._set_defaults()

    def _validate_org_name(self):
        """Ensure org_name is provided."""
        if not self.org_name:
            frappe.throw(_("Organization Name is required"))

    def _validate_org_type(self):
        """Validate org_type is one of the supported types (FR-010)."""
        if self.org_type and self.org_type not in ORG_TYPE_MAP:
            valid_types = ", ".join(ORG_TYPE_MAP.keys())
            frappe.throw(
                _("Invalid org_type: {0}. Must be one of: {1}").format(
                    self.org_type, valid_types
                )
            )

    def _validate_org_type_immutability(self):
        """Prevent org_type changes after creation (FR-007)."""
        if not self.is_new() and self.has_value_changed("org_type"):
            frappe.throw(_("Organization type cannot be changed after creation"))

    def _set_defaults(self):
        """Set default values."""
        if not self.status:
            self.status = "Active"

    def after_insert(self):
        """Create concrete type document after organization is created (FR-001)."""
        # Skip if this was created by a concrete type (to prevent recursion)
        if getattr(self.flags, "skip_concrete_type", False):
            return
        self._create_concrete_type()

    def on_trash(self):
        """Delete linked concrete type when organization is deleted (FR-005)."""
        self._delete_concrete_type()

    def _create_concrete_type(self):
        """
        Create the concrete type document and establish bidirectional link.

        Implements FR-001 through FR-004, FR-011, FR-012, FR-013.
        """
        concrete_doctype = ORG_TYPE_MAP.get(self.org_type)

        if not concrete_doctype:
            logger.warning(
                f"No concrete doctype mapping for org_type: {self.org_type}"
            )
            return

        # Check if concrete type already exists
        if self.linked_name and frappe.db.exists(concrete_doctype, self.linked_name):
            return

        # Check if the concrete doctype exists in the system
        if not frappe.db.exists("DocType", concrete_doctype):
            logger.warning(
                f"Concrete doctype {concrete_doctype} does not exist, skipping creation"
            )
            return

        try:
            concrete = frappe.new_doc(concrete_doctype)

            # Set the organization link (FR-004)
            concrete.organization = self.name

            # Set fields based on ORG_FIELD_MAP configuration
            field_config = ORG_FIELD_MAP.get(self.org_type, {})

            if field_config:
                # Set name field
                name_field = field_config.get("name_field")
                if name_field and hasattr(concrete, name_field):
                    setattr(concrete, name_field, self.org_name)
                else:
                    raise frappe.ValidationError(
                        _("Name field '{0}' not found on {1}; cannot set org_name").format(name_field, concrete_doctype)
                    )

                # Set status field
                status_field = field_config.get("status_field")
                if status_field and hasattr(concrete, status_field):
                    setattr(concrete, status_field, self.status)
            else:
                logger.warning(
                    f"No field mapping configured for org_type: {self.org_type}"
                )
            # Set linked_doctype BEFORE concrete creation to prevent race condition (FR-015)
            self.db_set("linked_doctype", concrete_doctype, update_modified=False)

            # Execute with system privileges (FR-013)
            concrete.flags.ignore_permissions = True
            concrete.flags.from_organization = True  # Prevent recursion
            concrete.insert()

            # Update organization with linked_name AFTER concrete creation (FR-002, FR-003)
            self.db_set("linked_name", concrete.name, update_modified=False)

            # Audit logging (FR-012)
            logger.info(
                f"Created {concrete_doctype} {concrete.name} for Organization {self.name}"
            )

        except Exception as e:
            # Error logging (FR-012)
            logger.error(
                f"Failed to create concrete type for Organization {self.name}: {str(e)}"
            )
            # Re-raise to trigger transaction rollback (FR-011)
            raise

    def _delete_concrete_type(self):
        """
        Delete the linked concrete type document (cascade delete).

        Implements FR-005, FR-006, FR-012, FR-013.
        """
        if not self.linked_doctype or not self.linked_name:
            return

        # Check existence before delete (FR-006)
        if frappe.db.exists(self.linked_doctype, self.linked_name):
            try:
                # Execute with system privileges (FR-013)
                frappe.delete_doc(
                    self.linked_doctype,
                    self.linked_name,
                    ignore_permissions=True
                )
                # Audit logging (FR-012)
                logger.info(
                    f"Cascade deleted {self.linked_doctype} {self.linked_name} "
                    f"for Organization {self.name}"
                )
            except frappe.LinkExistsError as e:
                # Re-raise with clearer message about link constraints
                logger.error(
                    f"Cannot delete {self.linked_doctype} {self.linked_name}: "
                    f"Other records still reference it"
                )
                frappe.throw(
                    _("Cannot delete {0} {1}: Other records still reference it").format(
                        self.linked_doctype, self.linked_name
                    )
                )
            except Exception as e:
                logger.error(
                    f"Error deleting {self.linked_doctype} {self.linked_name}: {str(e)}"
                )
                raise
        else:
            # Warning log when concrete type not found (FR-006, FR-012)
            logger.warning(
                f"Concrete type {self.linked_doctype} {self.linked_name} "
                f"not found during cascade delete for Organization {self.name}"
            )


# ============================================================================
# Whitelisted API Methods (FR-008, FR-009)
# ============================================================================

@frappe.whitelist()
def get_concrete_doc(organization: str) -> dict | None:
    """
    Return just the concrete type document for an Organization.

    Implements FR-009.

    Args:
        organization: The Organization name/ID

    Returns:
        dict: The concrete type document as a dictionary, or None if not linked

    Raises:
        DoesNotExistError: If the Organization does not exist
    """
    org = frappe.get_doc("Organization", organization)

    if not org.linked_doctype or not org.linked_name:
        return None

    if not frappe.db.exists(org.linked_doctype, org.linked_name):
        return None

    concrete = frappe.get_doc(org.linked_doctype, org.linked_name)
    return concrete.as_dict()


@frappe.whitelist()
def get_organization_with_details(organization: str) -> dict:
    """
    Return Organization merged with concrete type fields in a single request.

    Implements FR-008.

    Args:
        organization: The Organization name/ID

    Returns:
        dict: Organization data with nested 'concrete_type' object

    Raises:
        DoesNotExistError: If the Organization does not exist
    """
    org = frappe.get_doc("Organization", organization)
    result = org.as_dict()

    if org.linked_doctype and org.linked_name:
        if frappe.db.exists(org.linked_doctype, org.linked_name):
            concrete = frappe.get_doc(org.linked_doctype, org.linked_name)
            result["concrete_type"] = concrete.as_dict()
        else:
            result["concrete_type"] = None
    else:
        result["concrete_type"] = None

    return result


# ============================================================================
# Helper Functions
# ============================================================================

def get_organization_for_family(family_name: str) -> str | None:
    """Get the Organization linked to a Family."""
    org = frappe.db.get_value(
        "Organization",
        {"linked_doctype": "Family", "linked_name": family_name},
        "name"
    )
    return org


def create_organization_for_family(family_doc) -> str:
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
