# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from dartwing.dartwing_core.mixins import OrganizationMixin


class Family(Document, OrganizationMixin):
	"""
	Family DocType - represents a household unit.

	Inherits from OrganizationMixin to provide access to parent Organization
	properties (org_name, logo, org_status) and methods (get_organization_doc,
	update_org_name).
	"""

	def validate(self):
		"""Validate required fields and generate slug if needed."""
		if not self.family_name:
			frappe.throw(_("Family Name is required"))

		# Note: status default is set in Family.json ("default": "Active")
		# per Metadata-as-Data principle - no code default needed

		if not self.slug:
			self.slug = self._generate_unique_slug()

	def before_insert(self):
		"""Set created_date if missing."""
		if not self.created_date:
			self.created_date = frappe.utils.today()

	def _generate_unique_slug(self) -> str:
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
