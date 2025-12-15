"""
Integration tests for job retry functionality.
"""

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase
from frappe.utils import now_datetime, add_to_date


class TestJobRetry(FrappeTestCase):
    """Test automatic retry on transient failure."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()

        if not frappe.db.exists("Organization", "TEST-ORG-001"):
            org = frappe.new_doc("Organization")
            org.organization_name = "Test Organization"
            org.status = "Active"
            org.insert(ignore_permissions=True)
            cls.test_org = org.name
        else:
            cls.test_org = "TEST-ORG-001"

        if not frappe.db.exists("Job Type", "test_retry_job"):
            job_type = frappe.new_doc("Job Type")
            job_type.type_name = "test_retry_job"
            job_type.display_name = "Test Retry Job"
            job_type.handler_method = "dartwing.dartwing_core.background_jobs.samples.execute_sample_job"
            job_type.default_timeout = 60
            job_type.max_retries = 3
            job_type.deduplication_window = 5
            job_type.is_enabled = 1
            job_type.insert(ignore_permissions=True)

        frappe.db.commit()

    def setUp(self):
        """Set up each test."""
        frappe.db.delete("Background Job", {"job_type": "test_retry_job"})
        frappe.db.commit()

    def test_failed_job_schedules_retry(self):
        """Failed transient job should schedule retry."""
        from dartwing.dartwing_core.background_jobs.retry import schedule_retry

        # Create a job in failed state
        job = frappe.new_doc("Background Job")
        job.job_type = "test_retry_job"
        job.organization = self.test_org
        job.owner_user = frappe.session.user
        job.status = "Failed"
        job.retry_count = 0
        job.max_retries = 3
        job.error_type = "Transient"
        job.insert(ignore_permissions=True)
        frappe.db.commit()

        # Schedule retry
        schedule_retry(job.name)

        # Reload and check
        job.reload()
        self.assertEqual(job.retry_count, 1)
        self.assertIsNotNone(job.next_retry_at)

    def test_exhausted_retries_moves_to_dead_letter(self):
        """Job that exhausts retries should move to dead letter."""
        from dartwing.dartwing_core.background_jobs.retry import schedule_retry

        # Create a job that has exhausted retries
        job = frappe.new_doc("Background Job")
        job.job_type = "test_retry_job"
        job.organization = self.test_org
        job.owner_user = frappe.session.user
        job.status = "Failed"
        job.retry_count = 3  # Already at max
        job.max_retries = 3
        job.error_type = "Transient"
        job.insert(ignore_permissions=True)
        frappe.db.commit()

        # Try to schedule retry
        schedule_retry(job.name)

        # Reload and check
        job.reload()
        self.assertEqual(job.status, "Dead Letter")
        self.assertIsNone(job.next_retry_at)

    def test_process_retry_queue_picks_up_ready_jobs(self):
        """Retry scheduler should pick up jobs past their retry time."""
        from dartwing.dartwing_core.background_jobs.retry import process_retry_queue

        # Create a job ready for retry
        job = frappe.new_doc("Background Job")
        job.job_type = "test_retry_job"
        job.organization = self.test_org
        job.owner_user = frappe.session.user
        job.status = "Failed"
        job.retry_count = 1
        job.max_retries = 3
        job.next_retry_at = add_to_date(now_datetime(), minutes=-5)  # In the past
        job.insert(ignore_permissions=True)
        frappe.db.commit()

        initial_status = job.status

        # Process retry queue
        process_retry_queue()

        # Reload and check
        job.reload()
        # Job should be queued now
        self.assertEqual(job.status, "Queued")

    def test_retry_backoff_increases(self):
        """Retry delay should increase with each attempt."""
        from dartwing.dartwing_core.background_jobs.retry import calculate_backoff

        delay1 = calculate_backoff(1)
        delay2 = calculate_backoff(2)
        delay3 = calculate_backoff(3)

        # Each delay should be roughly double
        self.assertLess(delay1, delay2)
        self.assertLess(delay2, delay3)


class TestRetryJob(FrappeTestCase):
    """Test manual job retry by admin."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()

        if not frappe.db.exists("Organization", "TEST-ORG-001"):
            org = frappe.new_doc("Organization")
            org.organization_name = "Test Organization"
            org.status = "Active"
            org.insert(ignore_permissions=True)
            cls.test_org = org.name
        else:
            cls.test_org = "TEST-ORG-001"

        if not frappe.db.exists("Job Type", "test_manual_retry"):
            job_type = frappe.new_doc("Job Type")
            job_type.type_name = "test_manual_retry"
            job_type.display_name = "Test Manual Retry"
            job_type.handler_method = "dartwing.dartwing_core.background_jobs.samples.execute_echo_job"
            job_type.default_timeout = 60
            job_type.deduplication_window = 5
            job_type.is_enabled = 1
            job_type.insert(ignore_permissions=True)

        frappe.db.commit()

    def test_retry_dead_letter_job(self):
        """Admin should be able to retry dead letter job."""
        from dartwing.dartwing_core.background_jobs.engine import retry_job

        # Create a dead letter job
        job = frappe.new_doc("Background Job")
        job.job_type = "test_manual_retry"
        job.organization = self.test_org
        job.owner_user = frappe.session.user
        job.status = "Dead Letter"
        job.retry_count = 5
        job.max_retries = 5
        job.error_message = "Previous error"
        job.insert(ignore_permissions=True)
        frappe.db.commit()

        # Retry the job
        result = retry_job(job.name)

        self.assertEqual(result.status, "Queued")
        self.assertIsNone(result.error_message)


if __name__ == "__main__":
    unittest.main()
