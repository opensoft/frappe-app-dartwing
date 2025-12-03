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

# Import database-specific exceptions for proper error classification
try:
    import pymysql.err as db_errors

    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False

try:
    import redis.exceptions as redis_errors

    HAS_REDIS = True
except ImportError:
    HAS_REDIS = False

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


def is_retryable_error(exception: Exception) -> bool:
    """Determine if an exception represents a transient, retryable error.

    Retryable errors are typically transient issues that may succeed if retried,
    such as network interruptions, temporary database outages, or server timeouts.
    Non-retryable errors are permanent failures (e.g., validation errors, missing data)
    that will not succeed on retry and should be surfaced immediately.

    The following exception types are classified as retryable:
        - pymysql: OperationalError, InterfaceError
        - redis: ConnectionError, TimeoutError
        - Frappe: QueryTimeoutError
    All other exceptions are considered non-retryable to avoid wasting
    retries on permanent errors (validation failures, bad data, etc.).

    Args:
        exception: The exception to classify

    Returns:
        bool: True if the error is retryable, False otherwise
    """
    # Check for database connection errors
    if HAS_PYMYSQL:
        # OperationalError: connection issues, server gone away, etc.
        if isinstance(
            exception, (db_errors.OperationalError, db_errors.InterfaceError)
        ):
            return True

    # Check for Redis connection errors
    if HAS_REDIS:
        if isinstance(
            exception, (redis_errors.ConnectionError, redis_errors.TimeoutError)
        ):
            return True

    # Check for Frappe-specific transient errors
    if isinstance(exception, frappe.QueryTimeoutError):
        return True

    # Default: do not retry unless we're certain it's transient
    return False


def queue_user_sync(person_name: str, attempt: int = 1) -> None:
    """Queue background job for Frappe User creation with exponential backoff.

    Uses frappe.enqueue() with job_id deduplication per attempt to prevent
    duplicate jobs for the same Person at the same retry level.

    Implements exponential backoff: 2s, 4s, 8s, 16s, 32s (capped at 120s).

    Args:
        person_name: The Person document name
        attempt: Current attempt number (1-indexed)
    """
    # Calculate exponential backoff delay in seconds
    delay_seconds = min(BASE_DELAY * (2 ** (attempt - 1)), MAX_DELAY)

    # Include attempt in job_id to allow retries without dedup collision
    job_id = f"person-sync-{person_name}-attempt-{attempt}"

    if attempt == 1:
        # First attempt: enqueue immediately
        frappe.enqueue(
            "dartwing.utils.person_sync.sync_frappe_user",
            person_name=person_name,
            attempt=attempt,
            queue="default",
            timeout=300,
            job_id=job_id,
            enqueue_after_commit=True,
            at_front=False,
        )
    else:
        # Retry attempts: enqueue with delay
        frappe.enqueue(
            "dartwing.utils.person_sync.sync_frappe_user",
            person_name=person_name,
            attempt=attempt,
            queue="default",
            timeout=300,
            job_id=job_id,
            enqueue_after_commit=True,
            at_front=False,
            enqueue_in=delay_seconds,
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
            f"Person sync failed: {person_name} not found", "Person Sync Error"
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
                f"Person sync failed after {MAX_RETRIES} retries: {person_name}", str(e)
            )

    except NonRetryableError as e:
        person.user_sync_status = "failed"
        person.sync_error_message = str(e)
        person.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error(f"Person sync failed (non-retryable): {person_name}", str(e))

    except Exception as e:
        # Unexpected error - log and mark as failed
        person.user_sync_status = "failed"
        person.sync_error_message = f"Unexpected error: {e}"
        person.save(ignore_permissions=True)
        frappe.db.commit()
        frappe.log_error(f"Person sync unexpected error: {person_name}", str(e))


def create_frappe_user(person) -> "frappe.core.doctype.user.user.User":
    """Create Frappe User with default 'Dartwing User' role.

    If a user with the same email already exists, it will be reused
    and the 'Dartwing User' role will be added if not already present.

    Args:
        person: Person document

    Returns:
        User document (newly created or existing with role ensured)

    Raises:
        NonRetryableError: For validation errors, duplicate entries
        RetryableError: For connection/service errors
    """
    # Try to get existing user first (avoids race condition)
    try:
        existing_user = frappe.get_doc("User", {"email": person.primary_email})

        # Ensure the user has the required 'Dartwing User' role
        has_role = any(
            role.get("role") == "Dartwing User"
            for role in existing_user.get("roles", [])
        )

        if not has_role:
            # Add the role if missing to ensure consistent permissions
            existing_user.append("roles", {"role": "Dartwing User"})
            existing_user.flags.ignore_permissions = True
            existing_user.save()
            frappe.db.commit()

        return existing_user

    except frappe.DoesNotExistError:
        # User doesn't exist, proceed to create new one
        pass

    # Create new user
    try:
        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": person.primary_email,
                "first_name": person.first_name,
                "last_name": person.last_name,
                "full_name": person.full_name,
                "enabled": 1,
                "user_type": "Website User",
                "roles": [{"role": "Dartwing User"}],
            }
        )
        user.flags.ignore_permissions = True
        user.flags.no_welcome_mail = True
        user.insert()

        return user

    except frappe.DuplicateEntryError as e:
        raise NonRetryableError(f"Duplicate user entry: {e}")

    except frappe.ValidationError as e:
        raise NonRetryableError(f"Validation error: {e}")

    except Exception as e:
        # Use type-based error classification instead of string matching
        if is_retryable_error(e):
            raise RetryableError(f"Transient error (will retry): {e}")
        raise NonRetryableError(f"Non-retryable error: {e}")


def is_auto_creation_enabled() -> bool:
    """Check if Frappe User auto-creation is enabled via Settings DocType.

    Reads the 'auto_create_user_on_keycloak_signup' field from the Settings
    single DocType. Defaults to False if field doesn't exist or is not set.

    Returns:
        True if auto-creation is enabled, False otherwise
    """
    try:
        return bool(
            frappe.db.get_single_value(
                "Settings", "auto_create_user_on_keycloak_signup"
            )
        )
    except Exception as e:
        # Field doesn't exist or Settings DocType not accessible
        frappe.log_error(
            title="User Auto-Creation Configuration Error",
            message=(
                f"Could not read 'auto_create_user_on_keycloak_signup' from Settings: {e}\n\n"
                "User auto-creation is disabled. To enable, add the field to Settings DocType "
                "or run 'bench migrate' to update the schema."
            ),
        )
        return False
