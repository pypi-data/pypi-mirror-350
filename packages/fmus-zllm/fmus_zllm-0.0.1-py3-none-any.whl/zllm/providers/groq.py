"""
Groq provider implementation for ZLLM.

This module provides integration with the Groq API.
"""

import json
import base64
import asyncio
import aiohttp
from typing import Dict, List, Any, Optional, Tuple, Callable, Union, BinaryIO
import os
import logging
from datetime import datetime
from io import BytesIO

from groq import Groq, AsyncGroq
from groq.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from groq.types.chat.chat_completion_tool_param import ChatCompletionToolParam

from zllm.base import LLMProvider
from zllm.message import LLMMessage
from zllm.key_manager import KeyManager, report_error, get_key_info
from zllm.exceptions import ProviderError, ConfigurationError
from zllm.model_registry import get_registry


class GroqProvider(LLMProvider):
    """Provider implementation for Groq."""

    # Add compound models for agentic tooling
    COMPOUND_MODELS = ["compound-beta", "compound-beta-mini"]

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Groq provider.

        Args:
            key_manager: Key manager for API keys
        """
        super().__init__(key_manager)
        self._registry = get_registry()
        self._client = None
        self._async_client = None
        self._api_key = None

    def _get_client(self):
        """
        Get a Groq client with the current API key.

        Returns:
            Tuple of (initialized Groq client, API key)

        Raises:
            ValueError: If no API key is available
        """
        try:
            api_key = self.key_manager.get_api_key("groq")
        except Exception as e:
            raise ValueError(f"Failed to get Groq API key: {str(e)}")

        # Create a new client if the API key has changed
        if self._api_key != api_key:
            # Initialize with just the API key
            # The Groq client only accepts api_key as a parameter
            self._client = Groq(api_key=api_key)
            self._async_client = AsyncGroq(api_key=api_key)
            self._api_key = api_key

        return self._client, api_key

    def _get_async_client(self):
        """
        Get an async Groq client with the current API key.

        Returns:
            Tuple of (initialized AsyncGroq client, API key)

        Raises:
            ValueError: If no API key is available
        """
        # Ensure client is initialized
        client, api_key = self._get_client()
        return self._async_client, api_key

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        return self._registry.get_default_model("groq")

    def get_default_vision_model(self) -> str:
        """
        Get the default vision model for this provider.

        Returns:
            Default vision model ID
        """
        registry = get_registry()
        default_model = registry.get_default_model("groq", "vision_models")

        if default_model:
            return default_model

        # Fallback to a known model if registry doesn't have one
        return "meta-llama/llama-4-scout-17b-16e-instruct"

    def get_available_models(self) -> List[str]:
        """
        Get available models for this provider.

        Returns:
            List of available model names
        """
        return self._registry.get_models_for_provider("groq")

    def get_available_vision_models(self) -> List[str]:
        """
        Get a list of available vision models for this provider.

        Returns:
            List of vision model IDs
        """
        registry = get_registry()
        models = registry.get_models("groq", "vision_models")
        return [model.get("id") for model in models]

    def _format_messages(self, messages: List[LLMMessage]) -> List[Dict[str, Any]]:
        """
        Format ZLLM messages for the Groq API.

        Args:
            messages: List of LLMMessage objects

        Returns:
            List of formatted message dictionaries for the Groq API
        """
        formatted_messages = []
        for msg in messages:
            message_dict = {
                "role": msg.role.value,
                "content": msg.content
            }
            if msg.name:
                message_dict["name"] = msg.name
            if msg.function_call:
                # Format function_call as tool_calls for Groq API
                message_dict["tool_calls"] = [{
                    "id": msg.function_call.get("id", "call_" + str(hash(str(msg.function_call)))),
                    "type": "function",
                    "function": {
                        "name": msg.function_call.get("name", ""),
                        "arguments": msg.function_call.get("arguments", "{}")
                    }
                }]
            formatted_messages.append(message_dict)
        return formatted_messages

    def _format_tools(self, functions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Format functions as tools for the Groq API.

        Args:
            functions: List of function definitions

        Returns:
            List of formatted tool dictionaries for the Groq API
        """
        tools = []
        for function in functions:
            tools.append({
                "type": "function",
                "function": function
            })
        return tools

    async def generate_response(
        self,
        messages: List[LLMMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> str:
        """
        Generate a response from the Groq API.

        Args:
            messages: List of messages in the conversation
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            Generated text

        Raises:
            ProviderError: If the API returns an error
        """
        client = None
        api_key = None

        try:
            # Get async client
            client, api_key = self._get_async_client()

            # Use default model if not specified
            if not model:
                model = self.get_default_model()

            # Format messages for the API
            formatted_messages = self._format_messages(messages)

            # Prepare the request parameters
            params = {
                "model": model,
                "messages": formatted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # Add additional parameters
            for key, value in kwargs.items():
                if key not in params:
                    params[key] = value

            # Send the request
            response = await client.chat.completions.create(**params)

            # Extract and return the response text
            return response.choices[0].message.content

        except Exception as e:
            if api_key:
                report_error("groq", api_key)

            # Get information about the key that failed
            key_info = get_key_info("groq", api_key) if api_key else None

            # Include key info in error message if available
            if key_info:
                key_name = key_info.get("name", "unknown")
                error_count = key_info.get("error_count", 0)
                key_info_msg = f" (Key: {key_name}, Error count: {error_count})"
            else:
                key_info_msg = ""

            raise ProviderError(f"Groq API error{key_info_msg}: {str(e)}")

    async def generate_response_streaming(
        self,
        messages: List[LLMMessage],
        callback: Callable[[str], Any],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> None:
        """
        Generate a streaming response from the Groq API.

        Args:
            messages: List of messages in the conversation
            callback: Callback function for each chunk
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Raises:
            ProviderError: If the API returns an error
        """
        client = None
        api_key = None

        try:
            # Get async client
            client, api_key = self._get_async_client()

            # Use default model if not specified
            if not model:
                model = self.get_default_model()

            # Format messages for the API
            formatted_messages = self._format_messages(messages)

            # Prepare the request parameters
            params = {
                "model": model,
                "messages": formatted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }

            # Add additional parameters
            for key, value in kwargs.items():
                if key not in params:
                    params[key] = value

            # Send the streaming request
            stream = await client.chat.completions.create(**params)

            # Process the streaming response
            async for chunk in stream:
                if chunk.choices and len(chunk.choices) > 0:
                    choice = chunk.choices[0]

                    # Get content from the appropriate attribute based on the chunk structure
                    content = None

                    # Try different possible locations for the content
                    if hasattr(choice, 'delta'):
                        delta = choice.delta
                        if hasattr(delta, 'content') and delta.content is not None:
                            content = delta.content
                    elif hasattr(choice, 'message'):
                        message = choice.message
                        if hasattr(message, 'content') and message.content is not None:
                            content = message.content

                    # Call the callback if content was found
                    if content:
                        if asyncio.iscoroutinefunction(callback):
                            await callback(content)
                        else:
                            callback(content)

        except Exception as e:
            if api_key:
                report_error("groq", api_key)

            # Get information about the key that failed
            key_info = get_key_info("groq", api_key) if api_key else None

            # Include key info in error message if available
            if key_info:
                key_name = key_info.get("name", "unknown")
                error_count = key_info.get("error_count", 0)
                key_info_msg = f" (Key: {key_name}, Error count: {error_count})"
            else:
                key_info_msg = ""

            raise ProviderError(f"Groq API error{key_info_msg}: {str(e)}")

    async def call_function(
        self,
        messages: List[LLMMessage],
        functions: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call a function using the Groq API.

        Args:
            messages: List of messages in the conversation
            functions: List of function definitions
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            **kwargs: Additional parameters for the API

        Returns:
            Dictionary with function call information

        Raises:
            ProviderError: If the API returns an error
        """
        client = None
        api_key = None

        try:
            # Get async client
            client, api_key = self._get_async_client()

            # Use default model if not specified
            if not model:
                model = self.get_default_model()

            # Format messages for the API
            formatted_messages = self._format_messages(messages)

            # Format functions as tools
            tools = self._format_tools(functions)

            # Prepare the request parameters
            params = {
                "model": model,
                "messages": formatted_messages,
                "temperature": temperature,
                "tools": tools,
                "tool_choice": kwargs.pop("tool_choice", "auto")
            }

            # Add additional parameters
            for key, value in kwargs.items():
                if key not in params:
                    params[key] = value

            # Send the request
            response = await client.chat.completions.create(**params)

            # Extract and return the function call information
            message = response.choices[0].message
            if message.tool_calls and len(message.tool_calls) > 0:
                tool_call = message.tool_calls[0]
                return {
                    "name": tool_call.function.name,
                    "arguments": json.loads(tool_call.function.arguments),
                    "id": tool_call.id
                }
            else:
                # No function call was made, return the message content
                return {
                    "name": None,
                    "arguments": None,
                    "content": message.content
                }

        except Exception as e:
            if api_key:
                report_error("groq", api_key)

            # Get information about the key that failed
            key_info = get_key_info("groq", api_key) if api_key else None

            # Include key info in error message if available
            if key_info:
                key_name = key_info.get("name", "unknown")
                error_count = key_info.get("error_count", 0)
                key_info_msg = f" (Key: {key_name}, Error count: {error_count})"
            else:
                key_info_msg = ""

            raise ProviderError(f"Groq API error{key_info_msg}: {str(e)}")

    async def generate_structured_output(
        self,
        messages: List[LLMMessage],
        response_format: Dict[str, Any],
        model: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a structured output from the Groq API.

        Args:
            messages: List of messages in the conversation
            response_format: Format specification for the response
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            **kwargs: Additional parameters for the API

        Returns:
            Structured response data

        Raises:
            ProviderError: If the API returns an error
        """
        client = None
        api_key = None

        try:
            # Get async client
            client, api_key = self._get_async_client()

            # Use default model if not specified
            if not model:
                model = self.get_default_model()

            # Format messages for the API
            formatted_messages = self._format_messages(messages)

            # Prepare the request parameters
            params = {
                "model": model,
                "messages": formatted_messages,
                "temperature": temperature,
                "response_format": response_format
            }

            # Add additional parameters
            for key, value in kwargs.items():
                if key not in params:
                    params[key] = value

            # Send the request
            response = await client.chat.completions.create(**params)

            # Parse and return the JSON response
            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            if api_key:
                report_error("groq", api_key)

            # Get information about the key that failed
            key_info = get_key_info("groq", api_key) if api_key else None

            # Include key info in error message if available
            if key_info:
                key_name = key_info.get("name", "unknown")
                error_count = key_info.get("error_count", 0)
                key_info_msg = f" (Key: {key_name}, Error count: {error_count})"
            else:
                key_info_msg = ""

            raise ProviderError(f"Groq API error{key_info_msg}: {str(e)}")

    async def generate_response_with_image(
        self,
        messages: List[LLMMessage],
        image_data: Union[str, bytes, BinaryIO],
        image_format: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> str:
        """
        Generate a response using an image input.

        Args:
            messages: List of messages in the conversation
            image_data: Image data as URL, base64, bytes, or file-like object
            image_format: Format of the image (png, jpeg, etc.)
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API including:
                - response_format: Dict specifying response format, e.g. {"type": "json_object"}
                - tools: List of tools available to the model
                - tool_choice: String or object specifying tool choice behavior

        Returns:
            Generated text

        Raises:
            ProviderError: If the API returns an error
        """
        client = None
        api_key = None

        try:
            # Get async client
            client, api_key = self._get_async_client()

            # Use default vision model if not specified
            if not model:
                model = self.get_default_vision_model()

            # Process image data
            if isinstance(image_data, str):
                if image_data.startswith(('http://', 'https://')):
                    # It's a URL
                    image_url = image_data
                else:
                    # Assume it's a base64 encoded string
                    if not image_data.startswith('data:'):
                        # Add data URI prefix if not present
                        mime_type = f"image/{image_format or 'jpeg'}"
                        image_url = f"data:{mime_type};base64,{image_data}"
                    else:
                        image_url = image_data
            else:
                # It's bytes or a file-like object
                if isinstance(image_data, bytes):
                    image_bytes = image_data
                else:
                    # Read from file-like object
                    image_bytes = image_data.read()

                # Encode to base64
                base64_image = base64.b64encode(image_bytes).decode('utf-8')
                mime_type = f"image/{image_format or 'jpeg'}"
                image_url = f"data:{mime_type};base64,{base64_image}"

            # Format messages for the API, adding the image to the last user message
            formatted_messages = []

            # Handle existing messages in the conversation
            for i, msg in enumerate(messages):
                if i == len(messages) - 1 and msg.role.value == "user":
                    # Add image to the last user message
                    content_items = []

                    # Add text content if available
                    if msg.content:
                        content_items.append({
                            "type": "text",
                            "text": msg.content
                        })

                    # Add image
                    content_items.append({
                        "type": "image_url",
                        "image_url": {
                            "url": image_url
                        }
                    })

                    formatted_messages.append({
                        "role": msg.role.value,
                        "content": content_items
                    })
                else:
                    # Format other messages normally
                    if msg.role.value == "user" or msg.role.value == "assistant" or msg.role.value == "system":
                        message_dict = {
                            "role": msg.role.value,
                            "content": msg.content
                        }
                        if msg.name:
                            message_dict["name"] = msg.name
                        if msg.function_call:
                            # Format function_call as tool_calls for Groq API
                            message_dict["tool_calls"] = [{
                                "id": msg.function_call.get("id", "call_" + str(hash(str(msg.function_call)))),
                                "type": "function",
                                "function": {
                                    "name": msg.function_call.get("name", ""),
                                    "arguments": msg.function_call.get("arguments", "{}")
                                }
                            }]
                        formatted_messages.append(message_dict)

            # Prepare the request parameters
            params = {
                "model": model,
                "messages": formatted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # Add response_format if specified (for JSON output)
            if "response_format" in kwargs:
                params["response_format"] = kwargs.pop("response_format")

            # Add tools if specified
            if "tools" in kwargs:
                params["tools"] = kwargs.pop("tools")

                # Add tool_choice if specified
                if "tool_choice" in kwargs:
                    params["tool_choice"] = kwargs.pop("tool_choice")

            # Add additional parameters
            for key, value in kwargs.items():
                if key not in params:
                    params[key] = value

            # Send the request
            response = await client.chat.completions.create(**params)

            # Extract and return the response text
            return response.choices[0].message.content

        except Exception as e:
            if api_key:
                report_error("groq", api_key)

            # Get information about the key that failed
            key_info = get_key_info("groq", api_key) if api_key else None

            # Include key info in error message if available
            if key_info:
                key_name = key_info.get("name", "unknown")
                error_count = key_info.get("error_count", 0)
                key_info_msg = f" (Key: {key_name}, Error count: {error_count})"
            else:
                key_info_msg = ""

            raise ProviderError(f"Groq API error{key_info_msg}: {str(e)}")

    async def generate_response_with_reasoning(
        self,
        messages: List[LLMMessage],
        reasoning_format: str = "raw",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> Union[str, Dict[str, Any]]:
        """
        Generate a response with explicit reasoning.

        Args:
            messages: List of messages in the conversation
            reasoning_format: Format for the reasoning ("raw", "parsed", or "hidden")
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            Generated text or structured response with reasoning

        Raises:
            ProviderError: If the API returns an error
        """
        client = None
        api_key = None

        try:
            # Get async client
            client, api_key = self._get_async_client()

            # Use default model if not specified
            if not model:
                model = self.get_default_model()

            # Format messages for the API
            formatted_messages = self._format_messages(messages)

            # Prepare the request parameters
            params = {
                "model": model,
                "messages": formatted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "reasoning_format": reasoning_format
            }

            # Add additional parameters
            for key, value in kwargs.items():
                if key not in params:
                    params[key] = value

            # Send the request
            response = await client.chat.completions.create(**params)

            # Handle the response based on reasoning format
            if reasoning_format == "parsed":
                # For parsed format, the response contains a message with content and reasoning fields
                message = response.choices[0].message
                return {
                    "content": message.content,
                    "reasoning": message.reasoning
                }
            else:
                # For raw and hidden formats, just return the content
                return response.choices[0].message.content

        except Exception as e:
            if api_key:
                report_error("groq", api_key)

            # Get information about the key that failed
            key_info = get_key_info("groq", api_key) if api_key else None

            # Include key info in error message if available
            if key_info:
                key_name = key_info.get("name", "unknown")
                error_count = key_info.get("error_count", 0)
                key_info_msg = f" (Key: {key_name}, Error count: {error_count})"
            else:
                key_info_msg = ""

            raise ProviderError(f"Groq API error{key_info_msg}: {str(e)}")

    async def generate_response_with_tools(
        self,
        messages: List[LLMMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        search_settings: Optional[Dict[str, List[str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a response using Groq's agentic tooling (compound models).

        Args:
            messages: List of messages in the conversation
            model: Compound model to use (defaults to compound-beta)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            search_settings: Optional settings for web search tool
                - include_domains: List of domains to include
                - exclude_domains: List of domains to exclude
            **kwargs: Additional parameters for the API

        Returns:
            Dictionary with response content and executed tools information

        Raises:
            ProviderError: If the API returns an error
            ValueError: If an invalid model is specified
        """
        client = None
        api_key = None

        # Default to compound-beta if no model specified
        if not model:
            model = "compound-beta"

        # Validate model is a compound model
        if model not in self.COMPOUND_MODELS:
            raise ValueError(f"Model must be one of {self.COMPOUND_MODELS} for agentic tooling")

        try:
            # Get async client
            client, api_key = self._get_async_client()

            # Format messages for the API
            formatted_messages = self._format_messages(messages)

            # Prepare the request parameters
            params = {
                "model": model,
                "messages": formatted_messages,
                "temperature": temperature,
                "max_tokens": max_tokens
            }

            # Add search settings if provided
            if search_settings:
                params["search_settings"] = search_settings

            # Add additional parameters
            for key, value in kwargs.items():
                if key not in params:
                    params[key] = value

            # Send the request
            response = await client.chat.completions.create(**params)

            # Extract response content and executed tools
            message = response.choices[0].message
            result = {
                "content": message.content
            }

            # Add executed tools if available
            if hasattr(message, "executed_tools"):
                result["executed_tools"] = message.executed_tools

            return result

        except Exception as e:
            if api_key:
                report_error("groq", api_key)

            # Get information about the key that failed
            key_info = get_key_info("groq", api_key) if api_key else None

            # Include key info in error message if available
            if key_info:
                key_name = key_info.get("name", "unknown")
                error_count = key_info.get("error_count", 0)
                key_info_msg = f" (Key: {key_name}, Error count: {error_count})"
            else:
                key_info_msg = ""

            raise ProviderError(f"Groq API error{key_info_msg}: {str(e)}")

    async def debug_code(
        self,
        code_snippet: str,
        error_message: Optional[str] = None,
        model: str = "compound-beta-mini",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Debug a code snippet using Groq's agentic tooling.

        Args:
            code_snippet: The code snippet to debug
            error_message: Optional error message to include
            model: Compound model to use (defaults to compound-beta-mini)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            Dictionary with debugging response and executed tools information

        Raises:
            ProviderError: If the API returns an error
        """
        # Construct the prompt based on whether an error message is provided
        if error_message:
            prompt = f"Debug this code and explain what's wrong:\n```\n{code_snippet}\n```\n\nError message:\n```\n{error_message}\n```"
        else:
            prompt = f"Debug this code and explain what's wrong:\n```\n{code_snippet}\n```"

        # Create a user message with the prompt
        messages = [LLMMessage.user(prompt)]

        # Use the generate_response_with_tools method
        return await self.generate_response_with_tools(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    async def search_information(
        self,
        query: str,
        model: str = "compound-beta",
        temperature: float = 0.7,
        max_tokens: int = 1024,
        search_settings: Optional[Dict[str, List[str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search for information using Groq's agentic tooling.

        Args:
            query: The search query
            model: Compound model to use (defaults to compound-beta)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            search_settings: Optional settings for web search tool
                - include_domains: List of domains to include
                - exclude_domains: List of domains to exclude
            **kwargs: Additional parameters for the API

        Returns:
            Dictionary with search response and executed tools information

        Raises:
            ProviderError: If the API returns an error
        """
        # Create a user message with the query
        messages = [LLMMessage.user(query)]

        # Use the generate_response_with_tools method
        return await self.generate_response_with_tools(
            messages=messages,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            search_settings=search_settings,
            **kwargs
        )

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported
        """
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
        return True

    @property
    def supports_agentic_tools(self) -> bool:
        """
        Check if this provider supports agentic tools.

        Returns:
            True if agentic tools are supported
        """
        return True
