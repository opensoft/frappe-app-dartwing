# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Nonprofit(Document):
	"""Nonprofit document for managing charitable organizations."""

	def validate(self):
		"""Validate required fields and defaults."""
		if not self.nonprofit_name:
			frappe.throw(_("Nonprofit Name is required"))

		if not self.status:
			self.status = "Active"
