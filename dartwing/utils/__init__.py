# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Utility functions for Dartwing app.

This module contains reusable business logic that is not tied to specific DocTypes.
"""

# Import utility modules here for easier access
# Example:
# from dartwing.utils.validation import validate_email
# from dartwing.utils.notifications import send_notification

from dartwing.utils.doctype_utils import doctype_table_exists
from dartwing.utils.permission_logger import log_permission_event, get_permission_logger

__all__ = [
    "doctype_table_exists",
    "log_permission_event",
    "get_permission_logger",
]
