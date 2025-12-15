"""
Unit tests for error classification.
"""

import unittest
from dartwing.dartwing_core.background_jobs.errors import (
    TransientError,
    PermanentError,
    classify_error,
    get_error_type,
)


class TestErrorClassification(unittest.TestCase):
    """Test error type classification."""

    def test_transient_error_is_retryable(self):
        """TransientError should be classified as retryable."""
        error = TransientError("Network timeout")
        self.assertTrue(classify_error(error))
        self.assertTrue(error.is_retryable)

    def test_permanent_error_not_retryable(self):
        """PermanentError should not be classified as retryable."""
        error = PermanentError("Invalid input")
        self.assertFalse(classify_error(error))
        self.assertFalse(error.is_retryable)

    def test_connection_error_is_retryable(self):
        """Python ConnectionError should be retryable."""
        error = ConnectionError("Connection refused")
        self.assertTrue(classify_error(error))

    def test_timeout_error_is_retryable(self):
        """Python TimeoutError should be retryable."""
        error = TimeoutError("Request timed out")
        self.assertTrue(classify_error(error))

    def test_http_503_is_retryable(self):
        """HTTP 503 should be retryable."""

        class HttpError(Exception):
            http_status = 503

        error = HttpError("Service Unavailable")
        self.assertTrue(classify_error(error))

    def test_http_429_is_retryable(self):
        """HTTP 429 (rate limited) should be retryable."""

        class HttpError(Exception):
            http_status = 429

        error = HttpError("Too Many Requests")
        self.assertTrue(classify_error(error))

    def test_http_500_is_retryable(self):
        """HTTP 500 should be retryable."""

        class HttpError(Exception):
            http_status = 500

        error = HttpError("Internal Server Error")
        self.assertTrue(classify_error(error))

    def test_http_400_not_retryable(self):
        """HTTP 400 (bad request) should not be retryable."""

        class HttpError(Exception):
            http_status = 400

        error = HttpError("Bad Request")
        self.assertFalse(classify_error(error))

    def test_http_404_not_retryable(self):
        """HTTP 404 (not found) should not be retryable."""

        class HttpError(Exception):
            http_status = 404

        error = HttpError("Not Found")
        self.assertFalse(classify_error(error))

    def test_unknown_error_defaults_to_retryable(self):
        """Unknown errors should default to retryable (fail-safe)."""

        class UnknownError(Exception):
            pass

        error = UnknownError("Something went wrong")
        self.assertTrue(classify_error(error))

    def test_error_with_cause(self):
        """TransientError should preserve cause."""
        cause = ConnectionError("Original error")
        error = TransientError("Wrapper error", cause=cause)

        self.assertEqual(error.cause, cause)
        self.assertEqual(error.message, "Wrapper error")

    def test_get_error_type_transient(self):
        """get_error_type should return 'Transient' for retryable."""
        error = TransientError("Network error")
        self.assertEqual(get_error_type(error), "Transient")

    def test_get_error_type_permanent(self):
        """get_error_type should return 'Permanent' for non-retryable."""
        error = PermanentError("Validation error")
        self.assertEqual(get_error_type(error), "Permanent")

    def test_get_error_type_connection_error(self):
        """get_error_type for ConnectionError should be Transient."""
        error = ConnectionError("Connection refused")
        self.assertEqual(get_error_type(error), "Transient")


if __name__ == "__main__":
    unittest.main()
