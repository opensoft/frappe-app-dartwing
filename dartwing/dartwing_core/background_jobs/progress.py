"""
Progress tracking for Background Job Engine.

Provides JobContext for handlers to update progress and Socket.IO integration
for real-time updates to connected clients.
"""

import frappe
from frappe.utils import now_datetime
from dataclasses import dataclass, field
from typing import Optional

from dartwing.dartwing_core.background_jobs.errors import JobCanceledError


@dataclass
class JobContext:
    """
    Context object passed to job handlers.

    Provides access to job parameters and methods to update progress.

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
    timeout_seconds: int = 300
    _canceled: bool = field(default=False, repr=False)

    def update_progress(self, percent: int, message: Optional[str] = None) -> None:
        """
        Update job progress and broadcast to connected clients.

        Note: Progress updates are buffered and use update_modified=False to avoid
        unnecessary database overhead. Progress data is eventually consistent and
        may not survive job crashes. For critical state that must persist across
        failures, use checkpoints stored in input_parameters or external storage.

        Args:
            percent: Progress percentage (0-100)
            message: Optional status message describing current step

        Raises:
            JobCanceledError: If job has been marked for cancellation
        """
        # Check for cancellation at checkpoint
        if self.is_canceled():
            raise JobCanceledError("Job was canceled")

        # Clamp percent to valid range
        percent = max(0, min(100, percent))

        # Update database
        frappe.db.set_value(
            "Background Job",
            self.job_id,
            {"progress": percent, "progress_message": message},
            update_modified=False,
        )

        # Broadcast progress update via Socket.IO
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
