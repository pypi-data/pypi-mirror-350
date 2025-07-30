"""
Anthropic API provider implementation.

This module provides integration with Anthropic's Claude API for LLM functionality.
"""

import asyncio
import time
from typing import List, Optional, Callable, Dict, Any

import anthropic

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry


class AnthropicProvider(LLMProvider):
    """Anthropic Claude API implementation using the official Anthropic SDK."""

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Anthropic provider.

        Args:
            key_manager: KeyManager instance for API key management
        """
        super().__init__(key_manager)
        self._api_key = None
        self._client = None
        self._config = get_config()
        self._registry = get_registry()

    def _get_client(self):
        """
        Get an Anthropic client with the current API key.

        Returns:
            Tuple of (initialized Anthropic client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key = self.key_manager.get_random_key("anthropic")
        if not api_key:
            raise APIKeyError("No API key available for Anthropic")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            self._client = anthropic.AsyncAnthropic(api_key=api_key.key)
            self._api_key = api_key.key

        return self._client, api_key

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        return self._registry.get_models_for_provider("anthropic")

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        return self._registry.get_default_model("anthropic")

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the Anthropic API.

        Args:
            messages: List of messages in the conversation
            model: Name of the model to use (defaults to the default model)
            temperature: Temperature parameter for generation (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate

        Returns:
            Generated text response

        Raises:
            APIKeyError: If no API key is available
            RateLimitError: If the API rate limit is exceeded
            AuthenticationError: If the API key is invalid
            Exception: On other API errors
        """
        client = None
        api_key = None

        try:
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()

            # Format messages for Anthropic API
            formatted_messages = self._format_messages_for_api(messages)

            # Set generation parameters
            params = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": temperature,
            }

            if max_tokens:
                params["max_tokens"] = max_tokens
            else:
                params["max_tokens"] = 4096  # Default max tokens

            # Generate response
            response = await client.messages.create(**params)

            # Mark the API key as used
            api_key.mark_used()

            # Extract and return the response text
            return response.content[0].text

        except anthropic.APIError as e:
            if api_key is None:
                raise APIKeyError("Failed to initialize Anthropic client") from e

            # Handle specific error types
            error_type = type(e).__name__
            status_code = getattr(e, 'status_code', None)

            # Rate limit errors
            if status_code == 429:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                raise RateLimitError(
                    f"Anthropic rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if status_code == 401:
                api_key.mark_error()
                raise AuthenticationError("Invalid API key for Anthropic") from e

            # Other errors
            api_key.mark_error()
            raise ValueError(f"Error calling Anthropic API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            raise ValueError(f"Unexpected error with Anthropic API: {str(e)}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the Anthropic API.

        Args:
            messages: List of messages in the conversation
            callback: Function to call for each chunk of the response
            model: Name of the model to use
            temperature: Temperature parameter for generation (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate

        Raises:
            APIKeyError: If no API key is available
            RateLimitError: If the API rate limit is exceeded
            AuthenticationError: If the API key is invalid
            Exception: On other API errors
        """
        client = None
        api_key = None

        try:
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()

            # Format messages for Anthropic API
            formatted_messages = self._format_messages_for_api(messages)

            # Set generation parameters
            params = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": temperature,
                "stream": True
            }

            if max_tokens:
                params["max_tokens"] = max_tokens
            else:
                params["max_tokens"] = 4096  # Default max tokens

            # Generate streaming response
            stream = await client.messages.create(**params)

            # Process the stream
            async for chunk in stream:
                if chunk.type == "content_block_delta" and hasattr(chunk, "delta") and hasattr(chunk.delta, "text"):
                    callback(chunk.delta.text)

            # Mark the API key as used
            api_key.mark_used()

        except anthropic.APIError as e:
            if api_key is None:
                raise APIKeyError("Failed to initialize Anthropic client") from e

            # Handle specific error types
            error_type = type(e).__name__
            status_code = getattr(e, 'status_code', None)

            # Rate limit errors
            if status_code == 429:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                raise RateLimitError(
                    f"Anthropic rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if status_code == 401:
                api_key.mark_error()
                raise AuthenticationError("Invalid API key for Anthropic") from e

            # Other errors
            api_key.mark_error()
            raise ValueError(f"Error calling Anthropic API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            raise ValueError(f"Unexpected error with Anthropic API: {str(e)}") from e

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> List[Dict[str, Any]]:
        """
        Format messages for the Anthropic API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted messages for the Anthropic API
        """
        formatted_messages = []
        system_content = None

        # Extract system message if present
        for message in messages:
            if message.role.lower() == "system":
                system_content = message.content
                break

        # Format non-system messages
        for message in messages:
            role = message.role.lower()

            if role == "system":
                # System messages are handled separately
                continue
            elif role == "user":
                formatted_messages.append({
                    "role": "user",
                    "content": message.content
                })
            elif role == "assistant":
                formatted_messages.append({
                    "role": "assistant",
                    "content": message.content
                })
            else:
                # Unknown role, treat as user
                formatted_messages.append({
                    "role": "user",
                    "content": message.content
                })

        # Return formatted messages with system content if present
        if system_content:
            return formatted_messages, system_content
        else:
            return formatted_messages

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported, False otherwise
        """
        return True


# Register the provider
register_provider("anthropic", AnthropicProvider)
