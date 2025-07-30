"""
HuggingFace API provider implementation.

This module provides integration with HuggingFace's Inference API for LLM functionality.
"""

import asyncio
import json
import time
import logging
from typing import List, Optional, Callable, Dict, Any

from huggingface_hub import AsyncInferenceClient

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry

logger = logging.getLogger(__name__)

class HuggingFaceProvider(LLMProvider):
    """HuggingFace Inference API implementation using the official huggingface_hub SDK."""

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the HuggingFace provider.

        Args:
            key_manager: KeyManager instance for API key management
        """
        super().__init__(key_manager)
        self._clients = {}  # Cache for clients with different API keys
        self._config = get_config()
        self._registry = get_registry()

    async def _get_client(self):
        """
        Get an AsyncInferenceClient with the current API key.

        Returns:
            Tuple of (initialized AsyncInferenceClient, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key_obj = self.key_manager.get_random_key("huggingface")
        if not api_key_obj:
            logger.error("No API key available for HuggingFace")
            raise APIKeyError("No API key available for HuggingFace")

        api_key = api_key_obj.key

        # Create or reuse client for this API key
        if api_key not in self._clients:
            logger.debug(f"Creating new HuggingFace client for API key {api_key[:5]}...")
            self._clients[api_key] = AsyncInferenceClient(token=api_key)

        return self._clients[api_key], api_key_obj

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        return self._registry.get_models_for_provider("huggingface")

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        return self._registry.get_default_model("huggingface")

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the HuggingFace Inference API.

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
            logger.info(f"Generating response with HuggingFace, model={model or 'default'}, temperature={temperature}")
            client, api_key = await self._get_client()
            model_name = model or self.get_default_model()
            logger.debug(f"Using model: {model_name}")

            # Format messages for HuggingFace API
            prompt = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for HuggingFace API")

            # Set generation parameters
            params = {
                "do_sample": True,
                "temperature": temperature,
                "return_full_text": False
            }

            if max_tokens:
                params["max_new_tokens"] = max_tokens

            # Make the API request
            logger.debug("Sending request to HuggingFace API")
            result = await client.text_generation(
                prompt,
                model=model_name,
                **params
            )
            logger.debug("Received response from HuggingFace API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            return result

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            logger.error(f"Error with HuggingFace API: {error_type} - {error_msg}")

            if api_key is None:
                raise APIKeyError("Failed to initialize HuggingFace client") from e

            # Handle authentication errors
            if "401" in error_msg or "Unauthorized" in error_msg:
                api_key.mark_error()
                logger.error("Invalid API key for HuggingFace")
                raise AuthenticationError("Invalid API key for HuggingFace") from e

            # Handle rate limit errors
            if "429" in error_msg or "Rate limit" in error_msg:
                # Try to extract retry-after if present
                retry_after = 60
                if hasattr(e, 'headers') and e.headers.get("Retry-After"):
                    retry_after = int(e.headers.get("Retry-After", 60))

                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"HuggingFace rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"HuggingFace rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            # Other errors
            if api_key:
                api_key.mark_error()

            raise ValueError(f"Error calling HuggingFace API: {str(e)}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the HuggingFace API.

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
            logger.info(f"Generating streaming response with HuggingFace, model={model or 'default'}, temperature={temperature}")
            client, api_key = await self._get_client()
            model_name = model or self.get_default_model()
            logger.debug(f"Using model: {model_name}")

            # Format messages for HuggingFace API
            prompt = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for HuggingFace API")

            # Set generation parameters
            params = {
                "do_sample": True,
                "temperature": temperature,
                "return_full_text": False,
                "stream": True  # Enable streaming
            }

            if max_tokens:
                params["max_new_tokens"] = max_tokens

            # Make the API request with streaming
            logger.debug("Sending streaming request to HuggingFace API")
            text_generation_stream = await client.text_generation(
                prompt,
                model=model_name,
                **params
            )

            async for token in text_generation_stream:
                # Check if callback is a coroutine function and await it if it is
                if asyncio.iscoroutinefunction(callback):
                    await callback(token)
                else:
                    callback(token)

            logger.debug("Streaming response completed")
            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            logger.error(f"Error with HuggingFace API: {error_type} - {error_msg}")

            if api_key is None:
                raise APIKeyError("Failed to initialize HuggingFace client") from e

            # Handle authentication errors
            if "401" in error_msg or "Unauthorized" in error_msg:
                api_key.mark_error()
                logger.error("Invalid API key for HuggingFace")
                raise AuthenticationError("Invalid API key for HuggingFace") from e

            # Handle rate limit errors
            if "429" in error_msg or "Rate limit" in error_msg:
                # Try to extract retry-after if present
                retry_after = 60
                if hasattr(e, 'headers') and e.headers.get("Retry-After"):
                    retry_after = int(e.headers.get("Retry-After", 60))

                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"HuggingFace rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"HuggingFace rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            # Other errors
            if api_key:
                api_key.mark_error()

            raise ValueError(f"Error calling HuggingFace API: {str(e)}") from e

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> str:
        """
        Format messages for the HuggingFace API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted prompt string for HuggingFace API
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

    async def close(self):
        """Close any open resources when done."""
        # The AsyncInferenceClient handles its own resources, nothing to close explicitly
        self._clients = {}
        logger.debug("Cleared HuggingFace clients")

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported, False otherwise
        """
        return True

    @property
    def supports_embeddings(self) -> bool:
        """
        Check if this provider supports embeddings.

        Returns:
            True if embeddings are supported, False otherwise
        """
        return True

    @property
    def supports_image_generation(self) -> bool:
        """
        Check if this provider supports image generation.

        Returns:
            True if image generation is supported, False otherwise
        """
        return True

    async def generate_embeddings(self, text: str, model: Optional[str] = None) -> List[float]:
        """
        Generate embeddings for a given text.

        Args:
            text: Text to generate embeddings for
            model: Embedding model to use (defaults to provider's default model)

        Returns:
            List of embedding values

        Raises:
            APIKeyError: If no API key is available
            AuthenticationError: If the API key is invalid
            Exception: On other API errors
        """
        client = None
        api_key = None

        try:
            logger.info(f"Generating embeddings with HuggingFace, model={model or 'default'}")
            client, api_key = await self._get_client()

            # Get the model name
            if model is None:
                # Look for embedding models in the registry
                embedding_models = self._registry.get_models("huggingface", "embedding_models")
                if embedding_models:
                    # Find the default model or use the first one
                    for emb_model in embedding_models:
                        if emb_model.get("default", False):
                            model = emb_model.get("id")
                            break
                    if model is None and embedding_models:
                        model = embedding_models[0].get("id")

            if model is None:
                model = "sentence-transformers/all-mpnet-base-v2"  # Fallback default

            logger.debug(f"Using embedding model: {model}")

            # Make the API request
            logger.debug("Sending embedding request to HuggingFace API")
            result = await client.feature_extraction(
                text,
                model=model
            )

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Convert to list if it's a numpy array
            if hasattr(result, 'tolist'):
                return result.tolist()[0]  # Get the first vector if it's a batch
            return result[0] if isinstance(result, list) else result

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            logger.error(f"Error with HuggingFace API for embeddings: {error_type} - {error_msg}")

            if api_key is None:
                raise APIKeyError("Failed to initialize HuggingFace client") from e

            # Handle authentication errors
            if "401" in error_msg or "Unauthorized" in error_msg:
                api_key.mark_error()
                logger.error("Invalid API key for HuggingFace")
                raise AuthenticationError("Invalid API key for HuggingFace") from e

            # Handle rate limit errors
            if "429" in error_msg or "Rate limit" in error_msg:
                retry_after = 60
                if hasattr(e, 'headers') and e.headers.get("Retry-After"):
                    retry_after = int(e.headers.get("Retry-After", 60))

                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"HuggingFace rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"HuggingFace rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            # Other errors
            if api_key:
                api_key.mark_error()

            raise ValueError(f"Error calling HuggingFace API for embeddings: {str(e)}") from e

    async def generate_image(self, prompt: str, model: Optional[str] = None, n: int = 1) -> List[bytes]:
        """
        Generate images using text-to-image models.

        Args:
            prompt: Text prompt to generate images from
            model: Name of the model to use
            n: Number of images to generate

        Returns:
            List of image data as bytes

        Raises:
            APIKeyError: If no API key is available
            AuthenticationError: If the API key is invalid
            Exception: On other API errors
        """
        client = None
        api_key = None

        try:
            logger.info(f"Generating image with HuggingFace, model={model or 'default'}")
            client, api_key = await self._get_client()

            # Get the model name
            if model is None:
                # Look for image models in the registry
                image_models = self._registry.get_models("huggingface", "image_models")
                if image_models:
                    # Find the default model or use the first one
                    for img_model in image_models:
                        if img_model.get("default", False):
                            model = img_model.get("id")
                            break
                    if model is None and image_models:
                        model = image_models[0].get("id")

            if model is None:
                model = "stabilityai/stable-diffusion-xl-base-1.0"  # Fallback default

            logger.debug(f"Using image model: {model}")

            # Make the API request
            logger.debug("Sending image generation request to HuggingFace API")
            images = []

            for _ in range(n):
                image = await client.text_to_image(
                    prompt,
                    model=model
                )

                # Convert PIL image to bytes if needed
                if hasattr(image, 'tobytes'):
                    import io
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    images.append(img_byte_arr.getvalue())
                else:
                    images.append(image)

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            return images

        except Exception as e:
            error_type = type(e).__name__
            error_msg = str(e)
            logger.error(f"Error with HuggingFace API for image generation: {error_type} - {error_msg}")

            if api_key is None:
                raise APIKeyError("Failed to initialize HuggingFace client") from e

            # Handle authentication errors
            if "401" in error_msg or "Unauthorized" in error_msg:
                api_key.mark_error()
                logger.error("Invalid API key for HuggingFace")
                raise AuthenticationError("Invalid API key for HuggingFace") from e

            # Handle rate limit errors
            if "429" in error_msg or "Rate limit" in error_msg:
                retry_after = 60
                if hasattr(e, 'headers') and e.headers.get("Retry-After"):
                    retry_after = int(e.headers.get("Retry-After", 60))

                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"HuggingFace rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"HuggingFace rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            # Other errors
            if api_key:
                api_key.mark_error()

            raise ValueError(f"Error calling HuggingFace API for image generation: {str(e)}") from e


# Register the provider
register_provider("huggingface", HuggingFaceProvider)
