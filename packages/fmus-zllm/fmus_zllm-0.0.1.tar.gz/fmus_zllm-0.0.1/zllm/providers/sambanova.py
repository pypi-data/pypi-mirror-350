"""
Sambanova API provider implementation.

This module provides integration with Sambanova's API for LLM functionality.
"""

import asyncio
import time
import logging
from typing import List, Optional, Callable, Dict, Any, Union

from openai import AsyncOpenAI, OpenAIError

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry

# Set up logging
logger = logging.getLogger(__name__)


class SambanovaProvider(LLMProvider):
    """Sambanova API implementation using OpenAI SDK."""

    # Base URL for the Sambanova API
    API_BASE_URL = "https://api.sambanova.ai/v1"

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Sambanova provider.

        Args:
            key_manager: KeyManager instance for API key management
        """
        super().__init__(key_manager)
        self._api_key = None
        self._client = None
        self._config = get_config()
        self._registry = get_registry()
        logger.info("Sambanova provider initialized")

    def _get_client(self):
        """
        Get an OpenAI client with the current API key and Sambanova base URL.

        Returns:
            Tuple of (initialized OpenAI client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key = self.key_manager.get_random_key("sambanova")
        if not api_key:
            logger.error("No API key available for Sambanova")
            raise APIKeyError("No API key available for Sambanova")

        logger.debug(f"Using Sambanova API key: {api_key.key[:5]}...{api_key.key[-5:] if len(api_key.key) > 10 else ''}")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            logger.debug("Creating new OpenAI client with Sambanova base URL")
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
        logger.debug("Getting available Sambanova models")
        return self._registry.get_models_for_provider("sambanova")

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        default_model = self._registry.get_default_model("sambanova")
        logger.debug(f"Using default Sambanova model: {default_model}")
        return default_model

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the Sambanova API.

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
            logger.info(f"Generating response with Sambanova, model={model or 'default'}, temperature={temperature}")
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()
            print(f"Sambanova => Model name: {model_name}. api_key: {api_key.name}")
            # Format prompt for Sambanova API
            prompt = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for Sambanova API")

            # Set generation parameters
            params = {
                "model": model_name,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens or 512,
                "stop": ["Human:", "Assistant:"]
            }

            logger.debug(f"Sambanova request parameters: {params}")

            # Generate response
            logger.debug("Sending request to Sambanova API")
            response = await client.completions.create(**params)
            logger.debug("Received response from Sambanova API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Extract and return the response text
            result = response.choices[0].text.strip()
            logger.info(f"Generated response of length {len(result)}")
            return result

        except OpenAIError as e:
            if api_key is None:
                logger.error(f"Failed to initialize Sambanova client: {str(e)}")
                raise APIKeyError("Failed to initialize Sambanova client") from e

            # Handle specific error types
            error_type = type(e).__name__
            logger.error(f"Sambanova API error: {error_type} - {str(e)}")

            # Rate limit errors
            if "RateLimitError" in error_type:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Sambanova rate limit exceeded. Retry after {retry_delay}s.")
                raise RateLimitError(
                    f"Sambanova rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if "AuthenticationError" in error_type:
                api_key.mark_error()
                logger.error("Invalid API key for Sambanova")
                raise AuthenticationError("Invalid API key for Sambanova") from e

            # Other errors
            api_key.mark_error()
            logger.error(f"Error calling Sambanova API: {str(e)}")
            raise ValueError(f"Error calling Sambanova API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            logger.error(f"Unexpected error with Sambanova API: {str(e)}")
            raise ValueError(f"Unexpected error with Sambanova API: {str(e)}") from e

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> str:
        """
        Format messages for the Sambanova API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted prompt string for Sambanova API
        """
        system_message = None
        conversation = []

        # Extract system message if present
        for message in messages:
            if message.role.lower() == "system":
                system_message = message.content
                break

        # Format conversation
        for message in messages:
            role = message.role.lower()

            if role == "system":
                continue  # Already handled
            elif role == "user":
                conversation.append(f"Human: {message.content}")
            elif role == "assistant":
                conversation.append(f"Assistant: {message.content}")
            else:
                # Unknown role, treat as user
                conversation.append(f"Human: {message.content}")

        # Add final assistant prompt
        conversation.append("Assistant:")

        # Combine system message and conversation
        if system_message:
            prompt = f"{system_message}\n\n" + "\n".join(conversation)
        else:
            prompt = "\n".join(conversation)

        return prompt

    async def close(self) -> None:
        """Close any resources held by the provider."""
        # Nothing to close when using OpenAI client
        pass

    @property
    def supports_streaming(self) -> bool:
        """
        Returns whether the Sambanova provider supports streaming.
        """
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

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the Sambanova API.

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
            logger.info(f"Generating streaming response with Sambanova, model={model or 'default'}, temperature={temperature}")
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()

            # Format prompt for Sambanova API
            prompt = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for Sambanova API")

            # Set generation parameters
            params = {
                "model": model_name,
                "prompt": prompt,
                "temperature": temperature,
                "max_tokens": max_tokens or 512,
                "stop": ["Human:", "Assistant:"],
                "stream": True
            }

            logger.debug(f"Sambanova streaming request parameters: {params}")

            # Generate streaming response
            logger.debug("Sending streaming request to Sambanova API")
            stream = await client.completions.create(**params)

            # Process the stream
            chunk_count = 0
            logger.debug("Processing response stream")
            async for chunk in stream:
                if chunk.choices and chunk.choices[0].text:
                    content = chunk.choices[0].text
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
                logger.error(f"Failed to initialize Sambanova client: {str(e)}")
                raise APIKeyError("Failed to initialize Sambanova client") from e

            # Handle specific error types
            error_type = type(e).__name__
            logger.error(f"Sambanova API error: {error_type} - {str(e)}")

            # Rate limit errors
            if "RateLimitError" in error_type:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Sambanova rate limit exceeded. Retry after {retry_delay}s.")
                raise RateLimitError(
                    f"Sambanova rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if "AuthenticationError" in error_type:
                api_key.mark_error()
                logger.error("Invalid API key for Sambanova")
                raise AuthenticationError("Invalid API key for Sambanova") from e

            # Other errors
            api_key.mark_error()
            logger.error(f"Error calling Sambanova API: {str(e)}")
            raise ValueError(f"Error calling Sambanova API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            logger.error(f"Unexpected error with Sambanova API: {str(e)}")
            raise ValueError(f"Unexpected error with Sambanova API: {str(e)}") from e


# Register the provider
register_provider("sambanova", SambanovaProvider)
