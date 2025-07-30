#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Key management module for ZLLM.

This module handles reading API keys from files in the user's home directory.
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Optional, Any, Union
import time
import random
import logging

logger = logging.getLogger(__name__)

# Define key file paths for different providers
KEY_FILES = {
    "openai": "OPENAI_API_KEYS.json",
    "anthropic": "ANTHROPIC_API_KEYS.json",
    "gemini": "GOOGLE_GEMINI_API_KEYS.json",
    "groq": "GROQ_API_KEYS.json",
    "cohere": "COHERE_API_KEYS.json",
    "huggingface": "HUGGINGFACE_API_KEYS.json",
    "together": "TOGETHER_API_KEYS.json",
    "sambanova": "SAMBANOVA_API_KEYS.json",
    "cerebras": "CEREBRAS_API_KEYS.json",
    "glhf": "GLHF_API_KEYS.json",
    "hyperbolic": "HYPERBOLIC_API_KEYS.json"
}


class APIKey:
    """Represents an API key with metadata."""

    def __init__(self, name: str, key: str, provider: str, **kwargs):
        """
        Initialize a new API key.

        Args:
            name: A descriptive name for the key
            key: The actual API key value
            provider: The provider this key is for (e.g., "gemini", "openai")
            **kwargs: Additional metadata for the key
        """
        self.name = name
        self.key = key
        self.provider = provider
        self.metadata = kwargs
        self.last_used = kwargs.get("last_used", 0)  # timestamp
        self.error_count = kwargs.get("error_count", 0)
        self.is_valid = kwargs.get("is_valid", True)

    def mark_used(self):
        """Mark this key as used by updating its last_used timestamp."""
        self.last_used = time.time()

    def mark_error(self):
        """
        Mark that an error occurred with this key.

        Increments the error counter. Could be used for rate limiting or error tracking.
        """
        self.error_count += 1
        if self.error_count >= 10:  # Threshold for invalidating a key
            self.is_valid = False

    def reset_errors(self):
        """Reset the error counter for this key."""
        self.error_count = 0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the key to a dictionary representation."""
        return {
            "name": self.name,
            "key": self.key,
            "last_used": self.last_used,
            "error_count": self.error_count,
            **self.metadata
        }


class KeyManager:
    """
    Manages API keys for different providers.

    Reads API keys from JSON files stored in the user's home directory.
    Each file contains a list of key objects with name, key, last_used timestamp,
    and error_count fields.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the key manager.

        Args:
            config: Optional configuration dictionary
        """
        self.home_dir = Path.home()
        self.keys = {}  # provider -> list of APIKey objects
        self.config = config or {}

        # Load keys for all known providers
        for provider in KEY_FILES.keys():
            self._load_keys_for_provider(provider)

    def get_key_file_path(self, provider: str) -> Path:
        """Get the path to the key file for a provider."""
        if provider not in KEY_FILES:
            raise ValueError(f"Unknown provider: {provider}")

        # Check if path is specified in config
        path_key = f"{provider}_keys_path"
        if self.config.get(path_key):
            return Path(self.config[path_key])

        # Otherwise use default path
        return self.home_dir / KEY_FILES[provider]

    def _load_keys_for_provider(self, provider: str) -> None:
        """Load keys for a specific provider."""
        try:
            file_path = self.get_key_file_path(provider)
            if file_path.exists():
                self.load_keys_from_file(provider, str(file_path))
        except Exception as e:
            logger.warning(f"Failed to load keys for {provider}: {str(e)}")

    def load_keys_from_file(self, provider: str, filepath: str) -> bool:
        """
        Load API keys from a JSON file.

        Args:
            provider: The provider name
            filepath: Path to the JSON file containing the keys

        Returns:
            True if keys were loaded successfully, False otherwise
        """
        try:
            with open(filepath, "r") as f:
                key_data = json.load(f)

            # Case 1: List of key objects
            if isinstance(key_data, list):
                for item in key_data:
                    if "name" in item and "key" in item:
                        metadata = {k: v for k, v in item.items()
                                   if k not in ["name", "key"]}
                        key = APIKey(item["name"], item["key"], provider, **metadata)
                        self.add_key(provider, key)
                return True

            # Case 2: Simple object with api_key field
            elif isinstance(key_data, dict) and "api_key" in key_data:
                key = APIKey(f"{provider}-default", key_data["api_key"], provider)
                self.add_key(provider, key)
                return True

            else:
                logger.error(f"Invalid key file format for {provider}: {key_data}")
                return False

        except Exception as e:
            logger.error(f"Failed to load keys for {provider} from {filepath}: {e}")
            return False

    def add_key(self, provider: str, key: APIKey) -> None:
        """
        Add a new API key.

        Args:
            provider: The provider name
            key: The APIKey object to add
        """
        if provider not in self.keys:
            self.keys[provider] = []
        self.keys[provider].append(key)

    def save_keys(self, provider: str) -> None:
        """
        Save API keys for a provider to the key file.

        Args:
            provider: The provider name
        """
        if provider not in self.keys:
            return

        file_path = self.get_key_file_path(provider)

        # Create directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        # Convert APIKey objects to dictionaries
        keys_data = [key.to_dict() for key in self.keys[provider]]

        with open(file_path, "w") as f:
            json.dump(keys_data, f, indent=2)

    def get_random_key(self, provider: str) -> Optional[APIKey]:
        """
        Get a random valid API key for the specified provider.

        Args:
            provider: The provider name

        Returns:
            A random valid APIKey, or None if no valid keys are available
        """
        if provider not in self.keys or not self.keys[provider]:
            return None

        # Filter for valid keys
        valid_keys = [k for k in self.keys[provider] if k.is_valid]
        if not valid_keys:
            return None

        selected_key = random.choice(valid_keys)
        selected_key.mark_used()
        return selected_key

    def get_least_used_key(self, provider: str) -> Optional[APIKey]:
        """
        Get the least recently used valid API key.

        Args:
            provider: The provider name

        Returns:
            The least recently used valid APIKey, or None if no valid keys are available
        """
        if provider not in self.keys or not self.keys[provider]:
            return None

        # Filter for valid keys
        valid_keys = [k for k in self.keys[provider] if k.is_valid]
        if not valid_keys:
            return None

        selected_key = min(valid_keys, key=lambda k: k.last_used)
        selected_key.mark_used()
        return selected_key

    def get_api_key(self, provider: str, name: Optional[str] = None) -> str:
        """
        Get an API key for a provider.

        If name is provided, returns the key with that name.
        Otherwise, returns the key with the lowest error count and least recent usage.

        Args:
            provider: The provider name
            name: Optional key name

        Returns:
            API key string

        Raises:
            ValueError: If no valid key is found
        """
        # Check environment variables first
        env_var = f"{provider.upper()}_API_KEY"
        if env_var in os.environ:
            logger.info(f"Using {provider} API key from environment variable")
            return os.environ[env_var]

        # If name is provided, find the key with that name
        if name and provider in self.keys:
            for key_obj in self.keys[provider]:
                if key_obj.name == name:
                    key_obj.mark_used()
                    self.save_keys(provider)
                    return key_obj.key

            # If not found in memory, try loading from file
            try:
                self._load_keys_for_provider(provider)
                for key_obj in self.keys.get(provider, []):
                    if key_obj.name == name:
                        key_obj.mark_used()
                        self.save_keys(provider)
                        return key_obj.key
            except Exception:
                pass

            raise ValueError(f"API key '{name}' not found for {provider}")

        # Try to get a random key
        key_obj = self.get_random_key(provider)
        if key_obj:
            logger.info(f"Using {provider} API key: {key_obj.name}")
            return key_obj.key

        # If no keys in memory, try loading from file
        self._load_keys_for_provider(provider)
        key_obj = self.get_random_key(provider)
        if key_obj:
            return key_obj.key

        # If still no keys, raise error
        raise ValueError(f"No valid API key found for {provider}")

    def report_error(self, provider: str, api_key: str) -> None:
        """
        Report an error with an API key.

        Increments the error count for the key.

        Args:
            provider: The provider name
            api_key: The API key that had an error
        """
        if provider in self.keys:
            for key_obj in self.keys[provider]:
                if key_obj.key == api_key:
                    key_obj.mark_error()
                    self.save_keys(provider)
                    return

        # If key not found in memory, try loading from file
        try:
            self._load_keys_for_provider(provider)
            for key_obj in self.keys.get(provider, []):
                if key_obj.key == api_key:
                    key_obj.mark_error()
                    self.save_keys(provider)
                    return
        except Exception:
            pass

    def has_valid_key(self, provider: str) -> bool:
        """
        Check if there's a valid key available for the provider.

        Args:
            provider: The provider name

        Returns:
            True if a valid key is available, False otherwise
        """
        # Check environment variables first
        env_var = f"{provider.upper()}_API_KEY"
        if env_var in os.environ:
            return True

        # Check if we have valid keys in our store
        return self.get_valid_key_count(provider) > 0

    def get_valid_key_count(self, provider: str) -> int:
        """
        Get the number of valid keys available for a provider.

        Args:
            provider: The provider name

        Returns:
            The number of valid keys for the provider
        """
        if provider not in self.keys:
            return 0
        return len([k for k in self.keys[provider] if k.is_valid])

    def add_key_from_string(self, provider: str, key_str: str, name: str = None) -> None:
        """
        Add a new API key from a string.

        Args:
            provider: The provider name
            key_str: The key string
            name: Optional name for the key
        """
        if not name:
            name = f"{provider}-{len(self.keys.get(provider, []))+1}"

        key = APIKey(name, key_str, provider)
        self.add_key(provider, key)

    def save_key_to_file(self, provider: str, key_str: str) -> bool:
        """
        Save a single API key to the default file location.

        Args:
            provider: The provider name
            key_str: The key string

        Returns:
            True if key was saved successfully, False otherwise
        """
        try:
            # Use config path if available
            file_path = self.get_key_file_path(provider)

            # Save as simple format with api_key field
            with open(file_path, 'w') as f:
                json.dump({"api_key": key_str}, f, indent=2)

            # Add to our key store
            self.add_key_from_string(provider, key_str)

            logger.info(f"Saved {provider} API key to {file_path}")
            return True
        except Exception as e:
            logger.error(f"Failed to save key for {provider}: {e}")
            return False

    def get_available_providers(self) -> List[str]:
        """
        Get a list of providers with available keys.

        Returns:
            List of provider names
        """
        providers = []

        # Check environment variables
        for provider in KEY_FILES.keys():
            env_var = f"{provider.upper()}_API_KEY"
            if env_var in os.environ:
                providers.append(provider)
                continue

            # Check our key store
            valid_count = self.get_valid_key_count(provider)
            if valid_count > 0:
                providers.append(provider)

        return providers

    def get_key_info(self, provider: str, api_key: str) -> Optional[Dict[str, Any]]:
        """
        Get information about an API key given its string value.

        Args:
            provider: The provider name
            api_key: The API key string to look up

        Returns:
            A dictionary with key information (name, error_count, last_used, etc.),
            or None if the key is not found
        """
        if provider in self.keys:
            for key_obj in self.keys[provider]:
                if key_obj.key == api_key:
                    return {
                        "name": key_obj.name,
                        "error_count": key_obj.error_count,
                        "last_used": key_obj.last_used,
                        "is_valid": key_obj.is_valid,
                        **key_obj.metadata
                    }

        # If key not found in memory, try loading from file
        try:
            self._load_keys_for_provider(provider)
            for key_obj in self.keys.get(provider, []):
                if key_obj.key == api_key:
                    return {
                        "name": key_obj.name,
                        "error_count": key_obj.error_count,
                        "last_used": key_obj.last_used,
                        "is_valid": key_obj.is_valid,
                        **key_obj.metadata
                    }
        except Exception:
            pass

        return None


# Create a singleton instance
key_manager = KeyManager()


def get_api_key(provider: str, name: Optional[str] = None) -> str:
    """
    Get an API key for a provider.

    Args:
        provider: The provider name
        name: Optional key name

    Returns:
        API key string
    """
    return key_manager.get_api_key(provider, name)


def report_error(provider: str, api_key: str) -> None:
    """
    Report an error with an API key.

    Args:
        provider: The provider name
        api_key: The API key that had an error
    """
    key_manager.report_error(provider, api_key)


def get_key_info(provider: str, api_key: str) -> Optional[Dict[str, Any]]:
    """
    Get information about an API key given its string value.

    Args:
        provider: The provider name
        api_key: The API key string to look up

    Returns:
        A dictionary with key information (name, error_count, last_used, etc.),
        or None if the key is not found
    """
    return key_manager.get_key_info(provider, api_key)
