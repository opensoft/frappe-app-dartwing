# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

"""
Utility functions for the Dartwing Company module.
"""

import frappe
from frappe import _


def check_address_company_links(doc, method):
    """
    Prevent deletion of Address linked to Company.

    CR-011 FIX: Called via doc_events hook *before* Address is deleted, to allow blocking deletion.
    Checks if the Address is linked as registered_address or physical_address
    on any Company record.

    Args:
        doc: The Address document being deleted
        method: The event method (on_trash)

    Raises:
        frappe.LinkExistsError: If Address is linked to a Company
    """
    # Only check if Company doctype exists
    if not frappe.db.exists("DocType", "Company"):
        return

    # Check registered_address links
    registered_links = frappe.get_all(
        "Company",
        filters={"registered_address": doc.name},
        pluck="name",
        limit=1
    )

    if registered_links:
        frappe.throw(
            _("Cannot delete Address '{0}' - it is linked as registered address to Company '{1}'").format(
                doc.name, registered_links[0]
            ),
            frappe.LinkExistsError
        )

    # Check physical_address links
    physical_links = frappe.get_all(
        "Company",
        filters={"physical_address": doc.name},
        pluck="name",
        limit=1
    )

    if physical_links:
        frappe.throw(
            _("Cannot delete Address '{0}' - it is linked as physical address to Company '{1}'").format(
                doc.name, physical_links[0]
            ),
            frappe.LinkExistsError
        )
