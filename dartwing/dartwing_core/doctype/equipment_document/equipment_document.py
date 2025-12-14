# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

from frappe.model.document import Document


class EquipmentDocument(Document):
    """Equipment Document child table for attaching documents to equipment.

    Fields:
        document_type: Classification (Manual, Warranty, Receipt, Inspection Report, Other)
        file: Attached file
    """

    pass
