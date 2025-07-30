"""
Cerebras API provider implementation.

This module provides integration with Cerebras's API for LLM functionality.
"""

import asyncio
import time
import logging
from typing import List, Optional, Callable, Dict, Any, Union

from cerebras.cloud.sdk import Cerebras, AsyncCerebras
from cerebras.cloud.sdk import APIError, APIConnectionError, RateLimitError as CerebrasRateLimitError
from cerebras.cloud.sdk import AuthenticationError as CerebrasAuthenticationError

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry

# Set up logging
logger = logging.getLogger(__name__)


class CerebrasProvider(LLMProvider):
    """Cerebras API implementation using the official Cerebras SDK."""

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Cerebras provider.

        Args:
            key_manager: KeyManager instance for API key management
        """
        super().__init__(key_manager)
        self._api_key = None
        self._client = None
        self._async_client = None
        self._config = get_config()
        self._registry = get_registry()
        logger.info("Cerebras provider initialized")

    def _get_client(self):
        """
        Get a Cerebras client with the current API key.

        Returns:
            Tuple of (initialized Cerebras client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        api_key = self.key_manager.get_random_key("cerebras")
        if not api_key:
            logger.error("No API key available for Cerebras")
            raise APIKeyError("No API key available for Cerebras")

        logger.debug(f"Using Cerebras API key: {api_key.key[:5]}...{api_key.key[-5:] if len(api_key.key) > 10 else ''}")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            logger.debug("Creating new Cerebras client")
            self._client = Cerebras(api_key=api_key.key)
            self._async_client = AsyncCerebras(api_key=api_key.key)
            self._api_key = api_key.key

        return self._client, self._async_client, api_key

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        logger.debug("Getting available Cerebras models")
        return self._registry.get_models_for_provider("cerebras")

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        default_model = self._registry.get_default_model("cerebras")
        logger.debug(f"Using default Cerebras model: {default_model}")
        return default_model

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the Cerebras API.

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
        _, async_client, api_key = self._get_client()

        try:
            logger.info(f"Generating response with Cerebras, model={model or 'default'}, temperature={temperature}")
            model_name = model or self.get_default_model()

            # Check if the messages format indicates chat or completion API usage
            if self._should_use_chat_api(messages):
                # Format messages for chat API
                formatted_messages = self._format_messages_for_chat_api(messages)
                logger.debug(f"Using chat API with {len(formatted_messages)} messages")

                # Set generation parameters for chat
                params = {
                    "model": model_name,
                    "messages": formatted_messages,
                    "temperature": temperature,
                }

                if max_tokens:
                    params["max_tokens"] = max_tokens

                logger.debug(f"Cerebras chat request parameters: {params}")

                # Generate response using chat API
                response = await async_client.chat.completions.create(**params)
                result = response.choices[0].message.content

            else:
                # Format prompt for completions API
                prompt = self._format_messages_for_api(messages)
                logger.debug(f"Using completions API with prompt of length {len(prompt)}")

                # Set generation parameters for completions
                params = {
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens or 512,
                    "stop": ["Human:", "Assistant:"]
                }

                logger.debug(f"Cerebras completions request parameters: {params}")

                # Generate response using completions API
                response = await async_client.completions.create(**params)
                result = response.choices[0].text.strip()

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")
            logger.info(f"Generated response of length {len(result)}")

            return result

        except CerebrasRateLimitError as e:
            retry_delay = getattr(e, 'retry_after', 60)
            api_key.last_used = time.time()  # Mark as used but not errored
            logger.warning(f"Cerebras rate limit exceeded. Retry after {retry_delay}s.")
            raise RateLimitError(
                f"Cerebras rate limit exceeded. Retry after {retry_delay}s.",
                retry_after=retry_delay
            ) from e

        except CerebrasAuthenticationError as e:
            api_key.mark_error()
            logger.error("Invalid API key for Cerebras")
            raise AuthenticationError("Invalid API key for Cerebras") from e

        except APIError as e:
            api_key.mark_error()
            logger.error(f"Error calling Cerebras API: {str(e)}")
            raise ValueError(f"Error calling Cerebras API: {str(e)}") from e

        except APIConnectionError as e:
            api_key.mark_error()
            logger.error(f"Connection error with Cerebras API: {str(e)}")
            raise ValueError(f"Connection error with Cerebras API: {str(e)}") from e

        except Exception as e:
            api_key.mark_error()
            logger.error(f"Unexpected error with Cerebras API: {str(e)}")
            raise ValueError(f"Unexpected error with Cerebras API: {str(e)}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the Cerebras API.

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
        _, async_client, api_key = self._get_client()

        try:
            logger.info(f"Generating streaming response with Cerebras, model={model or 'default'}, temperature={temperature}")
            model_name = model or self.get_default_model()

            # Check if the messages format indicates chat or completion API usage
            if self._should_use_chat_api(messages):
                # Format messages for chat API
                formatted_messages = self._format_messages_for_chat_api(messages)
                logger.debug(f"Using chat API with {len(formatted_messages)} messages")

                # Set generation parameters for chat
                params = {
                    "model": model_name,
                    "messages": formatted_messages,
                    "temperature": temperature,
                    "stream": True
                }

                if max_tokens:
                    params["max_tokens"] = max_tokens

                logger.debug(f"Cerebras chat streaming request parameters: {params}")

                # Generate streaming response using chat API
                stream = await async_client.chat.completions.create(**params)

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

            else:
                # Format prompt for completions API
                prompt = self._format_messages_for_api(messages)
                logger.debug(f"Using completions API with prompt of length {len(prompt)}")

                # Set generation parameters for completions
                params = {
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens or 512,
                    "stop": ["Human:", "Assistant:"],
                    "stream": True
                }

                logger.debug(f"Cerebras completions streaming request parameters: {params}")

                # Generate streaming response using completions API
                stream = await async_client.completions.create(**params)

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

        except CerebrasRateLimitError as e:
            retry_delay = getattr(e, 'retry_after', 60)
            api_key.last_used = time.time()  # Mark as used but not errored
            logger.warning(f"Cerebras rate limit exceeded. Retry after {retry_delay}s.")
            raise RateLimitError(
                f"Cerebras rate limit exceeded. Retry after {retry_delay}s.",
                retry_after=retry_delay
            ) from e

        except CerebrasAuthenticationError as e:
            api_key.mark_error()
            logger.error("Invalid API key for Cerebras")
            raise AuthenticationError("Invalid API key for Cerebras") from e

        except APIError as e:
            api_key.mark_error()
            logger.error(f"Error calling Cerebras API: {str(e)}")
            raise ValueError(f"Error calling Cerebras API: {str(e)}") from e

        except APIConnectionError as e:
            api_key.mark_error()
            logger.error(f"Connection error with Cerebras API: {str(e)}")
            raise ValueError(f"Connection error with Cerebras API: {str(e)}") from e

        except Exception as e:
            api_key.mark_error()
            logger.error(f"Unexpected error with Cerebras API: {str(e)}")
            raise ValueError(f"Unexpected error with Cerebras API: {str(e)}") from e

    def _should_use_chat_api(self, messages: List[LLMMessage]) -> bool:
        """
        Determine whether to use the chat API or completions API based on message format.

        Args:
            messages: List of messages to analyze

        Returns:
            True if chat API should be used, False for completions API
        """
        # If there are multiple messages with different roles, use chat API
        roles = set(message.role.lower() for message in messages)
        if len(roles) > 1 and "assistant" in roles and "user" in roles:
            return True
        return False

    def _format_messages_for_chat_api(self, messages: List[LLMMessage]) -> List[Dict[str, str]]:
        """
        Format messages for the Cerebras Chat API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted messages for the Cerebras Chat API
        """
        formatted_messages = []

        for message in messages:
            role = message.role.lower()

            # Map roles to Cerebras roles
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

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> str:
        """
        Format messages for the Cerebras Completions API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted prompt string for Cerebras API
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
        # Nothing to close when using Cerebras SDK
        pass

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True as Cerebras SDK supports streaming
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


# Register the provider
register_provider("cerebras", CerebrasProvider)
