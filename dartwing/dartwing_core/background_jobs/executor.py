"""
Job Executor for Background Job Engine.

Handles job execution with timeout handling, checkpoint support, and error
classification.
"""

import frappe
from frappe.utils import now_datetime, add_to_date
from typing import Any, Callable
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

from dartwing.dartwing_core.background_jobs.config import (
    DEFAULT_TIMEOUT_SECONDS,
    DEPENDENCY_RETRY_DELAY_SECONDS,
)
from dartwing.dartwing_core.background_jobs.progress import JobContext, publish_job_status_changed
from dartwing.dartwing_core.background_jobs.errors import (
    classify_error,
    get_error_type,
    TransientError,
    JobCanceledError,
    ERROR_TYPE_CIRCUIT_BREAKER,
)
from dartwing.dartwing_core.background_jobs.circuit_breaker import (
    check_circuit_breaker,
    record_job_outcome,
    CircuitBreakerOpen,
)


class JobTimeoutError(TransientError):
    """Raised when job execution exceeds timeout."""

    pass


def execute_job(background_job_id: str | None = None, job_id: str | None = None) -> None:
    """
    Execute a background job.

    This is the main entry point called by Frappe's background worker.

    Args:
        background_job_id: Background Job ID to execute
        job_id: Backward-compatible alias for already-enqueued RQ jobs
    """
    if background_job_id is None:
        background_job_id = job_id
    elif job_id is not None and job_id != background_job_id:
        frappe.log_error(
            f"execute_job called with mismatched IDs: background_job_id={background_job_id}, job_id={job_id}",
            "Background Job Executor",
        )

    if not background_job_id:
        raise TypeError("execute_job() missing required argument: 'background_job_id'")

    job = frappe.get_doc("Background Job", background_job_id)

    # Validate job can be executed
    if job.status not in ["Queued"]:
        frappe.log_error(
            f"Job {background_job_id} cannot be executed in status {job.status}",
            "Background Job Executor",
        )
        return

    # Check dependency
    if not _check_dependency(job):
        return

    # Check circuit breaker
    try:
        check_circuit_breaker(job.job_type, job.organization)
    except CircuitBreakerOpen as e:
        # Circuit is open - don't execute, mark as failed
        job.status = "Dead Letter"
        job.error_message = str(e)
        job.error_type = ERROR_TYPE_CIRCUIT_BREAKER
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
        timeout_seconds=job.timeout_seconds if job.timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS,
    )

    # Execute with timeout
    try:
        result = _execute_with_timeout(handler, context, context.timeout_seconds)
        _handle_success(job, result)
    except JobCanceledError:
        _handle_canceled(job)
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

    # Parent still in progress (Pending/Queued/Running)
    # Schedule retry so scheduler picks this job up again after delay
    # This prevents orphaned jobs that would otherwise wait forever
    job.next_retry_at = add_to_date(now_datetime(), seconds=DEPENDENCY_RETRY_DELAY_SECONDS)
    job.save(ignore_permissions=True)
    frappe.db.commit()
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

    # Record execution metrics
    _record_job_metrics(job)

    # Record successful outcome for circuit breaker
    record_job_outcome(job.job_type, job.organization, success=True)


def _call_timeout_handler(job):
    """
    Call the timeout handler for a job if configured.

    The timeout handler can perform cleanup operations when a job times out,
    such as releasing resources, canceling external API calls, etc.

    Args:
        job: Background Job document that timed out
    """
    try:
        from dartwing.dartwing_core.doctype.job_type.job_type import get_timeout_handler

        timeout_handler = get_timeout_handler(job.job_type)
        if not timeout_handler:
            return

        # Create a minimal context with job information
        context = JobContext(
            job_id=job.name,
            job_type=job.job_type,
            organization=job.organization,
            parameters=frappe.parse_json(job.input_parameters) if job.input_parameters else {},
            timeout_seconds=job.timeout_seconds if job.timeout_seconds is not None else DEFAULT_TIMEOUT_SECONDS,
        )

        # Call timeout handler (best effort - don't fail if cleanup fails)
        timeout_handler(context)

    except Exception as e:
        # Log but don't raise - timeout handler failures shouldn't prevent retry scheduling
        frappe.log_error(
            f"Timeout handler failed for job {job.name}: {str(e)}",
            "Background Job Timeout Handler",
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

    # Call timeout handler if configured
    _call_timeout_handler(job)

    # Record execution metrics
    _record_job_metrics(job)

    # Record failed outcome for circuit breaker
    record_job_outcome(job.job_type, job.organization, success=False)

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

    # Record execution metrics
    _record_job_metrics(job)

    # Record failed outcome for circuit breaker
    record_job_outcome(job.job_type, job.organization, success=False)

    # Schedule retry if transient failure
    if job.status == "Failed":
        from dartwing.dartwing_core.background_jobs.retry import schedule_retry

        schedule_retry(job.name)

    # Log error for debugging
    frappe.log_error(
        f"Job {job.name} failed: {error}",
        "Background Job Executor",
    )


def _record_job_metrics(job):
    """
    Record execution metrics for monitoring and analytics.

    Calculates execution time and records metrics for performance tracking.
    This is best-effort and won't fail the job if metrics recording fails.

    Args:
        job: Background Job document with started_at and completed_at set
    """
    try:
        if not job.started_at or not job.completed_at:
            return

        execution_time = (job.completed_at - job.started_at).total_seconds()

        from dartwing.dartwing_core.background_jobs.metrics import record_execution_metrics

        record_execution_metrics(
            job_id=job.name,
            execution_time_seconds=execution_time,
            status=job.status,
            # error_type is only set for failures (timeout/error), not for successful completions
            error_type=getattr(job, 'error_type', None),
        )
    except Exception as e:
        # Metrics recording is best-effort - don't fail the job
        frappe.log_error(
            f"Failed to record metrics for job {job.name}: {str(e)}",
            "Background Job Metrics",
        )


def _handle_canceled(job) -> None:
    """Handle job cancellation from within a running handler."""
    job.reload()
    if job.status == "Canceled":
        return

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
