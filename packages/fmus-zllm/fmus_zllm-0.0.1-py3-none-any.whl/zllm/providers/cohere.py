"""
Cohere API provider implementation.

This module provides integration with Cohere's API for LLM functionality.
"""

import asyncio
import time
from typing import List, Optional, Callable, Dict, Any

import cohere
from cohere.errors import (
    UnauthorizedError, TooManyRequestsError, BadRequestError,
    InternalServerError, ServiceUnavailableError
)

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry


class CohereProvider(LLMProvider):
    """Cohere API implementation using the official Cohere SDK."""

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Cohere provider.

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
        Get a Cohere client with the current API key.

        Returns:
            Tuple of (initialized Cohere client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key = self.key_manager.get_random_key("cohere")
        if not api_key:
            raise APIKeyError("No API key available for Cohere")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            self._client = cohere.AsyncClient(api_key=api_key.key)
            self._api_key = api_key.key

        return self._client, api_key

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        return self._registry.get_models_for_provider("cohere")

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        return self._registry.get_default_model("cohere")

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the Cohere API.

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

            # Format messages for Cohere API
            chat_history, message = self._format_messages_for_api(messages)

            # Set generation parameters
            params = {
                "model": model_name,
                "message": message,
                "temperature": temperature,
            }

            if chat_history:
                params["chat_history"] = chat_history

            if max_tokens:
                params["max_tokens"] = max_tokens

            # Generate response
            response = await client.chat(**params)

            # Mark the API key as used
            api_key.mark_used()

            # Extract and return the response text
            return response.text

        except TooManyRequestsError as e:
            if api_key is None:
                raise APIKeyError("Failed to initialize Cohere client") from e

            retry_delay = 60  # Default retry delay
            api_key.last_used = time.time()  # Mark as used but not errored
            raise RateLimitError(
                f"Cohere rate limit exceeded. Retry after {retry_delay}s.",
                retry_after=retry_delay
            ) from e

        except UnauthorizedError as e:
            if api_key is None:
                raise APIKeyError("Failed to initialize Cohere client") from e

            api_key.mark_error()
            raise AuthenticationError("Invalid API key for Cohere") from e

        except (BadRequestError, InternalServerError, ServiceUnavailableError) as e:
            if api_key:
                api_key.mark_error()
            raise ValueError(f"Error calling Cohere API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            raise ValueError(f"Unexpected error with Cohere API: {str(e)}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the Cohere API.

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

            # Format messages for Cohere API
            chat_history, message = self._format_messages_for_api(messages)

            # Set generation parameters
            params = {
                "model": model_name,
                "message": message,
                "temperature": temperature,
            }

            if chat_history:
                params["chat_history"] = chat_history

            if max_tokens:
                params["max_tokens"] = max_tokens

            # Generate streaming response
            stream_response = client.chat_stream(**params)

            # Process the stream
            async for response in stream_response:
                if response.event_type == "text-generation":
                    # Check if callback is a coroutine function and await it if it is
                    if asyncio.iscoroutinefunction(callback):
                        await callback(response.text)
                    else:
                        callback(response.text)

            # Mark the API key as used
            api_key.mark_used()

        except TooManyRequestsError as e:
            if api_key is None:
                raise APIKeyError("Failed to initialize Cohere client") from e

            retry_delay = 60  # Default retry delay
            api_key.last_used = time.time()  # Mark as used but not errored
            raise RateLimitError(
                f"Cohere rate limit exceeded. Retry after {retry_delay}s.",
                retry_after=retry_delay
            ) from e

        except UnauthorizedError as e:
            if api_key is None:
                raise APIKeyError("Failed to initialize Cohere client") from e

            api_key.mark_error()
            raise AuthenticationError("Invalid API key for Cohere") from e

        except (BadRequestError, InternalServerError, ServiceUnavailableError) as e:
            if api_key:
                api_key.mark_error()
            raise ValueError(f"Error calling Cohere API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            raise ValueError(f"Unexpected error with Cohere API: {str(e)}") from e

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> tuple:
        """
        Format messages for the Cohere API.

        Args:
            messages: List of messages to format

        Returns:
            Tuple of (chat_history, message) for Cohere API
        """
        chat_history = []
        system_message = None
        user_message = None

        # Extract system message and build chat history
        for message in messages:
            role = message.role.lower()

            if role == "system":
                system_message = message.content
            elif role == "user":
                user_message = message.content
            elif role == "assistant" and len(chat_history) > 0:
                # Add user-assistant pair to chat history
                chat_history.append({
                    "role": "USER",
                    "message": chat_history[-1]["message"]
                })
                chat_history.append({
                    "role": "CHATBOT",
                    "message": message.content
                })

        # Construct final message with system prompt if available
        final_message = user_message or ""
        if system_message and final_message:
            final_message = f"{system_message}\n\n{final_message}"
        elif system_message:
            final_message = system_message

        return chat_history, final_message

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported, False otherwise
        """
        return True


# Register the provider
register_provider("cohere", CohereProvider)
