# Async Usage Example

This example shows how to use OpenAI Toolchain with async/await.

```python
import asyncio
from openai_toolchain import tool, AsyncOpenAIClient

@tool
async def fetch_data(url: str) -> str:
    """Fetch data from a URL asynchronously."""
    import aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.text()

async def main():
    # Initialize the async client
    client = AsyncOpenAIClient(api_key="your-api-key")

    # Use the client
    response = await client.chat_with_tools(
        messages=[{"role": "user", "content": "Fetch the homepage of example.com"}]
    )
    print(response)

# Run the async function
asyncio.run(main())
```

## Key Points

- Use `AsyncOpenAIClient` instead of `OpenAIClient` for async operations
- Define async tool functions with `async def`
- Use `await` when calling async methods
- Run the async code using `asyncio.run()`

## Error Handling

Make sure to handle potential errors in your async operations:

```python
try:
    response = await client.chat_with_tools(messages=messages)
except Exception as e:
    print(f"An error occurred: {e}")
```
