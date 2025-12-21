"""
Configuration constants for Background Job Engine.

Centralizes magic numbers and default values for easier maintenance
and consistent behavior across the module.
"""

# Default timeout for job execution in seconds
DEFAULT_TIMEOUT_SECONDS = 300

# Default maximum retry attempts for failed jobs
DEFAULT_MAX_RETRIES = 5

# Default rate limit window in seconds (1 minute)
DEFAULT_RATE_LIMIT_WINDOW_SECONDS = 60

# Maximum allowed rate limit window (24 hours)
MAX_RATE_LIMIT_WINDOW_SECONDS = 86400

# Default deduplication window in seconds (5 minutes)
DEFAULT_DEDUPLICATION_WINDOW_SECONDS = 300

# Delay before retrying a job with pending dependency
DEPENDENCY_RETRY_DELAY_SECONDS = 30

# Default batch size for cleanup operations
CLEANUP_BATCH_SIZE = 100

# Default retention period for completed jobs in days
DEFAULT_RETENTION_DAYS = 30

# Lock timeout for deduplication in seconds
DEDUPLICATION_LOCK_TIMEOUT_SECONDS = 30

# Progress update throttle interval in seconds (minimum time between updates)
PROGRESS_THROTTLE_SECONDS = 1.0

# Circuit breaker default configuration
CIRCUIT_BREAKER_FAILURE_THRESHOLD = 0.5  # 50% failure rate triggers circuit open
CIRCUIT_BREAKER_MIN_SAMPLES = 10  # Minimum jobs required before opening circuit
CIRCUIT_BREAKER_WINDOW_MINUTES = 30  # Time window for failure rate calculation
CIRCUIT_BREAKER_COOLDOWN_MINUTES = 15  # Wait time before testing recovery
