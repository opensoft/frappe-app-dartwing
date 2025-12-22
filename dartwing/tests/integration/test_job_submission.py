"""
Integration tests for Background Job submission API.

Tests the full job submission flow including validation and duplicate detection.
"""

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase


class TestJobSubmission(FrappeTestCase):
    """Integration tests for job submission."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()

        # Create test organization if it doesn't exist
        if not frappe.db.exists("Organization", "TEST-ORG-001"):
            org = frappe.new_doc("Organization")
            org.organization_name = "Test Organization"
            org.status = "Active"
            org.insert(ignore_permissions=True)
            cls.test_org = org.name
        else:
            cls.test_org = "TEST-ORG-001"

        # Create test job type if it doesn't exist
        if not frappe.db.exists("Job Type", "test_job"):
            job_type = frappe.new_doc("Job Type")
            job_type.type_name = "test_job"
            job_type.display_name = "Test Job"
            job_type.handler_method = "dartwing.dartwing_core.background_jobs.samples.execute_echo_job"
            job_type.default_timeout = 60
            job_type.default_priority = "Normal"
            job_type.max_retries = 3
            job_type.deduplication_window = 5  # Short window for testing
            job_type.is_enabled = 1
            job_type.insert(ignore_permissions=True)

        frappe.db.commit()

    def setUp(self):
        """Set up each test."""
        # Clear any existing test jobs
        frappe.db.delete("Background Job", {"job_type": "test_job"})
        frappe.db.commit()

    def test_submit_job_creates_record(self):
        """Submitting a job should create a Background Job record."""
        from dartwing.dartwing_core.background_jobs import submit_job

        job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"test_key": "test_value"},
        )

        self.assertIsNotNone(job.name)
        self.assertTrue(job.name.startswith("JOB-"))
        self.assertEqual(job.job_type, "test_job")
        self.assertEqual(job.organization, self.test_org)
        self.assertEqual(job.status, "Queued")

    def test_submit_job_sets_defaults_from_job_type(self):
        """Job should inherit defaults from Job Type."""
        from dartwing.dartwing_core.background_jobs import submit_job

        job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={},
        )

        self.assertEqual(job.priority, "Normal")
        self.assertEqual(job.max_retries, 3)
        self.assertEqual(job.timeout_seconds, 60)

    def test_submit_job_respects_custom_priority(self):
        """Custom priority should override default."""
        from dartwing.dartwing_core.background_jobs import submit_job

        job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={},
            priority="High",
        )

        self.assertEqual(job.priority, "High")

    def test_submit_job_generates_hash(self):
        """Job should have hash for duplicate detection."""
        from dartwing.dartwing_core.background_jobs import submit_job

        job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"key": "value"},
        )

        self.assertIsNotNone(job.job_hash)
        self.assertEqual(len(job.job_hash), 16)

    def test_submit_job_invalid_job_type_raises(self):
        """Invalid job type should raise error."""
        from dartwing.dartwing_core.background_jobs import submit_job

        with self.assertRaises(frappe.ValidationError):
            submit_job(
                job_type="nonexistent_job_type",
                organization=self.test_org,
                parameters={},
            )

    def test_submit_job_disabled_job_type_raises(self):
        """Disabled job type should raise error."""
        # Create disabled job type
        if not frappe.db.exists("Job Type", "disabled_test_job"):
            job_type = frappe.new_doc("Job Type")
            job_type.type_name = "disabled_test_job"
            job_type.display_name = "Disabled Test Job"
            job_type.handler_method = "dartwing.dartwing_core.background_jobs.samples.execute_echo_job"
            job_type.is_enabled = 0
            job_type.insert(ignore_permissions=True)
            frappe.db.commit()

        from dartwing.dartwing_core.background_jobs import submit_job

        with self.assertRaises(frappe.ValidationError):
            submit_job(
                job_type="disabled_test_job",
                organization=self.test_org,
                parameters={},
            )

    def test_duplicate_detection_rejects_same_job(self):
        """Submitting the same job twice within window should be rejected."""
        from dartwing.dartwing_core.background_jobs import submit_job

        # First submission should succeed
        submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"unique_key": "same_value"},
        )

        # Second submission with same params should fail
        with self.assertRaises(frappe.DuplicateEntryError):
            submit_job(
                job_type="test_job",
                organization=self.test_org,
                parameters={"unique_key": "same_value"},
            )

    def test_duplicate_detection_allows_different_params(self):
        """Jobs with different parameters should not be considered duplicates."""
        from dartwing.dartwing_core.background_jobs import submit_job

        job1 = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"key": "value1"},
        )

        job2 = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"key": "value2"},
        )

        self.assertNotEqual(job1.name, job2.name)
        self.assertNotEqual(job1.job_hash, job2.job_hash)

    def test_job_with_dependency(self):
        """Job can be created with dependency on another job."""
        from dartwing.dartwing_core.background_jobs import submit_job

        parent_job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"role": "parent"},
        )

        child_job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"role": "child"},
            depends_on=parent_job.name,
        )

        self.assertEqual(child_job.depends_on, parent_job.name)

    def test_job_creates_execution_log(self):
        """Job creation should create initial execution log entry."""
        from dartwing.dartwing_core.background_jobs import submit_job

        job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={},
        )

        # Check for log entries
        logs = frappe.get_all(
            "Job Execution Log",
            filters={"background_job": job.name},
            fields=["from_status", "to_status"],
        )

        # Should have entries for Pending and Queued transitions
        self.assertGreater(len(logs), 0)


class TestGetJobStatus(FrappeTestCase):
    """Test get_job_status API."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        super().setUpClass()

        # Ensure test org and job type exist (same as above)
        if not frappe.db.exists("Organization", "TEST-ORG-001"):
            org = frappe.new_doc("Organization")
            org.organization_name = "Test Organization"
            org.status = "Active"
            org.insert(ignore_permissions=True)
            cls.test_org = org.name
        else:
            cls.test_org = "TEST-ORG-001"

        if not frappe.db.exists("Job Type", "test_job"):
            job_type = frappe.new_doc("Job Type")
            job_type.type_name = "test_job"
            job_type.display_name = "Test Job"
            job_type.handler_method = "dartwing.dartwing_core.background_jobs.samples.execute_echo_job"
            job_type.default_timeout = 60
            job_type.is_enabled = 1
            job_type.insert(ignore_permissions=True)

        frappe.db.commit()

    def test_get_job_status_returns_details(self):
        """get_job_status should return job details."""
        from dartwing.dartwing_core.background_jobs import submit_job, get_job_status

        job = submit_job(
            job_type="test_job",
            organization=self.test_org,
            parameters={"test": True},
        )

        status = get_job_status(job.name)

        self.assertEqual(status["job_id"], job.name)
        self.assertEqual(status["job_type"], "test_job")
        self.assertEqual(status["status"], "Queued")
        self.assertIn("progress", status)
        self.assertIn("created_at", status)


if __name__ == "__main__":
    unittest.main()
