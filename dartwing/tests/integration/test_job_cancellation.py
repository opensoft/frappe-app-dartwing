"""
Integration tests for job cancellation.
"""

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase


class TestJobCancellation(FrappeTestCase):
    """Test job cancellation functionality."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()

        # Create test organization if needed
        if not frappe.db.exists("Organization", "TEST-ORG-001"):
            org = frappe.new_doc("Organization")
            org.organization_name = "Test Organization"
            org.status = "Active"
            org.insert(ignore_permissions=True)
            cls.test_org = org.name
        else:
            cls.test_org = "TEST-ORG-001"

        # Create test job type
        if not frappe.db.exists("Job Type", "test_cancel_job"):
            job_type = frappe.new_doc("Job Type")
            job_type.type_name = "test_cancel_job"
            job_type.display_name = "Test Cancel Job"
            job_type.handler_method = "dartwing.dartwing_core.background_jobs.samples.execute_long_running_job"
            job_type.default_timeout = 300
            job_type.deduplication_window = 5
            job_type.is_enabled = 1
            job_type.insert(ignore_permissions=True)

        frappe.db.commit()

    def setUp(self):
        """Set up each test."""
        frappe.db.delete("Background Job", {"job_type": "test_cancel_job"})
        frappe.db.commit()

    def test_cancel_pending_job(self):
        """Should be able to cancel a pending job."""
        from dartwing.dartwing_core.background_jobs import submit_job, cancel_job

        # Create a job and immediately cancel it
        job = submit_job(
            job_type="test_cancel_job",
            organization=self.test_org,
            parameters={"duration": 60},
        )

        # Cancel the job
        canceled_job = cancel_job(job.name)

        self.assertEqual(canceled_job.status, "Canceled")
        self.assertIsNotNone(canceled_job.canceled_at)
        self.assertEqual(canceled_job.canceled_by, frappe.session.user)

    def test_cancel_completed_job_fails(self):
        """Should not be able to cancel a completed job."""
        # Create a job and mark it completed
        job = frappe.new_doc("Background Job")
        job.job_type = "test_cancel_job"
        job.organization = self.test_org
        job.owner_user = frappe.session.user
        job.status = "Completed"
        job.insert(ignore_permissions=True)
        frappe.db.commit()

        from dartwing.dartwing_core.background_jobs import cancel_job

        with self.assertRaises(frappe.ValidationError):
            cancel_job(job.name)

    def test_cancel_creates_log_entry(self):
        """Cancellation should create execution log entry."""
        from dartwing.dartwing_core.background_jobs import submit_job, cancel_job

        job = submit_job(
            job_type="test_cancel_job",
            organization=self.test_org,
            parameters={"duration": 60},
        )

        cancel_job(job.name)

        # Check for cancellation log
        logs = frappe.get_all(
            "Job Execution Log",
            filters={
                "background_job": job.name,
                "to_status": "Canceled",
            },
        )

        self.assertEqual(len(logs), 1)


class TestCancellationPermissions(FrappeTestCase):
    """Test cancellation permission validation."""

    def test_owner_can_cancel(self):
        """Job owner should be able to cancel their job."""
        # This is tested implicitly in test_cancel_pending_job
        pass

    def test_can_cancel_method(self):
        """Background Job.can_cancel() should return correct value."""
        job = frappe.new_doc("Background Job")
        job.status = "Pending"
        self.assertTrue(job.can_cancel())

        job.status = "Queued"
        self.assertTrue(job.can_cancel())

        job.status = "Running"
        self.assertTrue(job.can_cancel())

        job.status = "Completed"
        self.assertFalse(job.can_cancel())

        job.status = "Dead Letter"
        self.assertFalse(job.can_cancel())

        job.status = "Canceled"
        self.assertFalse(job.can_cancel())


if __name__ == "__main__":
    unittest.main()
