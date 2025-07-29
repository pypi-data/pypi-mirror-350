# OpenAI Toolchain

[![PyPI](https://img.shields.io/pypi/v/openai-toolchain.svg)](https://pypi.org/project/openai-toolchain/)
[![Python Version](https://img.shields.io/pypi/pyversions/openai-toolchain)](https://pypi.org/project/openai-toolchain/)
[![Tests](https://github.com/bemade/openai-toolchain/actions/workflows/test.yml/badge.svg)](https://github.com/bemade/openai-toolchain/actions/workflows/test.yml)
[![Documentation](https://github.com/bemade/openai-toolchain/actions/workflows/docs.yml/badge.svg)](https://github.com/bemade/openai-toolchain/actions/workflows/docs.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A Python library for working with OpenAI's function calling API, making it
easier to create and manage tools that can be used with OpenAI's chat models.

## Features

- 🛠️ Simple function registration with `@tool` decorator
- 🤖 Automatic tool schema generation
- 🔄 Seamless integration with OpenAI's API
- ⚡ Support for both sync and async operations
- 📚 Clean and intuitive API

## Installation

```bash
pip install openai-toolchain
```

## Quick Start

1. **Define your tools** using the `@tool` decorator:

```python
from openai_toolchain import tool, OpenAIClient

@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location.

    Args:
        location: The city to get the weather for
        unit: The unit of temperature (celsius or fahrenheit)
    """
    return f"The weather in {location} is 22 {unit}"

@tool("get_forecast")
def get_forecast_function(location: str, days: int = 1) -> str:
    """Get a weather forecast for a location.

    Args:
        location: The city to get the forecast for
        days: Number of days to forecast (1-5)
    """
    return f"{days}-day forecast for {location}: Sunny"
```

2. **Use the tools with OpenAI**:

```python
# Initialize the client with your API key
client = OpenAIClient(api_key="your-api-key")

# Use the client
response = client.chat_with_tools(
    messages=[{"role": "user", "content": "What's the weather in Toronto?"}]
)
print(response)
```

## Documentation

For detailed documentation, including API reference and examples, please visit:

📚 [Documentation](https://github.com/bemade/openai-toolchain#readme)

Or run the documentation locally:

```bash
pip install -e ".[docs]"
mkdocs serve
```

## Contributing

Contributions are welcome! Please see our [Contributing Guide](CONTRIBUTING.md)
for details.

### Pre-commit Hooks

This project uses pre-commit to ensure code quality and style consistency. To
set it up:

1. Install pre-commit:

   ```bash
   pip install pre-commit
   ```

2. Install the git hook scripts:

   ```bash
   pre-commit install
   ```

3. (Optional) Run against all files:
   ```bash
   pre-commit run --all-files
   ```

The hooks will now run automatically on every commit. To skip the pre-commit
checks, use:

```bash
git commit --no-verify -m "Your commit message"
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file
for details.

# Initialize the client with your API key

client = OpenAIClient(api_key="your-api-key")

# Chat with automatic tool calling

response = client.chat_with_tools( messages=[{"role": "user", "content": "What's
the weather in Toronto?"}], tools=["get_weather"] # Optional: specify which
tools to use )

print(response)

````

## Features

### 1. Tool Registration

Use the `@tool` decorator to register functions as tools:

```python
from openai_toolchain import tool

@tool
def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"
````

### 2. Chat with Automatic Tool Calling

The `chat_with_tools` method handles tool calls automatically:

```python
client = OpenAIClient(api_key="your-api-key")

response = client.chat_with_tools(
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Search for the latest Python news"}
    ],
    tools=["search_web"],
    model="gpt-4"  # Optional: specify a different model
)
```

### 3. Accessing Registered Tools

You can access registered tools directly:

```python
from openai_toolchain import tool_registry

# Get all registered tools
tools = tool_registry.get_openai_tools()

# Call a tool directly
result = tool_registry.call_tool("get_weather", {"location": "Paris", "unit": "fahrenheit"})
```

## API Reference

### `@tool` decorator

Register a function as a tool:

```python
from openai_toolchain import tool

@tool
def my_function(param: str) -> str:
    """Function documentation."""
    return f"Result for {param}"
```

### `tool_registry`

The global registry instance with these methods:

- `register(func, **kwargs)`: Register a function as a tool
- `get_tool(name)`: Get a registered tool by name
- `call_tool(name, arguments)`: Call a registered tool by name with arguments
- `get_openai_tools()`: Get all tools in OpenAI format

## Development

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT
