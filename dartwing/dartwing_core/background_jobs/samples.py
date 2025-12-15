"""
Sample Job Handlers for Background Job Engine.

Provides example job handlers for testing the job engine.
"""

import time
import frappe
from dartwing.dartwing_core.background_jobs.progress import JobContext
from dartwing.dartwing_core.background_jobs.errors import TransientError, PermanentError


def execute_sample_job(context: JobContext) -> dict:
    """
    Sample job handler for testing.

    Parameters:
        duration (int): How long to run in seconds (default: 5)
        fail_type (str): Optional - "transient" or "permanent" to simulate failure
        fail_at_progress (int): Optional - progress percentage to fail at

    Returns:
        dict with output_reference
    """
    params = context.parameters
    duration = params.get("duration", 5)
    fail_type = params.get("fail_type")
    fail_at_progress = params.get("fail_at_progress")

    steps = 10
    step_duration = duration / steps

    for i in range(steps):
        # Check for cancellation
        if context.is_canceled():
            raise PermanentError("Job was canceled")

        progress = (i + 1) * 10
        context.update_progress(progress, f"Processing step {i + 1} of {steps}...")

        # Simulate failure at specific progress
        if fail_at_progress and progress >= fail_at_progress:
            if fail_type == "permanent":
                raise PermanentError(f"Simulated permanent failure at {progress}%")
            else:
                raise TransientError(f"Simulated transient failure at {progress}%")

        time.sleep(step_duration)

    # Final failure simulation
    if fail_type == "permanent":
        raise PermanentError("Simulated permanent failure at completion")
    elif fail_type == "transient":
        raise TransientError("Simulated transient failure at completion")

    return {
        "output_reference": f"/files/sample-output-{context.job_id}.txt",
    }


def execute_echo_job(context: JobContext) -> dict:
    """
    Simple echo job that immediately returns input parameters.

    Useful for quick testing of job submission and completion.
    """
    context.update_progress(50, "Processing...")
    context.update_progress(100, "Done!")

    return {
        "output_reference": frappe.as_json(context.parameters),
    }


def execute_long_running_job(context: JobContext) -> dict:
    """
    Long-running job for testing timeout handling.

    Parameters:
        duration (int): How long to run in seconds (default: 600)
    """
    params = context.parameters
    duration = params.get("duration", 600)

    start_time = time.time()
    last_progress = 0

    while True:
        if context.is_canceled():
            raise PermanentError("Job was canceled")

        elapsed = time.time() - start_time
        progress = min(100, int((elapsed / duration) * 100))

        if progress > last_progress:
            context.update_progress(progress, f"Running for {int(elapsed)}s...")
            last_progress = progress

        if elapsed >= duration:
            break

        time.sleep(1)

    return {
        "output_reference": f"Completed after {duration} seconds",
    }
