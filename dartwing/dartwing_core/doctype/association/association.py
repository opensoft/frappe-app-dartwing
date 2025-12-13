# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Association(Document):
	"""Association document for managing member organizations."""

	def validate(self):
		"""Validate required fields and defaults."""
		if not self.association_name:
			frappe.throw(_("Association Name is required"))

		if not self.status:
			self.status = "Active"
