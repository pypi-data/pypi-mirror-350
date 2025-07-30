"""
Exceptions for ZLLM.

This module contains custom exceptions used throughout the ZLLM package.
"""


class ZLLMError(Exception):
    """Base exception for all ZLLM errors."""
    pass


class ConfigurationError(ZLLMError):
    """Raised when there is an error in the configuration."""
    pass


class APIKeyError(ZLLMError):
    """Raised when there is an issue with API keys."""
    pass


class ProviderError(ZLLMError):
    """Raised when there is an error with an LLM provider."""
    pass


class ProviderNotFoundError(ZLLMError):
    """Raised when a requested provider is not found."""
    pass


class ValidationError(ZLLMError):
    """Raised when validation of inputs or outputs fails."""
    pass


class RateLimitError(ProviderError):
    """Raised when a rate limit is exceeded."""
    pass


class AuthenticationError(ProviderError):
    """Raised when authentication with a provider fails."""
    pass


class ServiceUnavailableError(ProviderError):
    """Raised when a provider's service is unavailable."""
    pass


class ModelNotFoundError(ProviderError):
    """Raised when a requested model is not found."""
    pass


class ContentFilterError(ProviderError):
    """Raised when content is filtered by the provider."""
    pass


class LLMProviderError(ZLLMError):
    """Exception raised when an LLM provider fails to generate a response."""
    pass


class ConnectionError(ZLLMError):
    """Exception raised for network connection errors."""
    pass


class TimeoutError(ZLLMError):
    """Exception raised when a request times out."""
    pass


class LLMError(Exception):
    """Base exception for all ZLLM errors."""
    pass


class LLMRateLimitError(ProviderError):
    """Rate limit exceeded for an LLM provider."""

    def __init__(self, message: str, retry_after: int = 60):
        """
        Initialize a new rate limit error.

        Args:
            message: Error message
            retry_after: Seconds to wait before retrying
        """
        super().__init__(message)
        self.retry_after = retry_after


class LLMTimeoutError(ProviderError):
    """Timeout while waiting for a response from an LLM provider."""
    pass


class LLMAuthenticationError(ProviderError):
    """Authentication error with an LLM provider."""
    pass
