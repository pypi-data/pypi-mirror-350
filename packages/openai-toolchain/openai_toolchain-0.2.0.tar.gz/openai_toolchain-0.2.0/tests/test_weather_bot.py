"""Integration tests for the weather bot example with real API calls.

This module contains integration tests for the weather bot example that make actual
API calls to the OpenAI API. These tests verify that the tool registration and
function calling functionality works as expected with the real API.
"""

import logging
import os
import sys
from typing import Any, Dict, List, Optional

import pytest

# Add the project root to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openai_toolchain.client import OpenAIClient

# Set up logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

# Skip if we don't have the required environment variables
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set",
)


# Define our test tools
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location.

    Args:
        location: The location to get weather for
        unit: The temperature unit to use (celsius or fahrenheit)

    Returns:
        str: A string describing the current weather
    """
    return f"The weather in {location} is 22 degrees {unit} and sunny."


def get_forecast(location: str, days: int = 1) -> str:
    """Get a weather forecast for a location.

    Args:
        location: The location to get the forecast for
        days: Number of days to forecast

    Returns:
        str: A string describing the forecast
    """
    return f"The forecast for {location} for the next {days} days is sunny."


def print_message(
    role: str,
    content: str,
    tool_calls: Optional[List[Dict[str, Any]]] = None,
) -> None:
    """Print a formatted message with role and content.

    Args:
        role: The role of the message sender (user, assistant, etc.)
        content: The content of the message
        tool_calls: Optional list of tool calls associated with the message
    """
    print(f"{role.upper()}: {content}")

    if tool_calls:
        print("  Tool calls:")
        for call in tool_calls:
            if hasattr(call, "function") and hasattr(call.function, "name"):
                print(
                    f"  - {call.function.name}: {getattr(call.function, 'arguments', '')}",
                )

    print("=" * 80)


def test_weather_bot_integration(tool_registry: Any) -> None:
    """Test the weather bot with the real API using OpenAIClient.

    Args:
        tool_registry: The tool registry instance to use for testing
    """
    # Skip if no API key is set
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No OPENAI_API_KEY set, skipping integration test")

    # Register the tools
    tool_registry.register(get_weather)
    tool_registry.register(get_forecast)

    # Create a client
    client = OpenAIClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        default_model="POP.qwen3:30b",
        base_url=os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    )

    # Print registered tools for debugging
    print("\n" + "#" * 40 + " REGISTERED TOOLS " + "#" * 40)
    print("\nTool registry contents:")
    for _name, tool_info in tool_registry._tools.items():
        print("#" * 80)
        print(f"Tool: {_name}")
        print("Type:", type(tool_info).__name__)
        if hasattr(tool_info, "keys"):
            print("Keys:", list(tool_info.keys()))
        if "function" in tool_info:
            func = tool_info["function"]
            func_name = func.__name__ if callable(func) else str(func)
            print(f"Function: {func_name}")
        if "schema" in tool_info:
            print(f"Schema: {tool_info['schema']}")
    print("#" * 80 + "\n")

    # Test 1: Simple weather query
    print("\n" + "=" * 40 + " TEST 1: SIMPLE WEATHER QUERY " + "=" * 40)
    user_message = "What's the weather like in Toronto?"
    print_message("User", user_message)

    response = client.chat_with_tools(
        messages=[{"role": "user", "content": user_message}],
        max_tool_calls=5,
    )

    print_message("Assistant", response)

    # Verify the response includes the expected weather information
    assert response is not None
    assert "22" in response  # Should include the temperature from our mock
    assert "Toronto" in response

    # Test 2: Complex query using multiple tools
    print("\n" + "=" * 40 + " TEST 2: COMPLEX QUERY " + "=" * 40)
    user_message = (
        "What's the weather like in Toronto and what's the forecast for tomorrow?"
    )
    print_message("User", user_message)

    response = client.chat_with_tools(
        messages=[{"role": "user", "content": user_message}],
        max_tool_calls=5,
    )

    print_message("Assistant", response)

    # Verify we got a response that includes both current weather and forecast
    assert response is not None
    assert "22" in response  # Current temp
    assert "forecast" in response.lower()
