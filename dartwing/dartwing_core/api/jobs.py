"""
Background Job API endpoints.

All endpoints require authentication and respect organization-based permissions.
Base Path: /api/method/dartwing.dartwing_core.api.jobs
"""

import frappe
from frappe import _


@frappe.whitelist()
def submit_job(job_type: str, organization: str, parameters: dict = None, priority: str = "Normal", depends_on: str = None):
    """
    Submit a new background job for execution.

    Args:
        job_type: Job Type identifier (e.g., "pdf_generation")
        organization: Organization name
        parameters: Job-specific input parameters (optional)
        priority: Low/Normal/High/Critical (default: Normal)
        depends_on: Parent job ID to wait for (optional)

    Returns:
        dict: {job_id, status, message}

    Raises:
        ValidationError: Invalid input parameters
        PermissionError: User lacks permission
        DuplicateError: Duplicate job submission detected
    """
    from dartwing.dartwing_core.background_jobs import submit_job as engine_submit_job

    job = engine_submit_job(
        job_type=job_type,
        organization=organization,
        parameters=parameters,
        priority=priority,
        depends_on=depends_on,
    )

    return {
        "job_id": job.name,
        "status": job.status,
        "message": "Job submitted successfully",
    }


@frappe.whitelist()
def get_job_status(job_id: str):
    """
    Retrieve current status and progress of a job.

    Args:
        job_id: Background Job ID

    Returns:
        dict: Job status details including progress, timestamps, and output
    """
    from dartwing.dartwing_core.background_jobs import get_job_status as engine_get_job_status

    return engine_get_job_status(job_id)


@frappe.whitelist()
def list_jobs(organization: str = None, status: str = None, job_type: str = None, limit: int = 20, offset: int = 0):
    """
    List jobs with filtering and pagination.

    Args:
        organization: Filter by organization (required for non-admin)
        status: Filter by status
        job_type: Filter by job type
        limit: Page size (default: 20, max: 100)
        offset: Pagination offset (default: 0)

    Returns:
        dict: {jobs: [...], total, limit, offset}
    """
    from dartwing.dartwing_core.background_jobs.engine import list_jobs as engine_list_jobs

    return engine_list_jobs(
        organization=organization,
        status=status,
        job_type=job_type,
        limit=min(int(limit), 100),
        offset=int(offset),
    )


@frappe.whitelist()
def cancel_job(job_id: str):
    """
    Request cancellation of a pending or running job.

    Args:
        job_id: Job to cancel

    Returns:
        dict: {job_id, status, message}

    Raises:
        ValidationError: Cannot cancel job in current status
        PermissionError: User lacks permission to cancel
    """
    from dartwing.dartwing_core.background_jobs import cancel_job as engine_cancel_job

    result = engine_cancel_job(job_id)

    return {
        "job_id": job_id,
        "status": result.status,
        "message": "Job canceled successfully",
    }


@frappe.whitelist()
def retry_job(job_id: str):
    """
    Manually retry a failed or dead letter job (admin only).

    Args:
        job_id: Job to retry

    Returns:
        dict: {job_id, status, message}
    """
    from dartwing.dartwing_core.background_jobs.engine import retry_job as engine_retry_job

    result = engine_retry_job(job_id)

    return {
        "job_id": job_id,
        "status": result.status,
        "message": "Job re-queued for execution",
    }


@frappe.whitelist()
def get_job_metrics(organization: str = None):
    """
    Retrieve operational metrics for monitoring.

    Args:
        organization: Filter by org (admin sees all if omitted)

    Returns:
        dict: Metrics including job counts, queue depth, processing times
    """
    from dartwing.dartwing_core.background_jobs.metrics import get_metrics

    return get_metrics(organization=organization)


@frappe.whitelist()
def get_job_history(job_id: str):
    """
    Retrieve execution log for a specific job.

    Args:
        job_id: Job to get history for

    Returns:
        dict: {job_id, history: [...]}
    """
    from dartwing.dartwing_core.background_jobs.engine import get_job_history as engine_get_job_history

    return engine_get_job_history(job_id)
