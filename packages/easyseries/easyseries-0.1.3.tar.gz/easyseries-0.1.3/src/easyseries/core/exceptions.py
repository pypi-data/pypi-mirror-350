"""Custom exceptions for EasySeries."""

from typing import Any


class EasySeriesError(Exception):
    """Base exception for all EasySeries errors."""

    def __init__(
        self,
        message: str,
        details: dict[str, Any] | None = None,
        original_error: Exception | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.original_error = original_error

    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class HTTPClientError(EasySeriesError):
    """Raised when HTTP client encounters an error."""

    pass


class ConfigurationError(EasySeriesError):
    """Raised when configuration is invalid."""

    pass


class RateLimitError(EasySeriesError):
    """Raised when rate limit is exceeded."""

    pass


class ValidationError(EasySeriesError):
    """Raised when data validation fails."""

    pass
