"""
Unit tests for Background Job Executor.

Focuses on backward-compatible worker argument handling for already-enqueued jobs.
"""

import unittest
from unittest.mock import MagicMock, patch


class TestExecuteJobArgCompatibility(unittest.TestCase):
    def test_accepts_legacy_job_id_kwarg(self):
        from dartwing.dartwing_core.background_jobs.executor import execute_job

        mock_job = MagicMock()
        mock_job.status = "Completed"

        with patch(
            "dartwing.dartwing_core.background_jobs.executor.frappe.get_doc", return_value=mock_job
        ) as get_doc, patch("dartwing.dartwing_core.background_jobs.executor.frappe.log_error"):
            execute_job(job_id="JOB-123")
            get_doc.assert_called_once_with("Background Job", "JOB-123")

    def test_accepts_background_job_id_kwarg(self):
        from dartwing.dartwing_core.background_jobs.executor import execute_job

        mock_job = MagicMock()
        mock_job.status = "Completed"

        with patch(
            "dartwing.dartwing_core.background_jobs.executor.frappe.get_doc", return_value=mock_job
        ) as get_doc, patch("dartwing.dartwing_core.background_jobs.executor.frappe.log_error"):
            execute_job(background_job_id="JOB-456")
            get_doc.assert_called_once_with("Background Job", "JOB-456")


if __name__ == "__main__":
    unittest.main()
