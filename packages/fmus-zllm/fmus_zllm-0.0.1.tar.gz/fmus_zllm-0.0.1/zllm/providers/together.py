"""
Together AI API provider implementation.

This module provides integration with Together AI's API for LLM functionality.
"""

import asyncio
import time
import logging
from typing import List, Optional, Callable, Dict, Any, AsyncGenerator, Union

from together import Together, AsyncTogether

from ..base import LLMProvider, LLMMessage
from ..config import get_config
from ..key_manager import KeyManager
from ..exceptions import APIKeyError, RateLimitError, AuthenticationError
from .provider_map import register_provider
from ..model_registry import get_registry

# Set up logging
logger = logging.getLogger(__name__)


class TogetherProvider(LLMProvider):
    """Together AI API implementation using the official Together SDK."""

    def __init__(self, key_manager: KeyManager):
        """
        Initialize the Together AI provider.

        Args:
            key_manager: KeyManager instance for API key management
        """
        super().__init__(key_manager)
        self._api_key = None
        self._client = None
        self._async_client = None
        self._config = get_config()
        self._registry = get_registry()
        logger.info("Together AI provider initialized")

    def _get_client(self):
        """
        Get a Together client with the current API key.

        Returns:
            Tuple of (initialized Together client, AsyncTogether client, API key)

        Raises:
            APIKeyError: If no API key is available
        """
        try:
            api_key = self.key_manager.get_random_key("together")
            if not api_key:
                logger.error("No API key available for Together AI")
                raise APIKeyError("No API key available for Together AI")

            logger.debug(f"Using Together API key: {api_key.key[:5]}...{api_key.key[-5:] if len(api_key.key) > 10 else ''}")
        except ValueError as e:
            logger.error(f"No API key available for Together AI: {str(e)}")
            raise APIKeyError(f"No API key available for Together AI: {str(e)}")

        # Configure the client if the API key has changed
        if self._api_key != api_key.key:
            logger.debug("Creating new Together AI client with updated API key")
            self._client = Together(api_key=api_key.key)
            self._async_client = AsyncTogether(api_key=api_key.key)
            self._api_key = api_key.key

        return self._client, self._async_client, api_key

    def get_available_models(self) -> List[str]:
        """
        Get a list of available models for this provider.

        Returns:
            List of model identifiers
        """
        logger.debug("Getting available Together AI models")
        models = self._registry.get_models("together", "text_models")
        return [model.get("id") for model in models]

    def get_default_model(self) -> str:
        """
        Get the default model for this provider.

        Returns:
            Default model name
        """
        default_model = self._registry.get_default_model("together", "text_models")
        logger.debug(f"Using default Together AI model: {default_model}")
        return default_model

    async def generate_response(self,
                         messages: List[LLMMessage],
                         model: Optional[str] = None,
                         temperature: float = 0.7,
                         max_tokens: Optional[int] = None) -> str:
        """
        Generate a response using the Together AI API.

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
            logger.info(f"Generating response with Together AI, model={model or 'default'}, temperature={temperature}")
            model_name = model or self.get_default_model()

            # Format messages for Together AI API
            formatted_messages = self._format_messages_for_api(messages)
            logger.debug(f"Formatted {len(messages)} messages for Together AI API")

            # Determine if we should use chat completions or text completions
            if self._should_use_chat_api(messages):
                # Set generation parameters for chat
                params = {
                    "model": model_name,
                    "messages": formatted_messages,
                    "temperature": temperature,
                }

                if max_tokens:
                    params["max_tokens"] = max_tokens

                logger.debug(f"Together AI chat request parameters: {params}")

                # Generate response
                logger.debug("Sending chat request to Together AI API")
                response = await async_client.chat.completions.create(**params)
                logger.debug("Received response from Together AI API")

                # Extract and return the response text
                response_text = response.choices[0].message.content.strip()
            else:
                # Use text completions API for simple prompts
                prompt = self._format_prompt_for_completions_api(messages)

                # Set generation parameters for completions
                params = {
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens or 512,
                }

                logger.debug(f"Together AI completions request parameters: {params}")

                # Generate response
                logger.debug("Sending completions request to Together AI API")
                response = await async_client.completions.create(**params)
                logger.debug("Received response from Together AI API")

                # Extract and return the response text
                response_text = response.choices[0].text.strip()

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")
            logger.info(f"Generated response of length {len(response_text)}")

            return response_text

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error with Together AI API: {error_msg}")

            if "401" in error_msg or "unauthorized" in error_msg.lower():
                api_key.mark_error()
                logger.error("Invalid API key for Together AI")
                raise AuthenticationError("Invalid API key for Together AI") from e

            elif "429" in error_msg or "rate limit" in error_msg.lower():
                retry_after = 60  # Default retry after 60 seconds
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Together AI rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"Together AI rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            else:
                api_key.mark_error()
                raise ValueError(f"Unexpected error with Together AI API: {error_msg}") from e

    async def generate_response_streaming(self,
                                   messages: List[LLMMessage],
                                   callback: Callable[[str], None],
                                   model: Optional[str] = None,
                                   temperature: float = 0.7,
                                   max_tokens: Optional[int] = None) -> None:
        """
        Generate a streaming response from the Together AI API.

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
            logger.info(f"Generating streaming response with Together AI, model={model or 'default'}, temperature={temperature}")
            model_name = model or self.get_default_model()

            # Determine if we should use chat completions or text completions
            if self._should_use_chat_api(messages):
                # Format messages for Together AI API
                formatted_messages = self._format_messages_for_api(messages)
                logger.debug(f"Formatted {len(messages)} messages for Together AI API")

                # Set generation parameters for chat
                params = {
                    "model": model_name,
                    "messages": formatted_messages,
                    "temperature": temperature,
                    "stream": True
                }

                if max_tokens:
                    params["max_tokens"] = max_tokens

                logger.debug(f"Together AI chat streaming request parameters: {params}")

                # Generate streaming response
                logger.debug("Sending streaming chat request to Together AI API")
                stream = await async_client.chat.completions.create(**params)

                # Process the stream
                chunk_count = 0
                logger.debug("Processing chat response stream")
                response_buffer = []
                first_valid_content_seen = False

                async for chunk in stream:
                    if chunk.choices and chunk.choices[0].delta and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content

                        # Check if this is valid content (heuristic)
                        if not first_valid_content_seen:
                            # Look for indicators of a proper response start
                            # Skip initial garbage chunks that often contain code-like or formatting characters
                            if len(content.strip()) > 0 and not any(marker in content for marker in ['"]', '"])', '[', ']', '>', '<', '\\', '{', '}']):
                                first_valid_content_seen = True
                                response_buffer.append(content)

                                # Send all buffered content
                                buffered_content = ''.join(response_buffer)
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(buffered_content)
                                else:
                                    callback(buffered_content)
                                chunk_count += 1
                                response_buffer = []
                            else:
                                # Keep buffering until we see valid content
                                logger.debug(f"Buffering potential header content: {repr(content)}")
                                continue
                        else:
                            # Already started valid content, just send it
                            if asyncio.iscoroutinefunction(callback):
                                await callback(content)
                            else:
                                callback(content)
                            chunk_count += 1

                logger.debug(f"Processed {chunk_count} chunks from chat stream")
            else:
                # Use text completions API for simple prompts
                prompt = self._format_prompt_for_completions_api(messages)

                # Set generation parameters for completions
                params = {
                    "model": model_name,
                    "prompt": prompt,
                    "temperature": temperature,
                    "max_tokens": max_tokens or 512,
                    "stream": True
                }

                logger.debug(f"Together AI completions streaming request parameters: {params}")

                # Generate streaming response
                logger.debug("Sending streaming completions request to Together AI API")
                stream = await async_client.completions.create(**params)

                # Process the stream
                chunk_count = 0
                logger.debug("Processing completions response stream")
                response_buffer = []
                first_valid_content_seen = False

                async for chunk in stream:
                    if chunk.choices and chunk.choices[0].text:
                        content = chunk.choices[0].text

                        # Check if this is valid content (heuristic)
                        if not first_valid_content_seen:
                            # Look for indicators of a proper response start
                            # Skip initial garbage chunks that often contain code-like or formatting characters
                            if len(content.strip()) > 0 and not any(marker in content for marker in ['"]', '"])', '[', ']', '>', '<', '\\', '{', '}']):
                                first_valid_content_seen = True
                                response_buffer.append(content)

                                # Send all buffered content
                                buffered_content = ''.join(response_buffer)
                                if asyncio.iscoroutinefunction(callback):
                                    await callback(buffered_content)
                                else:
                                    callback(buffered_content)
                                chunk_count += 1
                                response_buffer = []
                            else:
                                # Keep buffering until we see valid content
                                logger.debug(f"Buffering potential header content: {repr(content)}")
                                continue
                        else:
                            # Already started valid content, just send it
                            if asyncio.iscoroutinefunction(callback):
                                await callback(content)
                            else:
                                callback(content)
                            chunk_count += 1

                logger.debug(f"Processed {chunk_count} chunks from completions stream")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error with Together AI streaming API: {error_msg}")

            if "401" in error_msg or "unauthorized" in error_msg.lower():
                api_key.mark_error()
                logger.error("Invalid API key for Together AI")
                raise AuthenticationError("Invalid API key for Together AI") from e

            elif "429" in error_msg or "rate limit" in error_msg.lower():
                retry_after = 60  # Default retry after 60 seconds
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Together AI rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"Together AI rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            else:
                api_key.mark_error()
                raise ValueError(f"Unexpected error with Together AI streaming API: {error_msg}") from e

    def _should_use_chat_api(self, messages: List[LLMMessage]) -> bool:
        """
        Determine whether to use the chat API or completions API based on message format.

        Args:
            messages: List of messages to analyze

        Returns:
            True if chat API should be used, False for completions API
        """
        # Always use the chat API for better compatibility
        return True

    def _format_messages_for_api(self, messages: List[LLMMessage]) -> List[Dict[str, str]]:
        """
        Format messages for the Together AI API.

        Args:
            messages: List of messages to format

        Returns:
            List of formatted message dictionaries for Together AI API
        """
        formatted_messages = []

        for message in messages:
            role = message.role.lower()

            # Map roles to Together AI expected format
            if role == "system":
                formatted_messages.append({"role": "system", "content": message.content})
            elif role == "user":
                formatted_messages.append({"role": "user", "content": message.content})
            elif role == "assistant":
                formatted_messages.append({"role": "assistant", "content": message.content})
            else:
                # Unknown role, treat as user
                formatted_messages.append({"role": "user", "content": message.content})

        return formatted_messages

    def _format_prompt_for_completions_api(self, messages: List[LLMMessage]) -> str:
        """
        Format messages as a single prompt string for the completions API.

        Args:
            messages: List of messages to format

        Returns:
            Formatted prompt string
        """
        # For simple completions, just use the content of the first message
        if messages and len(messages) > 0:
            return messages[0].content
        return ""

    async def generate_image(
        self,
        prompt: str,
        model: Optional[str] = None,
        size: Optional[str] = None,
        format: str = "url",
        steps: int = 10,
        **kwargs
    ) -> Union[str, bytes]:
        """
        Generate an image from a text prompt using Together API.

        Args:
            prompt: Text prompt to generate image from
            model: Model to use (defaults to provider's default image model)
            size: Size of the image to generate (e.g., "1024x1024")
            format: Format of the returned image ("url" or "bytes")
            steps: Number of diffusion steps (specific to Together API)
            **kwargs: Additional parameters for the API

        Returns:
            Image URL or binary data depending on format parameter

        Raises:
            APIKeyError: If no API key is available
            Exception: On API errors
        """
        _, async_client, api_key = self._get_client()

        try:
            logger.info(f"Generating image with Together AI, prompt='{prompt}', model={model or 'default'}, steps={steps}")

            # Use the model registry to get the default image model if none is specified
            if model is None:
                default_image_model = self._registry.get_default_model("together", "image_models")
                model = default_image_model

            logger.debug(f"Using image model: {model}")

            # Set generation parameters
            params = {
                "model": model,
                "prompt": prompt,
                "steps": steps,
                "n": 1
            }

            if size:
                width, height = map(int, size.split("x"))
                params["width"] = width
                params["height"] = height
                logger.debug(f"Using image size: {width}x{height}")

            # Add any additional parameters
            for key, value in kwargs.items():
                params[key] = value

            logger.debug(f"Together AI image generation parameters: {params}")

            # Generate image
            logger.debug("Sending image generation request to Together AI API")
            response = await async_client.images.generate(**params)
            logger.debug("Received image generation response from Together AI API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Extract the image URL or data
            if response.data and len(response.data) > 0:
                if format.lower() == "url":
                    image_url = response.data[0].url
                    logger.debug(f"Generated image URL: {image_url}")
                    return image_url
                else:
                    # Get image data from base64
                    import base64
                    image_data = base64.b64decode(response.data[0].b64_json)
                    logger.info(f"Generated image data, size: {len(image_data)} bytes")
                    return image_data

            error_msg = "No image data in response"
            logger.error(error_msg)
            raise ValueError(error_msg)

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error with Together AI image generation API: {error_msg}")

            if "401" in error_msg or "unauthorized" in error_msg.lower():
                api_key.mark_error()
                logger.error("Invalid API key for Together AI")
                raise AuthenticationError("Invalid API key for Together AI") from e

            elif "429" in error_msg or "rate limit" in error_msg.lower():
                retry_after = 60  # Default retry after 60 seconds
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Together AI rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"Together AI rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            else:
                api_key.mark_error()
                raise ValueError(f"Unexpected error with Together AI image generation API: {error_msg}") from e

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
            model: Model to use (defaults to provider's default embedding model)
            **kwargs: Additional parameters for the API

        Returns:
            List of embedding vectors

        Raises:
            APIKeyError: If no API key is available
            Exception: On API errors
        """
        _, async_client, api_key = self._get_client()

        try:
            logger.info(f"Generating embeddings with Together AI for {len(texts)} texts")

            # Use the model registry to get the default embedding model if none is specified
            if model is None:
                default_embedding_model = self._registry.get_default_model("together", "embedding_models")
                model = default_embedding_model or "togethercomputer/m2-bert-80M-8k-retrieval"

            logger.debug(f"Using embedding model: {model}")

            # Preprocess texts
            texts = [text.replace("\n", " ") for text in texts]

            # Set generation parameters
            params = {
                "model": model,
                "input": texts
            }

            # Add any additional parameters
            for key, value in kwargs.items():
                params[key] = value

            logger.debug(f"Together AI embeddings request parameters: {params}")

            # Generate embeddings
            logger.debug("Sending embeddings request to Together AI API")
            response = await async_client.embeddings.create(**params)
            logger.debug("Received embeddings response from Together AI API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Extract the embeddings
            embeddings = [data.embedding for data in response.data]
            logger.info(f"Generated {len(embeddings)} embedding vectors")

            return embeddings

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error with Together AI embeddings API: {error_msg}")

            if "401" in error_msg or "unauthorized" in error_msg.lower():
                api_key.mark_error()
                logger.error("Invalid API key for Together AI")
                raise AuthenticationError("Invalid API key for Together AI") from e

            elif "429" in error_msg or "rate limit" in error_msg.lower():
                retry_after = 60  # Default retry after 60 seconds
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Together AI rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"Together AI rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            else:
                api_key.mark_error()
                raise ValueError(f"Unexpected error with Together AI embeddings API: {error_msg}") from e

    async def rerank_documents(
        self,
        query: str,
        documents: List[str],
        model: Optional[str] = None,
        top_n: int = 3,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Rerank documents based on relevance to a query.

        Args:
            query: Query string
            documents: List of documents to rerank
            model: Model to use (defaults to provider's default reranking model)
            top_n: Number of top documents to return
            **kwargs: Additional parameters for the API

        Returns:
            List of dictionaries containing reranked documents with scores

        Raises:
            APIKeyError: If no API key is available
            Exception: On API errors
        """
        _, async_client, api_key = self._get_client()

        try:
            logger.info(f"Reranking {len(documents)} documents with Together AI")

            # Use the model registry to get the default reranking model if none is specified
            if model is None:
                default_reranking_model = self._registry.get_default_model("together", "reranking_models")
                model = default_reranking_model or "Salesforce/Llama-Rank-V1"

            logger.debug(f"Using reranking model: {model}")

            # Set reranking parameters
            params = {
                "model": model,
                "query": query,
                "documents": documents,
                "top_n": top_n
            }

            # Add any additional parameters
            for key, value in kwargs.items():
                params[key] = value

            logger.debug(f"Together AI reranking request parameters: {params}")

            # Rerank documents
            logger.debug("Sending reranking request to Together AI API")
            response = await async_client.rerank.create(**params)
            logger.debug("Received reranking response from Together AI API")

            # Mark the API key as used
            api_key.mark_used()
            logger.debug("Marked API key as used")

            # Process and return results
            results = []
            for result in sorted(response.results, key=lambda x: x.relevance_score, reverse=True):
                results.append({
                    "document": documents[result.index],
                    "index": result.index,
                    "relevance_score": result.relevance_score
                })

            logger.info(f"Reranked {len(results)} documents")
            return results

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Error with Together AI reranking API: {error_msg}")

            if "401" in error_msg or "unauthorized" in error_msg.lower():
                api_key.mark_error()
                logger.error("Invalid API key for Together AI")
                raise AuthenticationError("Invalid API key for Together AI") from e

            elif "429" in error_msg or "rate limit" in error_msg.lower():
                retry_after = 60  # Default retry after 60 seconds
                api_key.last_used = time.time()  # Mark as used but not errored
                logger.warning(f"Together AI rate limit exceeded. Retry after {retry_after}s.")
                raise RateLimitError(
                    f"Together AI rate limit exceeded. Retry after {retry_after}s.",
                    retry_after=retry_after
                ) from e

            else:
                api_key.mark_error()
                raise ValueError(f"Unexpected error with Together AI reranking API: {error_msg}") from e

    async def close(self) -> None:
        """Close any resources held by the provider."""
        # Nothing to close when using Together SDK
        pass

    @property
    def supports_streaming(self) -> bool:
        """
        Check if this provider supports streaming.

        Returns:
            True if streaming is supported, False otherwise
        """
        logger.debug("Together AI provider supports streaming")
        return True

    @property
    def supports_image_generation(self) -> bool:
        """
        Check if this provider supports image generation.

        Returns:
            True if image generation is supported, False otherwise
        """
        logger.debug("Checking if Together AI provider supports image generation")
        return self._registry.supports_capability("together", "image_generation")

    @property
    def supports_embeddings(self) -> bool:
        """
        Check if this provider supports embeddings.

        Returns:
            True if embeddings are supported
        """
        logger.debug("Together AI provider supports embeddings")
        return True

    @property
    def supports_reranking(self) -> bool:
        """
        Check if this provider supports reranking.

        Returns:
            True if reranking is supported
        """
        logger.debug("Together AI provider supports reranking")
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


# Register the provider
register_provider("together", TogetherProvider)
