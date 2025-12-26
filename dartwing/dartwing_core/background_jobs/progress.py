"""
Progress tracking for Background Job Engine.

Provides JobContext for handlers to update progress and Socket.IO integration
for real-time updates to connected clients.
"""

import time
import threading
import frappe
from frappe.utils import now_datetime
from dataclasses import dataclass, field
from typing import Optional

from dartwing.dartwing_core.background_jobs.config import (
    DEFAULT_TIMEOUT_SECONDS,
    PROGRESS_THROTTLE_SECONDS,
)
from dartwing.dartwing_core.background_jobs.errors import JobCanceledError


@dataclass
class JobContext:
    """
    Context object passed to job handlers.

    Provides access to job parameters and methods to update progress.

    Thread Safety:
        JobContext instances now use a threading.Lock to protect access to the
        _last_broadcast field during throttling checks. This prevents race
        conditions when multiple threads call update_progress() concurrently.

        While update_progress() is now thread-safe for the throttling mechanism,
        be aware that:
        - Database updates are still not atomic across threads
        - Multiple threads updating progress rapidly may still cause race conditions
          in the database layer

        Best practice: Call update_progress() from a single thread when possible

    Usage:
        def my_job_handler(context: JobContext):
            params = context.parameters
            context.update_progress(10, "Starting...")

            # Do work
            result = process(params["input"])

            context.update_progress(100, "Done!")
            return {"output_reference": result}
    """

    job_id: str
    job_type: str
    organization: str
    parameters: dict = field(default_factory=dict)
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    _canceled: bool = field(default=False, repr=False)
    _last_broadcast: float = field(default=0.0, repr=False)
    _broadcast_lock: threading.Lock = field(default_factory=threading.Lock, repr=False)

    def update_progress(self, percent: int, message: Optional[str] = None, force: bool = False) -> None:
        """
        Update job progress and broadcast to connected clients.

        Progress updates are throttled to max once per PROGRESS_THROTTLE_SECONDS
        to prevent flooding Socket.IO with high-frequency updates. The database
        is always updated, but broadcasts are rate-limited.

        Note: Progress updates use update_modified=False to avoid unnecessary
        database overhead. Progress data is eventually consistent and may not
        survive job crashes. For critical state that must persist across
        failures, use checkpoints stored in input_parameters or external storage.

        Args:
            percent: Progress percentage (0-100)
            message: Optional status message describing current step
            force: If True, bypass throttling and always broadcast (use for 100%)

        Raises:
            JobCanceledError: If job has been marked for cancellation
        """
        # Check for cancellation at checkpoint
        if self.is_canceled():
            raise JobCanceledError("Job was canceled")

        # Clamp percent to valid range
        percent = max(0, min(100, percent))

        # Update database (always)
        frappe.db.set_value(
            "Background Job",
            self.job_id,
            {"progress": percent, "progress_message": message},
            update_modified=False,
        )

        # Throttle Socket.IO broadcasts to prevent flooding
        # Always broadcast at 100% completion or if forced
        # Use lock to prevent race conditions when checking/updating _last_broadcast
        with self._broadcast_lock:
            current_time = time.time()
            should_broadcast = (
                force
                or percent == 100
                or (current_time - self._last_broadcast) >= PROGRESS_THROTTLE_SECONDS
            )

            if should_broadcast:
                self._last_broadcast = current_time

        # Broadcast outside the lock to avoid holding it during I/O
        if should_broadcast:
            publish_job_progress(
                job_id=self.job_id,
                organization=self.organization,
                status="Running",
                progress=percent,
                progress_message=message,
            )

    def is_canceled(self) -> bool:
        """
        Check if job has been marked for cancellation.

        Returns:
            True if job should stop, False otherwise
        """
        if self._canceled:
            return True

        # Check database for cancellation flag
        status = frappe.db.get_value("Background Job", self.job_id, "status")
        if status == "Canceled":
            self._canceled = True
            return True

        return False


def _validate_broadcast_params(job_id: str, organization: str) -> bool:
    """
    Validate job exists and belongs to claimed organization.

    This security check prevents cross-tenant data leakage via Socket.IO.
    An attacker cannot spoof organization IDs to receive job updates
    from other organizations.

    Returns:
        True if valid (job exists and belongs to organization)
        False if invalid (silently fail to avoid exposing validation to attackers)
    """
    if not frappe.db.exists("Organization", organization):
        return False
    job_org = frappe.db.get_value("Background Job", job_id, "organization")
    return job_org == organization


def publish_job_progress(
    job_id: str,
    organization: str,
    status: str,
    progress: int,
    progress_message: Optional[str] = None,
) -> None:
    """
    Publish job progress update via Socket.IO.

    Args:
        job_id: Background Job ID
        organization: Organization name for room scoping
        status: Current job status
        progress: Progress percentage
        progress_message: Optional progress description
    """
    # Security: Validate job belongs to claimed organization
    if not _validate_broadcast_params(job_id, organization):
        return  # Silent fail - don't expose validation to attackers

    frappe.publish_realtime(
        event="job_progress",
        message={
            "job_id": job_id,
            "status": status,
            "progress": progress,
            "progress_message": progress_message,
            "updated_at": str(now_datetime()),
        },
        room=f"org:{organization}",
    )


def publish_job_status_changed(
    job_id: str,
    organization: str,
    from_status: str,
    to_status: str,
    output_reference: Optional[str] = None,
    error_message: Optional[str] = None,
) -> None:
    """
    Publish job status change event via Socket.IO.

    Args:
        job_id: Background Job ID
        organization: Organization name for room scoping
        from_status: Previous status
        to_status: New status
        output_reference: Optional output reference for completed jobs
        error_message: Optional error message for failed jobs
    """
    # Security: Validate job belongs to claimed organization
    if not _validate_broadcast_params(job_id, organization):
        return  # Silent fail - don't expose validation to attackers

    message = {
        "job_id": job_id,
        "from_status": from_status,
        "to_status": to_status,
        "updated_at": str(now_datetime()),
    }

    if output_reference:
        message["output_reference"] = output_reference

    if error_message:
        message["error_message"] = error_message

    frappe.publish_realtime(
        event="job_status_changed",
        message=message,
        room=f"org:{organization}",
    )
