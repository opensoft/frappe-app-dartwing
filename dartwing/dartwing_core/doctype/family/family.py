# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.model.document import Document
from dartwing.dartwing_core.doctype.family_member.family_member import (
	calculate_age,
	get_age_category,
)


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

		self._sync_member_fields()

	def _sync_member_fields(self):
		"""Update computed fields for family members."""
		for member in self.members or []:
			if hasattr(member, "calculate_age_fields"):
				member.calculate_age_fields()
			else:
				self._set_member_age_fields(member)

			if hasattr(member, "auto_split_name"):
				member.auto_split_name()
			else:
				self._set_member_name_fields(member)

	def _set_member_age_fields(self, member):
		if not member.date_of_birth:
			member.age = None
			member.age_category = None
			member.is_minor = 0
			member.is_coppa_protected = 0
			return

		age = calculate_age(member.date_of_birth)
		member.age = age
		member.age_category = get_age_category(age)
		member.is_minor = 1 if age is not None and age < 18 else 0
		member.is_coppa_protected = 1 if age is not None and age < 13 else 0

	def _set_member_name_fields(self, member):
		if member.full_name and not (member.first_name or member.last_name):
			parts = member.full_name.strip().split(" ", 1)
			member.first_name = parts[0]
			if len(parts) > 1:
				member.last_name = parts[1]

	def before_insert(self):
		"""Set created_date if missing."""
		if not self.created_date:
			self.created_date = frappe.utils.today()

	def after_insert(self):
		"""Create Organization if this Family doesn't have one."""
		# Skip if this was created by Organization (to prevent recursion)
		if getattr(self.flags, "from_organization", False):
			return

		if not self.organization:
			self._create_organization()

	def _create_organization(self):
		"""Create a linked Organization for this Family."""
		try:
			org = frappe.new_doc("Organization")
			org.org_name = self.family_name
			org.org_type = "Family"
			org.status = self.status or "Active"
			org.linked_doctype = "Family"
			org.linked_name = self.name
			org.flags.ignore_permissions = True
			org.flags.skip_concrete_type = True  # Don't create another Family
			org.insert()

			# Update this Family with the organization link
			self.db_set("organization", org.name, update_modified=False)

			frappe.msgprint(
				_("Created Organization: {0}").format(org.name),
				alert=True
			)
		except Exception as e:
			frappe.log_error(f"Error creating Organization for Family {self.name}: {str(e)}")

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
