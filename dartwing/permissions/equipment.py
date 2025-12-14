# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Permission query conditions for Equipment DocType.

Equipment visibility is controlled through Organization User Permissions.
Users can only see equipment belonging to organizations they have access to.
"""

import frappe


def get_permission_query_conditions_equipment(user):
    """Filter Equipment list by user's accessible Organizations (FR-003, FR-009).

    Generates SQL conditions to filter equipment records based on the user's
    Organization User Permissions. System Managers and Administrator bypass this filter.

    Args:
        user: The user to check permissions for

    Returns:
        str: SQL WHERE clause condition, empty string for no restriction,
             or "1=0" if user has no access to any organization
    """
    if not user:
        user = frappe.session.user

    # Administrator and System Manager can see all equipment
    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return ""

    # Get all organizations the user has permission for
    orgs = frappe.get_all(
        "User Permission",
        filters={"user": user, "allow": "Organization"},
        pluck="for_value",
    )

    if not orgs:
        # User has no organization access - return impossible condition
        return "1=0"

    # Build IN clause for allowed organizations
    # P1-01 FIX: frappe.db.escape() already returns quoted strings
    org_list = ", ".join(frappe.db.escape(o) for o in orgs)
    return f"`tabEquipment`.`owner_organization` IN ({org_list})"


def has_permission_equipment(doc, ptype, user):
    """Check if user has permission on a specific Equipment record (FR-003).

    Validates that the user has a User Permission for the equipment's
    owner organization. System Managers and Administrator always have access.

    Args:
        doc: The Equipment document
        ptype: Permission type (read, write, etc.)
        user: The user to check

    Returns:
        bool: True if user has permission, False otherwise
    """
    if not user:
        user = frappe.session.user

    # Administrator and System Manager can access any equipment
    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return True

    # Check if user has permission for the equipment's organization
    return bool(frappe.db.exists(
        "User Permission",
        {
            "user": user,
            "allow": "Organization",
            "for_value": doc.owner_organization,
        },
    ))
