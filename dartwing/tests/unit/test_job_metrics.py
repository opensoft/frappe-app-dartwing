"""
Unit tests for job metrics calculations.
"""

import unittest
from frappe.tests.utils import FrappeTestCase


class TestMetricsCalculations(FrappeTestCase):
    """Test metrics calculation functions."""

    def test_empty_metrics_structure(self):
        """Empty metrics should have correct structure."""
        from dartwing.dartwing_core.background_jobs.metrics import _empty_metrics

        metrics = _empty_metrics()

        self.assertIn("job_count_by_status", metrics)
        self.assertIn("queue_depth_by_priority", metrics)
        self.assertIn("processing_time", metrics)
        self.assertIn("failure_rate_by_type", metrics)
        self.assertIn("timestamp", metrics)

        self.assertEqual(metrics["job_count_by_status"], {})
        self.assertEqual(metrics["queue_depth_by_priority"], {})
        self.assertEqual(metrics["processing_time"]["average_seconds"], 0)
        self.assertEqual(metrics["processing_time"]["p95_seconds"], 0)

    def test_processing_time_structure(self):
        """Processing time should have average and p95."""
        from dartwing.dartwing_core.background_jobs.metrics import _empty_metrics

        metrics = _empty_metrics()
        processing = metrics["processing_time"]

        self.assertIn("average_seconds", processing)
        self.assertIn("p95_seconds", processing)


if __name__ == "__main__":
    unittest.main()
