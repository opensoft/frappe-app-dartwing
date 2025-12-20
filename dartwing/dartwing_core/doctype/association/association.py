# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document

from dartwing.dartwing_core.mixins import OrganizationMixin


class Association(Document, OrganizationMixin):
	"""
	Association DocType - represents member-based organizations (HOAs, clubs, etc.).

	Inherits from OrganizationMixin to provide access to parent Organization
	properties (org_name, logo, org_status) and methods (get_organization_doc,
	update_org_name).
	"""

	def validate(self):
		"""Validate required fields."""
		if not self.association_name:
			frappe.throw(_("Association Name is required"))

		# Note: status default is set in Association.json ("default": "Active")
		# per Metadata-as-Data principle - no code default needed
