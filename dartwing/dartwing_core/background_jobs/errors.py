"""
Error classification for Background Job Engine.

Provides error types to distinguish between transient (retryable) and
permanent (fail immediately) errors.
"""

# Error type constants for consistency across the system
ERROR_TYPE_TRANSIENT = "Transient"
ERROR_TYPE_PERMANENT = "Permanent"
ERROR_TYPE_CIRCUIT_BREAKER = "Circuit Breaker Open"


class JobError(Exception):
    """Base class for job errors with retry classification."""

    is_retryable = True

    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.message = message
        self.cause = cause


class TransientError(JobError):
    """
    Errors that may succeed on retry.

    Examples:
    - Network timeout
    - Connection refused
    - Service temporarily unavailable (HTTP 503)
    - Rate limited (HTTP 429)
    - Temporary resource exhaustion

    Usage:
        try:
            response = call_external_api()
        except ConnectionError as e:
            raise TransientError(f"API connection failed: {e}", cause=e)
    """

    is_retryable = True


class PermanentError(JobError):
    """
    Errors that will never succeed - fail immediately without retry.

    Examples:
    - Validation failure
    - Invalid input data
    - Permission denied
    - Resource not found (deleted during execution)
    - Authentication failure

    Usage:
        if not is_valid(data):
            raise PermanentError(f"Invalid input: {data}")
    """

    is_retryable = False


class JobCanceledError(JobError):
    """
    Raised by handlers when they detect the job has been canceled.

    This is not a failure condition and should result in the job remaining in
    "Canceled" status (not "Dead Letter").
    """

    is_retryable = False


def classify_error(exception: Exception) -> bool:
    """
    Classify an exception as retryable or not.

    Args:
        exception: The exception to classify

    Returns:
        True if the error is retryable (transient), False if permanent

    Classification rules:
    - PermanentError: Never retry
    - TransientError: Always retry
    - ConnectionError, TimeoutError: Retry
    - HTTP 429, 500, 502, 503, 504: Retry
    - Unknown errors: Default to retry (fail-safe)
    """
    # Explicit job error types
    if isinstance(exception, PermanentError):
        return False
    if isinstance(exception, JobCanceledError):
        return False
    if isinstance(exception, TransientError):
        return True

    # Python built-in network errors
    if isinstance(exception, (ConnectionError, TimeoutError)):
        return True

    # Check for HTTP status codes (from requests, httpx, etc.)
    http_status = getattr(exception, "http_status", None) or getattr(
        exception, "status_code", None
    )
    if http_status:
        retryable_codes = {429, 500, 502, 503, 504}
        return http_status in retryable_codes

    # Frappe-specific errors
    exception_type = type(exception).__name__
    permanent_frappe_errors = {
        "ValidationError",
        "PermissionError",
        "DoesNotExistError",
        "MandatoryError",
        "InvalidAuthorizationHeader",
        "LinkValidationError",
    }
    if exception_type in permanent_frappe_errors:
        return False

    # Default: retry unknown errors (fail-safe)
    return True


def get_error_type(exception: Exception) -> str:
    """
    Get the error type string for storage in Background Job.

    Args:
        exception: The exception to classify

    Returns:
        ERROR_TYPE_TRANSIENT or ERROR_TYPE_PERMANENT
    """
    return ERROR_TYPE_TRANSIENT if classify_error(exception) else ERROR_TYPE_PERMANENT
