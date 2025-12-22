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

	def after_insert(self):
		"""Create Organization after Family is created (bidirectional linking)."""
		# Skip if already linked or if created from Organization hooks
		if self.organization or getattr(self.flags, "from_organization", False):
			return

		from dartwing.dartwing_core.doctype.organization.organization import create_organization_for_family
		org_name = create_organization_for_family(self)
		if org_name:
			self.db_set("organization", org_name, update_modified=False)

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
