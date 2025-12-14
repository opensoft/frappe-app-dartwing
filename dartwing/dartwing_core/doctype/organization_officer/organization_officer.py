# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class OrganizationOfficer(Document):
    def validate(self):
        """Validate officer record."""
        self.validate_dates()

    def validate_dates(self):
        """Ensure end_date is >= start_date if both are provided."""
        if self.start_date and self.end_date:
            if self.end_date < self.start_date:
                frappe.throw(
                    _("End Date cannot be before Start Date"),
                    title=_("Invalid Date Range")
                )
