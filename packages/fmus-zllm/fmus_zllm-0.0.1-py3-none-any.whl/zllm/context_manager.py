"""
Conversation context management for LLM interactions.

This module provides classes for managing conversation context with LLMs.
"""

import json
from typing import List, Dict, Any, Optional

from .base import LLMMessage


class ConversationContext:
    """
    Manages conversation context for LLM interactions.

    This class keeps track of messages in a conversation and provides methods
    for adding, retrieving, and managing messages.

    Attributes:
        max_context_bytes: Maximum size of the context in bytes
        messages: List of messages in the conversation
    """

    def __init__(self, max_context_bytes: int = 8192):
        """
        Initialize a new conversation context.

        Args:
            max_context_bytes: Maximum size of the context in bytes
        """
        self.max_context_bytes = max_context_bytes
        self.messages: List[LLMMessage] = []
        self._system_message: Optional[LLMMessage] = None

    def add_message(self, role: str, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Add a message to the conversation.

        Args:
            role: The role of the message sender (user, assistant, system)
            content: The content of the message
            metadata: Additional metadata for the message
        """
        # If this is a system message, store it separately
        if role.lower() == "system":
            self._system_message = LLMMessage(role, content, metadata)
            return

        # Add the message to the list
        self.messages.append(LLMMessage(role, content, metadata))

        # Trim the context if it exceeds the maximum size
        self._trim_context_if_needed()

    def set_system_message(self, content: str, metadata: Optional[Dict[str, Any]] = None) -> None:
        """
        Set the system message for the conversation.

        Args:
            content: The content of the system message
            metadata: Additional metadata for the message
        """
        self._system_message = LLMMessage("system", content, metadata)

    def get_messages(self) -> List[LLMMessage]:
        """
        Get all messages in the conversation.

        Returns:
            List of messages, including the system message if present
        """
        # Start with the system message if present
        result = []
        if self._system_message:
            result.append(self._system_message)

        # Add the rest of the messages
        result.extend(self.messages)
        return result

    def clear(self) -> None:
        """Clear all messages from the conversation."""
        self.messages = []
        self._system_message = None

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the conversation context to a dictionary.

        Returns:
            Dictionary representation of the conversation context
        """
        return {
            "max_context_bytes": self.max_context_bytes,
            "system_message": self._system_message.to_dict() if self._system_message else None,
            "messages": [msg.to_dict() for msg in self.messages]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConversationContext':
        """
        Create a conversation context from a dictionary.

        Args:
            data: Dictionary representation of the conversation context

        Returns:
            New ConversationContext instance
        """
        context = cls(max_context_bytes=data.get("max_context_bytes", 8192))

        # Load system message if present
        system_data = data.get("system_message")
        if system_data:
            context._system_message = LLMMessage.from_dict(system_data)

        # Load messages
        for msg_data in data.get("messages", []):
            msg = LLMMessage.from_dict(msg_data)
            context.messages.append(msg)

        return context

    def save_to_file(self, filepath: str) -> None:
        """
        Save the conversation context to a file.

        Args:
            filepath: Path to save the conversation context
        """
        with open(filepath, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load_from_file(cls, filepath: str) -> 'ConversationContext':
        """
        Load a conversation context from a file.

        Args:
            filepath: Path to load the conversation context from

        Returns:
            New ConversationContext instance
        """
        with open(filepath, 'r') as f:
            data = json.load(f)
        return cls.from_dict(data)

    def _trim_context_if_needed(self) -> None:
        """
        Trim the context if it exceeds the maximum size.

        This method removes the oldest messages until the context size
        is below the maximum.
        """
        # Calculate current size
        current_size = sum(len(msg.content.encode('utf-8')) for msg in self.messages)

        # Add system message size if present
        if self._system_message:
            current_size += len(self._system_message.content.encode('utf-8'))

        # If size is within limit, do nothing
        if current_size <= self.max_context_bytes:
            return

        # Remove oldest messages until size is within limit
        while current_size > self.max_context_bytes and self.messages:
            # Remove oldest message (but never the system message)
            oldest = self.messages.pop(0)
            current_size -= len(oldest.content.encode('utf-8'))
