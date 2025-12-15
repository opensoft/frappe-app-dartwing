"""
Scheduler for Background Job Engine.

Provides scheduled tasks for retry processing and other maintenance.
"""

import frappe


def process_retry_queue():
    """
    Scheduled task: Process jobs ready for retry.

    This should be called every minute by Frappe's scheduler.
    """
    from dartwing.dartwing_core.background_jobs.retry import process_retry_queue as do_process

    try:
        do_process()
    except Exception as e:
        frappe.log_error(
            f"Error processing retry queue: {e}",
            "Background Job Scheduler",
        )


def process_dependent_jobs():
    """
    Scheduled task: Check dependent jobs that may be ready to run.

    This checks jobs that are waiting on a parent job and enqueues them
    if the parent has completed.
    """
    from dartwing.dartwing_core.background_jobs.engine import _enqueue_job

    # Find queued jobs with dependencies that are now satisfied
    jobs = frappe.db.sql(
        """
        SELECT bj.name, bj.depends_on
        FROM `tabBackground Job` bj
        INNER JOIN `tabBackground Job` parent ON bj.depends_on = parent.name
        WHERE bj.status = 'Queued'
        AND bj.depends_on IS NOT NULL
        AND parent.status = 'Completed'
        LIMIT 100
        """,
        as_dict=True,
    )

    for job_data in jobs:
        try:
            job = frappe.get_doc("Background Job", job_data.name)
            _enqueue_job(job)
        except Exception as e:
            frappe.log_error(
                f"Failed to enqueue dependent job {job_data.name}: {e}",
                "Background Job Scheduler",
            )

    if jobs:
        frappe.db.commit()
