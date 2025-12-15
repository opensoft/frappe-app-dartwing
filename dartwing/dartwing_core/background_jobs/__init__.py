"""
Background Job Engine for Dartwing.

Provides guaranteed asynchronous task execution with:
- Real-time progress tracking via Socket.IO
- Intelligent retry with error classification (transient vs permanent)
- Multi-tenant job isolation scoped to Organization
- Dead letter queue for failed job review
- Operational metrics for monitoring

Usage:
    from dartwing.dartwing_core.background_jobs import submit_job, get_job_status, cancel_job

    # Submit a job
    job = submit_job(
        job_type="pdf_generation",
        organization="ORG-2025-00001",
        parameters={"template": "monthly_report"}
    )

    # Check status
    status = get_job_status(job.name)

    # Cancel if needed
    cancel_job(job.name)
"""

from dartwing.dartwing_core.background_jobs.engine import (
    submit_job,
    get_job_status,
    cancel_job,
)
from dartwing.dartwing_core.background_jobs.errors import (
    TransientError,
    PermanentError,
)
from dartwing.dartwing_core.background_jobs.progress import (
    JobContext,
)

__all__ = [
    "submit_job",
    "get_job_status",
    "cancel_job",
    "TransientError",
    "PermanentError",
    "JobContext",
]
