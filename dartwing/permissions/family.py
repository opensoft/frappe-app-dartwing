# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Permission utilities for Family-related DocTypes.

This module implements organization-scoped access control using Frappe's
User Permission system. Users can only access Family documents belonging
to Organizations they have been granted access to.
"""

import frappe
from frappe.permissions import AUTOMATIC_ROLES


def get_permission_query_conditions(user=None):
    """
    Return SQL conditions to filter Family list based on user's org access.

    This is called by Frappe when listing Family documents to filter
    the results based on the user's permissions.

    Args:
        user: The user to check permissions for (defaults to current user)

    Returns:
        str: SQL WHERE clause condition, or empty string for no restriction
    """
    if not user:
        user = frappe.session.user

    # System Manager and Administrator see all
    if user == "Administrator":
        return ""

    user_roles = frappe.get_roles(user)
    if "System Manager" in user_roles:
        return ""

    # Get organizations this user has access to via User Permission
    organizations = get_user_organizations(user)

    if not organizations:
        # User has no org access - return impossible condition
        return "1=0"

    # Filter to families in user's organizations
    org_list = ", ".join(f"'{frappe.db.escape(org)}'" for org in organizations)
    return f"`tabFamily`.`organization` IN ({org_list})"


def has_permission(doc, ptype="read", user=None):
    """
    Check if user has permission on a specific Family document.

    Args:
        doc: The Family document to check
        ptype: Permission type (read, write, create, delete, etc.)
        user: The user to check permissions for (defaults to current user)

    Returns:
        bool: True if user has permission, False otherwise
    """
    user = user or frappe.session.user

    # Administrator always has access
    if user == "Administrator":
        return True

    # System Manager always has access
    user_roles = frappe.get_roles(user)
    if "System Manager" in user_roles:
        return True

    # Check if user has access to this Family's organization
    if not doc.organization:
        # Family without organization - allow for backwards compatibility
        # but log a warning
        frappe.log_error(
            f"Family {doc.name} has no organization - allowing access",
            "Permission Warning"
        )
        return True

    return has_org_access(user, doc.organization)


def get_member_permission_query_conditions(user=None):
    """
    Return SQL conditions to filter Family Member list based on user's org access.

    Family Members are child tables, so we filter based on the parent Family's
    organization.

    Args:
        user: The user to check permissions for (defaults to current user)

    Returns:
        str: SQL WHERE clause condition, or empty string for no restriction
    """
    if not user:
        user = frappe.session.user

    # System Manager and Administrator see all
    if user == "Administrator":
        return ""

    user_roles = frappe.get_roles(user)
    if "System Manager" in user_roles:
        return ""

    # Get organizations this user has access to
    organizations = get_user_organizations(user)

    if not organizations:
        return "1=0"

    # Filter to members whose parent Family is in user's organizations
    org_list = ", ".join(f"'{frappe.db.escape(org)}'" for org in organizations)

    # Join with Family table to check organization
    return f"""`tabFamily Member`.`parent` IN (
        SELECT name FROM `tabFamily` WHERE `organization` IN ({org_list})
    )"""


# Utility functions

def get_user_organizations(user):
    """
    Get list of Organization names the user has access to.

    Args:
        user: The user to check

    Returns:
        list: List of Organization names
    """
    # Check User Permission for Organization
    permissions = frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Organization",
        },
        pluck="for_value"
    )

    return permissions


def has_org_access(user, organization):
    """
    Check if user has access to a specific Organization.

    Args:
        user: The user to check
        organization: The Organization name

    Returns:
        bool: True if user has access
    """
    return frappe.db.exists(
        "User Permission",
        {
            "user": user,
            "allow": "Organization",
            "for_value": organization,
        }
    )


def add_org_user_permission(user, organization):
    """
    Grant a user access to an Organization.

    Args:
        user: The user to grant access to
        organization: The Organization name

    Returns:
        str: Name of the created User Permission document
    """
    if has_org_access(user, organization):
        return None  # Already has access

    doc = frappe.get_doc({
        "doctype": "User Permission",
        "user": user,
        "allow": "Organization",
        "for_value": organization,
        "apply_to_all_doctypes": 1,
    })
    doc.insert(ignore_permissions=True)

    return doc.name


def remove_org_user_permission(user, organization):
    """
    Revoke a user's access to an Organization.

    Args:
        user: The user to revoke access from
        organization: The Organization name
    """
    permissions = frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Organization",
            "for_value": organization,
        },
        pluck="name"
    )

    for perm in permissions:
        frappe.delete_doc("User Permission", perm, ignore_permissions=True)
