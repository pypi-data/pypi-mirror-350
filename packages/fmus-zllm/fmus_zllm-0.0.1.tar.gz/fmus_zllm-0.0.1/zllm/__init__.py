"""
ZLLM - Zero-dependency LLM API Client

A simple, unified interface for interacting with various LLM providers.
"""

__version__ = "0.2.0"

from zllm.client import LLMClient
from zllm.message import LLMMessage

__all__ = ["LLMClient", "LLMMessage"]
