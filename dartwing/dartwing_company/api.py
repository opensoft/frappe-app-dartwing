# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _


@frappe.whitelist()
def get_company_with_org_details(company: str) -> dict:
    """
    Get Company record with parent Organization details.

    Args:
        company: The name of the Company document

    Returns:
        dict: Company data with embedded Organization details

    Raises:
        frappe.DoesNotExistError: If company not found
        frappe.PermissionError: If user lacks permission
    """
    if not frappe.has_permission("Company", doc=company, ptype="read"):
        frappe.throw(_("Not permitted to access this Company"), frappe.PermissionError)

    doc = frappe.get_doc("Company", company)

    # CR-003 FIX: Use db.get_value to avoid permission check on Organization
    # Users with Company access should see basic org info
    org_data = frappe.db.get_value(
        "Organization",
        doc.organization,
        ["name", "org_name", "org_type", "status"],
        as_dict=True
    )

    # Collect all person IDs from officers and members
    person_ids = set()
    for officer in doc.officers or []:
        if officer.person:
            person_ids.add(officer.person)
    for member in doc.members_partners or []:
        if member.person:
            person_ids.add(member.person)

    # Fetch all person names in a single bulk query
    person_names = {}
    if person_ids:
        person_data = frappe.db.get_values(
            "Person",
            {"name": ["in", list(person_ids)]},
            ["name", "full_name"],
            as_dict=True
        )
        person_names = {p["name"]: p["full_name"] for p in person_data}

    # Get officers list
    officers = []
    for officer in doc.officers or []:
        officers.append({
            "person": officer.person,
            "person_name": person_names.get(officer.person),
            "title": officer.title,
            "start_date": str(officer.start_date) if officer.start_date else None,
            "end_date": str(officer.end_date) if officer.end_date else None
        })

    # Get members list
    members = []
    for member in doc.members_partners or []:
        members.append({
            "person": member.person,
            "person_name": person_names.get(member.person),
            "ownership_percent": member.ownership_percent,
            "capital_contribution": member.capital_contribution,
            "voting_rights": member.voting_rights
        })

    # CR-007 FIX: Match API contract structure
    return {
        "message": "success",
        "company": {
            "name": doc.name,
            "legal_name": doc.legal_name,
            "tax_id": doc.tax_id,
            "entity_type": doc.entity_type,
            "formation_date": str(doc.formation_date) if doc.formation_date else None,
            "jurisdiction_country": doc.jurisdiction_country,
            "jurisdiction_state": doc.jurisdiction_state,
            "registered_address": doc.registered_address,
            "physical_address": doc.physical_address,
            "registered_agent": doc.registered_agent
        },
        "org_details": {
            "name": org_data.name if org_data else None,
            "org_name": org_data.org_name if org_data else None,
            "org_type": org_data.org_type if org_data else None,
            "status": org_data.status if org_data else None
        },
        "officers": officers,
        "members": members
    }


@frappe.whitelist()
def get_user_companies(user: str = None) -> list[dict]:
    """
    Get all Companies accessible to a user.

    Args:
        user: User email (defaults to current user)

    Returns:
        list: List of Company records the user can access
    """
    if not user:
        user = frappe.session.user

    # System Manager can see all
    if "System Manager" in frappe.get_roles(user):
        companies = frappe.get_all(
            "Company",
            fields=["name", "legal_name", "entity_type", "organization"],
            order_by="creation desc"
        )
    else:
        # Get Organizations user has permission for
        permitted_orgs = frappe.get_all(
            "User Permission",
            filters={
                "user": user,
                "allow": "Organization"
            },
            pluck="for_value"
        )

        if not permitted_orgs:
            return []

        companies = frappe.get_all(
            "Company",
            filters={"organization": ["in", permitted_orgs]},
            fields=["name", "legal_name", "entity_type", "organization"],
            order_by="creation desc"
        )

    # Enrich with org_name
    for company in companies:
        company["org_name"] = frappe.db.get_value(
            "Organization", company["organization"], "org_name"
        )

    return companies


@frappe.whitelist()
def validate_ownership(company: str) -> dict:
    """
    Validate ownership percentages for a Company's members/partners.

    Args:
        company: The name of the Company document

    Returns:
        dict: Validation result with total percentage and any warnings
    """
    if not frappe.has_permission("Company", doc=company, ptype="read"):
        frappe.throw(_("Not permitted to access this Company"), frappe.PermissionError)

    doc = frappe.get_doc("Company", company)

    if not doc.members_partners:
        return {
            "valid": True,
            "total_ownership": 0,
            "total_voting_rights": 0,
            "member_count": 0,
            "warnings": []
        }

    total_ownership = sum(
        (mp.ownership_percent or 0) for mp in doc.members_partners
    )

    total_voting = sum(
        (mp.voting_rights or 0) for mp in doc.members_partners
    )

    warnings = []

    if total_ownership > 100:
        warnings.append(
            _("Total ownership percentage ({0}%) exceeds 100%").format(total_ownership)
        )

    if total_voting > 100:
        warnings.append(
            _("Total voting rights ({0}%) exceeds 100%").format(total_voting)
        )

    # CR-007 FIX: Use total_ownership instead of total_ownership_percent
    return {
        "valid": len(warnings) == 0,
        "total_ownership": total_ownership,
        "total_voting_rights": total_voting,
        "member_count": len(doc.members_partners),
        "warnings": warnings
    }
