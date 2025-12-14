# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import today


class OrgMember(Document):
    """
    Org Member DocType - Links Person to Organization with Role assignment.

    Handles membership relationships with:
    - Status tracking (Active/Inactive/Pending)
    - Role validation against organization type
    - Unique (Person, Organization) constraint
    - Last supervisor protection
    - Soft-cascade on Person deletion
    """

    def validate(self):
        """Run all validations before save."""
        self.validate_unique_membership()
        self.validate_role_for_org_type()
        self.validate_end_date()
        self.validate_not_last_supervisor()

    def before_insert(self):
        """Set defaults before first save."""
        if not self.start_date:
            self.start_date = today()
        if not self.status:
            self.status = "Active"

    def validate_unique_membership(self):
        """Ensure (Person, Organization) combination is unique (FR-002).

        Only one Org Member record allowed per (Person, Organization) pair,
        regardless of status. Rejoining is handled by reactivating existing record.
        """
        if not self.person or not self.organization:
            return

        filters = {
            "person": self.person,
            "organization": self.organization,
        }

        # Exclude current document when updating
        if not self.is_new():
            filters["name"] = ("!=", self.name)

        existing = frappe.db.exists("Org Member", filters)
        if existing:
            frappe.throw(
                _("Person is already a member of this organization"),
                title=_("Duplicate Membership"),
            )

    def validate_role_for_org_type(self):
        """Ensure assigned role is valid for the organization type (FR-003).

        Role Template's applies_to_org_type must match Organization's org_type.
        """
        if not self.role or not self.organization:
            return

        # Get organization type
        org_type = frappe.db.get_value("Organization", self.organization, "org_type")
        if not org_type:
            return

        # Get role's applies_to_org_type
        role_org_type = frappe.db.get_value(
            "Role Template", self.role, "applies_to_org_type"
        )

        if role_org_type and role_org_type != org_type:
            frappe.throw(
                _("Role '{0}' is not valid for {1} organizations").format(
                    self.role, org_type
                ),
                title=_("Invalid Role for Organization Type"),
            )

    def validate_end_date(self):
        """Ensure end_date >= start_date if provided (V-005)."""
        if self.end_date and self.start_date:
            if self.end_date < self.start_date:
                frappe.throw(
                    _("End date cannot be before start date"),
                    title=_("Invalid Date Range"),
                )

    def _is_status_becoming_inactive(self, db_doc):
        """Check if the member's status is changing to Inactive.

        Args:
            db_doc: The database document (None for new records)

        Returns:
            bool: True if status is becoming Inactive
        """
        return (
            self.status == "Inactive"
            and not self.is_new()
            and db_doc
            and db_doc.status != "Inactive"
        )

    def validate_not_last_supervisor(self):
        """Prevent deactivation of last supervisor (FR-015).

        When changing status to Inactive or changing from a supervisor role
        to a non-supervisor role, check if this would leave the organization
        without any supervisors.

        This check can be bypassed by setting flags.ignore_last_supervisor_check = True,
        which is used during Person deletion to allow soft-cascade cleanup.
        """
        # Allow bypass via specific flag (used by handle_person_deletion)
        if self.flags.get("ignore_last_supervisor_check"):
            return

        if not self.organization:
            return

        # Only check if member is being deactivated or role is changing
        db_doc = None
        if not self.is_new():
            db_doc = frappe.db.get_value(
                "Org Member",
                self.name,
                ["status", "role"],
                as_dict=True,
            )

        # Check if status is changing to Inactive (only for existing records)
        status_becoming_inactive = self._is_status_becoming_inactive(db_doc)

        # Check if role is changing from supervisor to non-supervisor
        role_losing_supervisor = False
        if db_doc and db_doc.role != self.role:
            old_is_supervisor = (
                frappe.db.get_value("Role Template", db_doc.role, "is_supervisor") or 0
            )
            new_is_supervisor = (
                frappe.db.get_value("Role Template", self.role, "is_supervisor") or 0
            )
            role_losing_supervisor = old_is_supervisor and not new_is_supervisor

        # If neither case applies, no need to check
        if not status_becoming_inactive and not role_losing_supervisor:
            return

        # Check if this member's current role is a supervisor role
        # For status change to Inactive or role change, always use db_doc.role (old role)
        current_role = db_doc.role if db_doc else self.role
        current_is_supervisor = (
            frappe.db.get_value("Role Template", current_role, "is_supervisor") or 0
        )
        if not current_is_supervisor:
            return

        # Count other active supervisors in the organization
        result = check_last_supervisor(self.organization, exclude_member=self.name)

        if result["is_last_supervisor"]:
            if status_becoming_inactive:
                frappe.throw(
                    _("Cannot deactivate: at least one supervisor must remain in the organization"),
                    title=_("Last Supervisor"),
                )
            elif role_losing_supervisor:
                frappe.throw(
                    _("Cannot change role: at least one supervisor must remain in the organization"),
                    title=_("Last Supervisor"),
                )


@frappe.whitelist()
def add_member_to_organization(
    person: str,
    organization: str,
    role: str,
    status: str = "Active",
    start_date: str | None = None,
) -> dict:
    """Add a new member or reactivate an existing inactive membership.

    Args:
        person: Person document name
        organization: Organization document name
        role: Role Template name
        status: Initial status (default: Active)
        start_date: Start date YYYY-MM-DD (default: today)

    Returns:
        dict with name, action (created/reactivated), and member details
    """
    # Check if membership already exists
    existing = frappe.db.get_value(
        "Org Member",
        {"person": person, "organization": organization},
        ["name", "status"],
        as_dict=True,
    )

    if existing:
        if existing.status == "Active":
            frappe.throw(
                _("Person is already an active member of this organization"),
                title=_("Duplicate Membership"),
            )

        # Reactivate existing inactive/pending membership
        doc = frappe.get_doc("Org Member", existing.name)
        previous_status = doc.status
        doc.status = status
        doc.role = role
        doc.start_date = start_date or today()
        doc.end_date = None  # Clear end_date on reactivation
        doc.save()

        return {
            "name": doc.name,
            "action": "reactivated",
            "person": doc.person,
            "organization": doc.organization,
            "role": doc.role,
            "status": doc.status,
            "start_date": str(doc.start_date),
            "previous_status": previous_status,
        }

    # Create new membership
    doc = frappe.get_doc(
        {
            "doctype": "Org Member",
            "person": person,
            "organization": organization,
            "role": role,
            "status": status,
            "start_date": start_date or today(),
        }
    )
    doc.insert()

    return {
        "name": doc.name,
        "action": "created",
        "person": doc.person,
        "organization": doc.organization,
        "role": doc.role,
        "status": doc.status,
        "start_date": str(doc.start_date),
    }


@frappe.whitelist()
def get_members_for_organization(
    organization: str,
    status: str | None = None,
    include_inactive: bool = False,
) -> list[dict]:
    """Get all members of an organization with optional filtering.

    Args:
        organization: Organization document name
        status: Filter by specific status (Active/Inactive/Pending)
        include_inactive: If True, include inactive members (default: False)

    Returns:
        List of member records with role supervisor flag
    """
    filters = {"organization": organization}

    if status:
        filters["status"] = status
    elif not include_inactive:
        filters["status"] = ("!=", "Inactive")

    members = frappe.get_all(
        "Org Member",
        filters=filters,
        fields=[
            "name",
            "person",
            "member_name",
            "role",
            "status",
            "start_date",
            "end_date",
        ],
        order_by="start_date desc",
    )

    # Add is_supervisor flag from Role Template
    for member in members:
        member["is_supervisor"] = (
            frappe.db.get_value("Role Template", member["role"], "is_supervisor") or 0
        )

    return members


@frappe.whitelist()
def get_organizations_for_person(
    person: str,
    status: str = "Active",
) -> list[dict]:
    """Get all organizations a person belongs to (FR-014).

    Args:
        person: Person document name
        status: Filter by membership status (default: Active)

    Returns:
        List of membership records with organization details
    """
    filters = {"person": person}

    if status:
        filters["status"] = status

    memberships = frappe.get_all(
        "Org Member",
        filters=filters,
        fields=[
            "name",
            "organization",
            "organization_name",
            "organization_type",
            "role",
            "status",
            "start_date",
            "end_date",
        ],
        order_by="start_date desc",
    )

    # Add is_supervisor flag from Role Template
    for membership in memberships:
        membership["is_supervisor"] = (
            frappe.db.get_value("Role Template", membership["role"], "is_supervisor")
            or 0
        )

    return memberships


@frappe.whitelist()
def deactivate_member(
    member: str,
    end_date: str | None = None,
) -> dict:
    """Deactivate a member (set status to Inactive).

    Args:
        member: Org Member document name
        end_date: End date YYYY-MM-DD (default: today)

    Returns:
        dict with name, status, and end_date
    """
    doc = frappe.get_doc("Org Member", member)

    if doc.status == "Inactive":
        frappe.throw(
            _("Member is already inactive"),
            title=_("Invalid Status Change"),
        )

    doc.status = "Inactive"
    doc.end_date = end_date or today()
    doc.save()

    return {
        "name": doc.name,
        "status": doc.status,
        "end_date": str(doc.end_date),
    }


@frappe.whitelist()
def change_member_role(
    member: str,
    new_role: str,
) -> dict:
    """Change a member's assigned role (FR-008).

    Args:
        member: Org Member document name
        new_role: New Role Template name

    Returns:
        dict with name, previous_role, and new role
    """
    doc = frappe.get_doc("Org Member", member)
    previous_role = doc.role

    if previous_role == new_role:
        frappe.throw(
            _("Member already has this role"),
            title=_("No Change"),
        )

    doc.role = new_role
    doc.save()  # This will trigger validate_role_for_org_type

    return {
        "name": doc.name,
        "previous_role": previous_role,
        "role": doc.role,
    }


def check_last_supervisor(organization: str, exclude_member: str | None = None) -> dict:
    """Check if there are any supervisors left in an organization (T019).

    Args:
        organization: Organization document name
        exclude_member: Org Member name to exclude from count (for checking before change)

    Returns:
        dict with is_last_supervisor and supervisor_count
    """
    # Get all active members with supervisor roles
    members = frappe.get_all(
        "Org Member",
        filters={
            "organization": organization,
            "status": "Active",
        },
        fields=["name", "role"],
    )

    # Count supervisors
    supervisor_count = 0
    for member in members:
        if exclude_member and member.name == exclude_member:
            continue
        is_supervisor = (
            frappe.db.get_value("Role Template", member.role, "is_supervisor") or 0
        )
        if is_supervisor:
            supervisor_count += 1

    return {
        "is_last_supervisor": supervisor_count == 0,
        "supervisor_count": supervisor_count,
    }


@frappe.whitelist()
def check_is_last_supervisor(member: str) -> dict:
    """Check if a member is the last supervisor in their organization (T021).

    Args:
        member (str): Org Member document name to check.

    Returns:
        dict: A dictionary with the following keys:
            - is_last_supervisor (bool): True if the member is the last supervisor in their organization.
            - supervisor_count (int | None): Number of active supervisors in the organization (including this member), or None if the member's role is not a supervisor role.
            - member_role_is_supervisor (bool): True if the member's role is a supervisor role.
    """
    doc = frappe.get_doc("Org Member", member)

    # Check if member's role is a supervisor role
    member_role_is_supervisor = (
        frappe.db.get_value("Role Template", doc.role, "is_supervisor") or 0
    )

    # Get supervisor count for the organization
    # For supervisors, exclude self to check if they're the last one
    # For non-supervisors, get the full count
    exclude = doc.name if member_role_is_supervisor else None
    result = check_last_supervisor(doc.organization, exclude_member=exclude)

    # Calculate total supervisor count
    supervisor_count = result["supervisor_count"]
    if member_role_is_supervisor:
        supervisor_count += 1  # Include current member

    return {
        "is_last_supervisor": bool(member_role_is_supervisor) and result["is_last_supervisor"],
        "supervisor_count": supervisor_count,
        "member_role_is_supervisor": bool(member_role_is_supervisor),
    }


def handle_person_deletion(doc, method):
    """Handle Person deletion by soft-cascading Org Member records (FR-010).

    Called via doc_events hook when a Person is deleted.
    Sets all associated Org Member records to status "Inactive" with end_date.

    Args:
        doc: The Person document being deleted
        method: The event method (on_trash)
    """
    # Get all Org Member records for this person
    members = frappe.get_all(
        "Org Member",
        filters={"person": doc.name},
        fields=["name", "status"],
    )

    for member_data in members:
        if member_data.status != "Inactive":
            member = frappe.get_doc("Org Member", member_data.name)
            member.status = "Inactive"
            member.end_date = today()
            # Skip only the last-supervisor check to allow soft-cascade cleanup
            # Other validations (unique membership, role, date range) remain active
            member.flags.ignore_last_supervisor_check = True
            member.save()
