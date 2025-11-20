# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import json
import frappe
from frappe import _


# Helpers

def _coerce_child_table(value):
	if value is None:
		return []
	if isinstance(value, str):
		value = json.loads(value)
	if not isinstance(value, (list, tuple)):
		frappe.throw(_("Members must be a list"))
	return value


def _get_family_doc(name):
	if not name:
		frappe.throw(_("Family name is required"))
	if not frappe.db.exists("Family", name):
		frappe.throw(_("Family '{0}' not found").format(name))
	return frappe.get_doc("Family", name)


# Families

@frappe.whitelist()
def create_family(family_name, description=None, status="Active", members=None):
	"""Create a new Family."""
	if not family_name:
		frappe.throw(_("Family Name is required"))

	if frappe.db.exists("Family", family_name):
		frappe.throw(_("Family '{0}' already exists").format(family_name))

	member_rows = _coerce_child_table(members)

	try:
		family = frappe.get_doc({
			"doctype": "Family",
			"family_name": family_name,
			"description": description,
			"status": status,
			"members": member_rows,
		})
		family.insert()
		frappe.db.commit()

		return {"success": True, "message": _("Family created successfully"), "data": family.as_dict()}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error creating family: {str(e)}")
		frappe.throw(_("Failed to create family: {0}").format(str(e)))


@frappe.whitelist()
def get_family(name):
	"""Get a Family by name."""
	try:
		family = _get_family_doc(name)
		return {"success": True, "data": family.as_dict()}
	except Exception as e:
		frappe.log_error(f"Error getting family: {str(e)}")
		frappe.throw(_("Failed to get family: {0}").format(str(e)))


@frappe.whitelist()
def get_all_families(filters=None, fields=None, limit_start=0, limit_page_length=20):
	"""Get Families with optional filters."""
	try:
		if isinstance(filters, str):
			filters = json.loads(filters)

		if isinstance(fields, str):
			fields = json.loads(fields)

		families = frappe.get_all(
			"Family",
			filters=filters or {},
			fields=fields or ["name", "family_name", "status", "created_date"],
			limit_start=int(limit_start),
			limit_page_length=int(limit_page_length),
			order_by="created_date desc",
		)

		return {"success": True, "count": len(families), "data": families}
	except Exception as e:
		frappe.log_error(f"Error getting families: {str(e)}")
		frappe.throw(_("Failed to get families: {0}").format(str(e)))


@frappe.whitelist()
def update_family(name, **kwargs):
	"""Update a Family."""
	family = _get_family_doc(name)
	try:
		allowed_fields = {"family_name", "description", "status"}
		member_rows = None
		if "members" in kwargs:
			member_rows = _coerce_child_table(kwargs.pop("members"))

		for field, value in kwargs.items():
			if field in allowed_fields:
				setattr(family, field, value)

		if member_rows is not None:
			family.members = member_rows

		family.save()
		frappe.db.commit()

		return {"success": True, "message": _("Family updated successfully"), "data": family.as_dict()}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error updating family: {str(e)}")
		frappe.throw(_("Failed to update family: {0}").format(str(e)))


@frappe.whitelist()
def delete_family(name):
	"""Delete a Family."""
	_get_family_doc(name)  # validates existence
	try:
		frappe.delete_doc("Family", name)
		frappe.db.commit()
		return {"success": True, "message": _("Family deleted successfully")}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error deleting family: {str(e)}")
		frappe.throw(_("Failed to delete family: {0}").format(str(e)))


@frappe.whitelist()
def search_families(query, limit=20):
	"""Search for Families by name or description."""
	if not query:
		frappe.throw(_("Search query is required"))

	try:
		families = frappe.get_all(
			"Family",
			filters=[["family_name", "like", f"%{query}%"]],
			or_filters=[["description", "like", f"%{query}%"]],
			fields=["name", "family_name", "status", "description"],
			limit=int(limit),
		)

		return {"success": True, "count": len(families), "data": families}
	except Exception as e:
		frappe.log_error(f"Error searching families: {str(e)}")
		frappe.throw(_("Failed to search families: {0}").format(str(e)))


@frappe.whitelist()
def get_family_stats():
	"""Get simple statistics about Families."""
	try:
		total = frappe.db.count("Family")
		active = frappe.db.count("Family", {"status": "Active"})
		inactive = frappe.db.count("Family", {"status": "Inactive"})
		archived = frappe.db.count("Family", {"status": "Archived"})

		return {
			"success": True,
			"data": {
				"total": total,
				"by_status": {
					"active": active,
					"inactive": inactive,
					"archived": archived,
				},
			},
		}
	except Exception as e:
		frappe.log_error(f"Error getting family stats: {str(e)}")
		frappe.throw(_("Failed to get family statistics: {0}").format(str(e)))


# Members

@frappe.whitelist()
def add_family_member(family, full_name, relationship=None, email=None, phone=None, date_of_birth=None, status="Active", notes=None):
	"""Add a member to a family."""
	doc = _get_family_doc(family)
	if not full_name:
		frappe.throw(_("Member full name is required"))

	try:
		row = doc.append("members", {
			"full_name": full_name,
			"relationship": relationship,
			"email": email,
			"phone": phone,
			"date_of_birth": date_of_birth,
			"status": status,
			"notes": notes,
		})
		doc.save()
		frappe.db.commit()
		return {"success": True, "message": _("Member added"), "data": row.as_dict()}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error adding member: {str(e)}")
		frappe.throw(_("Failed to add member: {0}").format(str(e)))


@frappe.whitelist()
def update_family_member(family, member_name, **kwargs):
	"""Update a family member row by child name."""
	doc = _get_family_doc(family)
	if not member_name:
		frappe.throw(_("Member name is required"))

	allowed = {"full_name", "relationship", "email", "phone", "date_of_birth", "status", "notes"}
	try:
		target = next((m for m in doc.members or [] if m.name == member_name), None)
		if not target:
			frappe.throw(_("Member not found"))
		for field, value in kwargs.items():
			if field in allowed:
				setattr(target, field, value)
		doc.save()
		frappe.db.commit()
		return {"success": True, "message": _("Member updated"), "data": target.as_dict()}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error updating member: {str(e)}")
		frappe.throw(_("Failed to update member: {0}").format(str(e)))


@frappe.whitelist()
def delete_family_member(family, member_name):
	"""Delete a member from a family."""
	doc = _get_family_doc(family)
	if not member_name:
		frappe.throw(_("Member name is required"))

	try:
		doc.members = [m for m in (doc.members or []) if m.name != member_name]
		doc.save()
		frappe.db.commit()
		return {"success": True, "message": _("Member deleted")}
	except Exception as e:
		frappe.db.rollback()
		frappe.log_error(f"Error deleting member: {str(e)}")
		frappe.throw(_("Failed to delete member: {0}").format(str(e)))
