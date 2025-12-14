# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe


def get_permission_query_conditions_company(user):
    """
    Return permission query conditions for Company DocType.

    Restricts Company access based on user's Organization permissions.
    Users can only see Companies linked to Organizations they have access to.
    """
    if not user:
        user = frappe.session.user

    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return ""

    # Get Organizations the user has permission to access
    permitted_orgs = frappe.get_all(
        "User Permission",
        filters={
            "user": user,
            "allow": "Organization"
        },
        pluck="for_value"
    )

    if not permitted_orgs:
        return "1=0"  # No access to any company

    # CR-001 FIX: Use frappe.db.escape() to prevent SQL injection
    org_list = ", ".join(frappe.db.escape(org) for org in permitted_orgs)
    return f"`tabCompany`.`organization` in ({org_list})"


def has_permission_company(doc, ptype, user):
    """
    Check if user has permission to access a specific Company document.

    Permission is granted if:
    1. User is Administrator or System Manager
    2. User has a User Permission for the linked Organization

    CR-002 FIX: Check User Permission directly instead of delegating to
    Organization permission (which users may not have).
    """
    if not user:
        user = frappe.session.user

    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        return True

    # Check if user has User Permission for this Organization
    # This allows Company access without requiring direct Organization read permission
    return bool(frappe.db.exists("User Permission", {
        "user": user,
        "allow": "Organization",
        "for_value": doc.organization
    }))
