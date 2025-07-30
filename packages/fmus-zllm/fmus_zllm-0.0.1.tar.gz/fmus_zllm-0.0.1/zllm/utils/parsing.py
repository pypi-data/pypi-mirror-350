"""
Parsing utilities for LLM responses.

This module provides utilities for parsing structured data from LLM responses.
"""

import json
import re
from typing import Dict, Any, Optional, List, Union


def extract_json_from_text(text: str) -> Optional[str]:
    """
    Extract JSON from text that may contain non-JSON content.

    Args:
        text: Text that may contain JSON

    Returns:
        Extracted JSON string or None if no JSON is found
    """
    # Look for JSON between triple backticks
    json_pattern = r"```(?:json)?\s*([\s\S]*?)\s*```"
    matches = re.findall(json_pattern, text)

    if matches:
        return matches[0]

    # Look for content between curly braces
    brace_pattern = r"\{[\s\S]*\}"
    matches = re.findall(brace_pattern, text)

    if matches:
        return matches[0]

    # If no JSON-like structure is found, return None
    return None


def parse_json_response(text: str) -> Dict[str, Any]:
    """
    Parse JSON from an LLM response.

    Args:
        text: LLM response text that may contain JSON

    Returns:
        Parsed JSON as a dictionary

    Raises:
        json.JSONDecodeError: If the text cannot be parsed as JSON
    """
    # First, try to parse the entire text as JSON
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # If that fails, try to extract JSON from the text
    json_str = extract_json_from_text(text)

    if json_str:
        return json.loads(json_str)

    # If all extraction attempts fail, try once more with the original text
    # This will raise a JSONDecodeError if it fails
    return json.loads(text)


def extract_list_from_text(text: str) -> List[str]:
    """
    Extract a list of items from text.

    Args:
        text: Text containing a list (e.g., with bullet points or numbers)

    Returns:
        List of extracted items
    """
    # Look for bullet points, numbers, or other common list formats
    patterns = [
        r"•\s*(.*?)(?=(?:\n•|\n\n|\Z))",  # Bullet points
        r"[\*\-]\s*(.*?)(?=(?:\n[\*\-]|\n\n|\Z))",  # Asterisks or hyphens
        r"\d+\.\s*(.*?)(?=(?:\n\d+\.|\n\n|\Z))",  # Numbered lists
    ]

    for pattern in patterns:
        items = re.findall(pattern, text, re.MULTILINE)
        if items:
            return [item.strip() for item in items]

    # If no list format is detected, split by newlines and filter empty lines
    lines = [line.strip() for line in text.split('\n')]
    return [line for line in lines if line and not line.isspace()]


def extract_key_value_pairs(text: str) -> Dict[str, str]:
    """
    Extract key-value pairs from text.

    Args:
        text: Text containing key-value pairs (e.g., "Key: Value")

    Returns:
        Dictionary of extracted key-value pairs
    """
    # Look for patterns like "Key: Value" or "Key - Value"
    patterns = [
        r"^([^:\n]+):\s*(.+)$",  # Key: Value
        r"^([^-\n]+)\s*-\s*(.+)$",  # Key - Value
    ]

    result = {}
    lines = text.split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                key, value = match.groups()
                result[key.strip()] = value.strip()
                break

    return result
