# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import threading
from typing import Dict, Any, Optional

import frappe
from frappe import _
from frappe.model.document import Document

# Configure logger for audit trail
logger = frappe.logger("dartwing_core.hooks", allow_site=True, file_count=10)

# DocType name constants (Issue #16)
DOCTYPE_ORGANIZATION = "Organization"
DOCTYPE_FAMILY = "Family"
DOCTYPE_COMPANY = "Company"
DOCTYPE_ASSOCIATION = "Association"
DOCTYPE_NONPROFIT = "Nonprofit"

# Mapping from org_type to concrete DocType
# CR-006 FIX: Added Association for consistency with fixtures
ORG_TYPE_MAP = {
    "Family": "Family",
    "Company": "Company",
    "Club": "Club",
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


def validate_org_field_map() -> bool:
    """
    Validate that ORG_FIELD_MAP field names exist on their respective DocTypes (Issue #10).

    This function checks configuration consistency at runtime to prevent errors
    from misconfigured field mappings.

    Returns:
        bool: True if validation passes

    Raises:
        frappe.ValidationError: If critical field mappings are invalid
    """
    errors = []

    for org_type, field_config in ORG_FIELD_MAP.items():
        concrete_doctype = ORG_TYPE_MAP.get(org_type)

        # Skip if DocType doesn't exist in system
        if not concrete_doctype or not frappe.db.exists("DocType", concrete_doctype):
            continue

        try:
            meta = frappe.get_meta(concrete_doctype)

            # Check name_field exists
            name_field = field_config.get("name_field")
            if name_field and not meta.has_field(name_field):
                errors.append(
                    f"DocType {concrete_doctype}: field '{name_field}' not found "
                    f"(required by ORG_FIELD_MAP for {org_type})"
                )

            # Check status_field exists
            status_field = field_config.get("status_field")
            if status_field and not meta.has_field(status_field):
                errors.append(
                    f"DocType {concrete_doctype}: field '{status_field}' not found "
                    f"(required by ORG_FIELD_MAP for {org_type})"
                )

        except Exception as e:
            errors.append(f"Error validating {concrete_doctype}: {str(e)}")

    if errors:
        error_msg = "ORG_FIELD_MAP validation errors:\n" + "\n".join(errors)
        logger.error(error_msg)
        # Fail fast: raise exception to prevent silent failures at runtime
        error_count = len(errors)
        # Limit displayed errors to avoid overwhelming UI; full list is in error log
        max_display = 3
        displayed_errors = "; ".join(errors[:max_display])
        if error_count > max_display:
            displayed_errors += _("; ... and {0} more (see error log)").format(error_count - max_display)
        raise frappe.ValidationError(
            _("Organization field mapping configuration is invalid ({0} error(s)): {1}").format(
                error_count, displayed_errors
            )
        )

    return True


# Thread-safe cache for field map validation
_field_map_validated = False
_validation_lock = threading.Lock()


def _ensure_field_map_validated() -> None:
    """Validate ORG_FIELD_MAP once on first use (thread-safe cached).

    Uses double-checked locking pattern for thread safety while minimizing
    lock contention after initial validation.

    Raises:
        frappe.ValidationError: If field mappings are invalid
    """
    global _field_map_validated
    if _field_map_validated:
        return  # Fast path, no lock needed
    with _validation_lock:
        if not _field_map_validated:  # Double-check after acquiring lock
            validate_org_field_map()  # Raises on error
            _field_map_validated = True


class Organization(Document):
    def validate(self) -> None:
        """Validate organization before save."""
        # Validate field mappings once on first use
        _ensure_field_map_validated()

        self._validate_org_name()
        self._validate_org_type()
        self._validate_org_type_immutability()
        self._set_defaults()

        # Validate link integrity for existing records (Issue #12)
        if not self.is_new():
            link_validation = self.validate_links()
            if not link_validation["valid"]:
                for error in link_validation["errors"]:
                    frappe.msgprint(
                        msg=_("Link validation warning: {0}").format(error),
                        indicator="orange",
                        alert=True
                    )

    def _validate_org_name(self) -> None:
        """Ensure org_name is provided."""
        if not self.org_name:
            frappe.throw(_("Organization Name is required"))

    def _validate_org_type(self) -> None:
        """Validate org_type is one of the supported types (FR-010)."""
        if self.org_type and self.org_type not in ORG_TYPE_MAP:
            valid_types = ", ".join(ORG_TYPE_MAP.keys())
            frappe.throw(
                _("Invalid org_type: {0}. Must be one of: {1}").format(
                    self.org_type, valid_types
                )
            )

    def _validate_org_type_immutability(self) -> None:
        """Prevent org_type changes after creation (FR-007)."""
        if not self.is_new() and self.has_value_changed("org_type"):
            frappe.throw(_("Organization type cannot be changed after creation"))

    def _set_defaults(self) -> None:
        """Set default values."""
        if not self.status:
            self.status = "Active"

    def validate_links(self) -> Dict[str, Any]:
        """
        Validate link integrity between Organization and concrete type (Issue #12).

        Returns:
            dict: {
                "valid": bool,
                "errors": List[str],
                "warnings": List[str]
            }
        """
        errors = []
        warnings = []

        # Check if linked_doctype is set
        if not self.linked_doctype:
            warnings.append("No linked_doctype set")
            return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

        # Check if linked_name is set
        if not self.linked_name:
            errors.append(f"linked_doctype is '{self.linked_doctype}' but linked_name is empty")
            return {"valid": False, "errors": errors, "warnings": warnings}

        # Check if concrete type exists
        if not frappe.db.exists(self.linked_doctype, self.linked_name):
            errors.append(
                f"Concrete type {self.linked_doctype} '{self.linked_name}' does not exist"
            )
            return {"valid": False, "errors": errors, "warnings": warnings}

        # Check bidirectional link
        try:
            concrete = frappe.get_doc(self.linked_doctype, self.linked_name)
            if hasattr(concrete, "organization"):
                if concrete.organization != self.name:
                    errors.append(
                        f"Bidirectional link broken: {self.linked_doctype} '{self.linked_name}' "
                        f"points to Organization '{concrete.organization}' instead of '{self.name}'"
                    )
            else:
                warnings.append(
                    f"{self.linked_doctype} does not have 'organization' field for bidirectional link"
                )
        except Exception as e:
            errors.append(f"Error checking bidirectional link: {str(e)}")

        return {"valid": len(errors) == 0, "errors": errors, "warnings": warnings}

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

        Security Model (Issue #13):
        - Uses ignore_permissions=True because concrete types are implementation details
        - Permissions are enforced at the Organization level, not on concrete types
        - Users create/delete Organizations, not concrete types directly
        - Concrete types are automatically managed as part of Organization lifecycle
        - This design prevents permission bypass since Organization permissions are checked

        Execution Flow:
        1. Validate org_type mapping exists
        2. Check if concrete type already created (idempotent)
        3. Create new concrete type document with mapped fields
        4. Set linked_doctype BEFORE insert (prevents race condition)
        5. Insert concrete type with system privileges
        6. Set linked_name AFTER insert (requires concrete.name)
        7. Log success for audit trail
        8. On error: log and re-raise to trigger transaction rollback
        """
    def create_concrete_type(self):
        """Create the concrete type document (e.g., Family, Company) and link it back."""
        concrete_doctype = ORG_TYPE_MAP.get(self.org_type)

        if not concrete_doctype:
            logger.warning(
                f"Organization {self.name}: No concrete doctype mapping for org_type: {self.org_type}"
            )
            return

        # Check if concrete type already exists
        if self.linked_name and frappe.db.exists(concrete_doctype, self.linked_name):
            return

        # Check if the concrete doctype exists in the system
        if not frappe.db.exists("DocType", concrete_doctype):
            logger.warning(
                f"Organization {self.name}: Concrete doctype {concrete_doctype} does not exist, skipping creation"
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
                        _("Organization '{0}': Name field '{1}' not found on {2}; cannot set org_name").format(
                            self.name, name_field, concrete_doctype
                        )
                    )

                # Set status field
                status_field = field_config.get("status_field")
                if status_field and hasattr(concrete, status_field):
                    setattr(concrete, status_field, self.status)
            else:
                logger.warning(
                    f"Organization {self.name}: No field mapping configured for org_type: {self.org_type}"
                )
            # Set linked_doctype BEFORE concrete creation to prevent race condition
            self.db_set("linked_doctype", concrete_doctype, update_modified=False)

            # Execute with system privileges (FR-013)
            concrete.flags.ignore_permissions = True
            concrete.flags.from_organization = True  # Prevent recursion

            # Set type-specific fields
            if concrete_doctype == "Family":
                concrete.family_name = self.org_name
                concrete.status = self.status
            elif concrete_doctype == "Company":
                concrete.legal_name = self.org_name

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
            frappe.log_error(f"Error creating concrete type {concrete_doctype}: {str(e)}")
            frappe.throw(
                _("Failed to create {0} record. Please try again or contact support.").format(
                    concrete_doctype
                )
            )

        Implements FR-005, FR-006, FR-012, FR-013.

        Security Model (Issue #13):
        - Uses ignore_permissions=True for same reasons as _create_concrete_type()
        - Permissions enforced at Organization level, not on concrete types
        - When user deletes Organization (with permissions check), concrete type auto-deletes
        - Concrete types cannot be deleted directly by users
        - This design ensures consistent deletion and prevents orphaned data

        Execution Flow:
        1. Check if linked_doctype and linked_name are set
        2. Verify concrete type exists before attempting delete
        3. Delete concrete type with system privileges
        4. Catch LinkExistsError if other records reference the concrete type
        5. Log success/failure for audit trail
        6. Silently continue if concrete type already missing (idempotent)
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
                    f"Other records still reference it. {str(e)}"
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
def get_concrete_doc(organization: str) -> Optional[dict]:
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
    logger.info(f"API: get_concrete_doc called for Organization '{organization}'")
    org = frappe.get_doc("Organization", organization)

    if not org.linked_doctype or not org.linked_name:
        logger.info(f"API: get_concrete_doc - No linked concrete type for '{organization}'")
        return None

    if not frappe.db.exists(org.linked_doctype, org.linked_name):
        logger.warning(
            f"API: get_concrete_doc - Concrete type {org.linked_doctype} "
            f"'{org.linked_name}' not found for Organization '{organization}'"
        )
        return None

    concrete = frappe.get_doc(org.linked_doctype, org.linked_name)
    logger.info(
        f"API: get_concrete_doc - Returning {org.linked_doctype} '{org.linked_name}' "
        f"for Organization '{organization}'"
    )
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
    logger.info(f"API: get_organization_with_details called for '{organization}'")
    org = frappe.get_doc("Organization", organization)
    result = org.as_dict()

    if org.linked_doctype and org.linked_name:
        # Optimize: use try/except instead of db.exists() + get_doc() (Issue #11)
        # This reduces queries from 3 to 2 (one for org, one for concrete)
        try:
            concrete = frappe.get_doc(org.linked_doctype, org.linked_name)
            result["concrete_type"] = concrete.as_dict()
            logger.info(
                f"API: get_organization_with_details - Including {org.linked_doctype} "
                f"'{org.linked_name}' for Organization '{organization}'"
            )
        except frappe.DoesNotExistError:
            logger.warning(
                f"API: get_organization_with_details - Concrete type {org.linked_doctype} "
                f"'{org.linked_name}' not found for Organization '{organization}'"
            )
            result["concrete_type"] = None
    else:
        logger.info(f"API: get_organization_with_details - No linked concrete type for '{organization}'")
        result["concrete_type"] = None

    return result


@frappe.whitelist()
def validate_organization_links(organization: str) -> dict:
    """
    Validate link integrity for an Organization (Issue #12).

    This whitelisted API allows external validation of Organization links,
    useful for data integrity checks and diagnostics.

    Args:
        organization: The Organization name/ID

    Returns:
        dict: {
            "valid": bool,
            "errors": List[str],
            "warnings": List[str]
        }

    Raises:
        DoesNotExistError: If the Organization does not exist
    """
    org = frappe.get_doc("Organization", organization)
    return org.validate_links()


# ============================================================================
# Helper Functions
# ============================================================================

def get_organization_for_family(family_name: str) -> Optional[str]:
    """Get the Organization linked to a Family."""
    org = frappe.db.get_value(
        "Organization",
        {"linked_doctype": "Family", "linked_name": family_name},
        "name"
    )
    return org


def create_organization_for_family(family_doc: Document) -> str:
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
