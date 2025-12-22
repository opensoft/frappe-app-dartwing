"""
Unit tests for Background Job Engine.

Tests job submission, hash generation, and duplicate detection.
"""

import unittest
import json
from frappe.tests.utils import FrappeTestCase
from unittest.mock import patch, MagicMock


class TestJobHashGeneration(FrappeTestCase):
    """Test job hash generation for duplicate detection."""

    def test_generate_job_hash_deterministic(self):
        """Same inputs should produce same hash."""
        from dartwing.dartwing_core.background_jobs.engine import generate_job_hash

        hash1 = generate_job_hash("pdf_generation", "ORG-001", {"template": "report"})
        hash2 = generate_job_hash("pdf_generation", "ORG-001", {"template": "report"})

        self.assertEqual(hash1, hash2)

    def test_generate_job_hash_different_params(self):
        """Different parameters should produce different hash."""
        from dartwing.dartwing_core.background_jobs.engine import generate_job_hash

        hash1 = generate_job_hash("pdf_generation", "ORG-001", {"template": "report"})
        hash2 = generate_job_hash("pdf_generation", "ORG-001", {"template": "invoice"})

        self.assertNotEqual(hash1, hash2)

    def test_generate_job_hash_different_org(self):
        """Different organizations should produce different hash."""
        from dartwing.dartwing_core.background_jobs.engine import generate_job_hash

        hash1 = generate_job_hash("pdf_generation", "ORG-001", {"template": "report"})
        hash2 = generate_job_hash("pdf_generation", "ORG-002", {"template": "report"})

        self.assertNotEqual(hash1, hash2)

    def test_generate_job_hash_different_type(self):
        """Different job types should produce different hash."""
        from dartwing.dartwing_core.background_jobs.engine import generate_job_hash

        hash1 = generate_job_hash("pdf_generation", "ORG-001", {"template": "report"})
        hash2 = generate_job_hash("fax_send", "ORG-001", {"template": "report"})

        self.assertNotEqual(hash1, hash2)

    def test_generate_job_hash_param_order_independent(self):
        """Parameter order should not affect hash."""
        from dartwing.dartwing_core.background_jobs.engine import generate_job_hash

        hash1 = generate_job_hash("test", "ORG-001", {"a": 1, "b": 2})
        hash2 = generate_job_hash("test", "ORG-001", {"b": 2, "a": 1})

        self.assertEqual(hash1, hash2)

    def test_generate_job_hash_length(self):
        """Hash should be 16 characters."""
        from dartwing.dartwing_core.background_jobs.engine import generate_job_hash

        job_hash = generate_job_hash("pdf_generation", "ORG-001", {"template": "report"})

        self.assertEqual(len(job_hash), 16)

    def test_generate_job_hash_empty_params(self):
        """Empty params should work."""
        from dartwing.dartwing_core.background_jobs.engine import generate_job_hash

        hash1 = generate_job_hash("test", "ORG-001", {})
        hash2 = generate_job_hash("test", "ORG-001", {})

        self.assertEqual(hash1, hash2)
        self.assertEqual(len(hash1), 16)


class TestErrorClassification(FrappeTestCase):
    """Test error classification for retry logic."""

    def test_transient_error_is_retryable(self):
        """TransientError should be classified as retryable."""
        from dartwing.dartwing_core.background_jobs.errors import TransientError, classify_error

        error = TransientError("Network timeout")
        self.assertTrue(classify_error(error))

    def test_permanent_error_not_retryable(self):
        """PermanentError should not be classified as retryable."""
        from dartwing.dartwing_core.background_jobs.errors import PermanentError, classify_error

        error = PermanentError("Invalid input")
        self.assertFalse(classify_error(error))

    def test_connection_error_retryable(self):
        """ConnectionError should be retryable."""
        from dartwing.dartwing_core.background_jobs.errors import classify_error

        error = ConnectionError("Connection refused")
        self.assertTrue(classify_error(error))

    def test_timeout_error_retryable(self):
        """TimeoutError should be retryable."""
        from dartwing.dartwing_core.background_jobs.errors import classify_error

        error = TimeoutError("Request timed out")
        self.assertTrue(classify_error(error))

    def test_unknown_error_defaults_retryable(self):
        """Unknown errors should default to retryable."""
        from dartwing.dartwing_core.background_jobs.errors import classify_error

        error = Exception("Unknown error")
        self.assertTrue(classify_error(error))

    def test_get_error_type_transient(self):
        """get_error_type should return 'Transient' for retryable errors."""
        from dartwing.dartwing_core.background_jobs.errors import TransientError, get_error_type

        error = TransientError("Network timeout")
        self.assertEqual(get_error_type(error), "Transient")

    def test_get_error_type_permanent(self):
        """get_error_type should return 'Permanent' for non-retryable errors."""
        from dartwing.dartwing_core.background_jobs.errors import PermanentError, get_error_type

        error = PermanentError("Invalid input")
        self.assertEqual(get_error_type(error), "Permanent")


class TestRetryBackoff(FrappeTestCase):
    """Test exponential backoff calculation."""

    def test_backoff_first_attempt(self):
        """First attempt should have base delay."""
        from dartwing.dartwing_core.background_jobs.retry import calculate_backoff

        delay = calculate_backoff(1, base_delay=60)
        # Should be 60 ± 20% = 48-72
        self.assertGreaterEqual(delay, 48)
        self.assertLessEqual(delay, 72)

    def test_backoff_second_attempt(self):
        """Second attempt should double the delay."""
        from dartwing.dartwing_core.background_jobs.retry import calculate_backoff

        delay = calculate_backoff(2, base_delay=60)
        # Should be 120 ± 20% = 96-144
        self.assertGreaterEqual(delay, 96)
        self.assertLessEqual(delay, 144)

    def test_backoff_third_attempt(self):
        """Third attempt should quadruple the delay."""
        from dartwing.dartwing_core.background_jobs.retry import calculate_backoff

        delay = calculate_backoff(3, base_delay=60)
        # Should be 240 ± 20% = 192-288
        self.assertGreaterEqual(delay, 192)
        self.assertLessEqual(delay, 288)

    def test_backoff_exponential_growth(self):
        """Delays should grow exponentially."""
        from dartwing.dartwing_core.background_jobs.retry import calculate_backoff

        delays = []
        for attempt in range(1, 6):
            # Use fixed seed for reproducibility by averaging multiple samples
            samples = [calculate_backoff(attempt, base_delay=60) for _ in range(100)]
            avg_delay = sum(samples) / len(samples)
            delays.append(avg_delay)

        # Each delay should be roughly double the previous
        for i in range(1, len(delays)):
            ratio = delays[i] / delays[i - 1]
            self.assertGreater(ratio, 1.5)  # Allow for jitter
            self.assertLess(ratio, 2.5)

    def test_backoff_minimum_one_second(self):
        """Delay should never be less than 1 second."""
        from dartwing.dartwing_core.background_jobs.retry import calculate_backoff

        # Even with very small base delay
        delay = calculate_backoff(1, base_delay=1)
        self.assertGreaterEqual(delay, 1)


if __name__ == "__main__":
    unittest.main()
