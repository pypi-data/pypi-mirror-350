"""
Hyperbolic API provider implementation.

This module provides integration with Hyperbolic's API for LLM functionality.
"""

import asyncio
import time
import logging
from typing import List, Optional, Callable, Dict, Any, Union

from openai import AsyncOpenAI, OpenAIError
from openai.types.chat import ChatCompletion

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry

# Set up logging
logger = logging.getLogger(__name__)


class HyperbolicProvider(LLMProvider):
    """Hyperbolic API implementation using OpenAI SDK."""

    # Base URL for the Hyperbolic API
    API_BASE_URL = "https://api.hyperbolic.xyz/v1"

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Hyperbolic provider.

        Args:
            key_manager: KeyManager instance for API key management
        """
        super().__init__(key_manager)
        self._api_key = None
        self._client = None
        self._config = get_config()
        self._registry = get_registry()
        logger.info("Hyperbolic provider initialized")

    def _get_client(self):
        """
        Get an OpenAI client with the current API key and Hyperbolic base URL.

        Returns:
            Tuple of (initialized OpenAI client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key = self.key_manager.get_random_key("hyperbolic")
        if not api_key:
            logger.error("No API key available for Hyperbolic")
            raise APIKeyError("No API key available for Hyperbolic")

        logger.debug(f"Using Hyperbolic API key: {api_key.key[:5]}...{api_key.key[-5:] if len(api_key.key) > 10 else ''}")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            logger.debug("Creating new OpenAI client with Hyperbolic base URL")
            self._client = AsyncOpenAI(
                api_key=api_key.key,
                base_url=self.API_BASE_URL
            )
            self._api_key = api_key.key

        return self._client, api_key

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        logger.debug("Getting available Hyperbolic models")
        return self._registry.get_models_for_provider("hyperbolic")

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        default_model = self._registry.get_default_model("hyperbolic")
        logger.debug(f"Using default Hyperbolic model: {default_model}")
        return default_model

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the Hyperbolic API.

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
            logger.info(f"Generating response with Hyperbolic, model={model or 'default'}, temperature={temperature}")
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()

            # Format messages for OpenAI API
            formatted_messages = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for Hyperbolic API")

            # Set generation parameters
            params = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": temperature,
            }

            if max_tokens:
                params["max_tokens"] = max_tokens

            logger.debug(f"Hyperbolic request parameters: {params}")

            # Generate response
            logger.debug("Sending request to Hyperbolic API")
            response = await client.chat.completions.create(**params)
            logger.debug("Received response from Hyperbolic API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Extract and return the response text
            result = response.choices[0].message.content
            logger.info(f"Generated response of length {len(result)}")
            return result

        except OpenAIError as e:
            if api_key is None:
                logger.error(f"Failed to initialize Hyperbolic client: {str(e)}")
                raise APIKeyError("Failed to initialize Hyperbolic client") from e

            # Handle specific error types
            error_type = type(e).__name__
            logger.error(f"Hyperbolic API error: {error_type} - {str(e)}")

            # Rate limit errors
            if "RateLimitError" in error_type:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Hyperbolic rate limit exceeded. Retry after {retry_delay}s.")
                raise RateLimitError(
                    f"Hyperbolic rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if "AuthenticationError" in error_type:
                api_key.mark_error()
                logger.error("Invalid API key for Hyperbolic")
                raise AuthenticationError("Invalid API key for Hyperbolic") from e

            # Other errors
            api_key.mark_error()
            logger.error(f"Error calling Hyperbolic API: {str(e)}")
            raise ValueError(f"Error calling Hyperbolic API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            logger.error(f"Unexpected error with Hyperbolic API: {str(e)}")
            raise ValueError(f"Unexpected error with Hyperbolic API: {str(e)}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the Hyperbolic API.

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
            logger.info(f"Generating streaming response with Hyperbolic, model={model or 'default'}, temperature={temperature}")
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()

            # Format messages for OpenAI API
            formatted_messages = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for Hyperbolic API")

            # Set generation parameters
            params = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": temperature,
                "stream": True
            }

            if max_tokens:
                params["max_tokens"] = max_tokens

            logger.debug(f"Hyperbolic streaming request parameters: {params}")

            # Generate streaming response
            logger.debug("Sending streaming request to Hyperbolic API")
            stream = await client.chat.completions.create(**params)

            # Process the stream
            chunk_count = 0
            logger.debug("Processing response stream")
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    # Check if callback is a coroutine function and await it if it is
                    if asyncio.iscoroutinefunction(callback):
                        await callback(content)
                    else:
                        callback(content)
                    chunk_count += 1

            logger.debug(f"Processed {chunk_count} chunks from stream")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

        except OpenAIError as e:
            if api_key is None:
                logger.error(f"Failed to initialize Hyperbolic client: {str(e)}")
                raise APIKeyError("Failed to initialize Hyperbolic client") from e

            # Handle specific error types
            error_type = type(e).__name__
            logger.error(f"Hyperbolic API error: {error_type} - {str(e)}")

            # Rate limit errors
            if "RateLimitError" in error_type:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Hyperbolic rate limit exceeded. Retry after {retry_delay}s.")
                raise RateLimitError(
                    f"Hyperbolic rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if "AuthenticationError" in error_type:
                api_key.mark_error()
                logger.error("Invalid API key for Hyperbolic")
                raise AuthenticationError("Invalid API key for Hyperbolic") from e

            # Other errors
            api_key.mark_error()
            logger.error(f"Error calling Hyperbolic API: {str(e)}")
            raise ValueError(f"Error calling Hyperbolic API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            logger.error(f"Unexpected error with Hyperbolic API: {str(e)}")
            raise ValueError(f"Unexpected error with Hyperbolic API: {str(e)}") from e

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> List[Dict[str, str]]:
        """
        Format messages for the Hyperbolic API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted messages for the Hyperbolic API
        """
        formatted_messages = []

        for message in messages:
            role = message.role.lower()

            # Map roles to OpenAI roles
            if role == "system":
                formatted_messages.append({
                    "role": "system",
                    "content": message.content
                })
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

        return formatted_messages

    async def close(self) -> None:
        """Close any resources held by the provider."""
        # Nothing to close when using OpenAI client
        pass

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported
        """
        logger.debug("Hyperbolic provider supports streaming")
        return True

    @property
    def supports_function_calling(self) -> bool:
        """
        Check if this provider supports function calling.

        Returns:
            True if function calling is supported
        """
        return False

    @property
    def supports_structured_output(self) -> bool:
        """
        Check if this provider supports structured output.

        Returns:
            True if structured output is supported
        """
        return False

    @property
    def supports_vision(self) -> bool:
        """
        Check if this provider supports vision/image input.

        Returns:
            True if vision is supported
        """
        return False

    @property
    def supports_reasoning(self) -> bool:
        """
        Check if this provider supports explicit reasoning formats.

        Returns:
            True if reasoning formats are supported
        """
        return False

    @property
    def supports_agentic_tools(self) -> bool:
        """
        Check if this provider supports agentic tools.

        Returns:
            True if agentic tools are supported
        """
        return False


# Register the provider
register_provider("hyperbolic", HyperbolicProvider)
