# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Permission propagation helpers for Org Member lifecycle events.

This module handles automatic User Permission creation and removal when
Org Member records are created, deleted, or have their status changed.

Key functions:
- create_user_permissions: Called on Org Member after_insert (FR-001, FR-002)
- remove_user_permissions: Called on Org Member on_trash (FR-003)
- handle_status_change: Called on Org Member on_update (FR-009)
"""

import logging

import frappe
from dartwing.utils.permission_logger import log_permission_event

# Valid organization types for concrete DocType validation
VALID_ORG_TYPES = {"Family", "Company", "Association", "Nonprofit"}


def create_user_permissions(doc, method):
    """
    Create User Permissions when an Org Member record is created.

    Creates permissions for BOTH the Organization AND its concrete type
    (Family/Company/Association/Nonprofit) if one exists.

    Args:
        doc: The Org Member document being inserted
        method: The event method name (after_insert)

    Implements:
        - FR-001: Create User Permission for Organization
        - FR-002: Create User Permission for concrete type
        - FR-007: Skip gracefully if Person has no linked Frappe User
        - FR-012: Log all permission events
    """
    # Only create permissions for Active members (Pending members don't get access yet)
    if doc.status != "Active":
        log_permission_event(
            "skip",
            doc,
            reason=f"Org Member status is '{doc.status}', not 'Active'"
        )
        return

    # Get the Frappe User from Person
    user = frappe.db.get_value("Person", doc.person, "frappe_user")

    if not user:
        # FR-007: Skip gracefully and log
        log_permission_event(
            "skip",
            doc,
            reason="Person has no linked Frappe User"
        )
        return

    # Get Organization details for concrete type lookup
    # Use ignore_permissions=True since the actor creating Org Members may not
    # have direct Organization read permission
    org = frappe.get_doc("Organization", doc.organization, ignore_permissions=True)

    # FR-001: Create permission for Organization
    _create_permission(user, "Organization", doc.organization)
    log_permission_event(
        "create",
        doc,
        user=user,
        doctype="Organization",
        for_value=doc.organization
    )

    # FR-002: Create permission for concrete type if it exists
    if org.linked_doctype and org.linked_name:
        _create_permission(user, org.linked_doctype, org.linked_name)
        log_permission_event(
            "create",
            doc,
            user=user,
            doctype=org.linked_doctype,
            for_value=org.linked_name
        )


def remove_user_permissions(doc, method):
    """
    Remove User Permissions when an Org Member record is deleted.

    Removes permissions for BOTH the Organization AND its concrete type.

    Args:
        doc: The Org Member document being deleted
        method: The event method name (on_trash)

    Implements:
        - FR-003: Remove User Permissions for Organization and concrete type
        - FR-012: Log all permission events
    """
    # Get the Frappe User from Person
    user = frappe.db.get_value("Person", doc.person, "frappe_user")

    if not user:
        # Nothing to remove - Person has no linked User
        log_permission_event(
            "skip",
            doc,
            reason="Person has no linked Frappe User - nothing to remove"
        )
        return

    # Get Organization details for concrete type lookup
    # Use ignore_permissions=True since the actor deleting Org Members may not
    # have direct Organization read permission
    try:
        org = frappe.get_doc("Organization", doc.organization, ignore_permissions=True)
    except frappe.DoesNotExistError:
        # Organization already deleted - clean up all related permissions
        # Try to determine concrete type from Org Member's cached organization_type field
        _cleanup_orphaned_permissions(user, doc)
        return

    # Remove permission for Organization
    _delete_permission(user, "Organization", doc.organization)
    log_permission_event(
        "remove",
        doc,
        user=user,
        doctype="Organization",
        for_value=doc.organization
    )

    # Remove permission for concrete type if it exists
    if org.linked_doctype and org.linked_name:
        _delete_permission(user, org.linked_doctype, org.linked_name)
        log_permission_event(
            "remove",
            doc,
            user=user,
            doctype=org.linked_doctype,
            for_value=org.linked_name
        )


def handle_status_change(doc, method):
    """
    Handle Org Member status changes for permission management.

    When status changes to Inactive, permissions are removed.
    When status changes to Active (from Inactive or Pending), permissions are created.

    Args:
        doc: The Org Member document being updated
        method: The event method name (on_update)

    Implements:
        - FR-009: Treat Inactive status same as deleted for permission purposes
    """
    if not doc.has_value_changed("status"):
        return

    previous_doc = doc.get_doc_before_save()
    old_status = previous_doc.status if previous_doc else None

    if doc.status == "Inactive" and old_status == "Active":
        # Status changed from Active to Inactive - remove permissions
        remove_user_permissions(doc, method)

    elif doc.status == "Active" and old_status in ("Inactive", "Pending"):
        # Status changed to Active from Inactive or Pending - create permissions
        create_user_permissions(doc, method)


def _create_permission(user: str, allow: str, for_value: str) -> None:
    """
    Create a User Permission if it doesn't already exist.

    Args:
        user: The Frappe User email
        allow: The DocType to permit access to
        for_value: The specific record name to grant access to
    """
    if not frappe.db.exists("User Permission", {
        "user": user,
        "allow": allow,
        "for_value": for_value
    }):
        frappe.get_doc({
            "doctype": "User Permission",
            "user": user,
            "allow": allow,
            "for_value": for_value,
            "apply_to_all_doctypes": 0
        }).insert(ignore_permissions=True)


def _delete_permission(user: str, allow: str, for_value: str) -> None:
    """
    Delete a User Permission if it exists.

    Uses frappe.db.delete for atomic deletion.

    Args:
        user: The Frappe User email
        allow: The DocType the permission is for
        for_value: The specific record name
    """
    frappe.db.delete("User Permission", {
        "user": user,
        "allow": allow,
        "for_value": for_value
    })


def _cleanup_orphaned_permissions(user: str, org_member_doc) -> None:
    """
    Clean up User Permissions when the Organization document is already deleted.
    
    This function attempts to remove both Organization and concrete type permissions
    even when the Organization document no longer exists. It uses the organization_type
    field cached in the Org Member document to determine the concrete type, and queries
    the concrete type DocType to find the specific document linked to this organization.
    
    Args:
        user: The Frappe User email
        org_member_doc: The Org Member document being deleted
    """
    # Get logger once for reuse
    logger = frappe.logger()
    
    # Remove the Organization permission
    _delete_permission(user, "Organization", org_member_doc.organization)
    log_permission_event(
        "remove",
        org_member_doc,
        user=user,
        doctype="Organization",
        for_value=org_member_doc.organization
    )
    
    # Map organization type to concrete DocType name
    # The org_type values are: Family, Company, Association, Nonprofit
    # These match the DocType names directly (capitalized)
    org_type = org_member_doc.organization_type
    
    # Validate org_type to prevent DocType injection attacks
    if org_type and org_type in VALID_ORG_TYPES:
        # Try to find the concrete document linked to this organization
        # Concrete types (Family, Company, etc.) have an 'organization' field
        try:
            concrete_docs = frappe.get_all(
                org_type,
                filters={"organization": org_member_doc.organization},
                pluck="name"
            )
            
            # Remove permissions for each found concrete document
            for concrete_name in concrete_docs:
                _delete_permission(user, org_type, concrete_name)
                log_permission_event(
                    "remove",
                    org_member_doc,
                    user=user,
                    doctype=org_type,
                    for_value=concrete_name
                )
                # Log successful cleanup as info, not error
                if logger.isEnabledFor(logging.INFO):
                    logger.info(
                        "Removed orphaned %s permission for '%s' during cleanup of Org Member '%s' "
                        "(Organization '%s' not found).",
                        org_type, concrete_name, org_member_doc.name, org_member_doc.organization
                    )
            
            if not concrete_docs:
                # No concrete document found - may have been deleted already
                if logger.isEnabledFor(logging.INFO):
                    logger.info(
                        "No %s document found linked to Organization '%s' during cleanup of Org Member '%s'. "
                        "Concrete type permissions may have already been cleaned up.",
                        org_type, org_member_doc.organization, org_member_doc.name
                    )
        except Exception as e:
            # If querying the concrete type fails, log it but continue
            frappe.log_error(
                f"Error querying {org_type} for Organization '{org_member_doc.organization}' "
                f"during cleanup of Org Member '{org_member_doc.name}': {str(e)}. "
                f"Concrete type permissions may need manual cleanup.",
                "Orphaned Permission Cleanup Error"
            )
    elif org_type and org_type not in VALID_ORG_TYPES:
        # Invalid org_type - log a warning
        frappe.log_error(
            f"Organization '{org_member_doc.organization}' not found and "
            f"organization_type '{org_type}' in Org Member '{org_member_doc.name}' "
            f"is not a valid organization type. Unable to clean up concrete type "
            f"permissions automatically. Manual cleanup may be required for user '{user}'.",
            "Permission Warning"
        )
    else:
        # No cached org_type - log a warning that we can't determine concrete type
        frappe.log_error(
            f"Organization '{org_member_doc.organization}' not found and no "
            f"organization_type cached in Org Member '{org_member_doc.name}'. "
            f"Unable to clean up concrete type permissions automatically. "
            f"Manual cleanup may be required for user '{user}'.",
            "Permission Warning"
        )
