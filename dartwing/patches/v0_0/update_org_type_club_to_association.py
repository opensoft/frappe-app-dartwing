# Copyright (c) 2025, Dartwing and contributors
# For license information, please see license.txt

import frappe


def execute():
    """Update Organization records with legacy org_type values to 'Association'.

    This migration aligns existing data with the updated Organization DocType
    where 'Association' is the canonical type (Club is a subtype of Association).
    Handles potential legacy values: 'Club', 'Club/Association', or any variation.
    """
    if not frappe.db.exists("DocType", "Organization"):
        return

    # Valid org_type values after migration
    valid_types = ("Family", "Company", "Nonprofit", "Association")

    # Update all legacy Club-related values to Association
    frappe.db.sql(
        """
        UPDATE `tabOrganization`
        SET org_type = 'Association'
        WHERE org_type LIKE '%Club%'
           OR org_type NOT IN %(valid_types)s
        """,
        {"valid_types": valid_types},
    )

    # Log any remaining invalid values (should be none after migration)
    invalid_rows = frappe.db.sql(
        """
        SELECT name, org_type FROM `tabOrganization`
        WHERE org_type NOT IN %(valid_types)s
        """,
        {"valid_types": valid_types},
        as_dict=True,
    )

    if invalid_rows:
        frappe.log_error(
            title="Organization org_type Migration Warning",
            message=f"Found {len(invalid_rows)} records with invalid org_type after migration: {invalid_rows}",
        )

    # Frappe automatically commits changes in patches
