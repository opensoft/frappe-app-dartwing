# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Permission utilities for Organization DocType.

This module implements organization-scoped access control using Frappe's
User Permission system. Users can only access Organization documents they
have been granted explicit access to via User Permissions.

Implements:
- FR-004: Filter list views to show only permitted organizations
- FR-005: Deny access to individual records without permission
- FR-006: System Manager bypass for administrative access
- FR-010: permission_query_conditions hook
- FR-011: has_permission hook
"""

import frappe


def get_permission_query_conditions(user: str = None) -> str:
    """
    Return SQL conditions to filter Organization list based on user's permissions.

    This is called by Frappe when listing Organization documents to filter
    the results based on the user's User Permissions.

    Args:
        user: The user to check permissions for (defaults to current user)

    Returns:
        str: SQL WHERE clause condition, or empty string for no restriction

    Implements:
        - FR-004: Filter list views to show only permitted records
        - FR-006: System Manager bypass
        - FR-010: permission_query_conditions hook
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

    # Filter to permitted organizations (handles multi-org via IN clause)
    # frappe.db.escape() already returns a quoted string
    org_list = ", ".join(frappe.db.escape(org) for org in organizations)
    return f"`tabOrganization`.`name` IN ({org_list})"


def has_permission(doc, ptype: str = "read", user: str = None) -> bool:
    """
    Check if user has permission on a specific Organization document.

    Args:
        doc: The Organization document to check
        ptype: Permission type (read, write, create, delete, etc.)
        user: The user to check permissions for (defaults to current user)

    Returns:
        bool: True if user has permission, False otherwise

    Implements:
        - FR-005: Deny access to individual records without permission
        - FR-006: System Manager bypass
        - FR-011: has_permission hook
    """
    user = user or frappe.session.user

    # FR-006: Administrator always has access
    if user == "Administrator":
        return True

    # FR-006: System Manager always has access
    user_roles = frappe.get_roles(user)
    if "System Manager" in user_roles:
        return True

    # Check if user has User Permission for this Organization
    return frappe.db.exists(
        "User Permission",
        {
            "user": user,
            "allow": "Organization",
            "for_value": doc.name,
        }
    )
