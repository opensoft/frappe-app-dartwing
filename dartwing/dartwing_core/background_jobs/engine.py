"""
Core Engine for Background Job Engine.

Provides the main API for job submission, status checking, and management.
"""

import hashlib
import json
import frappe
from frappe import _
from frappe.utils import now_datetime, add_to_date
from typing import Optional


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
        frappe.ValidationError: Invalid input parameters
        frappe.PermissionError: User lacks permission
        DuplicateJobError: Duplicate job submission detected
    """
    # Validate user can submit jobs for this organization
    _validate_organization_access(organization)

    # Get job type configuration
    job_type_doc = _get_job_type(job_type)

    # Check for permission requirement
    if job_type_doc.requires_permission:
        if not frappe.has_permission(job_type_doc.requires_permission, "create"):
            frappe.throw(_("You don't have permission to submit {0} jobs").format(job_type))

    # Generate hash for duplicate detection
    job_hash = generate_job_hash(job_type, organization, parameters or {})

    # Atomic duplicate check with row locking to prevent race conditions
    # Lock any existing non-terminal job with same hash during the check
    existing = _check_duplicate_with_lock(job_hash, job_type_doc.deduplication_window or 300)
    if existing:
        frappe.throw(
            _(
                "Duplicate job detected. Existing job: {0} (status: {1})"
            ).format(existing.name, existing.status),
            exc=frappe.DuplicateEntryError,
        )

    # Create job document
    job = frappe.new_doc("Background Job")
    job.job_type = job_type
    job.organization = organization
    job.owner_user = frappe.session.user
    job.status = "Pending"
    job.priority = priority if priority is not None else (job_type_doc.default_priority or "Normal")
    job.input_parameters = json.dumps(parameters) if parameters else None
    job.job_hash = job_hash
    job.timeout_seconds = job_type_doc.default_timeout if job_type_doc.default_timeout is not None else 300
    job.max_retries = job_type_doc.max_retries if job_type_doc.max_retries is not None else 5
    job.depends_on = depends_on
    job.created_at = now_datetime()

    try:
        job.insert(ignore_permissions=True)
    except frappe.DuplicateEntryError:
        # Handle race condition: another request inserted between our check and insert
        existing = frappe.db.get_value(
            "Background Job",
            {"job_hash": job_hash, "status": ("not in", ["Completed", "Dead Letter", "Canceled"])},
            ["name", "status"],
            as_dict=True,
        )
        if existing:
            frappe.throw(
                _("Duplicate job detected. Existing job: {0} (status: {1})").format(existing.name, existing.status),
                exc=frappe.DuplicateEntryError,
            )
        # If no existing found (edge case), re-raise original error
        raise

    # Enqueue the job
    _enqueue_job(job)

    return job


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
            }
            for log in logs
        ],
    }


# Internal helper functions


def generate_job_hash(job_type: str, organization: str, params: dict) -> str:
    """
    Generate unique hash for duplicate detection.

    Args:
        job_type: Job type name
        organization: Organization name
        params: Job parameters

    Returns:
        16-character hex hash
    """
    content = f"{job_type}:{organization}:{json.dumps(params, sort_keys=True)}"
    return hashlib.sha256(content.encode()).hexdigest()[:16]


def _validate_organization_access(organization: str):
    """Validate user has access to organization via Person -> Org Member."""
    # System Manager can access all
    if "System Manager" in frappe.get_roles():
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
    if "System Manager" in frappe.get_roles():
        return

    # Owner can always access their own jobs
    if job.owner_user == frappe.session.user:
        return

    # Check organization access
    _validate_organization_access(job.organization)


def _get_job_type(job_type: str) -> "frappe.Document":
    """Get and validate job type document."""
    if not frappe.db.exists("Job Type", job_type):
        frappe.throw(_("Job Type '{0}' not found").format(job_type))

    job_type_doc = frappe.get_cached_doc("Job Type", job_type)

    if not job_type_doc.is_enabled:
        frappe.throw(_("Job Type '{0}' is disabled").format(job_type))

    return job_type_doc


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


def _check_duplicate_with_lock(job_hash: str, window_seconds: int) -> Optional[dict]:
    """
    Check for existing duplicate job within window with row locking.

    Uses SELECT ... FOR UPDATE to prevent race conditions where two concurrent
    requests both pass the duplicate check before either inserts.

    Args:
        job_hash: The job hash to check
        window_seconds: Deduplication window in seconds

    Returns:
        Dict with name and status if duplicate found, None otherwise
    """
    cutoff = add_to_date(now_datetime(), seconds=-window_seconds)

    # Use FOR UPDATE to lock any matching rows during this transaction
    result = frappe.db.sql(
        """
        SELECT name, status
        FROM `tabBackground Job`
        WHERE job_hash = %(job_hash)s
        AND creation >= %(cutoff)s
        AND status NOT IN ('Completed', 'Dead Letter', 'Canceled')
        FOR UPDATE
        """,
        {"job_hash": job_hash, "cutoff": cutoff},
        as_dict=True,
    )

    return result[0] if result else None


def _enqueue_job(job, is_retry: bool = False):
    """Enqueue job for background execution."""
    from dartwing.dartwing_core.background_jobs.progress import publish_job_status_changed

    # Update status to Queued
    if job.status != "Queued":
        old_status = job.status
        job.status = "Queued"
        job.save(ignore_permissions=True)
        frappe.db.commit()

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
        job_id=job.name,
        queue=queue,
        timeout=job.timeout_seconds or 300,
        is_async=True,
        enqueue_after_commit=True,
    )
