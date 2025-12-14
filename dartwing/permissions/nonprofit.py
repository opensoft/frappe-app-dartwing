# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Permission utilities for Nonprofit DocType.

This module implements organization-scoped access control for Nonprofit records.
Users can only access Nonprofit documents belonging to Organizations they have
been granted access to via User Permissions.

Implements:
- FR-004: Filter list views to show only permitted nonprofits
- FR-005: Deny access to individual records without permission
- FR-006: System Manager bypass for administrative access
"""

import frappe


def get_permission_query_conditions(user: str = None) -> str:
    """
    Return SQL conditions to filter Nonprofit list based on user's org access.

    This is called by Frappe when listing Nonprofit documents to filter
    the results based on the user's Organization permissions.

    Args:
        user: The user to check permissions for (defaults to current user)

    Returns:
        str: SQL WHERE clause condition, or empty string for no restriction
    """
    if not user:
        user = frappe.session.user

    # FR-006: System Manager and Administrator bypass
    if user == "Administrator":
        return ""

    user_roles = frappe.get_roles(user)
    if "System Manager" in user_roles:
        return ""

    # Get organizations this user has access to via User Permission
    organizations = frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Organization",
        },
        pluck="for_value"
    )

    if not organizations:
        # User has no org access - return impossible condition
        return "1=0"

    # Filter to nonprofits in user's organizations
    # frappe.db.escape() already returns a quoted string
    org_list = ", ".join(frappe.db.escape(org) for org in organizations)
    return f"`tabNonprofit`.`organization` IN ({org_list})"


def has_permission(doc, ptype: str = "read", user: str = None) -> bool:
    """
    Check if user has permission on a specific Nonprofit document.

    Args:
        doc: The Nonprofit document to check
        ptype: Permission type (read, write, create, delete, etc.)
        user: The user to check permissions for (defaults to current user)

    Returns:
        bool: True if user has permission, False otherwise
    """
    user = user or frappe.session.user

    # FR-006: Administrator always has access
    if user == "Administrator":
        return True

    # FR-006: System Manager always has access
    user_roles = frappe.get_roles(user)
    if "System Manager" in user_roles:
        return True

    # Check if user has access to this Nonprofit's organization
    if not doc.organization:
        # BACKWARD COMPAT: Allow access to orphaned records created before
        # org-based permissions were implemented. These records should be
        # migrated to have an organization. See spec.md "Security Considerations".
        frappe.log_error(
            f"Nonprofit {doc.name} has no organization - allowing access",
            "Permission Warning"
        )
        return True

    return frappe.db.exists(
        "User Permission",
        {
            "user": user,
            "allow": "Organization",
            "for_value": doc.organization,
        }
    )
