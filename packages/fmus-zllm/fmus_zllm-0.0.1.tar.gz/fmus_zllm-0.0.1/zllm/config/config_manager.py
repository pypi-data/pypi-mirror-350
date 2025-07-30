"""
Configuration manager for ZLLM.

This module provides a class for managing ZLLM configuration.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional

from zllm.config.default_config import DEFAULT_CONFIG


class ConfigManager:
    """
    Manager for ZLLM configuration.

    This class handles loading, saving, and managing ZLLM configuration.
    """

    def __init__(self, initial_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the configuration manager.

        Args:
            initial_config: Initial configuration (defaults to DEFAULT_CONFIG)
        """
        self._config = initial_config.copy() if initial_config else DEFAULT_CONFIG.copy()

    def get_config(self) -> Dict[str, Any]:
        """
        Get the current configuration.

        Returns:
            Current configuration dictionary
        """
        return self._config

    def set_config(self, config: Dict[str, Any]) -> None:
        """
        Set the current configuration.

        Args:
            config: New configuration dictionary
        """
        self._config = config

    def update_config(self, updates: Dict[str, Any]) -> None:
        """
        Update the current configuration with new values.

        Args:
            updates: Dictionary of configuration updates
        """
        self._deep_update(self._config, updates)

    def load_config(self, config_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Load configuration from a file and environment variables.

        Args:
            config_path: Path to configuration file (defaults to environment variable or default locations)

        Returns:
            Loaded configuration dictionary
        """
        # Start with default configuration
        config = DEFAULT_CONFIG.copy()

        # Check environment variable for config path
        if not config_path:
            config_path = os.environ.get("ZLLM_CONFIG_PATH")

        # Check default locations if still not set
        if not config_path:
            locations = [
                Path("config.json"),
                Path("config.yaml"),
                Path("config.yml"),
                Path.home() / ".zllm" / "config.json",
                Path.home() / ".zllm" / "config.yaml",
                Path.home() / ".zllm" / "config.yml",
                Path("/etc/zllm/config.json"),
                Path("/etc/zllm/config.yaml"),
                Path("/etc/zllm/config.yml")
            ]

            for loc in locations:
                if loc.exists():
                    config_path = str(loc)
                    break

        # Load from file if it exists
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    if config_path.endswith(('.yaml', '.yml')):
                        import yaml
                        file_config = yaml.safe_load(f)
                    else:
                        file_config = json.load(f)

                    if file_config:
                        self._deep_update(config, file_config)
            except Exception as e:
                # Log error but continue with defaults
                import logging
                logging.getLogger(__name__).error(f"Failed to load config from {config_path}: {e}")

        # Override with environment variables
        self._load_from_env(config)

        # Update the internal config
        self._config = config

        return config

    def save_config(self, config_path: str) -> bool:
        """
        Save configuration to a file.

        Args:
            config_path: Path to save configuration

        Returns:
            True if successful, False otherwise
        """
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        try:
            with open(config_path, 'w') as f:
                if config_path.endswith(('.yaml', '.yml')):
                    import yaml
                    yaml.dump(self._config, f, default_flow_style=False)
                else:
                    json.dump(self._config, f, indent=2)
            return True
        except Exception as e:
            # Log error
            import logging
            logging.getLogger(__name__).error(f"Failed to save config to {config_path}: {e}")
            return False

    def _deep_update(self, d: Dict[str, Any], u: Dict[str, Any]) -> None:
        """
        Deep update dictionary d with values from dictionary u.

        Args:
            d: Dictionary to update
            u: Dictionary with new values
        """
        for k, v in u.items():
            if isinstance(v, dict) and k in d and isinstance(d[k], dict):
                self._deep_update(d[k], v)
            else:
                d[k] = v

    def _load_from_env(self, config: Dict[str, Any]) -> None:
        """
        Load configuration from environment variables.

        Args:
            config: Configuration dictionary to update
        """
        # Default provider
        if "ZLLM_DEFAULT_PROVIDER" in os.environ:
            config["default_provider"] = os.environ["ZLLM_DEFAULT_PROVIDER"]

        # API keys
        for provider in [
            "openai", "anthropic", "gemini", "groq", "cohere",
            "huggingface", "together", "sambanova", "cerebras",
            "glhf", "hyperbolic"
        ]:
            env_var = f"ZLLM_{provider.upper()}_API_KEY"
            if env_var in os.environ:
                if "api_keys" not in config:
                    config["api_keys"] = {}
                config["api_keys"][provider] = os.environ[env_var]

        # Logging
        if "ZLLM_LOG_LEVEL" in os.environ:
            if "logging" not in config:
                config["logging"] = {}
            config["logging"]["level"] = os.environ["ZLLM_LOG_LEVEL"]

        # Temperature
        if "ZLLM_TEMPERATURE" in os.environ:
            try:
                config["temperature"] = float(os.environ["ZLLM_TEMPERATURE"])
            except ValueError:
                pass

        # Max tokens
        if "ZLLM_MAX_TOKENS" in os.environ:
            try:
                config["max_tokens"] = int(os.environ["ZLLM_MAX_TOKENS"])
            except ValueError:
                pass
