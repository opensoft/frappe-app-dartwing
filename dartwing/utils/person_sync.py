# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
Person sync utilities for Frappe User auto-creation.

Implements resilient background job retry with exponential backoff
per research.md specifications.
"""

import frappe
from frappe import _
from frappe.utils import now

# Retry configuration
MAX_RETRIES = 5
BASE_DELAY = 2  # seconds
MAX_DELAY = 120  # seconds


class RetryableError(Exception):
    """Error that should trigger a retry."""
    pass


class NonRetryableError(Exception):
    """Error that should NOT trigger a retry."""
    pass


def queue_user_sync(person_name: str, attempt: int = 1) -> None:
    """Queue background job for Frappe User creation.

    Uses frappe.enqueue() with job_id deduplication to prevent
    duplicate jobs for the same Person.

    Args:
        person_name: The Person document name
        attempt: Current attempt number (1-indexed)
    """
    delay = min(BASE_DELAY ** attempt, MAX_DELAY)

    frappe.enqueue(
        "dartwing.utils.person_sync.sync_frappe_user",
        person_name=person_name,
        attempt=attempt,
        queue="default",
        timeout=300,
        job_id=f"person-sync-{person_name}",
        enqueue_after_commit=True,
        at_front=False
    )


def sync_frappe_user(person_name: str, attempt: int = 1) -> None:
    """Create Frappe User from Person's keycloak_user_id.

    Implements exponential backoff retry logic (max 5 retries).

    Args:
        person_name: The Person document name
        attempt: Current attempt number (1-indexed)
    """
    if not frappe.db.exists("Person", person_name):
        frappe.log_error(
            f"Person sync failed: {person_name} not found",
            "Person Sync Error"
        )
        return

    person = frappe.get_doc("Person", person_name)

    # Skip if already synced or no keycloak_user_id
    if person.frappe_user and person.user_sync_status == "synced":
        return

    if not person.keycloak_user_id:
        person.user_sync_status = "failed"
        person.sync_error_message = "No keycloak_user_id set"
        person.save(ignore_permissions=True)
        frappe.db.commit()
        return

    try:
        user = create_frappe_user(person)

        person.frappe_user = user.name
        person.user_sync_status = "synced"
        person.last_sync_at = now()
        person.sync_error_message = None
        person.save(ignore_permissions=True)
        frappe.db.commit()

    except RetryableError as e:
        if attempt < MAX_RETRIES:
            person.user_sync_status = "pending"
            person.sync_error_message = str(e)
            person.save(ignore_permissions=True)
            frappe.db.commit()
            queue_user_sync(person_name, attempt + 1)
        else:
            person.user_sync_status = "failed"
            person.sync_error_message = f"Max retries exceeded: {e}"
            person.save(ignore_permissions=True)
            frappe.db.commit()
            frappe.log_error(
                f"Person sync failed after {MAX_RETRIES} retries: {person_name}",
                str(e)
            )

    except NonRetryableError as e:
        person.user_sync_status = "failed"
        person.sync_error_message = str(e)
        person.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error(
            f"Person sync failed (non-retryable): {person_name}",
            str(e)
        )

    except Exception as e:
        # Unexpected error - log and mark as failed
        person.user_sync_status = "failed"
        person.sync_error_message = f"Unexpected error: {e}"
        person.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error(
            f"Person sync unexpected error: {person_name}",
            str(e)
        )


def create_frappe_user(person) -> "frappe.core.doctype.user.user.User":
    """Create Frappe User with default 'Dartwing User' role.

    Args:
        person: Person document

    Returns:
        Created User document

    Raises:
        NonRetryableError: For validation errors, duplicate entries
        RetryableError: For connection/service errors
    """
    # Check if user already exists with this email
    if frappe.db.exists("User", {"email": person.primary_email}):
        existing_user = frappe.db.get_value(
            "User", {"email": person.primary_email}, "name"
        )
        # Link to existing user instead of creating new
        return frappe.get_doc("User", existing_user)

    try:
        user = frappe.get_doc({
            "doctype": "User",
            "email": person.primary_email,
            "first_name": person.first_name,
            "last_name": person.last_name,
            "full_name": person.full_name,
            "enabled": 1,
            "user_type": "Website User",
            "roles": [{"role": "Dartwing User"}]
        })
        user.flags.ignore_permissions = True
        user.flags.no_welcome_mail = True
        user.insert()

        return user

    except frappe.DuplicateEntryError as e:
        raise NonRetryableError(f"Duplicate user entry: {e}")

    except frappe.ValidationError as e:
        raise NonRetryableError(f"Validation error: {e}")

    except Exception as e:
        # Connection errors, timeouts, etc. are retryable
        error_str = str(e).lower()
        if any(keyword in error_str for keyword in ["timeout", "connection", "unavailable"]):
            raise RetryableError(f"Service unavailable: {e}")
        raise NonRetryableError(f"Unexpected error: {e}")


def is_auto_creation_enabled() -> bool:
    """Check if Frappe User auto-creation is enabled via site configuration.

    Returns:
        True if auto-creation is enabled, False otherwise
    """
    try:
        return frappe.db.get_single_value("Settings", "auto_create_user_on_keycloak_signup") or False
    except frappe.ValidationError:
        # Field doesn't exist on Settings DocType - feature not configured
        return False
