"""
Unit tests for retry policy and backoff calculation.
"""

import unittest
from dartwing.dartwing_core.background_jobs.retry import calculate_backoff


class TestRetryPolicy(unittest.TestCase):
    """Test retry policy backoff calculations."""

    def test_calculate_backoff_attempt_1(self):
        """Attempt 1 should use base delay."""
        delay = calculate_backoff(1, base_delay=60)
        # With ±20% jitter: 48-72 seconds
        self.assertGreaterEqual(delay, 48)
        self.assertLessEqual(delay, 72)

    def test_calculate_backoff_attempt_2(self):
        """Attempt 2 should double base delay."""
        delay = calculate_backoff(2, base_delay=60)
        # With ±20% jitter: 96-144 seconds
        self.assertGreaterEqual(delay, 96)
        self.assertLessEqual(delay, 144)

    def test_calculate_backoff_attempt_3(self):
        """Attempt 3 should quadruple base delay."""
        delay = calculate_backoff(3, base_delay=60)
        # With ±20% jitter: 192-288 seconds
        self.assertGreaterEqual(delay, 192)
        self.assertLessEqual(delay, 288)

    def test_calculate_backoff_attempt_4(self):
        """Attempt 4 should be 8x base delay."""
        delay = calculate_backoff(4, base_delay=60)
        # With ±20% jitter: 384-576 seconds
        self.assertGreaterEqual(delay, 384)
        self.assertLessEqual(delay, 576)

    def test_calculate_backoff_attempt_5(self):
        """Attempt 5 should be 16x base delay."""
        delay = calculate_backoff(5, base_delay=60)
        # With ±20% jitter: 768-1152 seconds
        self.assertGreaterEqual(delay, 768)
        self.assertLessEqual(delay, 1152)

    def test_calculate_backoff_custom_base(self):
        """Custom base delay should be respected."""
        delay = calculate_backoff(1, base_delay=30)
        # With ±20% jitter: 24-36 seconds
        self.assertGreaterEqual(delay, 24)
        self.assertLessEqual(delay, 36)

    def test_calculate_backoff_returns_integer(self):
        """Backoff should return integer seconds."""
        delay = calculate_backoff(1, base_delay=60)
        self.assertIsInstance(delay, int)

    def test_calculate_backoff_jitter_variance(self):
        """Multiple calls should produce different values due to jitter."""
        delays = set()
        for _ in range(20):
            delays.add(calculate_backoff(1, base_delay=60))

        # Should have some variance
        self.assertGreater(len(delays), 1)


if __name__ == "__main__":
    unittest.main()
