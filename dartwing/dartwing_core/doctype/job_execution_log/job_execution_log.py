"""
Job Execution Log Controller.

Audit trail recording all job state transitions.
"""

import frappe
from frappe.model.document import Document


class JobExecutionLog(Document):
    pass
