# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Audit logging for permission lifecycle events.

This module provides structured logging for permission create, remove, and skip
events to support compliance auditing and debugging (FR-012).
"""

import frappe
from frappe.utils import now_datetime


def get_permission_logger():
    """
    Get the permission audit logger instance.

    Returns:
        Logger: Frappe logger configured for permission_audit module
    """
    return frappe.logger("permission_audit", allow_site=True)


def log_permission_event(event_type: str, org_member_doc, **kwargs) -> None:
    """
    Log a permission lifecycle event for audit trail.

    Args:
        event_type: Type of event - "create", "remove", or "skip"
        org_member_doc: The Org Member document triggering the event
        **kwargs: Additional context:
            - user: The Frappe User affected
            - doctype: The DocType for which permission was created/removed
            - for_value: The specific record name
            - reason: Reason for skip events

    Example:
        log_permission_event(
            "create",
            org_member_doc,
            user="john@example.com",
            doctype="Organization",
            for_value="ORG-2025-00001"
        )
    """
    logger = get_permission_logger()

    log_data = {
        "timestamp": str(now_datetime()),
        "event": event_type,
        "org_member": org_member_doc.name,
        "person": org_member_doc.person,
        "organization": org_member_doc.organization,
        **kwargs
    }

    # Format: PERMISSION_CREATE: {...}, PERMISSION_REMOVE: {...}, PERMISSION_SKIP: {...}
    logger.info(f"PERMISSION_{event_type.upper()}: {log_data}")
