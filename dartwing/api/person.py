# Copyright (c) 2025, Opensoft and contributors
# For license information, please see license.txt

"""
API endpoints for Person DocType.

All endpoints follow Frappe's @frappe.whitelist() convention.
See specs/001-person-doctype/contracts/person-api.yaml for full API contract.
"""

import frappe
from frappe import _
from frappe.utils import now

from dartwing.dartwing_core.doctype.person.person import _has_org_member_doctype

# Note: Using cached DocType existence checks for performance.
# The doctype_table_exists() utility is for low-level table existence checks.


@frappe.whitelist()
def capture_consent(person_name: str) -> dict:
    """Capture consent for a minor Person.

    This is the only write operation allowed on a minor without consent.
    Per contracts/person-api.yaml: POST /api/method/dartwing.api.person.capture_consent

    Args:
        person_name: The name (ID) of the Person document

    Returns:
        dict: Success status and consent timestamp

    Raises:
        frappe.DoesNotExistError: If Person not found
        frappe.ValidationError: If Person is not a minor or consent already captured
    """
    if not person_name:
        frappe.throw(_("person_name is required"), frappe.ValidationError)

    if not frappe.db.exists("Person", person_name):
        frappe.throw(
            _("Person {0} not found").format(person_name), frappe.DoesNotExistError
        )

    person = frappe.get_doc("Person", person_name)

    if not person.is_minor:
        frappe.throw(
            _("Person {0} is not a minor").format(person_name), frappe.ValidationError
        )

    if person.consent_captured:
        frappe.throw(
            _("Consent already captured for Person {0}").format(person_name),
            frappe.ValidationError,
        )

    # Capture consent - this bypasses the minor consent block check
    # because we're specifically changing consent_captured to True
    consent_time = now()
    person.consent_captured = 1
    person.consent_timestamp = consent_time
    person.save(ignore_permissions=True)

    return {"success": True, "consent_timestamp": consent_time}


@frappe.whitelist()
def get_sync_status(person_name: str) -> dict:
    """Get Person sync status for Frappe User creation.

    Per contracts/person-api.yaml: GET /api/method/dartwing.api.person.get_sync_status

    Args:
        person_name: The name (ID) of the Person document

    Returns:
        dict: Sync status details including user_sync_status, frappe_user,
              sync_error_message, and last_sync_at
    """
    if not person_name:
        frappe.throw(_("person_name is required"), frappe.ValidationError)

    if not frappe.db.exists("Person", person_name):
        frappe.throw(
            _("Person {0} not found").format(person_name), frappe.DoesNotExistError
        )

    person = frappe.get_doc("Person", person_name)

    return {
        "person_name": person.name,
        "user_sync_status": person.user_sync_status,
        "frappe_user": person.frappe_user,
        "sync_error_message": person.sync_error_message,
        "last_sync_at": person.last_sync_at,
    }


@frappe.whitelist()
def retry_sync(person_name: str) -> dict:
    """Manually trigger a retry of Frappe User creation.

    Per contracts/person-api.yaml: POST /api/method/dartwing.api.person.retry_sync

    Args:
        person_name: The name (ID) of the Person document

    Returns:
        dict: Success status and message

    Raises:
        frappe.DoesNotExistError: If Person not found
        frappe.ValidationError: If Person is already synced or has no keycloak_user_id
    """
    if not person_name:
        frappe.throw(_("person_name is required"), frappe.ValidationError)

    if not frappe.db.exists("Person", person_name):
        frappe.throw(
            _("Person {0} not found").format(person_name), frappe.DoesNotExistError
        )

    person = frappe.get_doc("Person", person_name)

    if person.user_sync_status == "synced":
        frappe.throw(
            _("Person {0} is already synced").format(person_name),
            frappe.ValidationError,
        )

    if not person.keycloak_user_id:
        frappe.throw(
            _("Person {0} has no keycloak_user_id").format(person_name),
            frappe.ValidationError,
        )

    # Queue the sync job
    from dartwing.utils.person_sync import queue_user_sync

    queue_user_sync(person_name, attempt=1)

    return {
        "success": True,
        "message": _("Sync job queued for Person {0}").format(person_name),
    }


@frappe.whitelist()
def merge_persons(source_person: str, target_person: str, notes: str = None) -> dict:
    """Merge source Person into target Person.

    Per contracts/person-api.yaml: POST /api/method/dartwing.api.person.merge_persons

    - Transfers all Org Member links to target
    - Creates audit log entry on target
    - Sets source status to "Merged"

    Args:
        source_person: Name of Person to merge from (will be marked Merged)
        target_person: Name of Person to merge into (survives)
        notes: Optional notes about the merge

    Returns:
        dict: Success status, source, target, and count of transferred Org Members
    """
    if not source_person or not target_person:
        frappe.throw(
            _("source_person and target_person are required"), frappe.ValidationError
        )

    if source_person == target_person:
        frappe.throw(_("Cannot merge a Person into itself"), frappe.ValidationError)

    if not frappe.db.exists("Person", source_person):
        frappe.throw(
            _("Source Person {0} not found").format(source_person),
            frappe.DoesNotExistError,
        )

    if not frappe.db.exists("Person", target_person):
        frappe.throw(
            _("Target Person {0} not found").format(target_person),
            frappe.DoesNotExistError,
        )

    source = frappe.get_doc("Person", source_person)
    target = frappe.get_doc("Person", target_person)

    if source.status == "Merged":
        frappe.throw(
            _("Source Person {0} has already been merged").format(source_person),
            frappe.ValidationError,
        )

    # Transfer Org Member links (if Org Member DocType exists - cached check)
    org_members_transferred = 0
    if _has_org_member_doctype():
        org_members = frappe.get_all(
            "Org Member", filters={"person": source_person}, pluck="name"
        )
        if org_members:
            frappe.db.update(
                "Org Member",
                filters={"person": source_person},
                values={"person": target_person},
            )
            org_members_transferred = len(org_members)

    # Create merge log entry on target
    target.append(
        "merge_logs",
        {
            "source_person": source_person,
            "target_person": target_person,
            "merged_at": now(),
            "merged_by": frappe.session.user,
            "notes": notes,
        },
    )
    target.save(ignore_permissions=True)

    # Mark source as Merged
    source.status = "Merged"
    source.save(ignore_permissions=True)

    frappe.db.commit()

    return {
        "success": True,
        "source": source_person,
        "target": target_person,
        "org_members_transferred": org_members_transferred,
    }
