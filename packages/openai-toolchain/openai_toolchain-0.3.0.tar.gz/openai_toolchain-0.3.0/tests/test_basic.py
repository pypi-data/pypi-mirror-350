"""Basic tests for the OpenAI Toolchain."""

import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Now we can import from the package directly
from openai_toolchain import ToolError, tool, tool_registry


def test_register_and_call_tool():
    """Test registering and calling a tool."""
    # Clear any existing tools
    tool_registry._tools = {}

    # Register a test tool
    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    # Get the tool info
    tool_info = tool_registry.get_tool("add")
    assert tool_info is not None

    # Call via the registry
    result = tool_registry.call_tool("add", {"a": 2, "b": 3})
    assert result == 5

    # Test with invalid args
    try:
        tool_registry.call_tool("add", {"a": 2})  # Missing 'b'
        raise AssertionError("Should have raised ToolError")
    except (ToolError, TypeError, KeyError):
        # Any of these errors are acceptable for missing required args
        pass


def test_get_openai_tools():
    """Test getting tools in OpenAI format."""
    # Clear any previous tools
    tool_registry._tools = {}

    # Register a test tool
    @tool
    def greet(name: str) -> str:
        """Greet someone."""
        return f"Hello, {name}!"

    # Get the tool schemas
    tools = tool_registry.get_openai_tools()
    assert len(tools) == 1

    tool_spec = tools[0]
    assert tool_spec["type"] == "function"
    assert "function" in tool_spec
    assert tool_spec["function"]["name"] == "greet"
    assert "parameters" in tool_spec["function"]

    # Check parameters
    params = tool_spec["function"]["parameters"]
    assert "properties" in params
    assert "name" in params["properties"]
    assert params["properties"]["name"]["type"] == "string"


def test_tool_decorator():
    """Test the @tool decorator with different function signatures."""
    # Clear any previous tools
    tool_registry._tools = {}

    @tool
    def no_params() -> str:
        """A function with no parameters."""
        return "success"

    @tool
    def with_defaults(a: int, b: int = 1) -> int:
        """A function with default parameters."""
        return a + b

    # Test calling the tools
    assert tool_registry.call_tool("no_params", {}) == "success"
    assert tool_registry.call_tool("with_defaults", {"a": 2}) == 3
    assert tool_registry.call_tool("with_defaults", {"a": 2, "b": 3}) == 5
