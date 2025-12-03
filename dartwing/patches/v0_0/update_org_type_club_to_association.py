# Copyright (c) 2025, Dartwing and contributors
# For license information, please see license.txt

import frappe


def execute():
    """Update Organization records with org_type 'Club' to 'Association'.

    This migration aligns existing data with the updated Organization DocType
    where 'Association' is the canonical type (Club is a subtype of Association).
    """
    if not frappe.db.exists("DocType", "Organization"):
        return

    # Update all Organization records with org_type = 'Club' to 'Association'
    frappe.db.sql(
        """
        UPDATE `tabOrganization`
        SET org_type = 'Association'
        WHERE org_type = 'Club'
        """
    )

    # Commit the changes
    frappe.db.commit()
