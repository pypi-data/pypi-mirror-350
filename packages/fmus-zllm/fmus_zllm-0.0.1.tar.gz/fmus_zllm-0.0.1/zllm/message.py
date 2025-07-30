"""
Message module for ZLLM.

This module defines the LLMMessage class used for representing messages in conversations.
"""

from typing import Dict, Any, List, Optional, Union
from enum import Enum


class MessageRole(str, Enum):
    """Enum for message roles."""
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

# Constants for easy access
USER = MessageRole.USER
SYSTEM = MessageRole.SYSTEM
ASSISTANT = MessageRole.ASSISTANT
FUNCTION = MessageRole.FUNCTION

class LLMMessage:
    """
    Represents a message in a conversation with an LLM.

    Attributes:
        role: The role of the message sender (system, user, assistant, function)
        content: The content of the message
        name: Optional name for the sender (used for function messages)
        function_call: Optional function call information
    """

    def __init__(
        self,
        role: Union[str, MessageRole],
        content: str,
        name: Optional[str] = None,
        function_call: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize a new message.

        Args:
            role: The role of the message sender
            content: The content of the message
            name: Optional name for the sender
            function_call: Optional function call information
        """
        # Convert string role to enum if needed
        if isinstance(role, str):
            try:
                self.role = MessageRole(role.lower())
            except ValueError:
                raise ValueError(f"Invalid role: {role}")
        else:
            self.role = role

        self.content = content
        self.name = name
        self.function_call = function_call

    @classmethod
    def system(cls, content: str) -> 'LLMMessage':
        """
        Create a system message.

        Args:
            content: The content of the message

        Returns:
            A new LLMMessage with role=system
        """
        return cls(MessageRole.SYSTEM, content)

    @classmethod
    def user(cls, content: str) -> 'LLMMessage':
        """
        Create a user message.

        Args:
            content: The content of the message

        Returns:
            A new LLMMessage with role=user
        """
        return cls(MessageRole.USER, content)

    @classmethod
    def assistant(cls, content: str, function_call: Optional[Dict[str, Any]] = None) -> 'LLMMessage':
        """
        Create an assistant message.

        Args:
            content: The content of the message
            function_call: Optional function call information

        Returns:
            A new LLMMessage with role=assistant
        """
        return cls(MessageRole.ASSISTANT, content, function_call=function_call)

    @classmethod
    def function(cls, content: str, name: str) -> 'LLMMessage':
        """
        Create a function message.

        Args:
            content: The content of the message (function result)
            name: The name of the function

        Returns:
            A new LLMMessage with role=function
        """
        return cls(MessageRole.FUNCTION, content, name=name)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the message to a dictionary.

        Returns:
            Dictionary representation of the message
        """
        result = {
            "role": self.role.value,
            "content": self.content
        }

        if self.name:
            result["name"] = self.name

        if self.function_call:
            result["function_call"] = self.function_call

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'LLMMessage':
        """
        Create a message from a dictionary.

        Args:
            data: Dictionary representation of the message

        Returns:
            A new LLMMessage
        """
        return cls(
            role=data["role"],
            content=data.get("content", ""),
            name=data.get("name"),
            function_call=data.get("function_call")
        )

    def __repr__(self) -> str:
        """Get string representation of the message."""
        return f"LLMMessage(role={self.role.value}, content={self.content!r})"
