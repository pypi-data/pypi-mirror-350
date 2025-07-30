"""
Client module for ZLLM.

This module provides the main client interface for interacting with LLMs.
"""

import asyncio
import json
import logging
import os
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any, Union, BinaryIO, Callable, TypeVar, Generic, Awaitable

from zllm.message import LLMMessage, MessageRole
from zllm.providers import get_provider, get_available_providers
from zllm.exceptions import ConfigurationError, ProviderError
from zllm.utils import get_provider_config


class LLMClient:
    """
    Main client for interacting with LLMs.

    This class provides a unified interface for generating responses from
    different LLM providers.
    """

    def __init__(
        self,
        provider: str = "groq",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ):
        """
        Initialize a new LLMClient.

        Args:
            provider: Name of the provider to use
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the provider
        """
        self.provider_name = provider
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.kwargs = kwargs
        self.system_message = None
        self.messages = []

        # Initialize the provider
        self._provider = get_provider(self.provider_name)

    def set_system_message(self, content: str) -> None:
        """
        Set the system message for the conversation.

        Args:
            content: Content of the system message
        """
        self.system_message = LLMMessage.system(content)

    def add_message(self, role: str, content: str) -> None:
        """
        Add a message to the conversation history.

        Args:
            role: Role of the message (user, assistant, system)
            content: Content of the message
        """
        if role == "system":
            self.system_message = LLMMessage.system(content)
        elif role == "user":
            self.messages.append(LLMMessage.user(content))
        elif role == "assistant":
            self.messages.append(LLMMessage.assistant(content))
        else:
            raise ValueError(f"Invalid message role: {role}")

    def get_messages(self) -> List[LLMMessage]:
        """
        Get all messages in the conversation, including the system message.

        Returns:
            List of messages
        """
        result = []
        if self.system_message:
            result.append(self.system_message)
        result.extend(self.messages)
        return result

    def get_last_user_message(self) -> Optional[str]:
        """
        Get the content of the last user message in the conversation.

        Returns:
            Content of the last user message, or None if there are no user messages
        """
        for message in reversed(self.messages):
            if message.role == MessageRole.USER:
                return message.content
        return None

    def get_last_assistant_message(self) -> Optional[str]:
        """
        Get the content of the last assistant message in the conversation.

        Returns:
            Content of the last assistant message, or None if there are no assistant messages
        """
        for message in reversed(self.messages):
            if message.role == MessageRole.ASSISTANT:
                return message.content
        return None

    def clear_conversation_history(self, keep_system_message: bool = True) -> None:
        """
        Clear the conversation history.

        Args:
            keep_system_message: Whether to keep the system message
        """
        self.messages = []
        if not keep_system_message:
            self.system_message = None

    def save_conversation(self, file_path: str) -> None:
        """
        Save the conversation history to a file.

        Args:
            file_path: Path to save the conversation to
        """
        conversation = {
            "provider": self.provider_name,
            "model": self.model,
            "system_message": self.system_message.to_dict() if self.system_message else None,
            "messages": [msg.to_dict() for msg in self.messages]
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(conversation, f, indent=2)

    def load_conversation(self, file_path: str) -> None:
        """
        Load a conversation history from a file.

        Args:
            file_path: Path to load the conversation from
        """
        with open(file_path, "r", encoding="utf-8") as f:
            conversation = json.load(f)

        if "system_message" in conversation and conversation["system_message"]:
            self.system_message = LLMMessage.from_dict(conversation["system_message"])
        else:
            self.system_message = None

        self.messages = [LLMMessage.from_dict(msg) for msg in conversation["messages"]]

        # Optionally update provider and model if they exist in the saved conversation
        if "provider" in conversation:
            self.provider_name = conversation["provider"]
            self._provider = get_provider(self.provider_name)

        if "model" in conversation:
            self.model = conversation["model"]

    def count_tokens(self, text: Optional[str] = None) -> int:
        """
        Count the number of tokens in the text or current conversation.

        Args:
            text: Text to count tokens for, or None to count tokens in the current conversation

        Returns:
            Number of tokens

        Raises:
            NotImplementedError: If token counting is not supported by the provider
        """
        if not hasattr(self._provider, "count_tokens"):
            raise NotImplementedError(f"Provider '{self.provider_name}' does not support token counting")

        if text is not None:
            return self._provider.count_tokens(text)
        else:
            # Count tokens in the current conversation
            messages = self.get_messages()
            return self._provider.count_tokens_for_messages(messages)

    def summarize_conversation(
        self,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> str:
        """
        Generate a summary of the current conversation.

        Args:
            max_tokens: Maximum tokens for the summary
            temperature: Temperature for generation
            **kwargs: Additional parameters for the provider

        Returns:
            Summary of the conversation
        """
        # Create a system message asking for a summary
        summary_system_message = LLMMessage.system(
            "Please provide a concise summary of the following conversation."
        )

        # Use the existing conversation messages
        messages = self.get_messages()

        # Add the summary request
        messages.append(LLMMessage.user("Summarize our conversation so far."))

        # Generate the summary
        return asyncio.run(self._provider.generate_response(
            messages=[summary_system_message] + messages,
            model=self.model,
            temperature=temperature if temperature is not None else self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            **{**self.kwargs, **kwargs}
        ))

    async def retry_last_response(
        self,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Retry generating the last response with potentially different parameters.

        Args:
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the provider

        Returns:
            New response
        """
        # Remove the last assistant message if it exists
        if self.messages and self.messages[-1].role == MessageRole.ASSISTANT:
            self.messages.pop()

        # Generate a new response
        return await self.generate_response(
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    def _prepare_messages(self, new_messages: List[LLMMessage]) -> List[LLMMessage]:
        """
        Prepare messages for sending to the provider.

        This helper method combines the system message (if any) with the provided messages.

        Args:
            new_messages: New messages to prepare

        Returns:
            Combined list of messages
        """
        result = []
        if self.system_message:
            result.append(self.system_message)
        result.extend(self.messages)
        result.extend(new_messages)
        return result

    async def ask(
        self,
        user_content: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Add a user message and generate a response in one step.

        Args:
            user_content: Content of the user message
            model: Model to use (overrides the client's model if provided)
            temperature: Temperature for generation (overrides the client's temperature if provided)
            max_tokens: Maximum tokens to generate (overrides the client's max_tokens if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            Generated text response

        Raises:
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
        """
        # Add the user message
        self.add_message("user", user_content)

        # Generate and return the response (automatically uses client's messages)
        return await self.generate_response(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    async def ask_streaming(
        self,
        user_content: str,
        callback: Optional[callable] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Add a user message and generate a streaming response in one step.

        Args:
            user_content: Content of the user message
            callback: Callback function for each chunk
            model: Model to use (overrides the client's model if provided)
            temperature: Temperature for generation (overrides the client's temperature if provided)
            max_tokens: Maximum tokens to generate (overrides the client's max_tokens if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            Complete generated text

        Raises:
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
            NotImplementedError: If streaming is not supported by the provider
        """
        # Add the user message
        self.add_message("user", user_content)

        # Generate and return the streaming response
        return await self.generate_response_streaming(
            callback=callback,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    async def generate_response(
        self,
        messages: Optional[List[LLMMessage]] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of messages (overrides the client's messages if provided)
            model: Model to use (overrides the client's model if provided)
            temperature: Temperature for generation (overrides the client's temperature if provided)
            max_tokens: Maximum tokens to generate (overrides the client's max_tokens if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            Generated text

        Raises:
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
        """
        # Use provided messages or the client's messages
        if messages is None:
            messages = self.get_messages()
        elif isinstance(messages, LLMMessage):
            # Handle single message case
            if self.system_message:
                messages = [self.system_message, messages]
            else:
                messages = [messages]

        # Use provided parameters or the client's parameters
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or self.max_tokens

        # Merge kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        try:
            # Generate response
            response = await self._provider.generate_response(
                messages=messages,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **merged_kwargs
            )

            # Add the response to the conversation history
            if messages == self.get_messages():
                self.messages.append(LLMMessage.assistant(response))

            return response
        except Exception as e:
            if isinstance(e, (ProviderError, ConfigurationError)):
                raise
            raise ProviderError(f"Provider '{self.provider_name}' failed: {str(e)}") from e

    async def generate_response_streaming(
        self,
        messages: Optional[List[LLMMessage]] = None,
        callback: Optional[callable] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a streaming response from the LLM.

        Args:
            messages: List of messages (overrides the client's messages if provided)
            callback: Callback function for each chunk
            model: Model to use (overrides the client's model if provided)
            temperature: Temperature for generation (overrides the client's temperature if provided)
            max_tokens: Maximum tokens to generate (overrides the client's max_tokens if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            Complete generated text

        Raises:
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
            NotImplementedError: If streaming is not supported by the provider
        """
        # Use provided messages or the client's messages
        if messages is None:
            messages = self.get_messages()
        elif isinstance(messages, LLMMessage):
            # Handle single message case
            if self.system_message:
                messages = [self.system_message, messages]
            else:
                messages = [messages]

        # Use provided parameters or the client's parameters
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or self.max_tokens

        # Merge kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        # Check if streaming is supported
        if not getattr(self._provider, "supports_streaming", False):
            raise NotImplementedError(f"Provider '{self.provider_name}' does not support streaming")

        # Collect the full response
        full_response = []

        # Define the callback function
        async def collect_chunks(chunk: str) -> None:
            full_response.append(chunk)
            if callback:
                # Check if the callback is a coroutine function and await it if it is
                if asyncio.iscoroutinefunction(callback):
                    await callback(chunk)
                else:
                    callback(chunk)

        try:
            # Generate streaming response
            await self._provider.generate_response_streaming(
                messages=messages,
                callback=collect_chunks,
                model=model,
                temperature=temperature,
                max_tokens=max_tokens,
                **merged_kwargs
            )

            # Combine chunks into the full response
            response = "".join(full_response)

            # Add the response to the conversation history
            if messages == self.get_messages():
                self.messages.append(LLMMessage.assistant(response))

            return response
        except Exception as e:
            if isinstance(e, (ProviderError, ConfigurationError, NotImplementedError)):
                raise
            raise ProviderError(f"Provider '{self.provider_name}' failed: {str(e)}") from e

    async def generate_response_with_reasoning(
        self,
        prompt: str,
        reasoning_format: str = "raw",
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> Union[str, Dict[str, str]]:
        """
        Generate a response with explicit reasoning.

        Args:
            prompt: Prompt to send to the model
            reasoning_format: Format of the reasoning ('raw', 'parsed', or 'hidden')
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the provider

        Returns:
            Generated text or dict with content and reasoning
        """
        # Create a message from the prompt
        message = LLMMessage(role=MessageRole.USER, content=prompt)

        # Add the message to the conversation
        messages = self._prepare_messages([message])

        # Generate the response with reasoning
        return await self.provider.generate_response_with_reasoning(
            messages=messages,
            reasoning_format=reasoning_format,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    async def generate_response_with_image(
        self,
        image_data: Union[str, bytes, BinaryIO],
        prompt: str = "",
        image_format: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> str:
        """
        Generate a response using an image input.

        Args:
            image_data: Image data as URL, base64, bytes, or file-like object
            prompt: Prompt to send to the model along with the image
            image_format: Format of the image (png, jpeg, etc.)
            model: Model to use (defaults to provider default vision model)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the provider

        Returns:
            Generated text

        Raises:
            ProviderError: If the provider doesn't support vision or if there's an API error
        """
        # Check if the provider supports vision
        if not hasattr(self._provider, "generate_response_with_image"):
            raise ProviderError(f"Provider {self.provider_name} does not support vision capabilities")

        # Create a message from the prompt
        message = LLMMessage(role=MessageRole.USER, content=prompt)

        # Add the message to the conversation
        messages = self._prepare_messages([message])

        # Generate the response with the image
        return await self._provider.generate_response_with_image(
            messages=messages,
            image_data=image_data,
            image_format=image_format,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **kwargs
        )

    async def generate_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        size: Optional[str] = None,
        format: str = "url",
        **kwargs
    ) -> Union[str, bytes]:
        """
        Generate an image from a text prompt.

        Args:
            prompt: Text prompt describing the image
            model: Model to use (overrides the client's model if provided)
            size: Size of the image (e.g., "1024x1024")
            format: Output format ("url" or "bytes")
            **kwargs: Additional parameters for the provider

        Returns:
            URL or bytes of the generated image

        Raises:
            NotImplementedError: If image generation is not supported by the provider
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
        """
        # Check if image generation is supported
        if not getattr(self._provider, "supports_image_generation", False):
            raise NotImplementedError(f"Provider '{self.provider_name}' does not support image generation")

        # Use provided model or the client's model
        model = model or self.model

        # Merge kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        try:
            # Generate image
            return await self._provider.generate_image(
                prompt=prompt,
                model=model,
                size=size,
                format=format,
                **merged_kwargs
            )
        except Exception as e:
            if isinstance(e, (ProviderError, ConfigurationError, NotImplementedError)):
                raise
            raise ProviderError(f"Provider '{self.provider_name}' failed: {str(e)}") from e

    async def call_function(
        self,
        functions: List[Dict[str, Any]],
        messages: Optional[List[LLMMessage]] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call a function using the LLM.

        Args:
            functions: List of function definitions
            messages: List of messages (overrides the client's messages if provided)
            model: Model to use (overrides the client's model if provided)
            temperature: Temperature for generation (overrides the client's temperature if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            Dictionary with function call information

        Raises:
            NotImplementedError: If function calling is not supported by the provider
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
        """
        # Check if function calling is supported
        if not getattr(self._provider, "supports_function_calling", False):
            raise NotImplementedError(f"Provider '{self.provider_name}' does not support function calling")

        # Use provided messages or the client's messages
        if messages is None:
            messages = self.get_messages()
        elif isinstance(messages, LLMMessage):
            # Handle single message case
            if self.system_message:
                messages = [self.system_message, messages]
            else:
                messages = [messages]

        # Use provided parameters or the client's parameters
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature

        # Merge kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        try:
            # Call function
            return await self._provider.call_function(
                messages=messages,
                functions=functions,
                model=model,
                temperature=temperature,
                **merged_kwargs
            )
        except Exception as e:
            if isinstance(e, (ProviderError, ConfigurationError, NotImplementedError)):
                raise
            raise ProviderError(f"Provider '{self.provider_name}' failed: {str(e)}") from e

    async def generate_structured_output(
        self,
        response_format: Dict[str, Any],
        messages: Optional[List[LLMMessage]] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a structured output from the LLM.

        Args:
            response_format: Format specification for the response
            messages: List of messages (overrides the client's messages if provided)
            model: Model to use (overrides the client's model if provided)
            temperature: Temperature for generation (overrides the client's temperature if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            Structured response data

        Raises:
            NotImplementedError: If structured output is not supported by the provider
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
        """
        # Check if structured output is supported
        if not getattr(self._provider, "supports_structured_output", False):
            raise NotImplementedError(f"Provider '{self.provider_name}' does not support structured output")

        # Use provided messages or the client's messages
        if messages is None:
            messages = self.get_messages()
        elif isinstance(messages, LLMMessage):
            # Handle single message case
            if self.system_message:
                messages = [self.system_message, messages]
            else:
                messages = [messages]

        # Use provided parameters or the client's parameters
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature

        # Merge kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        try:
            # Generate structured output
            return await self._provider.generate_structured_output(
                messages=messages,
                response_format=response_format,
                model=model,
                temperature=temperature,
                **merged_kwargs
            )
        except Exception as e:
            if isinstance(e, (ProviderError, ConfigurationError, NotImplementedError)):
                raise
            raise ProviderError(f"Provider '{self.provider_name}' failed: {str(e)}") from e

    async def generate_embeddings(
        self,
        texts: List[str],
        model: Optional[str] = None,
        **kwargs
    ) -> List[List[float]]:
        """
        Generate embeddings for a list of texts.

        Args:
            texts: List of texts to generate embeddings for
            model: Model to use (overrides the client's model if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            List of embedding vectors

        Raises:
            NotImplementedError: If embeddings are not supported by the provider
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
        """
        # Check if embeddings are supported
        if not getattr(self._provider, "supports_embeddings", False):
            raise NotImplementedError(f"Provider '{self.provider_name}' does not support embeddings")

        # Use provided model or the client's model
        model = model or self.model

        # Merge kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        try:
            # Generate embeddings
            return await self._provider.generate_embeddings(
                texts=texts,
                model=model,
                **merged_kwargs
            )
        except Exception as e:
            if isinstance(e, (ProviderError, ConfigurationError, NotImplementedError)):
                raise
            raise ProviderError(f"Provider '{self.provider_name}' failed: {str(e)}") from e

    async def generate_response_with_functions(
        self,
        prompt: str,
        function_schemas: List[Dict[str, Any]],
        available_functions: Dict[str, Callable],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> str:
        """
        Generate a response using function calling capabilities.

        Args:
            prompt: The user prompt to process
            function_schemas: List of function definitions
            available_functions: Dictionary mapping function names to their implementations
            model: Model to use (overrides the client's model if provided)
            temperature: Temperature for generation (overrides the client's temperature if provided)
            max_tokens: Maximum tokens to generate (overrides the client's max_tokens if provided)
            **kwargs: Additional parameters for the provider

        Returns:
            Generated text response after function calling

        Raises:
            NotImplementedError: If function calling is not supported by the provider
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
        """
        # Check if function calling is supported
        if not getattr(self._provider, "supports_function_calling", False):
            raise NotImplementedError(f"Provider '{self.provider_name}' does not support function calling")

        # Create a user message from the prompt
        user_message = LLMMessage.user(prompt)

        # Prepare messages
        messages = []
        if self.system_message:
            messages.append(self.system_message)
        messages.append(user_message)

        # Use provided parameters or the client's parameters
        model = model or self.model
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens or self.max_tokens

        # Merge kwargs
        merged_kwargs = {**self.kwargs, **kwargs}

        try:
            # First, call the function to get function call info
            function_call_result = await self._provider.call_function(
                messages=messages,
                functions=function_schemas,
                model=model,
                temperature=temperature,
                **merged_kwargs
            )

            # Check if a function was called
            if "function_call" in function_call_result:
                function_name = function_call_result["function_call"]["name"]

                # Parse arguments (handle different formats from different providers)
                if isinstance(function_call_result["function_call"]["arguments"], str):
                    import json
                    function_args = json.loads(function_call_result["function_call"]["arguments"])
                else:
                    function_args = function_call_result["function_call"]["arguments"]

                # Execute the function if it exists
                if function_name in available_functions:
                    function_result = available_functions[function_name](**function_args)

                    # Create a function message with the result
                    function_message = LLMMessage(
                        role="function",
                        content=json.dumps(function_result) if not isinstance(function_result, str) else function_result,
                        name=function_name
                    )

                    # Generate a response using the function result
                    response = await self.generate_response(
                        messages=[
                            *messages,
                            LLMMessage.assistant(content=None, function_call=function_call_result["function_call"]),
                            function_message
                        ],
                        model=model,
                        temperature=temperature,
                        max_tokens=max_tokens,
                        **merged_kwargs
                    )

                    return response
                else:
                    raise ProviderError(f"Function '{function_name}' was called but not found in available_functions")
            else:
                # No function was called, return the original response
                return function_call_result.get("content", "")

        except Exception as e:
            if isinstance(e, (ProviderError, ConfigurationError, NotImplementedError)):
                raise
            raise ProviderError(f"Provider '{self.provider_name}' failed: {str(e)}") from e

    async def close(self) -> None:
        """
        Close the client and any resources it holds.
        """
        pass

    # Add new methods for Groq's agentic tooling

    async def debug_code(
        self,
        code_snippet: str,
        error_message: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Debug a code snippet using agentic tooling.

        This method uses specialized models like Groq's compound-beta-mini
        that can execute code and search for solutions automatically.

        Args:
            code_snippet: The code snippet to debug
            error_message: Optional error message to include
            model: Model to use (defaults to provider's default compound model)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the provider

        Returns:
            Dictionary with debugging response and executed tools information

        Raises:
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
            NotImplementedError: If agentic tools are not supported by the provider
        """
        if not hasattr(self._provider, "supports_agentic_tools") or not self._provider.supports_agentic_tools:
            raise NotImplementedError("The current provider does not support agentic tools")

        # Use provider's debug_code method
        return await self._provider.debug_code(
            code_snippet=code_snippet,
            error_message=error_message,
            model=model or self.model,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            **{**self.kwargs, **kwargs}
        )

    async def search_information(
        self,
        query: str,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        search_settings: Optional[Dict[str, List[str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Search for information using agentic tooling.

        This method uses specialized models like Groq's compound-beta
        that can search the web and process information automatically.

        Args:
            query: The search query
            model: Model to use (defaults to provider's default compound model)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            search_settings: Optional settings for web search tool
                - include_domains: List of domains to include
                - exclude_domains: List of domains to exclude
            **kwargs: Additional parameters for the provider

        Returns:
            Dictionary with search response and executed tools information

        Raises:
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
            NotImplementedError: If agentic tools are not supported by the provider
        """
        if not hasattr(self._provider, "supports_agentic_tools") or not self._provider.supports_agentic_tools:
            raise NotImplementedError("The current provider does not support agentic tools")

        # Use provider's search_information method
        return await self._provider.search_information(
            query=query,
            model=model or self.model,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            search_settings=search_settings,
            **{**self.kwargs, **kwargs}
        )

    async def generate_with_tools(
        self,
        messages: Optional[List[LLMMessage]] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        search_settings: Optional[Dict[str, List[str]]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a response using agentic tooling.

        This method uses specialized models like Groq's compound-beta
        that can use tools like web search and code execution automatically.

        Args:
            messages: List of messages (overrides the client's messages if provided)
            model: Model to use (defaults to provider's default compound model)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            search_settings: Optional settings for web search tool
                - include_domains: List of domains to include
                - exclude_domains: List of domains to exclude
            **kwargs: Additional parameters for the provider

        Returns:
            Dictionary with response content and executed tools information

        Raises:
            ProviderError: If the provider encounters an error
            ConfigurationError: If the provider is not properly configured
            NotImplementedError: If agentic tools are not supported by the provider
        """
        if not hasattr(self._provider, "supports_agentic_tools") or not self._provider.supports_agentic_tools:
            raise NotImplementedError("The current provider does not support agentic tools")

        # Use provided messages or the client's messages
        if messages is None:
            messages = self.get_messages()

        # Use provider's generate_response_with_tools method
        return await self._provider.generate_response_with_tools(
            messages=messages,
            model=model or self.model,
            temperature=temperature or self.temperature,
            max_tokens=max_tokens or self.max_tokens,
            search_settings=search_settings,
            **{**self.kwargs, **kwargs}
        )
