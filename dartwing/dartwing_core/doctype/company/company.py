# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Company(Document):
	"""Company document for managing business entities."""

	def validate(self):
		"""Validate required fields and defaults."""
		if not self.company_name:
			frappe.throw(_("Company Name is required"))

		if not self.status:
			self.status = "Active"
