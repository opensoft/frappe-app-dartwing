"""
Job Type Controller.

Defines categories of background work with configuration for timeout,
retry policy, and priority.
"""

import frappe
from frappe import _
from frappe.model.document import Document


class JobType(Document):
    def validate(self):
        self.validate_handler_method()
        self.validate_timeout()
        self.validate_max_retries()

    def validate_handler_method(self):
        """Ensure handler method path is valid Python dotted path."""
        if not self.handler_method:
            return

        parts = self.handler_method.split(".")
        if len(parts) < 2:
            frappe.throw(
                _("Handler method must be a dotted Python path (e.g., module.function)")
            )

        # Check for valid identifier characters
        for part in parts:
            if not part.isidentifier():
                frappe.throw(
                    _("Invalid handler method path: '{0}' is not a valid identifier").format(part)
                )

    def validate_timeout(self):
        """Ensure timeout is reasonable."""
        if self.default_timeout is not None and self.default_timeout < 1:
            frappe.throw(_("Timeout must be at least 1 second"))

        # Max timeout is 24 hours
        if self.default_timeout and self.default_timeout > 86400:
            frappe.throw(_("Timeout cannot exceed 24 hours (86400 seconds)"))

    def validate_max_retries(self):
        """Ensure max retries is reasonable."""
        if self.max_retries is not None and self.max_retries < 0:
            frappe.throw(_("Max retries cannot be negative"))

        # Cap at 10 retries
        if self.max_retries and self.max_retries > 10:
            frappe.throw(_("Max retries cannot exceed 10"))

    def before_delete(self):
        """Prevent deletion if jobs reference this type."""
        jobs_count = frappe.db.count("Background Job", {"job_type": self.name})
        if jobs_count > 0:
            frappe.throw(
                _("Cannot delete Job Type '{0}' - {1} jobs reference it").format(
                    self.name, jobs_count
                )
            )


def get_handler(job_type: str):
    """
    Get the handler function for a job type.

    Args:
        job_type: Job type name

    Returns:
        callable: The handler function

    Raises:
        frappe.DoesNotExistError: If job type not found
        ImportError: If handler module not found
        AttributeError: If handler function not found
    """
    job_type_doc = frappe.get_doc("Job Type", job_type)

    if not job_type_doc.is_enabled:
        frappe.throw(_("Job Type '{0}' is disabled").format(job_type))

    handler_path = job_type_doc.handler_method
    module_path, func_name = handler_path.rsplit(".", 1)

    module = frappe.get_module(module_path)
    return getattr(module, func_name)
