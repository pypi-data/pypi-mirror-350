"""
Base classes for ZLLM.

This module defines the base classes used throughout the package.
"""

from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, Callable, Union, BinaryIO

from zllm.key_manager import KeyManager
from zllm.message import LLMMessage


class LLMProvider(ABC):
    """
    Base class for LLM providers.

    All provider implementations should inherit from this class.
    """

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the provider.

        Args:
            key_manager: Key manager for API keys
        """
        self.key_manager = key_manager

    @abstractmethod
    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        pass

    @abstractmethod
    def get_available_models(self) -> List[str]:
        """
        Get available models for this provider.

        Returns:
            List of available model names
        """
        pass

    @abstractmethod
    async def generate_response(
        self,
        messages: List[LLMMessage],
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of messages in the conversation
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            Generated text
        """
        pass

    async def generate_response_streaming(
        self,
        messages: List[LLMMessage],
        callback: callable,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1024,
        **kwargs
    ) -> None:
        """
        Generate a streaming response from the LLM.

        Args:
            messages: List of messages in the conversation
            callback: Callback function for each chunk
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Raises:
            NotImplementedError: If streaming is not supported by this provider
        """
        raise NotImplementedError("Streaming is not supported by this provider")

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported, False otherwise
        """
        return False

    @property
    def supports_vision(self) -> bool:
        """
        Check if this provider supports vision/image input.

        Returns:
            True if vision is supported, False otherwise
        """
        return False

    @property
    def supports_image_generation(self) -> bool:
        """
        Check if this provider supports image generation.

        Returns:
            True if image generation is supported, False otherwise
        """
        return False

    @property
    def supports_function_calling(self) -> bool:
        """
        Check if this provider supports function calling.

        Returns:
            True if function calling is supported, False otherwise
        """
        return False

    @property
    def supports_structured_output(self) -> bool:
        """
        Check if this provider supports structured output.

        Returns:
            True if structured output is supported, False otherwise
        """
        return False

    @property
    def supports_embeddings(self) -> bool:
        """
        Check if this provider supports text embeddings.

        Returns:
            True if embeddings are supported, False otherwise
        """
        return False

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
            **kwargs: Additional parameters for the API

        Returns:
            Generated text

        Raises:
            NotImplementedError: If vision is not supported by this provider
        """
        raise NotImplementedError("Vision is not supported by this provider")

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
            model: Model to use (defaults to provider default)
            size: Size of the image (e.g., "1024x1024")
            format: Output format ("url" or "bytes")
            **kwargs: Additional parameters for the API

        Returns:
            URL or bytes of the generated image

        Raises:
            NotImplementedError: If image generation is not supported by this provider
        """
        raise NotImplementedError("Image generation is not supported by this provider")

    async def call_function(
        self,
        messages: List[LLMMessage],
        functions: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Call a function using the LLM.

        Args:
            messages: List of messages in the conversation
            functions: List of function definitions
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            **kwargs: Additional parameters for the API

        Returns:
            Dictionary with function call information

        Raises:
            NotImplementedError: If function calling is not supported by this provider
        """
        raise NotImplementedError("Function calling is not supported by this provider")

    async def generate_structured_output(
        self,
        messages: List[LLMMessage],
        response_format: Dict[str, Any],
        model: Optional[str] = None,
        temperature: float = 0.7,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a structured output from the LLM.

        Args:
            messages: List of messages in the conversation
            response_format: Format specification for the response
            model: Model to use (defaults to provider default)
            temperature: Temperature for generation
            **kwargs: Additional parameters for the API

        Returns:
            Structured response data

        Raises:
            NotImplementedError: If structured output is not supported by this provider
        """
        raise NotImplementedError("Structured output is not supported by this provider")

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
            model: Model to use (defaults to provider default)
            **kwargs: Additional parameters for the API

        Returns:
            List of embedding vectors

        Raises:
            NotImplementedError: If embeddings are not supported by this provider
        """
        raise NotImplementedError("Embeddings are not supported by this provider")

    async def close(self) -> None:
        """
        Close any resources used by the provider.

        This method should be called when the provider is no longer needed.
        """
        pass
