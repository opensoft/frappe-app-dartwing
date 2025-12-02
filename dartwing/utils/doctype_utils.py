# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""Utility functions for DocType operations."""

import frappe


def doctype_exists(doctype_name: str) -> bool:
    """Check if a DocType table exists in the database.

    This utility function centralizes the table existence check to avoid
    duplication across the codebase and reduce coupling with Frappe's
    table naming conventions.

    Args:
        doctype_name: The name of the DocType (without 'tab' prefix)

    Returns:
        bool: True if the DocType table exists, False otherwise

    Example:
        >>> if doctype_exists("Org Member"):
        ...     # Safe to query Org Member records
        ...     pass
    """
    return frappe.db.table_exists(f"tab{doctype_name}")
