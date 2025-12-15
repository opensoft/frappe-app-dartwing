"""
Retry Policy for Background Job Engine.

Implements exponential backoff with jitter for transient failures.
"""

import random
import frappe
from frappe.utils import now_datetime, add_to_date


def calculate_backoff(attempt: int, base_delay: int = 60) -> int:
    """
    Calculate retry delay with exponential backoff and jitter.

    Args:
        attempt: Current retry attempt (1-based)
        base_delay: Base delay in seconds (default: 60)

    Returns:
        Delay in seconds with ±20% jitter

    Examples:
        attempt=1: ~60s (48s - 72s)
        attempt=2: ~120s (96s - 144s)
        attempt=3: ~240s (192s - 288s)
        attempt=4: ~480s (384s - 576s)
        attempt=5: ~960s (768s - 1152s)
    """
    delay = base_delay * (2 ** (attempt - 1))
    jitter = delay * 0.2 * (random.random() * 2 - 1)  # ±20%
    return max(1, int(delay + jitter))


def schedule_retry(job_id: str):
    """
    Schedule a retry for a failed job.

    Increments retry count, calculates backoff delay, and schedules
    the job to be picked up by the retry scheduler.

    Args:
        job_id: Background Job ID
    """
    job = frappe.get_doc("Background Job", job_id)

    # Check if we've exhausted retries
    if job.retry_count >= job.max_retries:
        _move_to_dead_letter(job)
        return

    # Calculate next retry time
    job.retry_count = (job.retry_count or 0) + 1
    backoff_seconds = calculate_backoff(job.retry_count)
    job.next_retry_at = add_to_date(now_datetime(), seconds=backoff_seconds)

    # Keep in Failed/Timed Out status until retry time
    job.save(ignore_permissions=True)
    frappe.db.commit()


def _move_to_dead_letter(job):
    """Move job to dead letter queue after exhausting retries."""
    from dartwing.dartwing_core.background_jobs.progress import publish_job_status_changed

    old_status = job.status
    job.status = "Dead Letter"
    job.next_retry_at = None
    job.save(ignore_permissions=True)
    frappe.db.commit()

    publish_job_status_changed(
        job_id=job.name,
        organization=job.organization,
        from_status=old_status,
        to_status="Dead Letter",
        error_message=f"Exhausted {job.max_retries} retries: {job.error_message}",
    )


def process_retry_queue():
    """
    Process jobs that are ready for retry.

    This function is called by the scheduler to re-queue jobs that have
    passed their retry wait time.
    """
    now = now_datetime()

    # Find jobs ready for retry
    jobs = frappe.get_all(
        "Background Job",
        filters={
            "status": ("in", ["Failed", "Timed Out"]),
            "next_retry_at": ("<=", now),
        },
        fields=["name", "organization", "status"],
        limit=100,  # Process in batches
    )

    for job_data in jobs:
        try:
            _retry_job(job_data.name, job_data.organization, job_data.status)
        except Exception as e:
            frappe.log_error(
                f"Failed to retry job {job_data.name}: {e}",
                "Background Job Retry Scheduler",
            )


def _retry_job(job_id: str, organization: str, old_status: str):
    """Re-queue a single job for retry."""
    from dartwing.dartwing_core.background_jobs.progress import publish_job_status_changed
    from dartwing.dartwing_core.background_jobs.engine import _enqueue_job

    job = frappe.get_doc("Background Job", job_id)

    # Clear error state for retry
    job.status = "Queued"
    job.next_retry_at = None
    job.error_message = None
    job.error_type = None
    job.save(ignore_permissions=True)

    # Re-enqueue
    _enqueue_job(job, is_retry=True)

    frappe.db.commit()
