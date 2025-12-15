"""
Background Job Controller.

Core entity representing a single unit of asynchronous work with state machine
validation and organization scoping.
"""

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


# Valid status transitions
VALID_TRANSITIONS = {
    None: ["Pending"],  # Creation
    "Pending": ["Queued", "Canceled"],
    "Queued": ["Running", "Canceled"],
    "Running": ["Completed", "Failed", "Dead Letter", "Canceled", "Timed Out"],
    "Failed": ["Queued", "Dead Letter"],  # Retry or exhaust
    "Timed Out": ["Queued", "Dead Letter"],  # Retry or exhaust
    # Terminal states - no outgoing transitions
    "Completed": [],
    "Dead Letter": ["Queued"],  # Admin can retry
    "Canceled": [],
}


class BackgroundJob(Document):
    def validate(self):
        self.validate_organization()
        self.validate_job_type()
        self.validate_depends_on()
        self.validate_status_transition()
        self.set_defaults()

    def validate_organization(self):
        """Ensure organization exists and is active."""
        if not self.organization:
            return

        org = frappe.db.get_value("Organization", self.organization, ["name", "status"], as_dict=True)
        if not org:
            frappe.throw(_("Organization '{0}' not found").format(self.organization))

        # Check if organization is suspended
        if org.get("status") == "Suspended":
            frappe.throw(_("Cannot create jobs for suspended organization '{0}'").format(self.organization))

    def validate_job_type(self):
        """Ensure job type exists and is enabled."""
        if not self.job_type:
            return

        job_type = frappe.db.get_value("Job Type", self.job_type, ["name", "is_enabled"], as_dict=True)
        if not job_type:
            frappe.throw(_("Job Type '{0}' not found").format(self.job_type))

        if not job_type.get("is_enabled"):
            frappe.throw(_("Job Type '{0}' is disabled").format(self.job_type))

    def validate_depends_on(self):
        """Ensure dependency is valid."""
        if not self.depends_on:
            return

        # Cannot depend on self
        if self.depends_on == self.name:
            frappe.throw(_("Job cannot depend on itself"))

        # Must be in same organization
        parent_org = frappe.db.get_value("Background Job", self.depends_on, "organization")
        if parent_org and parent_org != self.organization:
            frappe.throw(_("Dependent job must be in the same organization"))

    def validate_status_transition(self):
        """Ensure status transitions follow state machine rules."""
        if self.is_new():
            # New record - must start in Pending
            if self.status != "Pending":
                self.status = "Pending"
            return

        # Get previous status from database
        old_status = frappe.db.get_value("Background Job", self.name, "status")
        if old_status == self.status:
            return  # No change

        valid_next = VALID_TRANSITIONS.get(old_status, [])
        if self.status not in valid_next:
            frappe.throw(
                _("Invalid status transition: {0} → {1}. Valid transitions: {2}").format(
                    old_status, self.status, ", ".join(valid_next) or "None"
                )
            )

    def set_defaults(self):
        """Set default values from job type if not provided."""
        if self.is_new():
            self.created_at = now_datetime()
            self.owner_user = self.owner_user or frappe.session.user

            if self.job_type:
                job_type = frappe.get_cached_doc("Job Type", self.job_type)
                if not self.timeout_seconds:
                    self.timeout_seconds = job_type.default_timeout or 300
                if not self.max_retries:
                    self.max_retries = job_type.max_retries or 5
                if not self.priority:
                    self.priority = job_type.default_priority or "Normal"

    def on_update(self):
        """Log state transitions for audit."""
        self.log_state_transition()

    def log_state_transition(self):
        """Create Job Execution Log entry for status changes."""
        if not hasattr(self, "_doc_before_save"):
            return

        old_status = self._doc_before_save.status if self._doc_before_save else None
        if old_status == self.status:
            return

        # Create log entry
        log = frappe.new_doc("Job Execution Log")
        log.background_job = self.name
        log.from_status = old_status
        log.to_status = self.status
        log.timestamp = now_datetime()
        log.actor = frappe.session.user
        log.message = self._get_transition_message(old_status, self.status)
        log.retry_attempt = self.retry_count if self.status == "Queued" and old_status == "Failed" else None
        log.insert(ignore_permissions=True)

    def _get_transition_message(self, from_status, to_status):
        """Generate human-readable transition message."""
        messages = {
            (None, "Pending"): "Job created",
            ("Pending", "Queued"): "Job enqueued",
            ("Queued", "Running"): "Worker started execution",
            ("Running", "Completed"): "Job completed successfully",
            ("Running", "Failed"): f"Job failed: {self.error_message or 'Unknown error'}",
            ("Running", "Dead Letter"): f"Job moved to dead letter: {self.error_message or 'Permanent failure'}",
            ("Running", "Timed Out"): f"Job timed out after {self.timeout_seconds}s",
            ("Running", "Canceled"): "Job canceled during execution",
            ("Pending", "Canceled"): "Job canceled before execution",
            ("Queued", "Canceled"): "Job canceled while queued",
            ("Failed", "Queued"): f"Job re-queued for retry (attempt {self.retry_count + 1})",
            ("Failed", "Dead Letter"): "Job exhausted retries, moved to dead letter",
            ("Timed Out", "Queued"): f"Timed out job re-queued for retry (attempt {self.retry_count + 1})",
            ("Timed Out", "Dead Letter"): "Timed out job exhausted retries",
            ("Dead Letter", "Queued"): "Admin re-queued dead letter job",
        }
        return messages.get((from_status, to_status), f"Status changed from {from_status} to {to_status}")

    def can_cancel(self):
        """Check if job can be canceled."""
        return self.status in ["Pending", "Queued", "Running"]

    def is_terminal(self):
        """Check if job is in a terminal state."""
        return self.status in ["Completed", "Dead Letter", "Canceled"]
