# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Permission-related API endpoints for Dartwing.

These endpoints provide helpers for querying permission state and are
designed for use by Flutter clients and external integrations.

API-first design per constitution: All logic via @frappe.whitelist()
"""

import frappe
from frappe import _


def _parse_bool(value, default=False):
    """
    Safely parse a boolean value from HTTP parameter (string or bool).

    Args:
        value: The value to parse (can be string, bool, or None)
        default: Default value if parsing fails

    Returns:
        bool: Parsed boolean value
    """
    if value is None:
        return default
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.lower() in ('true', '1', 'yes')
    return default


def _parse_int(value, default=100):
    """
    Safely parse an integer value from HTTP parameter (string or int).

    Args:
        value: The value to parse (can be string, int, or None)
        default: Default value if parsing fails

    Returns:
        int: Parsed integer value
    """
    if value is None:
        return default
    if isinstance(value, int):
        return value
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


@frappe.whitelist()
def get_user_organizations():
    """
    Get list of Organizations accessible by the current user.

    Returns list of Organization summaries the current user has permission
    to access. Used by Flutter clients to populate organization selectors.

    Returns:
        list[dict]: List of organization summaries with keys:
            - name: Organization ID
            - org_name: Display name
            - org_type: Organization type (Family/Company/Nonprofit/Association)
            - logo: Logo URL if set (optional)

    Raises:
        frappe.PermissionError: If user is not authenticated
    """
    user = frappe.session.user

    if user == "Guest":
        frappe.throw(_("Authentication required"), frappe.PermissionError)

    # System Manager and Administrator see all organizations
    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        organizations = frappe.get_all(
            "Organization",
            fields=["name", "org_name", "org_type", "logo"],
            order_by="org_name asc"
        )
    else:
        # Get organizations from User Permissions
        permitted_orgs = frappe.get_all(
            "User Permission",
            filters={
                "user": user,
                "allow": "Organization",
            },
            pluck="for_value"
        )

        if not permitted_orgs:
            return []

        organizations = frappe.get_all(
            "Organization",
            filters={"name": ["in", permitted_orgs]},
            fields=["name", "org_name", "org_type", "logo"],
            order_by="org_name asc"
        )

    return organizations


@frappe.whitelist()
def check_organization_access(organization: str):
    """
    Check if current user has access to a specific Organization.

    Used for pre-flight checks before navigating to organization-specific views.

    Args:
        organization: Organization name/ID to check

    Returns:
        dict: Access check result with keys:
            - has_access: bool - Whether user has access
            - org_type: str - Organization type if access granted (optional)
            - concrete_type: str - Concrete type name if access granted (optional)

    Raises:
        frappe.PermissionError: If user is not authenticated
    """
    user = frappe.session.user

    if user == "Guest":
        frappe.throw(_("Authentication required"), frappe.PermissionError)

    if not organization:
        frappe.throw(_("Organization is required"))

    # Check if organization exists
    if not frappe.db.exists("Organization", organization):
        return {"has_access": False}

    # System Manager and Administrator always have access
    has_access = False
    if user == "Administrator" or "System Manager" in frappe.get_roles(user):
        has_access = True
    else:
        # Check User Permission
        has_access = frappe.db.exists(
            "User Permission",
            {
                "user": user,
                "allow": "Organization",
                "for_value": organization,
            }
        )

    if not has_access:
        return {"has_access": False}

    # Get organization details
    org = frappe.get_doc("Organization", organization)
    result = {
        "has_access": True,
        "org_type": org.org_type,
    }

    if org.linked_doctype and org.linked_name:
        result["concrete_type"] = org.linked_name

    return result


@frappe.whitelist()
def get_organization_members(organization: str, include_inactive=False):
    """
    Get members of an Organization.

    Returns list of Org Members for the given organization.
    Only returns results if user has permission to access the organization.

    Args:
        organization: Organization name/ID
        include_inactive: Whether to include inactive members (default: False)

    Returns:
        list[dict]: List of member summaries with keys:
            - name: Org Member ID
            - person: Person ID
            - person_name: Person's full name
            - role: Role Template name
            - status: Active/Inactive/Pending
            - start_date: Membership start date
            - is_supervisor: Whether role has supervisor flag

    Raises:
        frappe.PermissionError: If user lacks access to organization
    """
    user = frappe.session.user
    # Parse boolean from HTTP parameter (may arrive as string)
    include_inactive = _parse_bool(include_inactive, default=False)

    if user == "Guest":
        frappe.throw(_("Authentication required"), frappe.PermissionError)

    if not organization:
        frappe.throw(_("Organization is required"))

    # Check access to organization
    access_check = check_organization_access(organization)
    if not access_check.get("has_access"):
        frappe.throw(
            _("Access denied to organization {0}").format(organization),
            frappe.PermissionError
        )

    # Build filters
    filters = {"organization": organization}
    if not include_inactive:
        filters["status"] = ["!=", "Inactive"]

    # Get Org Members
    members = frappe.get_all(
        "Org Member",
        filters=filters,
        fields=["name", "person", "role", "status", "start_date"]
    )

    # Batch-fetch Person names to avoid N+1 queries
    person_ids = list({m["person"] for m in members if m.get("person")})
    person_map = {}
    if person_ids:
        persons = frappe.get_all(
            "Person",
            filters={"name": ["in", person_ids]},
            fields=["name", "first_name", "last_name"]
        )
        for p in persons:
            full_name = f"{p.first_name or ''} {p.last_name or ''}".strip()
            person_map[p.name] = full_name or p.name

    # Batch-fetch Role Template supervisor flags to avoid N+1 queries
    role_ids = list({m["role"] for m in members if m.get("role")})
    role_map = {}
    if role_ids:
        roles = frappe.get_all(
            "Role Template",
            filters={"name": ["in", role_ids]},
            fields=["name", "is_supervisor"]
        )
        for r in roles:
            role_map[r.name] = bool(r.is_supervisor)

    # Enrich members with batch-fetched data
    for member in members:
        member["person_name"] = person_map.get(member["person"], member["person"])
        member["is_supervisor"] = role_map.get(member.get("role"), False)

    return members


@frappe.whitelist()
def get_permission_audit_log(
    organization: str = None,
    user: str = None,
    event_type: str = None,
    from_date: str = None,
    to_date: str = None,
    limit=100
):
    """
    Get permission audit log entries.

    Returns audit log entries for permission events. Only accessible
    by users with System Manager role.

    Note: Currently logs are stored in the file system (permission_audit.log).
    This endpoint returns metadata about the log location and applied filters.

    Args:
        organization: Filter by organization (optional)
        user: Filter by user (optional)
        event_type: Filter by event type - create, remove, skip (optional)
        from_date: Start date for log entries (optional)
        to_date: End date for log entries (optional)
        limit: Maximum entries to return (default: 100)

    Returns:
        dict: Log metadata with message, log_path, and filters_applied

    Raises:
        frappe.PermissionError: If user is not System Manager
    """
    current_user = frappe.session.user
    # Parse integer from HTTP parameter (may arrive as string)
    limit = _parse_int(limit, default=100)

    if current_user == "Guest":
        frappe.throw(_("Authentication required"), frappe.PermissionError)

    # Only System Manager can access audit logs
    if current_user != "Administrator" and "System Manager" not in frappe.get_roles(current_user):
        frappe.throw(
            _("Only System Manager can access permission audit logs"),
            frappe.PermissionError
        )

    # Note: In a production implementation, this would query from a proper
    # audit log DocType or parse log files. For now, return a placeholder
    # indicating logs are in the file system.
    return {
        "message": "Permission audit logs are stored in site logs under permission_audit.log",
        "log_path": "logs/permission_audit.log",
        "filters_applied": {
            "organization": organization,
            "user": user,
            "event_type": event_type,
            "from_date": from_date,
            "to_date": to_date,
            "limit": limit
        }
    }
