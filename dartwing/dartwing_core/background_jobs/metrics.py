"""
Metrics for Background Job Engine.

Provides operational metrics for monitoring job queue health.
"""

import frappe
from frappe.utils import now_datetime, add_to_date


def get_metrics(organization: str = None) -> dict:
    """
    Get operational metrics for job monitoring.

    Args:
        organization: Filter by organization (admin sees all if None)

    Returns:
        Dict with job_count_by_status, queue_depth_by_priority,
        processing_time, failure_rate_by_type
    """
    filters = {}
    if organization:
        filters["organization"] = organization
    elif "System Manager" not in frappe.get_roles():
        # Non-admin must have organization filter
        # Find Person linked to current user, then get their org memberships
        person = frappe.db.get_value("Person", {"frappe_user": frappe.session.user}, "name")
        if person:
            orgs = frappe.get_all(
                "Org Member",
                filters={"person": person, "status": "Active"},
                pluck="organization",
            )
        else:
            orgs = []

        if orgs:
            filters["organization"] = ("in", orgs)
        else:
            return _empty_metrics()

    return {
        "job_count_by_status": _get_job_count_by_status(filters),
        "queue_depth_by_priority": _get_queue_depth_by_priority(filters),
        "processing_time": _get_processing_time(filters),
        "failure_rate_by_type": _get_failure_rate_by_type(filters),
        "timestamp": str(now_datetime()),
    }


def _apply_organization_filter(filters: dict, conditions: list[str], values: dict) -> None:
    """
    Apply organization filter to SQL conditions + parameter dict.

    Supports:
    - filters["organization"] = "ORG-001"
    - filters["organization"] = ("in", ["ORG-001", "ORG-002"])
    """
    org_filter = filters.get("organization")
    if not org_filter:
        return

    if isinstance(org_filter, tuple):
        orgs = list(org_filter[1] or [])
        if not orgs:
            conditions.append("1=0")
            return

        placeholders = []
        for idx, org in enumerate(orgs):
            key = f"org_{idx}"
            placeholders.append(f"%({key})s")
            values[key] = org

        conditions.append(f"organization IN ({', '.join(placeholders)})")
        return

    conditions.append("organization = %(org)s")
    values["org"] = org_filter


def _empty_metrics() -> dict:
    """Return empty metrics structure."""
    return {
        "job_count_by_status": {},
        "queue_depth_by_priority": {},
        "processing_time": {"average_seconds": 0, "p95_seconds": 0},
        "failure_rate_by_type": {},
        "timestamp": str(now_datetime()),
    }


def _get_job_count_by_status(filters: dict) -> dict:
    """Get count of jobs by status with parameterized queries."""
    conditions = ["1=1"]
    values = {}

    _apply_organization_filter(filters, conditions, values)

    result = frappe.db.sql(
        f"""
        SELECT status, COUNT(*) as count
        FROM `tabBackground Job`
        WHERE {" AND ".join(conditions)}
        GROUP BY status
        """,
        values,
        as_dict=True,
    )

    return {row.status: row.count for row in result}


def _get_queue_depth_by_priority(filters: dict) -> dict:
    """Get count of queued jobs by priority with parameterized queries."""
    conditions = ["status IN ('Pending', 'Queued')"]
    values = {}

    _apply_organization_filter(filters, conditions, values)

    result = frappe.db.sql(
        f"""
        SELECT priority, COUNT(*) as count
        FROM `tabBackground Job`
        WHERE {" AND ".join(conditions)}
        GROUP BY priority
        """,
        values,
        as_dict=True,
    )

    return {row.priority: row.count for row in result}


def _get_processing_time(filters: dict) -> dict:
    """Get average and p95 processing time for completed jobs in last hour."""
    conditions = ["status = 'Completed'", "completed_at >= %(one_hour_ago)s", "started_at IS NOT NULL"]
    values = {}

    _apply_organization_filter(filters, conditions, values)

    one_hour_ago = add_to_date(now_datetime(), hours=-1)
    values["one_hour_ago"] = one_hour_ago

    result = frappe.db.sql(
        f"""
        SELECT
            AVG(TIMESTAMPDIFF(SECOND, started_at, completed_at)) as avg_seconds,
            COUNT(*) as total_count
        FROM `tabBackground Job`
        WHERE {" AND ".join(conditions)}
        """,
        values,
        as_dict=True,
    )

    avg_seconds = result[0].avg_seconds if result and result[0].avg_seconds else 0

    # Get p95 using a percentile approach
    p95_result = frappe.db.sql(
        f"""
        SELECT TIMESTAMPDIFF(SECOND, started_at, completed_at) as duration
        FROM `tabBackground Job`
        WHERE {" AND ".join(conditions)}
        ORDER BY duration
        """,
        values,
        as_list=True,
    )

    p95_seconds = 0
    if p95_result:
        durations = [r[0] for r in p95_result if r[0] is not None]
        if durations:
            p95_index = int(len(durations) * 0.95)
            p95_seconds = durations[min(p95_index, len(durations) - 1)]

    return {
        "average_seconds": round(avg_seconds, 2) if avg_seconds else 0,
        "p95_seconds": round(p95_seconds, 2) if p95_seconds else 0,
    }


def _get_failure_rate_by_type(filters: dict) -> dict:
    """Get failure rate by job type for jobs in last 24 hours."""
    conditions = ["created_at >= %(one_day_ago)s"]
    values = {}

    _apply_organization_filter(filters, conditions, values)

    one_day_ago = add_to_date(now_datetime(), hours=-24)
    values["one_day_ago"] = one_day_ago

    result = frappe.db.sql(
        f"""
        SELECT
            job_type,
            COUNT(*) as total,
            SUM(CASE WHEN status IN ('Failed', 'Dead Letter', 'Timed Out') THEN 1 ELSE 0 END) as failed
        FROM `tabBackground Job`
        WHERE {" AND ".join(conditions)}
        GROUP BY job_type
        HAVING total > 0
        """,
        values,
        as_dict=True,
    )

    return {
        row.job_type: round(row.failed / row.total, 4) if row.total else 0
        for row in result
    }
