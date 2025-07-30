"""
Configuration module for ZLLM.

This module handles loading and managing configuration settings for ZLLM.
"""

from zllm.config.config_manager import ConfigManager
from zllm.config.default_config import DEFAULT_CONFIG

# Create a global config manager instance
_config_manager = ConfigManager()

def get_config():
    """
    Get the current configuration.

    Returns:
        The current configuration dictionary
    """
    return _config_manager.get_config()

def set_config(config):
    """
    Set the global configuration.

    Args:
        config: The new configuration dictionary
    """
    _config_manager.set_config(config)

def load_config(config_path=None):
    """
    Load configuration from a file.

    Args:
        config_path: Path to the configuration file

    Returns:
        The loaded configuration
    """
    return _config_manager.load_config(config_path)

def save_config(config_path):
    """
    Save the current configuration to a file.

    Args:
        config_path: Path to save the configuration
    """
    _config_manager.save_config(config_path)

__all__ = [
    'get_config',
    'set_config',
    'load_config',
    'save_config',
    'DEFAULT_CONFIG',
    'ConfigManager'
]
