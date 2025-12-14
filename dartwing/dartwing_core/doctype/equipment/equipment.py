# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

from __future__ import annotations

import frappe
from frappe import _
from frappe.model.document import Document

from dartwing.permissions.helpers import is_privileged_user


def _escape_sql_wildcards(text: str) -> str:
    """Escape SQL LIKE wildcards in search text (P3-03).

    Prevents % and _ characters from being interpreted as wildcards,
    which could cause unexpected search results.

    Args:
        text: Search text that may contain wildcard characters

    Returns:
        Text with wildcards escaped for literal matching
    """
    return text.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")


class Equipment(Document):
    """Equipment DocType - Tracks physical assets owned by organizations.

    Handles asset management with:
    - Organization ownership (polymorphic via Organization link)
    - Person assignment (validated against Org Member)
    - Serial number uniqueness (global)
    - Status tracking (Active, In Repair, Retired, Lost, Stolen)
    - Location tracking via Address link
    - Document attachments via child table
    - Maintenance scheduling via child table
    """

    def validate(self) -> None:
        """Run all validations before save."""
        # P2-03 FIX: Removed validate_equipment_name - handled by reqd: 1 in JSON
        self.validate_serial_number_unique()
        self.validate_owner_organization_immutable()
        self.validate_assigned_person()
        self.validate_user_can_access_owner_organization()

    def after_insert(self) -> None:
        """Log initial assignment after equipment creation (P1-NEW-03)."""
        if self.assigned_to:
            self.add_comment(
                "Info",
                _("Equipment initially assigned to {0}").format(self.assigned_to)
            )

    def on_update(self) -> None:
        """Track assignment changes with audit logging (P2-06)."""
        self._log_assignment_change()

    def _log_assignment_change(self) -> None:
        """Add comment when equipment assignment changes (P2-06)."""
        # For existing documents, log changes (P2-NEW-04: fetch doc_before once)
        doc_before = self.get_doc_before_save()
        if not doc_before:
            return

        old_assignee = doc_before.assigned_to
        new_assignee = self.assigned_to

        if old_assignee != new_assignee:
            old_name = old_assignee or "Unassigned"
            new_name = new_assignee or "Unassigned"
            self.add_comment(
                "Info",
                _("Equipment assignment changed from {0} to {1}").format(
                    old_name, new_name
                )
            )

    def validate_owner_organization_immutable(self) -> None:
        """Prevent changing owner_organization after creation (P2-05).

        Equipment ownership is immutable - must be transferred via a formal
        transfer process if needed, not by changing the field directly.
        """
        if not self.is_new():
            doc_before = self.get_doc_before_save()
            if doc_before and doc_before.owner_organization != self.owner_organization:
                frappe.throw(
                    _("Cannot change Equipment ownership after creation. "
                      "Original organization: {0}. Contact an administrator if ownership transfer is required.").format(
                        doc_before.owner_organization
                    ),
                    title=_("Immutable Field"),
                )

    def validate_serial_number_unique(self) -> None:
        """Validate serial number uniqueness with user-friendly message (FR-002).

        The database unique constraint handles enforcement, but this provides
        a clearer error message before hitting the database.
        """
        if not self.serial_number:
            return

        filters = {"serial_number": self.serial_number}

        # Exclude current document when updating
        if not self.is_new():
            filters["name"] = ("!=", self.name)

        existing = frappe.db.exists("Equipment", filters)
        if existing:
            frappe.throw(
                _("Serial number '{0}' is already in use by another equipment record").format(
                    self.serial_number
                ),
                title=_("Duplicate Serial Number"),
            )

    def validate_assigned_person(self) -> None:
        """Validate assigned_to is an active Org Member of owner_organization (FR-010).

        Ensures equipment can only be assigned to persons who are active members
        of the same organization that owns the equipment.

        Also validates equipment status allows assignment (P1-NEW-04).
        """
        # P1-NEW-04: Block assignment for non-active equipment statuses
        non_assignable_statuses = ("Lost", "Stolen", "Retired")
        if self.assigned_to and self.status in non_assignable_statuses:
            frappe.throw(
                _("Cannot assign equipment with status '{0}'. "
                  "Clear the assignment or change status to 'Active' or 'In Repair'.").format(
                    self.status
                ),
                title=_("Invalid Status for Assignment"),
            )

        if not self.assigned_to:
            return

        if not self.owner_organization:
            frappe.throw(
                _("Cannot assign equipment without an owner organization"),
                title=_("Missing Organization"),
            )

        is_member = frappe.db.exists(
            "Org Member",
            {
                "organization": self.owner_organization,
                "person": self.assigned_to,
                "status": "Active",
            },
        )

        if not is_member:
            frappe.throw(
                _("Assigned person '{0}' must be an active member of organization '{1}'").format(
                    self.assigned_to, self.owner_organization
                ),
                title=_("Invalid Assignment"),
            )

    def validate_user_can_access_owner_organization(self) -> None:
        """Validate user has permission for the specific owner_organization (P1-05 FIX).

        Users must have User Permission for the specific Organization they are
        creating/modifying equipment for, not just any organization.
        """
        user = frappe.session.user

        # P2-NEW-06: Use centralized helper for privileged user check
        if is_privileged_user(user):
            return

        if not self.owner_organization:
            return

        # Check if user has permission for this specific organization
        has_org_permission = frappe.db.exists(
            "User Permission",
            {
                "user": user,
                "allow": "Organization",
                "for_value": self.owner_organization,
            },
        )

        if not has_org_permission:
            frappe.throw(
                _("You do not have permission to manage equipment for organization '{0}'").format(
                    self.owner_organization
                ),
                title=_("Permission Denied"),
                exc=frappe.PermissionError,
            )


@frappe.whitelist()
def get_org_members(
    doctype: str,
    txt: str,
    searchfield: str,
    start: int,
    page_len: int,
    filters: dict,
) -> list[tuple[str, str]]:
    """Get Person records who are active Org Members of specified organization.

    Used for populating the assigned_to field dropdown with only valid assignees.
    P2-NEW-07: Refactored to use Frappe ORM for better maintainability.

    Args:
        doctype: The doctype being searched (Person)
        txt: Search text
        searchfield: Field to search
        start: Pagination start
        page_len: Page length
        filters: Must contain 'organization' key

    Returns:
        List of tuples (name, description) for matching persons

    Raises:
        frappe.PermissionError: If user lacks access to the organization (P1-02 FIX)
    """
    organization = filters.get("organization")
    if not organization:
        return []

    # P1-02 FIX: Verify user has access to this organization
    # P2-NEW-06: Use centralized helper for privileged user check
    user = frappe.session.user
    if not is_privileged_user(user):
        has_permission = frappe.db.exists(
            "User Permission",
            {"user": user, "allow": "Organization", "for_value": organization},
        )
        if not has_permission:
            frappe.throw(
                _("You do not have permission to access organization '{0}'").format(organization),
                frappe.PermissionError,
            )

    # P2-NEW-07: Use ORM instead of raw SQL for better maintainability
    # Step 1: Get active Org Members for this organization
    active_members = frappe.get_all(
        "Org Member",
        filters={"organization": organization, "status": "Active"},
        pluck="person",
    )

    if not active_members:
        return []

    # Step 2: Build Person filters with search text
    person_filters = {"name": ["in", active_members]}

    # Add search text filter if provided
    if txt:
        person_filters["name"] = ["in", active_members]
        # P3-03: Escape SQL wildcards to prevent unexpected search behavior
        escaped_txt = _escape_sql_wildcards(txt)
        # Use OR filter for search across multiple fields
        or_filters = [
            ["name", "like", f"%{escaped_txt}%"],
            ["first_name", "like", f"%{escaped_txt}%"],
            ["last_name", "like", f"%{escaped_txt}%"],
        ]
    else:
        or_filters = None

    # Step 3: Get matching persons
    persons = frappe.get_all(
        "Person",
        filters=person_filters,
        or_filters=or_filters,
        fields=["name", "first_name", "last_name"],
        order_by="first_name",
        start=int(start),
        page_length=int(page_len),
    )

    # Step 4: Format as tuples (name, description) for link field query
    return [
        (p.name, f"{p.first_name} {p.last_name or ''}".strip())
        for p in persons
    ]


@frappe.whitelist()
def get_equipment_by_organization(organization: str, status: str | None = None) -> list:
    """Get all equipment for a specific organization.

    Args:
        organization: Organization document name
        status: Optional filter by status (Active, In Repair, Retired, Lost, Stolen)

    Returns:
        List of equipment records with summary info

    Raises:
        frappe.PermissionError: If user lacks access to the organization (P1-02 FIX)
    """
    # P1-02 FIX: Verify user has access to this organization
    # P2-NEW-06: Use centralized helper for privileged user check
    user = frappe.session.user
    if not is_privileged_user(user):
        has_permission = frappe.db.exists(
            "User Permission",
            {"user": user, "allow": "Organization", "for_value": organization},
        )
        if not has_permission:
            frappe.throw(
                _("You do not have permission to view equipment for organization '{0}'").format(
                    organization
                ),
                frappe.PermissionError,
            )

    filters = {"owner_organization": organization}
    if status:
        filters["status"] = status

    # P1-NEW-01: Use get_list to apply permission hooks
    return frappe.get_list(
        "Equipment",
        filters=filters,
        fields=[
            "name",
            "equipment_name",
            "equipment_type",
            "serial_number",
            "status",
            "assigned_to",
            "current_location",
        ],
        order_by="equipment_name",
    )


@frappe.whitelist()
def get_equipment_by_person(person: str) -> list:
    """Get all equipment currently assigned to a specific person.

    Args:
        person: Person document name

    Returns:
        List of equipment records assigned to the person (filtered by user's org access)

    Raises:
        frappe.PermissionError: If user lacks access to the person (P1-02 FIX)
    """
    user = frappe.session.user

    # P1-02 FIX: Verify user has access to view this person's data
    # P2-NEW-06: Use centralized helper for privileged user check
    if not is_privileged_user(user):
        if not frappe.has_permission("Person", "read", person):
            frappe.throw(
                _("You do not have permission to view equipment for this person"),
                frappe.PermissionError,
            )

        # P1-NEW-01: Filter equipment to only orgs the user can access
        # This prevents cross-org leakage when a Person belongs to multiple orgs
        user_orgs = frappe.get_all(
            "User Permission",
            filters={"user": user, "allow": "Organization"},
            pluck="for_value",
        )

        if not user_orgs:
            return []

        filters = {"assigned_to": person, "owner_organization": ["in", user_orgs]}
    else:
        # Admin/System Manager: return all equipment for this person
        filters = {"assigned_to": person}

    # P1-NEW-01: Use get_list to apply permission hooks
    return frappe.get_list(
        "Equipment",
        filters=filters,
        fields=[
            "name",
            "equipment_name",
            "equipment_type",
            "serial_number",
            "status",
            "owner_organization",
            "current_location",
        ],
        order_by="equipment_name",
    )


def check_equipment_on_org_deletion(doc: "Document", method: str) -> None:
    """Prevent Organization deletion if equipment exists (FR-012).

    Called via doc_events hook when an Organization is being deleted.
    Throws an error if any equipment is linked to this organization.

    Args:
        doc: The Organization document being deleted
        method: The event method (on_trash)
    """
    equipment_count = frappe.db.count("Equipment", {"owner_organization": doc.name})
    if equipment_count > 0:
        frappe.throw(
            _("Cannot delete Organization with {0} equipment item(s). "
              "Transfer or delete equipment first.").format(equipment_count),
            title=_("Equipment Exists"),
        )


def check_equipment_assignments_on_member_removal(doc: "Document", method: str) -> None:
    """Prevent Org Member removal if equipment is assigned to them (FR-013).

    Called via doc_events hook when an Org Member is being deleted.
    Throws an error if the person has equipment assigned in this organization.

    Args:
        doc: The Org Member document being deleted
        method: The event method (on_trash)
    """
    equipment_count = frappe.db.count(
        "Equipment",
        {
            "owner_organization": doc.organization,
            "assigned_to": doc.person,
        },
    )
    if equipment_count > 0:
        frappe.throw(
            _("Cannot remove Org Member with {0} assigned equipment item(s). "
              "Reassign equipment first.").format(equipment_count),
            title=_("Equipment Assigned"),
        )


def check_equipment_assignments_on_member_deactivation(doc: "Document", method: str) -> None:
    """Prevent Org Member deactivation if equipment is assigned to them (FR-013, P1-03 FIX).

    Called via doc_events hook when an Org Member is being updated.
    Throws an error if status changes away from 'Active' while person has equipment assigned.

    Args:
        doc: The Org Member document being updated
        method: The event method (on_update)
    """
    # P2-NEW-04/05 FIX: Fetch doc_before once with error handling instead of using has_value_changed()
    try:
        doc_before = doc.get_doc_before_save()
    except Exception as e:
        frappe.log_error(f"Failed to get doc_before_save for Org Member {doc.name}: {e}")
        return

    if not doc_before:
        return

    # Only check if status is changing away from Active
    if doc_before.status == doc.status:
        return

    # If changing from Active to something else
    if doc_before.status == "Active" and doc.status != "Active":
        equipment_count = frappe.db.count(
            "Equipment",
            {
                "owner_organization": doc.organization,
                "assigned_to": doc.person,
            },
        )
        if equipment_count > 0:
            frappe.throw(
                _("Cannot deactivate Org Member with {0} assigned equipment item(s). "
                  "Reassign equipment first.").format(equipment_count),
                title=_("Equipment Assigned"),
            )
