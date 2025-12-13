# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class OrganizationMemberPartner(Document):
    """Child table for LLC members or partnership partners.

    CR-010 FIX: Added validation for percentage fields.
    """

    def validate(self):
        """Validate member/partner record."""
        self.validate_percentages()

    def validate_percentages(self):
        """Ensure percentages are within valid range (0-100)."""
        if self.ownership_percent is not None:
            if self.ownership_percent < 0:
                frappe.throw(
                    _("Ownership percentage cannot be negative"),
                    title=_("Invalid Percentage")
                )
            if self.ownership_percent > 100:
                frappe.throw(
                    _("Ownership percentage cannot exceed 100%"),
                    title=_("Invalid Percentage")
                )

        if self.voting_rights is not None:
            if self.voting_rights < 0:
                frappe.throw(
                    _("Voting rights percentage cannot be negative"),
                    title=_("Invalid Percentage")
                )
            if self.voting_rights > 100:
                frappe.throw(
                    _("Voting rights percentage cannot exceed 100%"),
                    title=_("Invalid Percentage")
                )
