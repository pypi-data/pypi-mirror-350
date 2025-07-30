"""
Google Gemini API provider implementation.

This module provides integration with Google's Gemini API for LLM functionality.
"""

import asyncio
import time
from typing import List, Optional, Callable

from google import genai

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry


class GeminiProvider(LLMProvider):
    """Google Gemini API implementation using official google.genai SDK."""

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Gemini provider.

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
        Get a Gemini client with the current API key.

        Returns:
            Tuple of (initialized Gemini client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key = self.key_manager.get_random_key("gemini")
        if not api_key:
            raise APIKeyError("No API key available for Gemini")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            self._client = genai.Client(api_key=api_key.key)
            self._api_key = api_key.key

        return self._client, api_key

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        models = self._registry.get_models("gemini", "text_models")
        return [model.get("id") for model in models]

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        return self._registry.get_default_model("gemini", "text_models")

    @property
    def supports_vision(self) -> bool:
        """
        Check if this provider supports vision/image input.

        Returns:
            True if vision is supported, False otherwise
        """
        return self._registry.supports_capability("gemini", "vision")

    @property
    def supports_image_generation(self) -> bool:
        """
        Check if this provider supports image generation.

        Returns:
            True if image generation is supported, False otherwise
        """
        return self._registry.supports_capability("gemini", "image_generation")

    @property
    def supports_embeddings(self) -> bool:
        """
        Check if this provider supports embeddings.

        Returns:
            True if embeddings are supported, False otherwise
        """
        return self._registry.supports_capability("gemini", "embeddings")

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the Gemini API.

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

            # Format messages for Gemini API
            formatted_contents = self._format_messages_for_api(messages)

            # Set generation config
            generation_config = {
                "temperature": temperature
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens

            # Run in an executor to avoid blocking the event loop
            response = await asyncio.to_thread(
                client.models.generate_content,
                model=model_name,
                contents=formatted_contents,
                config=generation_config
            )

            api_key.mark_used()
            return response.text

        except Exception as e:
            if api_key is None:
                # Error occurred before we got an API key
                raise APIKeyError("Failed to initialize Gemini client") from e

            # Handle rate limiting
            if hasattr(e, 'retry_after'):
                retry_delay = getattr(e, 'retry_after', 60)

                # Mark the key as used but not as an error
                api_key.last_used = time.time()

                raise RateLimitError(
                    f"Rate limit exceeded. Retry after {retry_delay}s. "
                    "Try using a different model like 'gemini-1.5-flash'.",
                    retry_after=retry_delay
                ) from e

            # All other errors mark the key as errored
            api_key.mark_error()

            # Categorize the error type
            error_type = type(e).__name__
            if "Unauthorized" in error_type:
                raise AuthenticationError("Invalid API key for Gemini") from e
            if "InvalidArgument" in error_type:
                raise ValueError(f"Invalid argument: {str(e)}") from e
            if "API" in error_type:
                raise ValueError(f"Gemini API error: {str(e)}") from e

            raise ValueError(f"Error calling Gemini API: {str(e)}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the Gemini API.

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

            # Format messages for Gemini API
            formatted_contents = self._format_messages_for_api(messages)

            # Set generation config
            generation_config = {
                "temperature": temperature
            }
            if max_tokens:
                generation_config["max_output_tokens"] = max_tokens

            # Run in an executor to avoid blocking the event loop
            stream = await asyncio.to_thread(
                client.models.generate_content,
                model=model_name,
                contents=formatted_contents,
                config=generation_config,
                stream=True  # Enable streaming
            )

            # Process the stream in chunks
            async def process_stream():
                try:
                    # Process chunks as they arrive
                    async for chunk in stream:
                        if hasattr(chunk, 'candidates') and chunk.candidates:
                            for candidate in chunk.candidates:
                                if hasattr(candidate, 'content') and candidate.content and candidate.content.parts:
                                    for part in candidate.content.parts:
                                        if hasattr(part, 'text') and part.text:
                                            if asyncio.iscoroutinefunction(callback):
                                                await callback(part.text)
                                            else:
                                                callback(part.text)
                except Exception as e:
                    raise ValueError(f"Error processing response stream: {str(e)}") from e

            await process_stream()
            api_key.mark_used()

        except Exception as e:
            if api_key is None:
                # Error occurred before we got an API key
                raise APIKeyError("Failed to initialize Gemini client") from e

            # Handle rate limiting
            if hasattr(e, 'retry_after'):
                retry_delay = getattr(e, 'retry_after', 60)

                # Mark the key as used but not as an error
                api_key.last_used = time.time()

                raise RateLimitError(
                    f"Rate limit exceeded. Retry after {retry_delay}s. "
                    "Try using a different model like 'gemini-1.5-flash'.",
                    retry_after=retry_delay
                ) from e

            # All other errors mark the key as errored
            api_key.mark_error()

            # Categorize the error type
            error_type = type(e).__name__
            if "Unauthorized" in error_type:
                raise AuthenticationError("Invalid API key for Gemini") from e
            if "InvalidArgument" in error_type:
                raise ValueError(f"Invalid argument: {str(e)}") from e
            if "API" in error_type:
                raise ValueError(f"Gemini API error: {str(e)}") from e

            raise ValueError(f"Error calling Gemini API: {str(e)}") from e

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> List:
        """
        Format messages for the Gemini API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted messages for the Gemini API
        """
        formatted_contents = []

        for message in messages:
            role = message.role.lower()

            # Map roles to Gemini roles
            if role == "system":
                # For system messages, we need to prepend to the first user message
                # or add as a separate user message if there are no user messages
                continue
            elif role == "user":
                formatted_contents.append({
                    "role": "user",
                    "parts": [{"text": message.content}]
                })
            elif role == "assistant":
                formatted_contents.append({
                    "role": "model",
                    "parts": [{"text": message.content}]
                })
            else:
                # Unknown role, treat as user
                formatted_contents.append({
                    "role": "user",
                    "parts": [{"text": message.content}]
                })

        # Handle system message by prepending to the first user message
        system_messages = [m for m in messages if m.role.lower() == "system"]
        if system_messages and formatted_contents:
            # Find the first user message
            for i, content in enumerate(formatted_contents):
                if content["role"] == "user":
                    # Prepend system message to this user message
                    system_text = "\n\n".join(m.content for m in system_messages)
                    content["parts"][0]["text"] = f"{system_text}\n\n{content['parts'][0]['text']}"
                    break
            else:
                # No user messages found, add as a separate user message
                system_text = "\n\n".join(m.content for m in system_messages)
                formatted_contents.insert(0, {
                    "role": "user",
                    "parts": [{"text": system_text}]
                })
        elif system_messages:
            # No other messages, just add the system message as a user message
            system_text = "\n\n".join(m.content for m in system_messages)
            formatted_contents.append({
                "role": "user",
                "parts": [{"text": system_text}]
            })

        return formatted_contents

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported, False otherwise
        """
        return True


# Register the provider
register_provider("gemini", GeminiProvider)
