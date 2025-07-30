# Tutorial

This tutorial will guide you through using OpenAI Toolchain to create and manage
OpenAI function tools.

## Basic Usage

### 1. Import and Setup

```python
from openai_toolchain import tool, OpenAIClient

# Initialize the client
client = OpenAIClient(api_key="your-api-key")
```

### 2. Create a Tool

```python
@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location.

    Args:
        location: The city to get the weather for
        unit: The unit of temperature (celsius or fahrenheit)

    Returns:
        str: The current weather information
    """
    # In a real app, you would call a weather API here
    return f"The weather in {location} is 22 {unit}"
```

### 3. Use the Tool

```python
response = client.chat_with_tools(
    messages=[{"role": "user", "content": "What's the weather in Toronto?"}]
)
print(response)
```

## Advanced Features

### Async Support

```python
import asyncio
from openai_toolchain import AsyncOpenAIClient

async def main():
    client = AsyncOpenAIClient(api_key="your-api-key")
    response = await client.chat_with_tools(
        messages=[{"role": "user", "content": "What's the weather in Paris?"}]
    )
    print(response)

asyncio.run(main())
```

### Custom Tool Naming

```python
@tool("get_current_time")
def get_time(timezone: str = "UTC") -> str:
    """Get the current time in the specified timezone."""
    from datetime import datetime
    import pytz
    tz = pytz.timezone(timezone)
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
```

### Tool Dependencies

```python
@tool
def get_weather_with_deps(location: str) -> str:
    """Get weather with dependencies."""
    # You can use other tools or dependencies
    from some_weather_lib import get_weather as fetch_weather
    return fetch_weather(location)
```

## Using Non-AI Parameters

Non-AI parameters allow you to pass system-level dependencies (like database connections or configuration) to your tools without exposing them to the AI. Here's how to use them:

### 1. Define a Tool with Non-AI Parameters

```python
@tool(non_ai_params=["config"])
def get_config_value(key: str, config: dict) -> str:
    """Get a value from the configuration.

    Args:
        key: The configuration key to retrieve
        config: The configuration dictionary (handled by the system)
    """
    return config.get(key, "Key not found")
```

### 2. Use the Tool with Non-AI Parameters

```python
# System configuration
app_config = {
    "api_key": "secret-key-123",
    "environment": "production",
    "max_retries": 3
}

# Pass the configuration when calling the tool
response = client.chat_with_tools(
    messages=[{"role": "user", "content": "What's the API environment?"}],
    tools=["get_config_value"],
    tool_params={
        "get_config_value": {
            "config": app_config
        }
    }
)
```

### Benefits of Non-AI Parameters

- **Runtime Context**: Non-AI parameters allow you to pass system-level dependencies (like database connections or configuration) to your tools without exposing them to the AI.
- **Security**: Keep sensitive information out of AI prompts
- **Performance**: Avoid serializing/deserializing large objects
- **Control**: Maintain system-level control over certain parameters
- **Flexibility**: Easily swap implementations without changing tool logic

## Best Practices

1. **Document Your Tools**: Always include docstrings with clear parameter and
   return type information.
2. **Handle Errors**: Implement proper error handling in your tool functions.
3. **Type Hints**: Use Python type hints for better AI tool calling, IDE support
   and documentation.
4. **Testing**: Write tests for your tools to ensure they work as expected.
5. **Non-AI Parameters**: Use non-AI parameters for system dependencies and sensitive data.

## Next Steps

- Explore the [API Reference](reference/) for detailed documentation
- Check out more [examples](reference/examples/)
- Learn how to [contribute](contributing.md) to the project
