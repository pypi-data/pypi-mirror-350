"""Custom exceptions for the ReZEN API wrapper."""

from typing import Any, Dict, Optional


class RezenError(Exception):
    """Base exception for all ReZEN API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize ReZEN error.

        Args:
            message: Error message
            status_code: HTTP status code if applicable
            response_data: Response data from API if available
        """
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(RezenError):
    """Raised when authentication fails."""

    pass


class ValidationError(RezenError):
    """Raised when request validation fails."""

    pass


class NotFoundError(RezenError):
    """Raised when a resource is not found."""

    pass


class RateLimitError(RezenError):
    """Raised when rate limit is exceeded."""

    pass


class ServerError(RezenError):
    """Raised when server returns 5xx error."""

    pass


class NetworkError(RezenError):
    """Raised when network connection fails."""

    pass
