"""
Utility modules for ZLLM.

This package provides utility functions for working with LLM responses and other common tasks.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from zllm.utils.parsing import (
    parse_json_response,
    extract_json_from_text,
    extract_list_from_text,
    extract_key_value_pairs
)

def get_provider_config(provider_name: str) -> Dict[str, Any]:
    """
    Get configuration for a provider.

    Args:
        provider_name: Name of the provider

    Returns:
        Provider configuration
    """
    # Look for provider config in the config directory
    config_dir = Path(__file__).parent.parent / "config"
    config_file = config_dir / f"{provider_name}.json"

    if config_file.exists():
        with open(config_file, "r", encoding="utf-8") as f:
            return json.load(f)

    # Return empty config if no config file found
    return {}

__all__ = [
    "parse_json_response",
    "extract_json_from_text",
    "extract_list_from_text",
    "extract_key_value_pairs",
    "get_provider_config"
]
