# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""Utility functions for DocType operations."""

import frappe


def doctype_table_exists(doctype_name: str) -> bool:
    """Check if a DocType's database table exists.

    This utility function centralizes the table existence check to avoid
    duplication across the codebase and reduce coupling with Frappe's
    table naming conventions (the 'tab' prefix).

    Note: This checks TABLE existence, not DocType metadata. For checking
    if a DocType is installed/available, use frappe.db.exists("DocType", name).

    Args:
        doctype_name: The name of the DocType (without 'tab' prefix)

    Returns:
        bool: True if the DocType table exists, False otherwise

    Example:
        >>> if doctype_table_exists("Org Member"):
        ...     # Database table exists, safe for low-level operations
        ...     pass
    """
    return frappe.db.table_exists(f"tab{doctype_name}")
