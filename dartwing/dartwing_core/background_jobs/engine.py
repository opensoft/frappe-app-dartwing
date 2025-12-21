"""
Core Engine for Background Job Engine.

Provides the main API for job submission, status checking, and management.
"""

import hashlib
import json
from contextlib import contextmanager
import frappe
from frappe import _
from frappe.utils import now_datetime, add_to_date
from typing import Optional, Iterator

try:
    import redis
except ImportError:
    redis = None

from dartwing.dartwing_core.background_jobs.config import (
    DEFAULT_TIMEOUT_SECONDS,
    DEFAULT_MAX_RETRIES,
    DEFAULT_DEDUPLICATION_WINDOW_SECONDS,
    DEFAULT_RATE_LIMIT_WINDOW_SECONDS,
    MAX_RATE_LIMIT_WINDOW_SECONDS,
    DEDUPLICATION_LOCK_TIMEOUT_SECONDS,
)


def submit_job(
    job_type: str,
    organization: str,
    parameters: dict = None,
    priority: str = "Normal",
    depends_on: str = None,
) -> "frappe.Document":
    """
    Submit a new background job for execution.

    Args:
        job_type: Job Type identifier (e.g., "pdf_generation")
        organization: Organization name
        parameters: Job-specific input parameters (optional)
        priority: Low/Normal/High/Critical (default: Normal)
        depends_on: Parent job ID to wait for (optional)

    Returns:
        Background Job document

    Raises:
        frappe.ValidationError: Invalid input parameters or rate limit exceeded
        frappe.PermissionError: User lacks permission
        frappe.DuplicateEntryError: Duplicate job submission detected
    """
    # Phase 1: Validation
    _validate_organization_access(organization)
    job_type_doc = _get_job_type(job_type)
    _check_rate_limit(job_type_doc)
    _validate_job_type_permission(job_type_doc, job_type)

    # Phase 2: Prepare job parameters
    job_hash = generate_job_hash(job_type, organization, parameters or {})
    deduplication_window = _get_deduplication_window(job_type_doc)

    # Phase 3: Create job (with optional deduplication)
    if deduplication_window > 0:
        # Check redis availability early before entering context manager
        # This fails fast with a clear error if redis is not installed
        if not redis:
            raise ImportError(
                "Redis module is not available. The background job system requires redis for "
                "distributed locking when deduplication is enabled. Please install redis: pip install redis"
            )
        with _deduplication_lock(organization=organization, job_hash=job_hash):
            _check_duplicate_and_throw(job_hash, deduplication_window)
            return _create_job_record(
                job_type, organization, parameters, priority,
                depends_on, job_hash, job_type_doc
            )
    else:
        return _create_job_record(
            job_type, organization, parameters, priority,
            depends_on, job_hash, job_type_doc
        )


def get_job_status(job_id: str) -> dict:
    """
    Get current status and progress of a job.

    Args:
        job_id: Background Job ID

    Returns:
        Dict with job status details
    """
    job = frappe.get_doc("Background Job", job_id)

    # Check permission
    _validate_job_access(job)

    return {
        "job_id": job.name,
        "job_type": job.job_type,
        "status": job.status,
        "progress": job.progress or 0,
        "progress_message": job.progress_message,
        "created_at": str(job.created_at) if job.created_at else None,
        "started_at": str(job.started_at) if job.started_at else None,
        "completed_at": str(job.completed_at) if job.completed_at else None,
        "retry_count": job.retry_count or 0,
        "next_retry_at": str(job.next_retry_at) if job.next_retry_at else None,
        "output_reference": job.output_reference,
        "error_message": job.error_message,
        "error_type": job.error_type,
    }


def cancel_job(job_id: str) -> "frappe.Document":
    """
    Cancel a pending or running job.

    Uses row-level locking to prevent race conditions where job status
    changes between the check and the update.

    Note: This function marks the job as canceled in the database but does NOT
    immediately terminate a running RQ worker. Running jobs detect cancellation
    cooperatively by calling `JobContext.is_canceled()` at progress checkpoints.
    Jobs that don't check for cancellation will run to completion.

    See GitHub Issue #34 for planned RQ job termination enhancement.

    Args:
        job_id: Job to cancel

    Returns:
        Updated Background Job document

    Raises:
        frappe.ValidationError: Cannot cancel job in current status
        frappe.PermissionError: User lacks permission to cancel
    """
    # Lock the row to prevent concurrent modification (race condition fix)
    # This ensures the job status doesn't change between our check and update
    frappe.db.sql(
        "SELECT name FROM `tabBackground Job` WHERE name = %s FOR UPDATE",
        (job_id,)
    )

    job = frappe.get_doc("Background Job", job_id)

    # Check permission - owner or admin can cancel
    _validate_job_access(job, require_write=True)

    if not job.can_cancel():
        frappe.throw(
            _("Cannot cancel job in status: {0}").format(job.status)
        )

    from dartwing.dartwing_core.background_jobs.progress import publish_job_status_changed

    old_status = job.status
    job.status = "Canceled"
    job.canceled_at = now_datetime()
    job.canceled_by = frappe.session.user
    job.save(ignore_permissions=True)
    frappe.db.commit()

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status=old_status,
        to_status="Canceled",
    )

    return job


def retry_job(job_id: str) -> "frappe.Document":
    """
    Manually retry a failed or dead letter job (admin only).

    Args:
        job_id: Job to retry

    Returns:
        Updated Background Job document
    """
    # Admin only
    if not frappe.has_permission("Background Job", "write"):
        frappe.throw(_("Only administrators can retry jobs"), frappe.PermissionError)

    job = frappe.get_doc("Background Job", job_id)

    if job.status not in ["Failed", "Dead Letter", "Timed Out"]:
        frappe.throw(
            _("Cannot retry job in status: {0}").format(job.status)
        )

    from dartwing.dartwing_core.background_jobs.progress import publish_job_status_changed

    old_status = job.status
    job.status = "Queued"
    job.error_message = None
    job.error_type = None
    job.next_retry_at = None
    job.save(ignore_permissions=True)

    # Re-enqueue
    _enqueue_job(job, is_retry=True)

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status=old_status,
        to_status="Queued",
    )

    return job


def list_jobs(
    organization: str = None,
    status: str = None,
    job_type: str = None,
    limit: int = 20,
    offset: int = 0,
) -> dict:
    """
    List jobs with filtering and pagination.

    Args:
        organization: Filter by organization
        status: Filter by status
        job_type: Filter by job type
        limit: Page size (default: 20, max: 100)
        offset: Pagination offset

    Returns:
        Dict with jobs list, total count, and pagination info
    """
    filters = {}

    # Non-admin users must filter by organization
    if not frappe.has_permission("Background Job", "read"):
        if not organization:
            # Get user's organizations via Person -> Org Member chain
            person = frappe.db.get_value("Person", {"frappe_user": frappe.session.user}, "name")
            if person:
                orgs = frappe.get_all(
                    "Org Member",
                    filters={"person": person, "status": "Active"},
                    pluck="organization",
                )
            else:
                orgs = []

            if orgs:
                filters["organization"] = ("in", orgs)
            else:
                return {"jobs": [], "total": 0, "limit": limit, "offset": offset}
        else:
            _validate_organization_access(organization)
            filters["organization"] = organization
    elif organization:
        filters["organization"] = organization

    if status:
        filters["status"] = status
    if job_type:
        filters["job_type"] = job_type

    total = frappe.db.count("Background Job", filters)

    jobs = frappe.get_all(
        "Background Job",
        filters=filters,
        fields=["name", "job_type", "status", "progress", "created_at", "organization"],
        order_by="created_at desc",
        start=offset,
        page_length=limit,
    )

    return {
        "jobs": [
            {
                "job_id": j.name,
                "job_type": j.job_type,
                "status": j.status,
                "progress": j.progress or 0,
                "created_at": str(j.created_at) if j.created_at else None,
            }
            for j in jobs
        ],
        "total": total,
        "limit": limit,
        "offset": offset,
    }


def get_job_history(job_id: str) -> dict:
    """
    Get execution log for a specific job.

    Args:
        job_id: Job to get history for

    Returns:
        Dict with job_id and history list
    """
    job = frappe.get_doc("Background Job", job_id)
    _validate_job_access(job)

    logs = frappe.get_all(
        "Job Execution Log",
        filters={"background_job": job_id},
        fields=["from_status", "to_status", "timestamp", "actor", "message", "retry_attempt"],
        order_by="timestamp asc",
        ignore_permissions=True,
    )

    return {
        "job_id": job_id,
        "history": [
            {
                "from_status": log.from_status,
                "to_status": log.to_status,
                "timestamp": str(log.timestamp) if log.timestamp else None,
                "actor": log.actor,
                "message": log.message,
                "retry_attempt": log.retry_attempt,
            }
            for log in logs
        ],
    }


# Internal helper functions


def _validate_job_type_permission(job_type_doc: "frappe.Document", job_type: str) -> None:
    """Validate user has permission for this job type if required."""
    if job_type_doc.requires_permission:
        if not frappe.has_permission(job_type_doc.requires_permission, "create"):
            frappe.throw(_("You don't have permission to submit {0} jobs").format(job_type))


def _get_deduplication_window(job_type_doc: "frappe.Document") -> int:
    """Get deduplication window in seconds from job type config."""
    if job_type_doc.deduplication_window is not None:
        return job_type_doc.deduplication_window
    return DEFAULT_DEDUPLICATION_WINDOW_SECONDS


def _check_duplicate_and_throw(job_hash: str, window_seconds: int) -> None:
    """Check for duplicate job and throw if found."""
    existing = _check_duplicate(job_hash, window_seconds)
    if existing:
        frappe.throw(
            _("Duplicate job detected. Existing job: {0} (status: {1})").format(
                existing.name, existing.status
            ),
            exc=frappe.DuplicateEntryError,
        )


def _create_job_record(
    job_type: str,
    organization: str,
    parameters: dict,
    priority: str,
    depends_on: str,
    job_hash: str,
    job_type_doc: "frappe.Document",
) -> "frappe.Document":
    """Create a new Background Job record and enqueue it for execution."""
    job = frappe.new_doc("Background Job")
    job.job_type = job_type
    job.organization = organization
    job.owner_user = frappe.session.user
    job.status = "Pending"
    job.priority = priority if priority is not None else (job_type_doc.default_priority or "Normal")
    job.input_parameters = json.dumps(parameters) if parameters is not None else None
    job.job_hash = job_hash
    job.timeout_seconds = (
        job_type_doc.default_timeout
        if job_type_doc.default_timeout is not None
        else DEFAULT_TIMEOUT_SECONDS
    )
    job.max_retries = (
        job_type_doc.max_retries
        if job_type_doc.max_retries is not None
        else DEFAULT_MAX_RETRIES
    )
    job.depends_on = depends_on
    job.created_at = now_datetime()

    job.insert(ignore_permissions=True)
    _enqueue_job(job)
    return job


def _is_system_manager() -> bool:
    """Check if current user has System Manager role."""
    return "System Manager" in frappe.get_roles()


def generate_job_hash(job_type: str, organization: str, params: dict) -> str:
    """
    Generate unique hash for duplicate detection.

    Uses frappe.as_json() for stable serialization of Frappe types
    (datetime, date, Decimal, etc.) that would crash with standard json.dumps().

    Args:
        job_type: Job type name
        organization: Organization name
        params: Job parameters

    Returns:
        16-character hex hash
    """
    params_json = frappe.as_json(params, sort_keys=True)
    content = f"{job_type}:{organization}:{params_json}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _validate_organization_access(organization: str):
    """Validate user has access to organization via Person -> Org Member."""
    # System Manager can access all
    if _is_system_manager():
        return

    # Find Person linked to current user
    person = frappe.db.get_value("Person", {"frappe_user": frappe.session.user}, "name")
    if not person:
        frappe.throw(
            _("You don't have access to organization {0}").format(organization),
            frappe.PermissionError,
        )

    # Check if person is member of organization
    is_member = frappe.db.exists(
        "Org Member",
        {"organization": organization, "person": person, "status": "Active"},
    )
    if not is_member:
        frappe.throw(
            _("You don't have access to organization {0}").format(organization),
            frappe.PermissionError,
        )


def _validate_job_access(job, require_write: bool = False):
    """Validate user has access to view/modify job."""
    # System Manager can access all
    if _is_system_manager():
        return

    # Owner can always access their own jobs
    if job.owner_user == frappe.session.user:
        return

    # Check organization access
    _validate_organization_access(job.organization)

    if require_write:
        # Only users with explicit write permission on the doctype may modify
        # other members' jobs.
        if not frappe.has_permission("Background Job", "write"):
            frappe.throw(_("You don't have permission to modify this job"), frappe.PermissionError)


def _get_job_type(job_type: str) -> "frappe.Document":
    """Get and validate job type document."""
    if not frappe.db.exists("Job Type", job_type):
        frappe.throw(_("Job Type '{0}' not found").format(job_type))

    job_type_doc = frappe.get_cached_doc("Job Type", job_type)

    if not job_type_doc.is_enabled:
        frappe.throw(_("Job Type '{0}' is disabled").format(job_type))

    return job_type_doc


def _check_rate_limit(job_type_doc: "frappe.Document"):
    """
    Check if user has exceeded rate limit for this job type.

    Args:
        job_type_doc: Job Type document with rate limit configuration

    Raises:
        frappe.ValidationError: If rate limit exceeded

    Note:
        This rate limit check has a minor race condition window where concurrent
        requests could all check the count before any job is created, allowing
        slightly more jobs than the limit. This is acceptable as rate limiting is
        a soft UX protection, not a hard security boundary. The window is typically
        <100ms and unlikely to cause significant limit violations in practice.
    """
    # Skip if no rate limit configured (None or 0 both mean "no limit")
    # Note: 'if not rate_limit' is True when rate_limit is None or 0 (both falsy)
    if not job_type_doc.rate_limit:
        return

    # System Manager bypasses rate limiting (check early to avoid DB query)
    if _is_system_manager():
        return

    window_seconds = job_type_doc.rate_limit_window if job_type_doc.rate_limit_window is not None else DEFAULT_RATE_LIMIT_WINDOW_SECONDS
    if window_seconds < 1:
        frappe.throw(_("Rate limit window must be at least 1 second"))
    if window_seconds > MAX_RATE_LIMIT_WINDOW_SECONDS:
        frappe.throw(_("Rate limit window cannot exceed 24 hours ({0} seconds)").format(MAX_RATE_LIMIT_WINDOW_SECONDS))
    cutoff = add_to_date(now_datetime(), seconds=-window_seconds)

    # Count recent jobs by this user for this job type
    recent_count = frappe.db.count(
        "Background Job",
        {
            "job_type": job_type_doc.name,
            "owner_user": frappe.session.user,
            "creation": (">=", cutoff),
        },
    )

    if recent_count >= job_type_doc.rate_limit:
        frappe.throw(
            _(
                "Rate limit exceeded for '{0}' jobs. You have submitted {1} of {2} allowed "
                "submissions in the last {3} seconds. Please wait before submitting more jobs."
            ).format(job_type_doc.name, recent_count, job_type_doc.rate_limit, window_seconds)
        )


def _check_duplicate(job_hash: str, window_seconds: int) -> Optional["frappe.Document"]:
    """Check for existing duplicate job within window (non-locking version)."""
    cutoff = add_to_date(now_datetime(), seconds=-window_seconds)

    existing = frappe.db.get_value(
        "Background Job",
        {
            "job_hash": job_hash,
            "creation": (">=", cutoff),
            "status": ("not in", ["Completed", "Dead Letter", "Canceled"]),
        },
        ["name", "status"],
        as_dict=True,
    )

    return existing


@contextmanager
def _deduplication_lock(organization: str, job_hash: str, timeout_seconds: int = DEDUPLICATION_LOCK_TIMEOUT_SECONDS) -> Iterator[None]:
    """
    Serialize duplicate detection + insert across workers.

    This is required because the current schema intentionally does not enforce a
    unique constraint on job_hash (the same job must be allowed again after the
    deduplication window). A distributed lock prevents concurrent inserts of the
    same (organization, job_hash) within the same window.

    Raises:
        frappe.ValidationError: If Redis is unavailable
    """
    lock_key = f"dartwing_core:background_job:dedup:{organization}:{job_hash}"

    # Define specific exceptions to catch for Redis connectivity issues
    # Note: redis.ConnectionError is a subclass of redis.RedisError
    # Only catch redis.RedisError to avoid catching unrelated built-in ConnectionError exceptions
    # Redis availability is checked in submit_job() before calling this function
    redis_exceptions = (redis.RedisError,)

    try:
        lock = frappe.cache().lock(lock_key, timeout=timeout_seconds)
        lock.acquire()
    except redis_exceptions as e:
        # Log detailed context for debugging
        import traceback  # Only used for error logging in this handler

        error_details = (
            f"Lock key: {lock_key}\n"
            f"Organization: {organization}\n"
            f"Job hash: {job_hash}\n"
            f"Timeout: {timeout_seconds}s\n\n"
            f"Error: {str(e)}\n\n"
            f"Traceback:\n{traceback.format_exc()}"
        )
        frappe.log_error(error_details, "Redis Lock Acquisition Failed")
        frappe.throw(
            _("Unable to submit job due to cache service unavailability. "
              "Please try again in a few moments or contact support if this persists."),
            title=_("Cache Service Unavailable")
        )

    try:
        yield
    finally:
        try:
            lock.release()
        except Exception:
            # If Redis connection drops, the lock will expire by timeout.
            pass


def _enqueue_job(job, is_retry: bool = False):
    """
    Enqueue job for background execution.

    Note: We intentionally do NOT call frappe.db.commit() here. The
    enqueue_after_commit=True parameter ensures the RQ job is only
    enqueued after the outer transaction commits. This preserves
    atomicity when submit_job() is called within a larger transaction.
    """
    from dartwing.dartwing_core.background_jobs.progress import publish_job_status_changed

    # Update status to Queued
    if job.status != "Queued":
        old_status = job.status
        job.status = "Queued"
        job.save(ignore_permissions=True)
        # Removed: frappe.db.commit() - rely on enqueue_after_commit=True

        publish_job_status_changed(
            job_id=job.name,
            organization=job.organization,
            from_status=old_status,
            to_status="Queued",
        )

    # Map priority to Frappe queue
    queue_map = {
        "Critical": "short",
        "High": "short",
        "Normal": "default",
        "Low": "long",
    }
    queue = queue_map.get(job.priority, "default")

    # Enqueue using Frappe's background jobs
    # Use enqueue_after_commit to ensure job record is persisted before RQ picks it up
    frappe.enqueue(
        "dartwing.dartwing_core.background_jobs.executor.execute_job",
        background_job_id=job.name,
        queue=queue,
        timeout=job.timeout_seconds if job.timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS,
        is_async=True,
        enqueue_after_commit=True,
    )
