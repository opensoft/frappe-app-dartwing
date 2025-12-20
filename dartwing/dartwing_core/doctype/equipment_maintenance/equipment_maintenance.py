# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class EquipmentMaintenance(Document):
    """Equipment Maintenance child table for scheduling maintenance tasks.

    Fields:
        task: Description of the maintenance task (required)
        frequency: How often (Daily, Weekly, Monthly, Quarterly, Yearly)
        next_due: Next scheduled date for the task
    """

    pass
