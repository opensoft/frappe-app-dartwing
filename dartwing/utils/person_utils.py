# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Person utility functions.

Shared helper functions for Person DocType operations and API endpoints.
"""

import frappe


def is_self_modification_attempt(person) -> bool:
    """Check if the current user is attempting to modify their own Person record.

    Used to enforce guardian/role gates for minors - prevents minors from
    capturing their own consent or making other restricted modifications.

    Args:
        person: The Person document (can be a dict-like object with frappe_user attribute)

    Returns:
        bool: True if the session user is the Person themselves, False otherwise
    """
    # Check if Person has a linked Frappe User and if it matches the current session user
    frappe_user = getattr(person, "frappe_user", None) if hasattr(person, "frappe_user") else person.get("frappe_user")
    return frappe_user and frappe.session.user == frappe_user
