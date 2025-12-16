# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Organization API - Whitelisted methods for Flutter client integration.

This module provides standardized REST API endpoints enabling external clients
to retrieve organization data, member information, and concrete type details.

API Methods:
    - get_user_organizations(): Returns all organizations the authenticated user belongs to
    - get_org_members(): Returns paginated list of members for an organization

Note: get_organization_with_details() and get_concrete_doc() are defined in
dartwing_core/doctype/organization/organization.py as they are document-centric.

API Versioning Notice (P3-005):
-------------------------------
This module provides NEW API endpoints that differ from the legacy endpoints in
`dartwing/permissions/api.py`. Key differences:

1. get_user_organizations():
   - THIS module: Returns orgs based on Org Member table (membership data)
   - LEGACY (permissions/api.py): Returns orgs based on User Permission table
   - USE THIS for: Membership-aware org lists (shows roles, status, supervisor flag)
   - USE LEGACY for: Permission-only checks (simpler, faster)

2. get_org_members() vs get_organization_members():
   - THIS module: Paginated (limit/offset), status enum filter, supervisor email privacy
   - LEGACY (permissions/api.py): include_inactive boolean, no pagination
   - USE THIS for: Flutter client member lists with pagination
   - USE LEGACY for: Simple member fetches without pagination needs

Recommendation: For new Flutter integrations, prefer this module's endpoints.
The legacy endpoints in permissions/api.py remain supported for backward compatibility.
"""

from typing import Optional

import frappe
from frappe import _
from frappe.rate_limiter import rate_limit

# Configure logger for audit trail (following pattern from organization.py)
logger = frappe.logger("dartwing_core.api", allow_site=True, file_count=10)

# P2-005: Rate limiting constants
API_RATE_LIMIT = 100  # requests per window
API_RATE_WINDOW = 60  # seconds

# CR-003: Cache TTL for supervisor status (seconds)
# Supervisor status rarely changes during active sessions
SUPERVISOR_CACHE_TTL = 60


def _is_supervisor_cached(person: str, organization: str) -> bool:
    """
    Check if person has supervisor role in organization, with caching.

    CR-003: Caches result for 60 seconds to reduce DB load since
    supervisor status rarely changes during active sessions.

    Args:
        person: Person document name
        organization: Organization document name

    Returns:
        bool: True if person has active supervisor role
    """
    cache_key = f"supervisor_check:{frappe.local.site}:{person}:{organization}"

    # Try to get from cache first
    cached = frappe.cache.get_value(cache_key)
    if cached is not None:
        return cached

    # Query database
    is_supervisor = bool(frappe.db.sql(
        """
        SELECT 1 FROM `tabOrg Member` om
        JOIN `tabRole Template` rt ON om.role = rt.name
        WHERE om.person = %s AND om.organization = %s
        AND om.status = 'Active' AND rt.is_supervisor = 1
        LIMIT 1
        """,
        (person, organization)
    ))

    # Cache result with TTL
    frappe.cache.set_value(cache_key, is_supervisor, expires_in_sec=SUPERVISOR_CACHE_TTL)

    return is_supervisor


@rate_limit(limit=API_RATE_LIMIT, seconds=API_RATE_WINDOW)
@frappe.whitelist()
def get_user_organizations() -> dict:
    """
    Return all organizations the authenticated user belongs to.

    Implements FR-001: System MUST provide an API method get_user_organizations()
    that returns all organizations the authenticated user is a member of.

    Returns:
        dict: {
            "data": List of organization records with membership info,
            "total_count": Total number of organizations
        }

    Raises:
        AuthenticationError: If user is not logged in (handled by @frappe.whitelist)
    """
    # T012: Derive current user's Person from frappe.session.user
    user = frappe.session.user
    if user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    # Get Person linked to current user
    person = frappe.db.get_value("Person", {"frappe_user": user}, "name")

    if not person:
        # User exists but has no Person record - return empty list
        logger.info(f"API: get_user_organizations - No Person found for user '{user}'")
        return {"data": [], "total_count": 0}

    # T013: Query Org Member records for current user's Person
    # T014: Join Organization to include org_name, org_type, logo, status
    # T15: Join Role Template to include role name and is_supervisor flag
    memberships = frappe.db.sql(
        """
        SELECT
            om.name as membership_name,
            om.organization,
            om.role,
            om.status as membership_status,
            om.start_date,
            om.end_date,
            org.org_name,
            org.org_type,
            org.logo,
            org.status,
            org.linked_doctype,
            org.linked_name,
            rt.is_supervisor
        FROM `tabOrg Member` om
        INNER JOIN `tabOrganization` org ON om.organization = org.name
        LEFT JOIN `tabRole Template` rt ON om.role = rt.name
        WHERE om.person = %(person)s
        ORDER BY om.start_date DESC
        """,
        {"person": person},
        as_dict=True,
    )

    # T16: Format response as {data: [...], total_count: N}
    # P1-005: Add has_access field to indicate actual permission status
    data = []
    for m in memberships:
        data.append({
            "name": m.organization,
            "org_name": m.org_name,
            "org_type": m.org_type,
            "logo": m.logo,
            "status": m.status,
            "linked_doctype": m.linked_doctype,
            "linked_name": m.linked_name,
            "role": m.role,
            "membership_status": m.membership_status,
            "is_supervisor": m.is_supervisor or 0,
            "has_access": frappe.has_permission("Organization", "read", m.organization),
        })

    # T17: Add INFO-level audit logging for successful calls
    logger.info(
        f"API: get_user_organizations - User '{user}' retrieved {len(data)} organizations"
    )

    return {"data": data, "total_count": len(data)}


# P1-006: Validation constants
VALID_MEMBER_STATUSES = {"Active", "Inactive", "Pending"}
DEFAULT_PAGE_LIMIT = 20
MAX_PAGE_LIMIT = 100


@rate_limit(limit=API_RATE_LIMIT, seconds=API_RATE_WINDOW)
@frappe.whitelist()
def get_org_members(
    organization: str,
    limit: int = DEFAULT_PAGE_LIMIT,
    offset: int = 0,
    status: Optional[str] = None,
) -> dict:
    """
    Return paginated list of members for an organization.

    Implements FR-004, FR-006, FR-007: System MUST provide an API method
    get_org_members() with pagination and status filtering.

    Args:
        organization: Organization name/ID
        limit: Number of records to return (max 100, default 20)
        offset: Number of records to skip (default 0)
        status: Filter by member status (Active/Inactive/Pending)

    Returns:
        dict: {
            "data": List of member records,
            "total_count": Total matching records,
            "limit": Applied limit,
            "offset": Applied offset
        }

    Raises:
        AuthenticationError: If user is not logged in
        ValidationError: If parameters are invalid
        DoesNotExistError: If the organization does not exist
        PermissionError: If user lacks permission to access the organization
    """
    # P1-006: Authentication check (401)
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    # P1-006: Required parameter check
    if not organization:
        frappe.throw(_("Organization parameter is required"), frappe.ValidationError)

    # P1-006: Organization existence check (404) - before permission check for proper semantics
    if not frappe.db.exists("Organization", organization):
        frappe.throw(_("Organization {0} not found").format(organization), frappe.DoesNotExistError)

    # T038: Permission check (403)
    if not frappe.has_permission("Organization", "read", organization):
        logger.warning(f"API: get_org_members - User '{frappe.session.user}' denied access to '{organization}'")
        frappe.throw(_("Not permitted to access this organization"), frappe.PermissionError)

    # P1-006: Validate and clamp limit parameter
    try:
        limit = max(1, min(int(limit), MAX_PAGE_LIMIT))
    except (ValueError, TypeError):
        limit = DEFAULT_PAGE_LIMIT

    # P1-006: Validate and clamp offset parameter
    try:
        offset = max(0, int(offset))
    except (ValueError, TypeError):
        offset = 0

    # P1-006: Validate status enum
    if status and status not in VALID_MEMBER_STATUSES:
        frappe.throw(
            _("Invalid status: {0}. Must be one of: {1}").format(
                status, ", ".join(sorted(VALID_MEMBER_STATUSES))
            ),
            frappe.ValidationError
        )

    # T043: Build filters with optional status filter
    filters = {"organization": organization}
    if status:
        filters["status"] = status

    # P2-001: Check if current user is a supervisor for this organization
    # Supervisors can see member emails; non-supervisors can only see their own
    user = frappe.session.user
    current_person = None
    is_current_user_supervisor = False

    if user == "Administrator":
        # Administrator always has supervisor access
        is_current_user_supervisor = True
    else:
        # Get current user's Person (needed for both supervisor check and self-email visibility)
        current_person = frappe.db.get_value("Person", {"frappe_user": user}, "name")
        if current_person:
            # CR-001: Single query to check supervisor role (fixes boolean logic and redundant queries)
            # CR-003: Use cached check to reduce DB load during active sessions
            is_current_user_supervisor = _is_supervisor_cached(current_person, organization)

    # T044-T047: Query Org Member with joins to Person and Role Template
    # P2-004: Use window function COUNT(*) OVER() to get total in single query
    members = frappe.db.sql(
        """
        SELECT
            om.name,
            om.person,
            om.member_name,
            om.organization,
            om.role,
            om.status,
            om.start_date,
            om.end_date,
            p.primary_email as person_email,
            rt.is_supervisor,
            COUNT(*) OVER() as total_count
        FROM `tabOrg Member` om
        LEFT JOIN `tabPerson` p ON om.person = p.name
        LEFT JOIN `tabRole Template` rt ON om.role = rt.name
        WHERE om.organization = %(organization)s
        {status_filter}
        ORDER BY om.start_date DESC
        LIMIT %(limit)s OFFSET %(offset)s
        """.format(
            status_filter="AND om.status = %(status)s" if status else ""
        ),
        {"organization": organization, "status": status, "limit": limit, "offset": offset},
        as_dict=True,
    )

    # P2-004: Extract total_count from first row
    # Note: total_count comes from COUNT(*) OVER() window function in the SQL query above.
    # This value is identical across all rows, so we only need to read it from the first row.
    # The window function calculates total matching rows BEFORE LIMIT is applied.
    # CR-004: Use .get() for defensive access in case query format changes
    total_count = members[0].get("total_count", 0) if members else 0

    # T46: Format response
    # P2-001: Only include person_email for supervisors
    data = []
    for m in members:
        member_data = {
            "name": m.name,
            "person": m.person,
            "member_name": m.member_name,
            "organization": m.organization,
            "role": m.role,
            "status": m.status,
            "start_date": m.start_date.isoformat() if m.start_date else None,
            "end_date": m.end_date.isoformat() if m.end_date else None,
            "is_supervisor": m.is_supervisor or 0,
        }
        # CR-002: Include email for supervisors OR users viewing their own record
        # CR-005: Guard against current_person being None (user not linked to Person)
        if is_current_user_supervisor or (current_person and m.person == current_person):
            member_data["person_email"] = m.person_email
        data.append(member_data)

    # T47: Add INFO-level audit logging
    logger.info(
        f"API: get_org_members - User '{frappe.session.user}' retrieved {len(data)} of {total_count} "
        f"members for organization '{organization}' (limit={limit}, offset={offset})"
    )

    return {
        "data": data,
        "total_count": total_count,
        "limit": limit,
        "offset": offset,
    }
