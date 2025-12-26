"""
Metrics for Background Job Engine.

Provides operational metrics for monitoring job queue health, including
execution time tracking and performance analytics.
"""

import frappe
from frappe.utils import now_datetime, add_to_date
from typing import Optional, List


def _calculate_percentile(values: List[float], percentile: float) -> float:
    """
    Calculate a percentile from a sorted or unsorted list of values.

    Args:
        values: List of numeric values
        percentile: Percentile to calculate (0.0 to 1.0, e.g., 0.95 for p95)

    Returns:
        The calculated percentile value, or 0 if the list is empty

    Note:
        Uses the proper percentile calculation: index = (len - 1) * percentile
        This avoids off-by-one errors and matches standard percentile algorithms.
    """
    if not values:
        return 0
    # Ensure values are sorted
    sorted_values = sorted(values)
    index = int((len(sorted_values) - 1) * percentile)
    return sorted_values[index]


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

    # Calculate p95 percentile using helper function
    durations = [r[0] for r in p95_result if r[0] is not None] if p95_result else []
    p95_seconds = _calculate_percentile(durations, 0.95)

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


def record_execution_metrics(
    job_id: str,
    execution_time_seconds: float,
    status: str,
    error_type: Optional[str] = None,
):
    """
    Record execution metrics for a completed job.

    This function stores execution time and outcome data that can be used for
    performance analysis, SLA monitoring, and identifying slow job types.

    Args:
        job_id: Background Job ID
        execution_time_seconds: Total execution time in seconds
        status: Final job status (Completed, Failed, Timed Out, etc.)
        error_type: Error classification if job failed (Transient, Permanent, etc.)

    Performance Considerations:
        This performs an individual database insert for each job completion.
        At high scale (hundreds/thousands of jobs per second), this could become
        a bottleneck. Consider these optimizations for high-volume scenarios:

        1. Batch metrics writes: Collect metrics in memory and flush periodically
        2. Async queue: Use a background queue (Redis, RabbitMQ) to decouple metrics
           recording from job execution
        3. Sampling: Record metrics for only a percentage of jobs
        4. Pre-aggregation: Calculate statistics in-memory and store summaries

    Note:
        This data is stored in a separate metrics table to avoid bloating the main
        Background Job table with historical data. Metrics can be aggregated and
        archived periodically.
    """
    try:
        job = frappe.get_doc("Background Job", job_id)

        # Create a metrics record (lightweight record for analytics)
        metrics_doc = frappe.get_doc({
            "doctype": "Background Job Metrics",
            "job_id": job_id,
            "job_type": job.job_type,
            "organization": job.organization,
            "priority": job.priority,
            "execution_time_seconds": execution_time_seconds,
            "status": status,
            "error_type": error_type,
            "recorded_at": now_datetime(),
        })
        metrics_doc.insert(ignore_permissions=True)
        frappe.db.commit()

    except Exception as e:
        # Metrics recording failures shouldn't break job execution
        frappe.log_error(
            f"Failed to record execution metrics for job {job_id}: {str(e)}",
            "Background Job Metrics",
        )


def get_execution_time_stats(
    organization: Optional[str] = None,
    job_type: Optional[str] = None,
    hours: int = 24,
) -> dict:
    """
    Get execution time statistics for jobs.

    Args:
        organization: Filter by organization (optional)
        job_type: Filter by job type (optional)
        hours: Time window in hours (default: 24)

    Returns:
        Dict with average, median, p50, p95, p99 execution times, and sample count
    """
    conditions = ["recorded_at >= %(time_threshold)s"]
    values = {"time_threshold": add_to_date(now_datetime(), hours=-hours)}

    if organization:
        conditions.append("organization = %(organization)s")
        values["organization"] = organization

    if job_type:
        conditions.append("job_type = %(job_type)s")
        values["job_type"] = job_type

    # Get basic stats
    result = frappe.db.sql(
        f"""
        SELECT
            AVG(execution_time_seconds) as avg_time,
            MIN(execution_time_seconds) as min_time,
            MAX(execution_time_seconds) as max_time,
            COUNT(*) as sample_count
        FROM `tabBackground Job Metrics`
        WHERE {" AND ".join(conditions)}
        """,
        values,
        as_dict=True,
    )

    if not result or not result[0].sample_count:
        return {
            "average_seconds": 0,
            "min_seconds": 0,
            "max_seconds": 0,
            "p50_seconds": 0,
            "p95_seconds": 0,
            "p99_seconds": 0,
            "sample_count": 0,
        }

    stats = result[0]

    # Get percentiles
    # NOTE: This loads all execution times into memory for sorting and percentile calculation.
    # For large datasets (thousands+ of jobs), this could be inefficient.
    # Performance improvement options:
    #   1. Use SQL window functions: PERCENT_RANK() or NTILE() (requires MySQL 8.0+/MariaDB 10.2+)
    #   2. Use sampling: SELECT ... ORDER BY RAND() LIMIT N for approximate percentiles
    #   3. Pre-aggregate percentiles in a separate summary table updated periodically
    percentiles_result = frappe.db.sql(
        f"""
        SELECT execution_time_seconds
        FROM `tabBackground Job Metrics`
        WHERE {" AND ".join(conditions)}
        ORDER BY execution_time_seconds
        """,
        values,
        as_list=True,
    )

    times = [r[0] for r in percentiles_result if r[0] is not None]

    # Calculate percentiles using helper function
    p50 = _calculate_percentile(times, 0.50)
    p95 = _calculate_percentile(times, 0.95)
    p99 = _calculate_percentile(times, 0.99)

    return {
        "average_seconds": round(stats.avg_time, 2) if stats.avg_time else 0,
        "min_seconds": round(stats.min_time, 2) if stats.min_time else 0,
        "max_seconds": round(stats.max_time, 2) if stats.max_time else 0,
        "p50_seconds": round(p50, 2),
        "p95_seconds": round(p95, 2),
        "p99_seconds": round(p99, 2),
        "sample_count": stats.sample_count,
    }


def get_slowest_jobs(
    organization: Optional[str] = None,
    job_type: Optional[str] = None,
    hours: int = 24,
    limit: int = 10,
) -> list:
    """
    Get the slowest jobs within a time window.

    Args:
        organization: Filter by organization (optional)
        job_type: Filter by job type (optional)
        hours: Time window in hours (default: 24)
        limit: Maximum number of results (default: 10)

    Returns:
        List of dicts with job_id, job_type, execution_time_seconds, status
    """
    conditions = ["recorded_at >= %(time_threshold)s"]
    values = {
        "time_threshold": add_to_date(now_datetime(), hours=-hours),
        "limit": limit,
    }

    if organization:
        conditions.append("organization = %(organization)s")
        values["organization"] = organization

    if job_type:
        conditions.append("job_type = %(job_type)s")
        values["job_type"] = job_type

    result = frappe.db.sql(
        f"""
        SELECT
            job_id,
            job_type,
            execution_time_seconds,
            status,
            recorded_at
        FROM `tabBackground Job Metrics`
        WHERE {" AND ".join(conditions)}
        ORDER BY execution_time_seconds DESC
        LIMIT %(limit)s
        """,
        values,
        as_dict=True,
    )

    return result
