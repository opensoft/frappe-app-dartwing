"""
Job Executor for Background Job Engine.

Handles job execution with timeout handling, checkpoint support, and error
classification.
"""

import frappe
from frappe import _
from frappe.utils import now_datetime
from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from dartwing.dartwing_core.background_jobs.progress import JobContext, publish_job_status_changed
from dartwing.dartwing_core.background_jobs.errors import (
    classify_error,
    get_error_type,
    TransientError,
    PermanentError,
)


class JobTimeoutError(TransientError):
    """Raised when job execution exceeds timeout."""

    pass


def execute_job(job_id: str):
    """
    Execute a background job.

    This is the main entry point called by Frappe's background worker.

    Args:
        job_id: Background Job ID to execute
    """
    job = frappe.get_doc("Background Job", job_id)

    # Validate job can be executed
    if job.status not in ["Queued"]:
        frappe.log_error(
            f"Job {job_id} cannot be executed in status {job.status}",
            "Background Job Executor",
        )
        return

    # Check dependency
    if not _check_dependency(job):
        return

    # Transition to Running
    old_status = job.status
    job.status = "Running"
    job.started_at = now_datetime()
    job.save(ignore_permissions=True)
    frappe.db.commit()

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status=old_status,
        to_status="Running",
    )

    # Get handler
    try:
        handler = _get_handler(job.job_type)
    except Exception as e:
        _handle_failure(job, e, is_handler_error=True)
        return

    # Create context
    context = JobContext(
        job_id=job.name,
        job_type=job.job_type,
        organization=job.organization,
        parameters=frappe.parse_json(job.input_parameters) if job.input_parameters else {},
        timeout_seconds=job.timeout_seconds or 300,
    )

    # Execute with timeout
    try:
        result = _execute_with_timeout(handler, context, job.timeout_seconds or 300)
        _handle_success(job, result)
    except JobTimeoutError as e:
        _handle_timeout(job, e)
    except Exception as e:
        _handle_failure(job, e)


def _check_dependency(job) -> bool:
    """
    Check if job dependency is satisfied.

    Args:
        job: Background Job document

    Returns:
        True if job can proceed, False if blocked
    """
    if not job.depends_on:
        return True

    parent_status = frappe.db.get_value("Background Job", job.depends_on, "status")

    if parent_status == "Completed":
        return True

    if parent_status in ["Failed", "Dead Letter", "Canceled", "Timed Out"]:
        # Parent failed - fail this job too
        job.status = "Dead Letter"
        job.error_message = f"Parent job {job.depends_on} failed with status: {parent_status}"
        job.error_type = "Permanent"
        job.completed_at = now_datetime()
        job.save(ignore_permissions=True)
        frappe.db.commit()

        publish_job_status_changed(
            job_id=job.name,
            organization=job.organization,
            from_status="Queued",
            to_status="Dead Letter",
            error_message=job.error_message,
        )
        return False

    # Parent still in progress - re-queue this job
    # The scheduler will pick it up again later
    return False


def _get_handler(job_type: str) -> Callable:
    """
    Get the handler function for a job type.

    Args:
        job_type: Job Type name

    Returns:
        The handler callable
    """
    from dartwing.dartwing_core.doctype.job_type.job_type import get_handler

    return get_handler(job_type)


def _execute_with_timeout(handler: Callable, context: JobContext, timeout_seconds: int) -> Any:
    """
    Execute handler with portable thread-based timeout.

    Uses ThreadPoolExecutor for cross-platform compatibility (works on Windows
    and in non-main threads, unlike signal.SIGALRM).

    Args:
        handler: Job handler function
        context: JobContext instance
        timeout_seconds: Maximum execution time

    Returns:
        Handler result

    Raises:
        JobTimeoutError: If execution exceeds timeout
    """
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(handler, context)
        try:
            return future.result(timeout=timeout_seconds)
        except FuturesTimeoutError:
            raise JobTimeoutError(f"Job exceeded {timeout_seconds}s timeout")


def _handle_success(job, result: Any):
    """Handle successful job completion."""
    job.reload()
    job.status = "Completed"
    job.progress = 100
    job.completed_at = now_datetime()

    if result and isinstance(result, dict):
        if "output_reference" in result:
            job.output_reference = result["output_reference"]

    job.save(ignore_permissions=True)
    frappe.db.commit()

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status="Running",
        to_status="Completed",
        output_reference=job.output_reference,
    )


def _handle_timeout(job, error: JobTimeoutError):
    """Handle job timeout."""
    job.reload()
    job.status = "Timed Out"
    job.error_message = str(error)
    job.error_type = "Transient"
    job.completed_at = now_datetime()
    job.save(ignore_permissions=True)
    frappe.db.commit()

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status="Running",
        to_status="Timed Out",
        error_message=job.error_message,
    )

    # Schedule retry if retries remaining
    from dartwing.dartwing_core.background_jobs.retry import schedule_retry

    schedule_retry(job.name)


def _handle_failure(job, error: Exception, is_handler_error: bool = False):
    """Handle job failure."""
    job.reload()
    job.error_message = str(error)
    job.error_type = get_error_type(error)
    job.completed_at = now_datetime()

    is_retryable = classify_error(error)

    if is_retryable and not is_handler_error:
        job.status = "Failed"
    else:
        job.status = "Dead Letter"

    job.save(ignore_permissions=True)
    frappe.db.commit()

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status="Running",
        to_status=job.status,
        error_message=job.error_message,
    )

    # Schedule retry if transient failure
    if job.status == "Failed":
        from dartwing.dartwing_core.background_jobs.retry import schedule_retry

        schedule_retry(job.name)

    # Log error for debugging
    frappe.log_error(
        f"Job {job.name} failed: {error}",
        "Background Job Executor",
    )
