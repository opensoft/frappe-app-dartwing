"""
Circuit Breaker Pattern for Background Jobs.

Prevents cascading failures by automatically stopping job execution when
a job type has a high failure rate. The circuit "opens" (blocks execution)
when failures exceed a threshold, then "closes" (allows execution) after
a cooldown period.

States:
- CLOSED: Normal operation, jobs execute normally
- OPEN: High failure rate detected, jobs are rejected
- HALF_OPEN: Testing if the issue is resolved, limited job execution allowed
"""

import frappe
from frappe.utils import now_datetime, add_to_date
from typing import Optional, Tuple
from enum import Enum

from dartwing.dartwing_core.background_jobs.config import (
    CIRCUIT_BREAKER_FAILURE_THRESHOLD,
    CIRCUIT_BREAKER_MIN_SAMPLES,
    CIRCUIT_BREAKER_WINDOW_MINUTES,
    CIRCUIT_BREAKER_COOLDOWN_MINUTES,
)


class CircuitState(str, Enum):
    """Circuit breaker states."""
    CLOSED = "Closed"
    OPEN = "Open"
    HALF_OPEN = "Half-Open"


class CircuitBreakerOpen(Exception):
    """Raised when attempting to execute a job while circuit breaker is open."""
    pass


def check_circuit_breaker(job_type: str, organization: str) -> None:
    """
    Check if circuit breaker allows job execution.

    Args:
        job_type: Job type name
        organization: Organization name

    Raises:
        CircuitBreakerOpen: If circuit is open and job should not execute
    """
    state, reason = get_circuit_state(job_type, organization)

    if state == CircuitState.OPEN:
        raise CircuitBreakerOpen(
            f"Circuit breaker is OPEN for job type '{job_type}' in organization '{organization}'. "
            f"Reason: {reason}"
        )

    # If HALF_OPEN, allow execution but we'll monitor closely


def get_circuit_state(job_type: str, organization: str) -> Tuple[CircuitState, Optional[str]]:
    """
    Get the current circuit breaker state for a job type.

    Args:
        job_type: Job type name
        organization: Organization name

    Returns:
        Tuple of (state, reason) where reason explains why circuit is open
    """
    # Check if there's an active circuit breaker record
    breaker = frappe.db.get_value(
        "Background Job Circuit Breaker",
        {"job_type": job_type, "organization": organization},
        ["state", "opened_at", "reason", "cooldown_minutes"],
        as_dict=True,
    )

    if not breaker:
        # No breaker record = circuit is closed (normal operation)
        return CircuitState.CLOSED, None

    if breaker.state == CircuitState.OPEN:
        # Check if cooldown period has elapsed
        if breaker.opened_at and breaker.cooldown_minutes:
            cooldown_end = add_to_date(breaker.opened_at, minutes=breaker.cooldown_minutes)
            if now_datetime() >= cooldown_end:
                # Transition to HALF_OPEN
                _transition_to_half_open(job_type, organization)
                return CircuitState.HALF_OPEN, None

        return CircuitState.OPEN, breaker.reason

    return CircuitState(breaker.state), breaker.reason


def record_job_outcome(job_type: str, organization: str, success: bool) -> None:
    """
    Record a job execution outcome and update circuit breaker state.

    Args:
        job_type: Job type name
        organization: Organization name
        success: True if job completed successfully, False if failed
    """
    try:
        current_state, _ = get_circuit_state(job_type, organization)

        if current_state == CircuitState.HALF_OPEN:
            if success:
                # Success in HALF_OPEN state -> close the circuit
                _close_circuit(job_type, organization)
            else:
                # Failure in HALF_OPEN state -> reopen the circuit
                _open_circuit(
                    job_type,
                    organization,
                    "Job failed during half-open state",
                    cooldown_minutes=10,
                )
        elif current_state == CircuitState.CLOSED:
            # Check if we should open the circuit based on recent failure rate
            _check_and_update_failure_rate(job_type, organization)

    except Exception as e:
        # Circuit breaker failures shouldn't break job execution
        frappe.log_error(
            f"Circuit breaker update failed for {job_type} in {organization}: {str(e)}",
            "Circuit Breaker",
        )


def _check_and_update_failure_rate(job_type: str, organization: str) -> None:
    """
    Check recent failure rate and open circuit if threshold exceeded.

    Uses a sliding window of the last N jobs to calculate failure rate.
    """
    # Get configuration from Job Type
    job_type_doc = frappe.get_doc("Job Type", job_type)

    # Use getattr() with defaults to support optional circuit breaker fields on Job Type.
    # These fields allow per-job-type customization (documented in job_type.py docstring).
    # If not set, fall back to system-wide constants from config.py.
    # This pattern allows circuit breaker configuration without requiring schema changes.
    failure_threshold = getattr(job_type_doc, 'circuit_breaker_failure_threshold', CIRCUIT_BREAKER_FAILURE_THRESHOLD)
    min_samples = getattr(job_type_doc, 'circuit_breaker_min_samples', CIRCUIT_BREAKER_MIN_SAMPLES)
    window_minutes = getattr(job_type_doc, 'circuit_breaker_window_minutes', CIRCUIT_BREAKER_WINDOW_MINUTES)

    # Skip if circuit breaker is disabled for this job type
    if not getattr(job_type_doc, 'enable_circuit_breaker', False):
        return

    # Get recent job outcomes
    time_threshold = add_to_date(now_datetime(), minutes=-window_minutes)

    result = frappe.db.sql(
        """
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status IN ('Failed', 'Dead Letter', 'Timed Out') THEN 1 ELSE 0 END) as failed
        FROM `tabBackground Job`
        WHERE job_type = %(job_type)s
            AND organization = %(organization)s
            AND completed_at >= %(time_threshold)s
            AND status IN ('Completed', 'Failed', 'Dead Letter', 'Timed Out')
        """,
        {
            "job_type": job_type,
            "organization": organization,
            "time_threshold": time_threshold,
        },
        as_dict=True,
    )

    if not result or result[0].total < min_samples:
        # Not enough data to make a decision
        return

    total = result[0].total
    failed = result[0].failed or 0
    failure_rate = failed / total if total > 0 else 0

    if failure_rate >= failure_threshold:
        # Open the circuit
        cooldown_minutes = getattr(job_type_doc, 'circuit_breaker_cooldown_minutes', CIRCUIT_BREAKER_COOLDOWN_MINUTES)
        _open_circuit(
            job_type,
            organization,
            f"Failure rate {failure_rate:.1%} exceeds threshold {failure_threshold:.1%} "
            f"({failed}/{total} jobs failed in last {window_minutes} minutes)",
            cooldown_minutes=cooldown_minutes,
        )


def _open_circuit(job_type: str, organization: str, reason: str, cooldown_minutes: int = None) -> None:
    """Open the circuit breaker."""
    if cooldown_minutes is None:
        cooldown_minutes = CIRCUIT_BREAKER_COOLDOWN_MINUTES
    existing = frappe.db.get_value(
        "Background Job Circuit Breaker",
        {"job_type": job_type, "organization": organization},
        "name",
    )

    if existing:
        doc = frappe.get_doc("Background Job Circuit Breaker", existing)
        doc.state = CircuitState.OPEN
        doc.opened_at = now_datetime()
        doc.reason = reason
        doc.cooldown_minutes = cooldown_minutes
        doc.save(ignore_permissions=True)
    else:
        doc = frappe.get_doc({
            "doctype": "Background Job Circuit Breaker",
            "job_type": job_type,
            "organization": organization,
            "state": CircuitState.OPEN,
            "opened_at": now_datetime(),
            "reason": reason,
            "cooldown_minutes": cooldown_minutes,
        })
        doc.insert(ignore_permissions=True)

    frappe.db.commit()

    # Log as error since circuit opening is a system degradation event
    # This allows monitoring/alerting systems to track circuit breaker activations
    frappe.log_error(
        f"Circuit breaker OPENED for {job_type} in {organization}. Reason: {reason}",
        "Circuit Breaker Opened",
    )


def _transition_to_half_open(job_type: str, organization: str) -> None:
    """Transition circuit from OPEN to HALF_OPEN."""
    existing = frappe.db.get_value(
        "Background Job Circuit Breaker",
        {"job_type": job_type, "organization": organization},
        "name",
    )

    if existing:
        doc = frappe.get_doc("Background Job Circuit Breaker", existing)
        doc.state = CircuitState.HALF_OPEN
        doc.reason = "Cooldown period elapsed, testing recovery"
        doc.save(ignore_permissions=True)
        frappe.db.commit()


def _close_circuit(job_type: str, organization: str) -> None:
    """Close the circuit breaker (delete the record)."""
    existing = frappe.db.get_value(
        "Background Job Circuit Breaker",
        {"job_type": job_type, "organization": organization},
        "name",
    )

    if existing:
        frappe.delete_doc("Background Job Circuit Breaker", existing, ignore_permissions=True)
        frappe.db.commit()

        # Log recovery as info (not error) since circuit closing is a positive event
        # Different from opening (which uses log_error) to allow filtering in monitoring
        frappe.logger().info(
            f"Circuit breaker CLOSED for {job_type} in {organization}. System recovered."
        )


def get_open_circuits(organization: Optional[str] = None) -> list:
    """
    Get all currently open or half-open circuit breakers.

    Args:
        organization: Filter by organization (optional)

    Returns:
        List of circuit breaker records
    """
    filters = {"state": ["in", [CircuitState.OPEN, CircuitState.HALF_OPEN]]}
    if organization:
        filters["organization"] = organization

    return frappe.get_all(
        "Background Job Circuit Breaker",
        filters=filters,
        fields=["job_type", "organization", "state", "opened_at", "reason", "cooldown_minutes"],
        order_by="opened_at desc",
    )


def manually_close_circuit(job_type: str, organization: str) -> None:
    """
    Manually close a circuit breaker (admin override).

    Args:
        job_type: Job type name
        organization: Organization name
    """
    _close_circuit(job_type, organization)
