import enum
import logging
import os
import sys
from typing import Any

import pytest
from pydantic import BaseModel

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from openai_toolchain import OpenAIClient

# Set up logging
_logger = logging.getLogger(__name__)
client_logger = logging.getLogger("openai_toolchain.client")
client_logger.setLevel(logging.DEBUG)

# Skip if we don't have the required environment variables
pytestmark = pytest.mark.skipif(
    not os.getenv("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY environment variable not set",
)

# Define our test tools


class TemperatureUnit(str, enum.Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class WeatherDatabase(BaseModel):
    temperature: int
    unit: TemperatureUnit

    def get_weather(
        self, location: str, unit: TemperatureUnit = TemperatureUnit.CELSIUS
    ) -> str:
        return (
            f"The weather in {location} is {self.temperature} degrees {unit} and sunny."
        )


class WeatherBot:
    def get_weather(
        self,
        weather_db: WeatherDatabase,
        location: str,
        unit: str = "celsius",
    ) -> str:
        """
        Get the current weather in a given location.

        :param weather_db: The weather database to use
        :param location: The location to get weather for
        :param unit: The temperature unit to use (celsius or fahrenheit)
        :return: A string describing the current weather
        """
        return weather_db.get_weather(location, unit)


def test_non_api_params(tool_registry: Any) -> None:
    """Test the weather bot with the real API using OpenAIClient."""
    # Skip if no API key is set
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("No OPENAI_API_KEY set, skipping integration test")

    weather_bot = WeatherBot()
    # Register the tools
    tool_registry.register(
        weather_bot.get_weather,
        non_ai_params=["weather_db"],
    )

    # Create a client
    client = OpenAIClient(
        api_key=os.getenv("OPENAI_API_KEY"),
        default_model="POP.qwen3:30b",
        base_url=os.getenv("OPENAI_BASE_URL"),
    )

    # Create a weather database
    weather_db = WeatherDatabase(temperature=28, unit=TemperatureUnit.CELSIUS)

    # Test the weather bot
    response = client.chat_with_tools(
        messages=[{"role": "user", "content": "What's the weather like in Toronto?"}],
        tools=["get_weather"],
        tool_params={
            "get_weather": {
                "weather_db": weather_db,
            }
        },
        max_tool_calls=10,
    )

    assert response is not None
    assert "28" in response
    assert "Toronto" in response
