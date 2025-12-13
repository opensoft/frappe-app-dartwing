# Copyright (c) 2025, Brett and contributors
# For license information, please see license.txt

import frappe


def execute():
    """Update Family records with legacy status 'Archived' to 'Dissolved'.

    This migration aligns existing Family data with the updated status options.
    The status field options changed from Active/Inactive/Archived to
    Active/Inactive/Dissolved to maintain consistency across all organization types.
    """
    if not frappe.db.exists("DocType", "Family"):
        return

    # Update all Archived status values to Dissolved
    updated_count = frappe.db.sql(
        """
        UPDATE `tabFamily`
        SET status = 'Dissolved'
        WHERE status = 'Archived'
        """
    )

    # Log any invalid status values that might exist
    valid_statuses = ("Active", "Inactive", "Dissolved")
    invalid_rows = frappe.db.sql(
        """
        SELECT name, status FROM `tabFamily`
        WHERE status NOT IN %(valid_statuses)s
        """,
        {"valid_statuses": valid_statuses},
        as_dict=True,
    )

    if invalid_rows:
        frappe.log_error(
            title="Family Status Migration Warning",
            message=f"Found {len(invalid_rows)} records with invalid status after migration: {invalid_rows}",
        )

    # Frappe automatically commits changes in patches
