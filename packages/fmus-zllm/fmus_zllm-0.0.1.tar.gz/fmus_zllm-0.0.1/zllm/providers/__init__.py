"""
Provider initialization and management for ZLLM.

This module handles importing and initializing LLM providers.
"""

import importlib
import logging
from typing import Dict, Type, Optional, Any

from zllm.base import LLMProvider
from zllm.exceptions import ConfigurationError, ProviderNotFoundError
from zllm.key_manager import KeyManager
from zllm.config import get_config

from zllm.providers.anthropic import AnthropicProvider
from zllm.providers.cerebras import CerebrasProvider
from zllm.providers.cohere import CohereProvider
from zllm.providers.gemini import GeminiProvider
from zllm.providers.glhf import GLHFProvider
from zllm.providers.groq import GroqProvider
from zllm.providers.huggingface import HuggingFaceProvider
from zllm.providers.hyperbolic import HyperbolicProvider
from zllm.providers.openai import OpenAIProvider
from zllm.providers.sambanova import SambanovaProvider
from zllm.providers.together import TogetherProvider


logger = logging.getLogger(__name__)


provider_classes = {
    "anthropic": AnthropicProvider,
    "cerebras": CerebrasProvider,
    "cohere": CohereProvider,
    "gemini": GeminiProvider,
    "glhf": GLHFProvider,
    "groq": GroqProvider,
    "huggingface": HuggingFaceProvider,
    "hyperbolic": HyperbolicProvider,
    "openai": OpenAIProvider,
    "sambanova": SambanovaProvider,
    "together": TogetherProvider,
}

def get_provider_class() -> Dict[str, Type[LLMProvider]]:
    """
    Get a dictionary of available provider classes using static imports.
    This is much faster than the dynamic import approach.

    Returns:
        Dictionary mapping provider names to provider classes
    """
    # providers = {}

    # # Define providers with their imported classes


    # # Add only the available providers (not None)
    # for provider_name, provider_class in provider_classes.items():
    #     if provider_class is not None:
    #         providers[provider_name] = provider_class

    return provider_classes


def get_provider_class_dynamic() -> Dict[str, Type[LLMProvider]]:
    """
    Get a dictionary of available provider classes using dynamic imports.
    This is slower but more flexible for future changes.

    Returns:
        Dictionary mapping provider names to provider classes
    """
    providers = {}

    # Define provider names and their corresponding class names
    provider_classes = {
        "anthropic": "AnthropicProvider",
        "cerebras": "CerebrasProvider",
        "cohere": "CohereProvider",
        "gemini": "GeminiProvider",
        "glhf": "GLHFProvider",
        "groq": "GroqProvider",
        "huggingface": "HuggingFaceProvider",
        "hyperbolic": "HyperbolicProvider",
        "openai": "OpenAIProvider",
        "sambanova": "SambanovaProvider",
        "together": "TogetherProvider",
    }

    # Try to import each provider
    for provider_name, class_name in provider_classes.items():
        try:
            # print(f"Importing provider: {provider_name}")
            module = importlib.import_module(f"zllm.providers.{provider_name}")
            provider_class = getattr(module, class_name)
            providers[provider_name] = provider_class
        except (ImportError, AttributeError) as e:
            logger.debug(f"Provider {provider_name} not available: {str(e)}")

    return providers


def get_provider(provider_name: str) -> Optional[LLMProvider]:
    """
    Get an instance of the specified provider.

    Args:
        provider_name: Name of the provider to get

    Returns:
        Provider instance, or None if the provider is not found

    Raises:
        ConfigurationError: If the provider is found but cannot be instantiated
    """
    provider_classes = get_provider_class()
    if provider_name.lower() not in provider_classes:
        available_providers = list(provider_classes.keys())
        raise ProviderNotFoundError(f"Provider '{provider_name}' not found. Available providers: {available_providers}")

    try:
        # Get the provider class
        provider_class = provider_classes[provider_name.lower()]

        # Create a key manager
        key_manager = KeyManager()

        # Instantiate the provider
        return provider_class(key_manager)
    except Exception as e:
        logger.error(f"Failed to initialize provider '{provider_name}': {str(e)}")
        raise ConfigurationError(f"Failed to initialize provider '{provider_name}': {str(e)}") from e


def get_available_providers() -> Dict[str, Type[LLMProvider]]:
    """
    Get a dictionary of available providers.

    Returns:
        Dictionary mapping provider names to provider classes
    """
    return get_provider_class()


__all__ = ["get_provider", "get_available_providers", "get_provider_class", "get_provider_class_dynamic"]
