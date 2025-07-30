"""
OpenAI API provider implementation.

This module provides integration with OpenAI's API for LLM functionality.
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


class OpenAIProvider(LLMProvider):
    """OpenAI API implementation using the official OpenAI SDK."""

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the OpenAI provider.

        Args:
            key_manager: KeyManager instance for API key management
        """
        super().__init__(key_manager)
        self._api_key = None
        self._client = None
        self._config = get_config()
        self._registry = get_registry()
        logger.info("OpenAI provider initialized")

    def _get_client(self):
        """
        Get an OpenAI client with the current API key.

        Returns:
            Tuple of (initialized OpenAI client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key = self.key_manager.get_random_key("openai")
        if not api_key:
            logger.error("No API key available for OpenAI")
            raise APIKeyError("No API key available for OpenAI")

        logger.debug(f"Using OpenAI API key: {api_key.key[:5]}...{api_key.key[-5:] if len(api_key.key) > 10 else ''}")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            logger.debug("Creating new OpenAI client with updated API key")
            self._client = AsyncOpenAI(api_key=api_key.key)
            self._api_key = api_key.key

        return self._client, api_key

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        logger.debug("Getting available OpenAI models")
        return self._registry.get_models_for_provider("openai")

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        default_model = self._registry.get_default_model("openai")
        logger.debug(f"Using default OpenAI model: {default_model}")
        return default_model

    def get_available_image_models(self) -> List[str]:
        """
        Get a list of available image models for this provider.

        Returns:
            List of image model identifiers
        """
        logger.debug("Getting available OpenAI image models")
        return self._registry.get_image_models_for_provider("openai")

    def get_default_image_model(self) -> str:
        """
        Get the default image model for this provider.

        Returns:
            Default image model name
        """
        default_image_model = self._registry.get_default_image_model("openai")
        logger.debug(f"Using default OpenAI image model: {default_image_model}")
        return default_image_model

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the OpenAI API.

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
            logger.info(f"Generating response with OpenAI, model={model or 'default'}, temperature={temperature}")
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()

            # Format messages for OpenAI API
            formatted_messages = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for OpenAI API")

            # Set generation parameters
            params = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": temperature,
            }

            if max_tokens:
                params["max_tokens"] = max_tokens

            logger.debug(f"OpenAI request parameters: {params}")

            # Generate response
            logger.debug("Sending request to OpenAI API")
            response = await client.chat.completions.create(**params)
            logger.debug("Received response from OpenAI API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Extract and return the response text
            result = response.choices[0].message.content
            logger.info(f"Generated response of length {len(result)}")
            return result

        except OpenAIError as e:
            if api_key is None:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                raise APIKeyError("Failed to initialize OpenAI client") from e

            # Handle specific error types
            error_type = type(e).__name__
            logger.error(f"OpenAI API error: {error_type} - {str(e)}")

            # Rate limit errors
            if "RateLimitError" in error_type:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"OpenAI rate limit exceeded. Retry after {retry_delay}s.")
                raise RateLimitError(
                    f"OpenAI rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if "AuthenticationError" in error_type:
                api_key.mark_error()
                logger.error("Invalid API key for OpenAI")
                raise AuthenticationError("Invalid API key for OpenAI") from e

            # Other errors
            api_key.mark_error()
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise ValueError(f"Error calling OpenAI API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            logger.error(f"Unexpected error with OpenAI API: {str(e)}")
            raise ValueError(f"Unexpected error with OpenAI API: {str(e)}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the OpenAI API.

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
            logger.info(f"Generating streaming response with OpenAI, model={model or 'default'}, temperature={temperature}")
            client, api_key = self._get_client()
            model_name = model or self.get_default_model()

            # Format messages for OpenAI API
            formatted_messages = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for OpenAI API")

            # Set generation parameters
            params = {
                "model": model_name,
                "messages": formatted_messages,
                "temperature": temperature,
                "stream": True
            }

            if max_tokens:
                params["max_tokens"] = max_tokens

            logger.debug(f"OpenAI streaming request parameters: {params}")

            # Generate streaming response
            logger.debug("Sending streaming request to OpenAI API")
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
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                raise APIKeyError("Failed to initialize OpenAI client") from e

            # Handle specific error types
            error_type = type(e).__name__
            logger.error(f"OpenAI API error: {error_type} - {str(e)}")

            # Rate limit errors
            if "RateLimitError" in error_type:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"OpenAI rate limit exceeded. Retry after {retry_delay}s.")
                raise RateLimitError(
                    f"OpenAI rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if "AuthenticationError" in error_type:
                api_key.mark_error()
                logger.error("Invalid API key for OpenAI")
                raise AuthenticationError("Invalid API key for OpenAI") from e

            # Other errors
            api_key.mark_error()
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise ValueError(f"Error calling OpenAI API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            logger.error(f"Unexpected error with OpenAI API: {str(e)}")
            raise ValueError(f"Unexpected error with OpenAI API: {str(e)}") from e

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> List[Dict[str, str]]:
        """
        Format messages for the OpenAI API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted messages for the OpenAI API
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

    async def generate_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        size: Optional[str] = None,
        format: str = "url",
        **kwargs
    ) -> Union[str, bytes]:
        """
        Generate an image from a text prompt using OpenAI's DALL-E.

        Args:
            prompt: Text prompt to generate image from
            model: Model to use (defaults to dall-e-3)
            size: Size of the image to generate (e.g., "1024x1024")
            format: Format of the returned image ("url" or "bytes")
            **kwargs: Additional parameters for the API

        Returns:
            Image URL or binary data depending on format parameter

        Raises:
            APIKeyError: If no API key is available
            Exception: On API errors
        """
        client = None
        api_key = None

        try:
            logger.info(f"Generating image with OpenAI, prompt='{prompt}', model={model or 'default'}, size={size or '1024x1024'}, format={format}")
            client, api_key = self._get_client()
            model_name = model or self.get_default_image_model()

            # Default size if not specified
            if not size:
                size = "1024x1024"

            logger.debug(f"Using image model: {model_name}, size: {size}")

            # Set generation parameters
            params = {
                "model": model_name,
                "prompt": prompt,
                "size": size,
                "n": 1,
            }

            # Add any additional parameters
            for key, value in kwargs.items():
                params[key] = value

            logger.debug(f"OpenAI image generation parameters: {params}")

            # Generate image
            logger.debug("Sending image generation request to OpenAI API")
            response = await client.images.generate(**params)
            logger.debug("Received image generation response from OpenAI API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Extract the image URL
            if response.data and len(response.data) > 0:
                image_url = response.data[0].url
                logger.debug(f"Generated image URL: {image_url}")

                # If format is "url", return the URL directly
                if format.lower() == "url":
                    logger.info("Returning image URL")
                    return image_url

                # Otherwise, download the image data
                logger.debug("Downloading image data from URL")
                import aiohttp
                async with aiohttp.ClientSession() as session:
                    async with session.get(image_url) as img_response:
                        if img_response.status == 200:
                            image_data = await img_response.read()
                            logger.info(f"Downloaded image data, size: {len(image_data)} bytes")
                            return image_data
                        else:
                            error_msg = f"Failed to download image: {img_response.status}"
                            logger.error(error_msg)
                            raise ValueError(error_msg)

            error_msg = "No image data in response"
            logger.error(error_msg)
            raise ValueError(error_msg)

        except OpenAIError as e:
            if api_key is None:
                logger.error(f"Failed to initialize OpenAI client: {str(e)}")
                raise APIKeyError("Failed to initialize OpenAI client") from e

            # Handle specific error types
            error_type = type(e).__name__
            logger.error(f"OpenAI API error: {error_type} - {str(e)}")

            # Rate limit errors
            if "RateLimitError" in error_type:
                retry_delay = getattr(e, 'retry_after', 60)
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"OpenAI rate limit exceeded. Retry after {retry_delay}s.")
                raise RateLimitError(
                    f"OpenAI rate limit exceeded. Retry after {retry_delay}s.",
                    retry_after=retry_delay
                ) from e

            # Authentication errors
            if "AuthenticationError" in error_type:
                api_key.mark_error()
                logger.error("Invalid API key for OpenAI")
                raise AuthenticationError("Invalid API key for OpenAI") from e

            # Other errors
            api_key.mark_error()
            logger.error(f"Error calling OpenAI API: {str(e)}")
            raise ValueError(f"Error calling OpenAI API: {str(e)}") from e

        except Exception as e:
            if api_key:
                api_key.mark_error()
            logger.error(f"Unexpected error with OpenAI API: {str(e)}")
            raise ValueError(f"Unexpected error with OpenAI API: {str(e)}") from e

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported, False otherwise
        """
        logger.debug("OpenAI provider supports streaming")
        return True

    @property
    def supports_image_generation(self) -> bool:
        """
        Check if this provider supports image generation.

        Returns:
            True if image generation is supported, False otherwise
        """
        logger.debug("OpenAI provider supports image generation")
        return True

    @property
    def supports_function_calling(self) -> bool:
        """
        Check if this provider supports function calling.

        Returns:
            True if function calling is supported
        """
        return True

    @property
    def supports_structured_output(self) -> bool:
        """
        Check if this provider supports structured output.

        Returns:
            True if structured output is supported
        """
        return True

    @property
    def supports_vision(self) -> bool:
        """
        Check if this provider supports vision/image input.

        Returns:
            True if vision is supported
        """
        return True

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
register_provider("openai", OpenAIProvider)
