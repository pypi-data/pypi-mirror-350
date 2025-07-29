# Welcome to OpenAI Toolchain

A minimal and intuitive library for working with OpenAI's function calling API.

## Features

- 🛠️ Simple function registration with `@tool` decorator
- 🤖 Automatic tool schema generation
- 🔄 Seamless integration with OpenAI's API
- ⚡ Support for both sync and async operations
- 📚 Clean and intuitive API

## Quick Start

```python
from openai_toolchain import tool, OpenAIClient

@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location."""
    return f"The weather in {location} is 22 {unit}"

# Initialize the client with your API key
client = OpenAIClient(api_key="your-api-key")

# Use the client
response = client.chat_with_tools(
    messages=[{"role": "user", "content": "What's the weather in Toronto?"}]
)
print(response)
```

## Installation

```bash
pip install openai-toolchain
```

## Next Steps

- [Installation Guide](installation.md)
- [Tutorial](tutorial.md)
- [API Reference](reference/)

## License

This project is licensed under the MIT License - see the
[LICENSE](https://github.com/bemade/openai-toolchain/blob/main/LICENSE) file for
details.
