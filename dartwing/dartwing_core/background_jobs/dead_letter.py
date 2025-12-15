"""
Dead Letter Queue handling for Background Job Engine.

Dead letter is implemented as a status on Background Job doctype,
not a separate queue. This module provides utilities for managing
dead letter jobs.
"""

import frappe
from frappe import _


def get_dead_letter_jobs(organization: str = None, limit: int = 100) -> list:
    """
    Get jobs in dead letter queue.

    Args:
        organization: Filter by organization (admin sees all if None)
        limit: Maximum jobs to return

    Returns:
        List of dead letter job details
    """
    filters = {"status": "Dead Letter"}

    if organization:
        filters["organization"] = organization
    elif "System Manager" not in frappe.get_roles():
        # Non-admin must have organization filter
        orgs = frappe.get_all(
            "Org Member",
            filters={"user": frappe.session.user, "status": "Active"},
            pluck="organization",
        )
        if orgs:
            filters["organization"] = ("in", orgs)
        else:
            return []

    jobs = frappe.get_all(
        "Background Job",
        filters=filters,
        fields=[
            "name",
            "job_type",
            "organization",
            "error_message",
            "error_type",
            "retry_count",
            "created_at",
            "completed_at",
        ],
        order_by="completed_at desc",
        limit=limit,
    )

    return [
        {
            "job_id": j.name,
            "job_type": j.job_type,
            "organization": j.organization,
            "error_message": j.error_message,
            "error_type": j.error_type,
            "retry_count": j.retry_count,
            "created_at": str(j.created_at) if j.created_at else None,
            "failed_at": str(j.completed_at) if j.completed_at else None,
        }
        for j in jobs
    ]


def delete_dead_letter_job(job_id: str):
    """
    Delete a dead letter job (admin only).

    Args:
        job_id: Job to delete
    """
    if "System Manager" not in frappe.get_roles():
        frappe.throw(_("Only administrators can delete dead letter jobs"), frappe.PermissionError)

    job = frappe.get_doc("Background Job", job_id)

    if job.status != "Dead Letter":
        frappe.throw(_("Can only delete jobs in Dead Letter status"))

    frappe.delete_doc("Background Job", job_id, force=True)
    frappe.db.commit()


def bulk_retry_dead_letter(organization: str = None, job_type: str = None, limit: int = 50):
    """
    Bulk retry dead letter jobs (admin only).

    Args:
        organization: Filter by organization
        job_type: Filter by job type
        limit: Maximum jobs to retry

    Returns:
        Count of jobs retried
    """
    if "System Manager" not in frappe.get_roles():
        frappe.throw(_("Only administrators can bulk retry jobs"), frappe.PermissionError)

    from dartwing.dartwing_core.background_jobs.engine import retry_job

    filters = {"status": "Dead Letter"}
    if organization:
        filters["organization"] = organization
    if job_type:
        filters["job_type"] = job_type

    jobs = frappe.get_all(
        "Background Job",
        filters=filters,
        pluck="name",
        limit=limit,
    )

    retried = 0
    for job_id in jobs:
        try:
            retry_job(job_id)
            retried += 1
        except Exception as e:
            frappe.log_error(
                f"Failed to retry dead letter job {job_id}: {e}",
                "Dead Letter Bulk Retry",
            )

    frappe.db.commit()
    return retried
