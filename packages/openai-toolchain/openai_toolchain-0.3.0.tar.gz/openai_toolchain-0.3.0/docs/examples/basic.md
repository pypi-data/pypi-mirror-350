# Basic Usage Example

This example shows the basic usage of OpenAI Toolchain.

```python
from openai_toolchain import tool, OpenAIClient

@tool
def get_weather(location: str, unit: str = "celsius") -> str:
    """Get the current weather in a given location."""
    return f"The weather in {location} is 22 {unit}"

# Initialize the client
client = OpenAIClient(api_key="your-api-key")

# Use the client
response = client.chat_with_tools(
    messages=[{"role": "user", "content": "What's the weather in Toronto?"}]
)
print(response)
```

## Explanation

1. We import the necessary components from the library
2. We define a tool using the `@tool` decorator
3. We initialize the client with our API key
4. We use the client to send a message and get a response

The tool will automatically be registered and available for use with the OpenAI
API.
