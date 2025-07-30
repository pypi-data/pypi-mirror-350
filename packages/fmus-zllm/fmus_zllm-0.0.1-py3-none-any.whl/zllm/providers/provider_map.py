"""
Provider map for LLM providers.

This module maps provider names to provider classes.
"""

from typing import Dict, Type, Optional

from ..base import LLMProvider

# This will be populated by provider modules
PROVIDER_MAP: Dict[str, Type[LLMProvider]] = {}


def register_provider(name: str, provider_class: Type[LLMProvider]) -> None:
    """
    Register a provider class with the provider map.

    Args:
        name: Provider name
        provider_class: Provider class
    """
    PROVIDER_MAP[name.lower()] = provider_class


def get_provider_class(provider_name: Optional[str] = None) -> Dict[str, Type[LLMProvider]]:
    """
    Get the provider class for a given provider name or the entire provider map.

    Args:
        provider_name: Name of the provider (optional)

    Returns:
        Provider class if provider_name is specified, or the entire provider map if not
    """
    if provider_name is None:
        return PROVIDER_MAP
    return {provider_name.lower(): PROVIDER_MAP.get(provider_name.lower())} if provider_name.lower() in PROVIDER_MAP else {}
