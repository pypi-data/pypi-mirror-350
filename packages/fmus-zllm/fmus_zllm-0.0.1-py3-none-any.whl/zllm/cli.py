#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Command-line interface for ZLLM.

This module provides a command-line interface for interacting with LLMs using ZLLM.
"""

import argparse
import asyncio
import os
import sys
import json
from typing import Optional, Dict, Any

from zllm import LLMClient, LLMMessage
from zllm.providers import get_available_providers
from zllm.exceptions import ProviderError, ConfigurationError


def callback(chunk: str) -> None:
    """
    Handle streaming chunks.

    Args:
        chunk: Text chunk from the streaming response
    """
    print(chunk, end="", flush=True)


async def chat_mode(args: argparse.Namespace) -> None:
    """
    Run the CLI in interactive chat mode.

    Args:
        args: Command-line arguments
    """
    # Create client
    client_options = {
        "provider": args.provider,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens
    }

    if args.model:
        client_options["model"] = args.model

    try:
        client = LLMClient(**client_options)
    except (ProviderError, ConfigurationError) as e:
        print(f"Error initializing client: {str(e)}")
        return

    # Set system message
    if args.system:
        client.set_system_message(args.system)
    else:
        client.set_system_message(
            "You are a helpful, friendly assistant. Your responses are clear, "
            "concise, and accurate."
        )

    print(f"ZLLM Chat - Using {args.provider.upper()} provider")
    print("Type 'exit', 'quit', or press Ctrl+C to end the conversation")
    print("-" * 60)

    try:
        while True:
            # Get user input
            user_input = input("\nYou: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            # Create user message
            user_message = LLMMessage.user(user_input)

            # Generate response
            print("\nAssistant: ", end="")
            if args.streaming:
                await client.generate_response_streaming(
                    messages=[user_message],
                    callback=callback
                )
                print()
            else:
                response = await client.generate_response(user_message)
                print(response)

    except KeyboardInterrupt:
        print("\nExiting...")
    except EOFError:
        print("\nInput stream closed. Exiting...")
    except Exception as e:
        print(f"\nError: {str(e)}")

    print("\nConversation ended.")


async def single_query_mode(args: argparse.Namespace) -> None:
    """
    Run the CLI in single query mode.

    Args:
        args: Command-line arguments
    """
    # Create client
    client_options = {
        "provider": args.provider,
        "temperature": args.temperature,
        "max_tokens": args.max_tokens
    }

    if args.model:
        client_options["model"] = args.model

    try:
        client = LLMClient(**client_options)
    except (ProviderError, ConfigurationError) as e:
        print(f"Error initializing client: {str(e)}")
        return

    # Set system message
    if args.system:
        client.set_system_message(args.system)

    # Create user message
    user_message = LLMMessage.user(args.query)

    try:
        # Generate response
        if args.streaming:
            await client.generate_response_streaming(
                messages=[user_message],
                callback=callback
            )
            print()
        else:
            response = await client.generate_response(user_message)
            print(response)
    except Exception as e:
        print(f"Error: {str(e)}")


async def list_providers_mode(args: argparse.Namespace) -> None:
    """
    List available providers and models.

    Args:
        args: Command-line arguments
    """
    providers = get_available_providers()

    if not providers:
        print("No providers available.")
        return

    print("Available providers:")
    for provider_name in providers.keys():
        print(f"  - {provider_name}")

        # Try to get models for the provider
        try:
            client = LLMClient(provider=provider_name)
            models = client._provider.get_available_models()
            default_model = client._provider.get_default_model()

            print("    Models:")
            for model in models:
                if model == default_model:
                    print(f"      - {model} (default)")
                else:
                    print(f"      - {model}")
        except Exception:
            print("    Unable to retrieve models")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(
        description="ZLLM - Command-line interface for LLMs"
    )

    # Global options
    parser.add_argument(
        "--provider", "-p",
        default="groq",
        help="LLM provider to use (default: groq)"
    )
    parser.add_argument(
        "--model", "-m",
        help="Model to use (provider-specific)"
    )
    parser.add_argument(
        "--temperature", "-t",
        type=float,
        default=0.7,
        help="Temperature for generation (default: 0.7)"
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="Maximum tokens to generate (default: 1024)"
    )
    parser.add_argument(
        "--streaming", "-s",
        action="store_true",
        help="Enable streaming mode"
    )
    parser.add_argument(
        "--system",
        help="System message to use"
    )

    # Subcommands
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Chat mode
    chat_parser = subparsers.add_parser("chat", help="Interactive chat mode")

    # Query mode
    query_parser = subparsers.add_parser("query", help="Single query mode")
    query_parser.add_argument(
        "query",
        help="Query to send to the LLM"
    )

    # List providers mode
    list_parser = subparsers.add_parser("list", help="List available providers and models")

    return parser.parse_args()


def main() -> None:
    """Main entry point for the CLI."""
    args = parse_args()

    if args.command == "list":
        asyncio.run(list_providers_mode(args))
    elif args.command == "query":
        asyncio.run(single_query_mode(args))
    elif args.command == "chat" or not args.command:
        # Default to chat mode if no command is specified
        asyncio.run(chat_mode(args))
    else:
        print(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
