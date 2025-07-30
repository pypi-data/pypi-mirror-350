# Advanced Features

## Custom Tool Naming

You can specify a custom name for your tool:

```python
from openai_toolchain import tool

@tool("get_current_time")
def get_time(timezone: str = "UTC") -> str:
    """Get the current time in the specified timezone."""
    from datetime import datetime
    import pytz
    tz = pytz.timezone(timezone)
    return datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S %Z")
```

## Tool Dependencies

Tools can depend on other tools or external libraries:

```python
from openai_toolchain import tool

@tool
def analyze_weather(location: str) -> dict:
    """Analyze weather patterns for a location."""
    # This is a mock implementation
    return {
        "location": location,
        "temperature": 22,
        "conditions": "sunny",
        "forecast": ["sunny", "partly_cloudy", "rain"]
    }

@tool
def suggest_activity(location: str) -> str:
    """Suggest an activity based on weather."""
    weather = analyze_weather(location)
    if weather["conditions"] == "sunny":
        return f"It's sunny in {location}! Perfect for a walk in the park."
    elif weather["conditions"] == "rain":
        return f"It's raining in {location}. How about visiting a museum?"
    return f"Weather in {location} is {weather['conditions']}. Good day to stay in and code!"
```

## Error Handling in Tools

Handle errors gracefully in your tools:

```python
from openai_toolchain import tool

@tool
def divide_numbers(a: float, b: float) -> float:
    """Divide two numbers."""
    try:
        return a / b
    except ZeroDivisionError:
        raise ValueError("Cannot divide by zero")
    except Exception as e:
        raise ValueError(f"An error occurred: {str(e)}")
```

## Using External APIs

Example of a tool that calls an external API:

```python
import requests
from openai_toolchain import tool

@tool
def get_github_user(username: str) -> dict:
    """Get GitHub user information."""
    response = requests.get(f"https://api.github.com/users/{username}")
    response.raise_for_status()
    return response.json()
```

## Using Non-AI Parameters

You can mark certain parameters as non-AI parameters, which means they will be provided by the system rather than the AI. This is useful for passing in dependencies like database connections, configuration, or other runtime objects.

```python
from openai_toolchain import tool, OpenAIClient

class Database:
    def query(self, query: str) -> str:
        # Mock database query
        return f"Results for: {query}"

@tool(non_ai_params=["db"])
def search_database(query: str, db: Database) -> str:
    """Search the database for information.
    
    Args:
        query: The search query
        db: Database connection (handled by the system, not AI)
    """
    return db.query(query)

# Initialize client and dependencies
client = OpenAIClient(api_key="your-api-key")
db = Database()

# Call with non-AI parameters
response = client.chat_with_tools(
    messages=[{"role": "user", "content": "Find information about Python"}],
    tools=["search_database"],
    tool_params={
        "search_database": {
            "db": db  # Pass the database connection
        }
    }
)
```

## Testing Your Tools

Here's how you can test your tools:

```python
import pytest
from openai_toolchain import tool

@tool
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

def test_add_tool():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
    assert add(0, 0) == 0
```
