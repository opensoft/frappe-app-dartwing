# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


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

    def validate(self):
        """Run all validations before save."""
        # P2-03 FIX: Removed validate_equipment_name - handled by reqd: 1 in JSON
        self.validate_serial_number_unique()
        self.validate_owner_organization_immutable()
        self.validate_assigned_person()
        self.validate_user_can_access_owner_organization()

    def after_insert(self):
        """Log initial assignment after equipment creation (P1-NEW-03)."""
        if self.assigned_to:
            self.add_comment(
                "Info",
                _("Equipment initially assigned to {0}").format(self.assigned_to)
            )

    def on_update(self):
        """Track assignment changes with audit logging (P2-06)."""
        self._log_assignment_change()

    def _log_assignment_change(self):
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

    def validate_owner_organization_immutable(self):
        """Prevent changing owner_organization after creation (P2-05).

        Equipment ownership is immutable - must be transferred via a formal
        transfer process if needed, not by changing the field directly.
        """
        if not self.is_new():
            doc_before = self.get_doc_before_save()
            if doc_before and doc_before.owner_organization != self.owner_organization:
                frappe.throw(
                    _("Cannot change Equipment ownership after creation. "
                      "Original organization: {0}. Use Equipment Transfer if ownership needs to change.").format(
                        doc_before.owner_organization
                    ),
                    title=_("Immutable Field"),
                )

    def validate_serial_number_unique(self):
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

    def validate_assigned_person(self):
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

    def validate_user_can_access_owner_organization(self):
        """Validate user has permission for the specific owner_organization (P1-05 FIX).

        Users must have User Permission for the specific Organization they are
        creating/modifying equipment for, not just any organization.
        """
        user = frappe.session.user

        # Administrator and System Manager can always access
        if user == "Administrator" or "System Manager" in frappe.get_roles(user):
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
def get_org_members(doctype, txt, searchfield, start, page_len, filters):
    """Get Person records who are active Org Members of specified organization.

    Used for populating the assigned_to field dropdown with only valid assignees.

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
    user = frappe.session.user
    if user != "Administrator" and "System Manager" not in frappe.get_roles(user):
        has_permission = frappe.db.exists(
            "User Permission",
            {"user": user, "allow": "Organization", "for_value": organization},
        )
        if not has_permission:
            frappe.throw(
                _("You do not have permission to access organization '{0}'").format(organization),
                frappe.PermissionError,
            )

    return frappe.db.sql(
        """
        SELECT p.name, CONCAT(p.first_name, ' ', IFNULL(p.last_name, '')) as description
        FROM `tabPerson` p
        INNER JOIN `tabOrg Member` om ON om.person = p.name
        WHERE om.organization = %s
          AND om.status = 'Active'
          AND (p.name LIKE %s OR p.first_name LIKE %s OR IFNULL(p.last_name, '') LIKE %s)
        ORDER BY p.first_name
        LIMIT %s, %s
        """,
        (organization, f"%{txt}%", f"%{txt}%", f"%{txt}%", start, page_len),
    )


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
    user = frappe.session.user
    if user != "Administrator" and "System Manager" not in frappe.get_roles(user):
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
    if user != "Administrator" and "System Manager" not in frappe.get_roles(user):
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


def check_equipment_on_org_deletion(doc, method):
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


def check_equipment_assignments_on_member_removal(doc, method):
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


def check_equipment_assignments_on_member_deactivation(doc, method):
    """Prevent Org Member deactivation if equipment is assigned to them (FR-013, P1-03 FIX).

    Called via doc_events hook when an Org Member is being updated.
    Throws an error if status changes away from 'Active' while person has equipment assigned.

    Args:
        doc: The Org Member document being updated
        method: The event method (on_update)
    """
    # Only check if status is changing away from Active
    if not doc.has_value_changed("status"):
        return

    doc_before = doc.get_doc_before_save()
    if not doc_before:
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
