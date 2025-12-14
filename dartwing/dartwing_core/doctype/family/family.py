# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document


class Family(Document):
	"""Family document for managing households and members."""

	def validate(self):
		"""Validate required fields and defaults."""
		if not self.family_name:
			frappe.throw(_("Family Name is required"))

		if not self.status:
			self.status = "Active"

		if not self.slug:
			self.slug = self._generate_unique_slug()

	def before_insert(self):
		"""Set created_date if missing."""
		if not self.created_date:
			self.created_date = frappe.utils.today()

	def _generate_unique_slug(self):
		"""Generate a unique slug from the family name."""
		base = frappe.utils.slug(self.family_name)
		if not base:
			frappe.throw(_("Unable to generate slug"))

		slug = base
		i = 1
		while frappe.db.exists("Family", {"slug": slug}):
			slug = f"{base}-{i}"
			i += 1
		return slug
