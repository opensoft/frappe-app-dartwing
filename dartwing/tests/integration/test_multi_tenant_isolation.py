"""
Integration tests for multi-tenant job isolation.
"""

import unittest
import frappe
from frappe.tests.utils import FrappeTestCase


class TestMultiTenantIsolation(FrappeTestCase):
    """Test that jobs are properly isolated by organization."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures with multiple organizations."""
        super().setUpClass()

        # Create first test organization
        if not frappe.db.exists("Organization", "TEST-ORG-001"):
            org = frappe.new_doc("Organization")
            org.organization_name = "Test Organization 1"
            org.status = "Active"
            org.insert(ignore_permissions=True)
            cls.org1 = org.name
        else:
            cls.org1 = "TEST-ORG-001"

        # Create second test organization
        if not frappe.db.exists("Organization", "TEST-ORG-002"):
            org = frappe.new_doc("Organization")
            org.organization_name = "Test Organization 2"
            org.status = "Active"
            org.insert(ignore_permissions=True)
            cls.org2 = org.name
        else:
            cls.org2 = "TEST-ORG-002"

        # Create test job type
        if not frappe.db.exists("Job Type", "test_isolation_job"):
            job_type = frappe.new_doc("Job Type")
            job_type.type_name = "test_isolation_job"
            job_type.display_name = "Test Isolation Job"
            job_type.handler_method = "dartwing.dartwing_core.background_jobs.samples.execute_echo_job"
            job_type.default_timeout = 60
            job_type.deduplication_window = 5
            job_type.is_enabled = 1
            job_type.insert(ignore_permissions=True)

        frappe.db.commit()

    def setUp(self):
        """Set up each test."""
        frappe.db.delete("Background Job", {"job_type": "test_isolation_job"})
        frappe.db.commit()

    def test_job_scoped_to_organization(self):
        """Each job should be scoped to its organization."""
        from dartwing.dartwing_core.background_jobs import submit_job

        job1 = submit_job(
            job_type="test_isolation_job",
            organization=self.org1,
            parameters={"org": "1"},
        )

        job2 = submit_job(
            job_type="test_isolation_job",
            organization=self.org2,
            parameters={"org": "2"},
        )

        self.assertEqual(job1.organization, self.org1)
        self.assertEqual(job2.organization, self.org2)

    def test_list_jobs_filters_by_organization(self):
        """list_jobs should only return jobs for specified organization."""
        from dartwing.dartwing_core.background_jobs import submit_job
        from dartwing.dartwing_core.background_jobs.engine import list_jobs

        # Create jobs in both organizations
        submit_job(
            job_type="test_isolation_job",
            organization=self.org1,
            parameters={"org": "1"},
        )
        submit_job(
            job_type="test_isolation_job",
            organization=self.org2,
            parameters={"org": "2"},
        )

        # List jobs for org1 only
        result = list_jobs(organization=self.org1)

        job_orgs = set()
        for job in result["jobs"]:
            # Look up the job to get organization
            job_doc = frappe.get_doc("Background Job", job["job_id"])
            job_orgs.add(job_doc.organization)

        # Should only have org1 jobs
        self.assertEqual(job_orgs, {self.org1})

    def test_dependency_must_be_same_organization(self):
        """Job dependency must be in the same organization."""
        from dartwing.dartwing_core.background_jobs import submit_job

        # Create parent in org1
        parent_job = submit_job(
            job_type="test_isolation_job",
            organization=self.org1,
            parameters={"role": "parent"},
        )

        # Try to create child in org2 with parent from org1
        with self.assertRaises(frappe.ValidationError):
            submit_job(
                job_type="test_isolation_job",
                organization=self.org2,
                parameters={"role": "child"},
                depends_on=parent_job.name,
            )

    def test_same_params_different_orgs_not_duplicate(self):
        """Same parameters in different orgs should not be duplicates."""
        from dartwing.dartwing_core.background_jobs import submit_job

        # Same parameters, different organizations
        job1 = submit_job(
            job_type="test_isolation_job",
            organization=self.org1,
            parameters={"common": "params"},
        )

        job2 = submit_job(
            job_type="test_isolation_job",
            organization=self.org2,
            parameters={"common": "params"},
        )

        # Both should succeed - different orgs mean different hashes
        self.assertNotEqual(job1.name, job2.name)
        self.assertNotEqual(job1.job_hash, job2.job_hash)


if __name__ == "__main__":
    unittest.main()
