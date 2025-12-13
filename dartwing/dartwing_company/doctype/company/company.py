# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from dartwing.dartwing_core.mixins import OrganizationMixin


class Company(Document, OrganizationMixin):
    """
    Company DocType - represents a business entity.

    Inherits from OrganizationMixin to provide access to parent Organization
    properties (org_name, logo, org_status).

    Note: Audit logging is handled by Frappe's built-in track_changes feature
    (configured in company.json). No custom audit logging needed.
    """

    def validate(self):
        """Validate company before save."""
        self.validate_ownership_percentage()

    # CR-008 FIX: Removed after_insert, on_update, on_trash, and _log_audit_event
    # Frappe's track_changes: 1 in company.json handles audit logging via Version doctype

    def validate_ownership_percentage(self):
        """Warn if total ownership percentage exceeds 100%."""
        if not self.members_partners:
            return

        total_ownership = sum(
            (mp.ownership_percent or 0) for mp in self.members_partners
        )

        if total_ownership > 100:
            frappe.msgprint(
                _("Total ownership percentage ({0}%) exceeds 100%").format(
                    total_ownership
                ),
                indicator="orange",
                alert=True
            )
