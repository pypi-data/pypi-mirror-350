"""
Integration module for ZLLM.

This module provides integration between the ModelRegistry and other components.
"""

from typing import Optional, Dict, Any, List

from zllm.model_registry import get_registry
from zllm.client import LLMClient
from zllm.base import LLMProvider


def get_client_from_registry(
    provider: Optional[str] = None,
    model: Optional[str] = None,
    temperature: float = 0.7,
    max_tokens: int = 1024,
    **kwargs
) -> LLMClient:
    """
    Create an LLMClient using settings from the ModelRegistry.

    Args:
        provider: Provider name (defaults to registry default)
        model: Model name (defaults to registry default for the provider)
        temperature: Temperature for generation
        max_tokens: Maximum tokens to generate
        **kwargs: Additional parameters for the client

    Returns:
        LLMClient instance
    """
    registry = get_registry()

    # Use registry default if provider not specified
    if provider is None:
        provider = registry.get_default_provider()

    # Use registry default model if not specified
    if model is None:
        model = registry.get_default_model(provider)

    # Create and return the client
    return LLMClient(
        provider=provider,
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        **kwargs
    )


def get_model_info(provider: str, model_id: str) -> Optional[Dict[str, Any]]:
    """
    Get model information from the registry.

    Args:
        provider: Provider name
        model_id: Model ID

    Returns:
        Model information or None if not found
    """
    registry = get_registry()
    return registry.get_model_by_id(provider, model_id)


def get_available_models_for_provider(provider: str) -> List[Dict[str, Any]]:
    """
    Get all available models for a provider from the registry.

    Args:
        provider: Provider name

    Returns:
        List of model configurations
    """
    registry = get_registry()
    return registry.get_models(provider)


def get_default_model_for_provider(provider: str) -> Optional[str]:
    """
    Get the default model for a provider from the registry.

    Args:
        provider: Provider name

    Returns:
        Default model ID or None if not found
    """
    registry = get_registry()
    return registry.get_default_model(provider)


def provider_supports_capability(provider: str, capability: str) -> bool:
    """
    Check if a provider supports a specific capability.

    Args:
        provider: Provider name
        capability: Capability to check (vision, image_generation, etc.)

    Returns:
        True if the capability is supported, False otherwise
    """
    registry = get_registry()
    return registry.supports_capability(provider, capability)


def update_provider_models(
    provider_instance: LLMProvider,
    provider_name: str
) -> None:
    """
    Update a provider instance with models from the registry.

    This function can be used to inject model information from the registry
    into a provider instance.

    Args:
        provider_instance: Provider instance to update
        provider_name: Name of the provider in the registry
    """
    registry = get_registry()

    # Get models for the provider
    models = registry.get_models(provider_name)

    # If the provider has a method to update models, use it
    if hasattr(provider_instance, "update_models") and callable(getattr(provider_instance, "update_models")):
        model_ids = [model["id"] for model in models]
        provider_instance.update_models(model_ids)


def register_provider_models(
    provider_name: str,
    model_ids: List[str],
    default_model: Optional[str] = None
) -> None:
    """
    Register models for a provider in the registry.

    Args:
        provider_name: Name of the provider
        model_ids: List of model IDs to register
        default_model: Default model ID (if None, first model is used)
    """
    registry = get_registry()

    # Create model configurations
    for model_id in model_ids:
        is_default = (model_id == default_model) or (default_model is None and model_id == model_ids[0])

        # Add the model to the registry
        registry.add_model(provider_name, "text_models", {
            "id": model_id,
            "name": model_id,  # Use ID as name for simplicity
            "context_length": 8192,  # Default context length
            "default": is_default
        })

    # Save the registry
    registry.save()
