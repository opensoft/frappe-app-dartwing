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

import frappe
from dartwing.utils.permission_logger import log_permission_event


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
        # Organization already deleted - remove what we can and log warning
        frappe.log_error(
            f"Organization '{doc.organization}' not found during permission cleanup "
            f"for Org Member '{doc.name}'. Removing Organization permission only; "
            f"concrete type permission may be orphaned.",
            "Permission Warning"
        )
        _delete_permission(user, "Organization", doc.organization)
        log_permission_event(
            "remove",
            doc,
            user=user,
            doctype="Organization",
            for_value=doc.organization
        )
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
