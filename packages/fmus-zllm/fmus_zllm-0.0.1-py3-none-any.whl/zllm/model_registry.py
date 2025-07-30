"""
Model Registry for ZLLM.

This module provides a registry for managing model configurations.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Set up logging
logger = logging.getLogger(__name__)


class ModelRegistry:
    """
    Registry for managing model configurations.

    This class loads model configurations from a JSON file and provides
    methods for accessing and updating them.
    """

    # DEFAULT_CONFIG_PATH = "~/LLM_MODELS.json"
    DEFAULT_CONFIG_PATH = r'C:\projects\fmustools-rework\zsido\zllm\LLM_MODELS.json'

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the model registry.

        Args:
            config_path: Path to the configuration file (defaults to ~/LLM_MODELS.json)
        """
        self.config_path = Path(config_path or self.DEFAULT_CONFIG_PATH).expanduser()
        logger.info(f"Initializing ModelRegistry with config path: {self.config_path}")
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """
        Load the configuration from the JSON file.

        If the file doesn't exist, create it with default settings.

        Returns:
            Configuration dictionary
        """
        logger.info(f"Loading model registry configuration from: {self.config_path}")
        if not self.config_path.exists():
            logger.warning(f"Configuration file not found at {self.config_path}, creating default")
            # Create default configuration
            default_config = self._create_default_config()
            self._save_config(default_config)
            return default_config

        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                config = json.load(f)
                logger.info(f"Successfully loaded configuration with {len(config.get('providers', {}))} providers")
                # Log available providers
                providers = config.get("providers", {}).keys()
                logger.info(f"Available providers in config: {', '.join(providers)}")
                return config
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading model configuration: {str(e)}")
            # Create and return default configuration
            default_config = self._create_default_config()
            self._save_config(default_config)
            return default_config

    def _create_default_config(self) -> Dict[str, Any]:
        """
        Create a default configuration.

        Returns:
            Default configuration dictionary
        """
        return {
            "providers": {
                "openai": {
                    "text_models": [
                        {
                            "id": "gpt-4o",
                            "context_length": 128000,
                            "default": False
                        },
                        {
                            "id": "gpt-4o-mini",
                            "context_length": 128000,
                            "default": False
                        },
                        {
                            "id": "gpt-4-turbo",
                            "context_length": 128000,
                            "default": False
                        },
                        {
                            "id": "gpt-4",
                            "context_length": 8192,
                            "default": False
                        },
                        {
                            "id": "gpt-3.5-turbo",
                            "context_length": 16385,
                            "default": True
                        },
                        {
                            "id": "gpt-3.5-turbo-16k",
                            "context_length": 16385,
                            "default": False
                        }
                    ],
                    "vision_models": [
                        {
                            "id": "gpt-4-vision-preview",
                            "context_length": 128000,
                            "default": True
                        },
                        {
                            "id": "gpt-4o",
                            "context_length": 128000,
                            "default": False
                        }
                    ],
                    "image_models": [
                        {
                            "id": "dall-e-3",
                            "name": "DALL-E 3",
                            "default": True
                        },
                        {
                            "id": "dall-e-2",
                            "name": "DALL-E 2",
                            "default": False
                        }
                    ],
                    "embedding_models": [
                        {
                            "id": "text-embedding-ada-002",
                            "default": True
                        },
                        {
                            "id": "text-embedding-3-small",
                            "default": False
                        },
                        {
                            "id": "text-embedding-3-large",
                            "default": False
                        }
                    ]
                },
                "groq": {
                    "text_models": [
                        {
                            "id": "llama-3-70b-8192",
                            "context_length": 8192,
                            "default": True
                        },
                        {
                            "id": "llama-3-8b-8192",
                            "context_length": 8192,
                            "default": False
                        },
                        {
                            "id": "mixtral-8x7b-32768",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "gemma-7b-it",
                            "context_length": 8192,
                            "default": False
                        }
                    ]
                },
                "anthropic": {
                    "text_models": [
                        {
                            "id": "claude-3-opus-20240229",
                            "context_length": 200000,
                            "default": False
                        },
                        {
                            "id": "claude-3-sonnet-20240229",
                            "context_length": 200000,
                            "default": True
                        },
                        {
                            "id": "claude-3-haiku-20240307",
                            "context_length": 200000,
                            "default": False
                        },
                        {
                            "id": "claude-2.1",
                            "context_length": 100000,
                            "default": False
                        },
                        {
                            "id": "claude-2.0",
                            "context_length": 100000,
                            "default": False
                        },
                        {
                            "id": "claude-instant-1.2",
                            "context_length": 100000,
                            "default": False
                        }
                    ],
                    "vision_models": [
                        {
                            "id": "claude-3-opus-20240229",
                            "context_length": 200000,
                            "default": True
                        },
                        {
                            "id": "claude-3-sonnet-20240229",
                            "context_length": 200000,
                            "default": False
                        },
                        {
                            "id": "claude-3-haiku-20240307",
                            "context_length": 200000,
                            "default": False
                        }
                    ]
                },
                "gemini": {
                    "text_models": [
                        {
                            "id": "gemini-2.0-flash",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "gemini-1.5-flash-latest",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "gemini-2.0-flash-exp",
                            "context_length": 32768,
                            "default": True
                        },
                        {
                            "id": "gemini-2.0-flash-thinking-exp-1219",
                            "context_length": 32768,
                            "default": False
                        }
                    ],
                    "vision_models": [
                        {
                            "id": "gemini-2.0-flash",
                            "context_length": 32768,
                            "default": True
                        },
                        {
                            "id": "gemini-1.5-flash-latest",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "gemini-2.0-flash-exp",
                            "context_length": 32768,
                            "default": False
                        }
                    ],
                    "image_models": [
                        {"id": "imagegeneration@006", "name": "Imagen", "default": True}
                    ],
                    "embedding_models": [
                        {"id": "embedding-001", "name": "Embedding 001", "dimensions": 768, "default": True}
                    ]
                },
                "cohere": {
                    "text_models": [
                        {
                            "id": "command-r-plus",
                            "context_length": 128000,
                            "default": True
                        },
                        {
                            "id": "command-r",
                            "context_length": 128000,
                            "default": False
                        },
                        {
                            "id": "command-light",
                            "context_length": 4096,
                            "default": False
                        }
                    ],
                    "embedding_models": [
                        {
                            "id": "embed-english-v3.0",
                            "default": True
                        },
                        {
                            "id": "embed-multilingual-v3.0",
                            "default": False
                        }
                    ]
                },
                "huggingface": {
                    "text_models": [
                        {
                            "id": "meta-llama/Llama-2-70b-chat-hf",
                            "context_length": 4096,
                            "default": False
                        },
                        {
                            "id": "mistralai/Mistral-7B-Instruct-v0.2",
                            "context_length": 8192,
                            "default": True
                        },
                        {
                            "id": "microsoft/phi-2",
                            "context_length": 2048,
                            "default": False
                        },
                        {
                            "id": "tiiuae/falcon-40b-instruct",
                            "context_length": 2048,
                            "default": False
                        },
                        {
                            "id": "google/gemma-7b-it",
                            "context_length": 8192,
                            "default": False
                        }
                    ],
                    "image_models": [
                        {"id": "stabilityai/stable-diffusion-xl-base-1.0", "name": "Stable Diffusion XL", "default": True},
                        {"id": "runwayml/stable-diffusion-v1-5", "name": "Stable Diffusion v1.5", "default": False}
                    ],
                    "embedding_models": [
                        {"id": "sentence-transformers/all-mpnet-base-v2", "name": "MPNet Base v2", "dimensions": 768, "default": True},
                        {"id": "sentence-transformers/all-MiniLM-L6-v2", "name": "MiniLM L6 v2", "dimensions": 384, "default": False}
                    ]
                },
                "cerebras": {
                    "text_models": [
                        {"id": "llama3.1-8b", "name": "Llama 3.1 8B", "context_length": 8192, "default": True},
                        {"id": "llama3.1-70b", "name": "Llama 3.1 70B", "context_length": 8192, "default": False},
                        {"id": "llama-3.3-70b", "name": "Llama 3.3 70B", "context_length": 8192, "default": False}
                    ]
                },
                "sambanova": {
                    "text_models": [
                        {"id": "sambanova-7b", "name": "SambaNova 7B", "context_length": 8192, "default": False},
                        {"id": "sambanova-13b", "name": "SambaNova 13B", "context_length": 8192, "default": True},
                        {"id": "sambanova-70b", "name": "SambaNova 70B", "context_length": 8192, "default": False}
                    ]
                },
                "glhf": {
                    "text_models": [
                        {"id": "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO", "name": "Nous Hermes 2 Mixtral", "context_length": 32768, "default": True}
                    ]
                },
                "hyperbolic": {
                    "text_models": [
                        {"id": "meta-llama/Llama-3.3-70B-Instruct", "name": "Llama 3.3 70B Instruct", "context_length": 8192, "default": True}
                    ]
                },
                "together": {
                    "text_models": [
                        {
                            "id": "togethercomputer/llama-2-7b-chat",
                            "context_length": 4096,
                            "default": False
                        },
                        {
                            "id": "togethercomputer/llama-2-13b-chat",
                            "context_length": 4096,
                            "default": False
                        },
                        {
                            "id": "togethercomputer/llama-2-70b-chat",
                            "context_length": 4096,
                            "default": True
                        },
                        {
                            "id": "mistralai/Mistral-7B-Instruct-v0.1",
                            "context_length": 8192,
                            "default": False
                        },
                        {
                            "id": "mistralai/Mistral-7B-Instruct-v0.2",
                            "context_length": 8192,
                            "default": False
                        },
                        {
                            "id": "mistralai/Mixtral-8x7B-Instruct-v0.1",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "meta-llama/Llama-2-70b-chat-hf",
                            "context_length": 4096,
                            "default": False
                        },
                        {
                            "id": "meta-llama/Llama-2-13b-chat-hf",
                            "context_length": 4096,
                            "default": False
                        },
                        {
                            "id": "meta-llama/Llama-2-7b-chat-hf",
                            "context_length": 4096,
                            "default": False
                        },
                        {
                            "id": "google/gemma-7b-it",
                            "context_length": 8192,
                            "default": False
                        },
                        {
                            "id": "google/gemma-2b-it",
                            "context_length": 8192,
                            "default": False
                        },
                        {
                            "id": "Qwen/Qwen1.5-72B-Chat",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "Qwen/Qwen1.5-14B-Chat",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "Qwen/Qwen1.5-7B-Chat",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "Qwen/Qwen1.5-4B-Chat",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "NousResearch/Nous-Hermes-2-Yi-34B",
                            "context_length": 4096,
                            "default": False
                        },
                        {
                            "id": "NousResearch/Nous-Hermes-2-Mixtral-8x7B-DPO",
                            "context_length": 32768,
                            "default": False
                        },
                        {
                            "id": "openchat/openchat-3.5-1210",
                            "context_length": 8192,
                            "default": False
                        }
                    ],
                    "image_models": [
                        {
                            "id": "black-forest-labs/FLUX.1-schnell",
                            "name": "FLUX.1-schnell",
                            "default": True
                        },
                        {
                            "id": "stabilityai/stable-diffusion-xl-base-1.0",
                            "name": "Stable Diffusion XL",
                            "default": False
                        }
                    ]
                }
            },
            "defaults": {
                "provider": "openai",
                "text_model": "gpt-3.5-turbo"
            }
        }

    def _save_config(self, config: Dict[str, Any]) -> None:
        """
        Save the configuration to the JSON file.

        Args:
            config: Configuration dictionary
        """
        try:
            # Ensure the directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2)
        except IOError as e:
            print(f"Error saving model configuration: {str(e)}")

    def save(self) -> None:
        """Save the current configuration to the JSON file."""
        self._save_config(self.config)

    def get_providers(self) -> List[str]:
        """
        Get a list of all configured providers.

        Returns:
            List of provider names
        """
        return list(self.config.get("providers", {}).keys())

    def get_default_provider(self) -> str:
        """
        Get the default provider.

        Returns:
            Default provider name
        """
        return self.config.get("defaults", {}).get("provider", "groq")

    def set_default_provider(self, provider: str) -> None:
        """
        Set the default provider.

        Args:
            provider: Provider name
        """
        if "defaults" not in self.config:
            self.config["defaults"] = {}
        self.config["defaults"]["provider"] = provider

    def get_models(self, provider: str, model_type: str = "text_models") -> List[Dict[str, Any]]:
        """
        Get models for a specific provider and type.

        Args:
            provider: Provider name
            model_type: Type of models to get (text_models, vision_models, etc.)

        Returns:
            List of model configurations
        """
        logger.debug(f"Getting {model_type} for provider: {provider}")
        provider_config = self.config.get("providers", {}).get(provider, {})
        logger.debug(f"Provider config keys: {list(provider_config.keys())}")
        models = provider_config.get(model_type, [])
        logger.debug(f"Found {len(models)} {model_type} for provider {provider}")
        return models

    def get_default_model(self, provider: str, model_type: str = "text_models") -> Optional[str]:
        """
        Get the default model for a provider and type.

        Args:
            provider: Provider name
            model_type: Type of models to get (text_models, vision_models, etc.)

        Returns:
            Default model ID or None if not found
        """
        models = self.get_models(provider, model_type)

        # First try to find a model marked as default
        for model in models:
            if model.get("default", False):
                return model.get("id")

        # If no default is marked, return the first model
        if models:
            return models[0].get("id")

        # If provider has no models of this type, check global defaults
        if model_type == "text_models":
            return self.config.get("defaults", {}).get("text_model")

        return None

    def supports_capability(self, provider: str, capability: str) -> bool:
        """
        Check if a provider supports a specific capability.

        Args:
            provider: Provider name
            capability: Capability to check (vision, image_generation, etc.)

        Returns:
            True if the capability is supported, False otherwise
        """
        capability_model_map = {
            "vision": "vision_models",
            "image_generation": "image_models",
            "embeddings": "embedding_models",
            "text": "text_models",
            "audio": "audio_models",
            "reasoning": "reasoning_models"
        }

        model_type = capability_model_map.get(capability)
        if not model_type:
            return False

        return len(self.get_models(provider, model_type)) > 0

    def add_model(self, provider: str, model_type: str, model_config: Dict[str, Any]) -> None:
        """
        Add a new model configuration.

        Args:
            provider: Provider name
            model_type: Type of model (text_models, vision_models, etc.)
            model_config: Model configuration
        """
        if "providers" not in self.config:
            self.config["providers"] = {}

        if provider not in self.config["providers"]:
            self.config["providers"][provider] = {}

        if model_type not in self.config["providers"][provider]:
            self.config["providers"][provider][model_type] = []

        # Check if model already exists
        for i, model in enumerate(self.config["providers"][provider][model_type]):
            if model.get("id") == model_config.get("id"):
                # Update existing model
                self.config["providers"][provider][model_type][i] = model_config
                return

        # Add new model
        self.config["providers"][provider][model_type].append(model_config)

    def remove_model(self, provider: str, model_type: str, model_id: str) -> bool:
        """
        Remove a model configuration.

        Args:
            provider: Provider name
            model_type: Type of model (text_models, vision_models, etc.)
            model_id: Model ID

        Returns:
            True if the model was removed, False otherwise
        """
        if (provider not in self.config.get("providers", {}) or
                model_type not in self.config["providers"][provider]):
            return False

        models = self.config["providers"][provider][model_type]
        for i, model in enumerate(models):
            if model.get("id") == model_id:
                del self.config["providers"][provider][model_type][i]
                return True

        return False

    def get_model_by_id(self, provider: str, model_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a model configuration by its ID.

        Args:
            provider: Provider name
            model_id: Model ID

        Returns:
            Model configuration or None if not found
        """
        provider_config = self.config.get("providers", {}).get(provider, {})

        for model_type in provider_config:
            for model in provider_config[model_type]:
                if model.get("id") == model_id:
                    return model

        return None

    def update(self) -> None:
        """
        Update the configuration from the file.

        This is useful when the file has been modified externally.
        """
        self.config = self._load_config()

    def get_models_for_provider(self, provider: str) -> List[str]:
        """
        Get a list of model identifiers for a specific provider.

        Args:
            provider: Provider name

        Returns:
            List of model IDs
        """
        models = self.get_models(provider, "text_models")
        return [model.get("id") for model in models]


# Create a singleton instance
_instance = None

def get_registry(config_path: Optional[str] = None) -> ModelRegistry:
    """
    Get the model registry instance.

    Args:
        config_path: Path to the configuration file (defaults to ~/LLM_MODELS.json)

    Returns:
        ModelRegistry instance
    """
    global _instance
    if _instance is None:
        _instance = ModelRegistry(config_path)
    return _instance
