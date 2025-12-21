"""
Cleanup for Background Job Engine.

Provides data retention cleanup for old job records.
"""

import frappe
from frappe.utils import add_to_date, now_datetime

from dartwing.dartwing_core.background_jobs.config import (
    CLEANUP_BATCH_SIZE,
    DEFAULT_RETENTION_DAYS,
)


def cleanup_old_jobs(retention_days: int = DEFAULT_RETENTION_DAYS, batch_size: int = CLEANUP_BATCH_SIZE):
    """
    Delete completed/failed jobs older than retention period.

    Uses batched commits to prevent long-running transactions and lock timeouts.

    Args:
        retention_days: Number of days to retain jobs (default: 30)
        batch_size: Number of deletions per commit (default: 100)

    Returns:
        Count of jobs deleted
    """
    cutoff_date = add_to_date(now_datetime(), days=-retention_days)

    # Get jobs to delete (terminal states only)
    jobs = frappe.get_all(
        "Background Job",
        filters={
            "status": ("in", ["Completed", "Dead Letter", "Canceled"]),
            "modified": ("<", cutoff_date),
        },
        pluck="name",
        limit=1000,  # Delete in batches
    )

    deleted_count = 0
    for i, job_id in enumerate(jobs):
        try:
            frappe.delete_doc("Background Job", job_id, force=True, delete_permanently=True)
            deleted_count += 1

            # Commit every batch_size deletions to prevent long transactions
            if (i + 1) % batch_size == 0:
                frappe.db.commit()
        except Exception as e:
            frappe.log_error(
                f"Failed to delete old job {job_id}: {e}",
                "Background Job Cleanup",
            )

    # Final commit for remaining deletions
    if deleted_count > 0 and deleted_count % batch_size != 0:
        frappe.db.commit()

    return deleted_count


def daily_cleanup():
    """
    Scheduled task: Run daily cleanup of old jobs.

    This is called by Frappe's scheduler daily.
    """
    try:
        deleted = cleanup_old_jobs()
        if deleted:
            frappe.logger().info(f"Background Job Cleanup: Deleted {deleted} old jobs")
    except Exception as e:
        frappe.log_error(
            f"Error during job cleanup: {e}",
            "Background Job Cleanup",
        )
