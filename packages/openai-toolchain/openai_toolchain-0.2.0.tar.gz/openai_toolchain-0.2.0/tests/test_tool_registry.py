"""Tests for the ToolRegistry class."""

import pytest

from openai_toolchain.tools import tool, tool_registry


@pytest.fixture(autouse=True)
def reset_tool_registry():
    """Fixture to reset the tool registry before each test."""
    tool_registry.clear()
    return tool_registry


def test_register_tool():
    """Test registering a tool with the registry."""
    # Clear any existing tools
    tool_registry.clear()

    @tool
    def test_func(a: int, b: int = 1) -> int:
        """Add two numbers."""
        return a + b

    # Check that the tool was registered
    assert "test_func" in tool_registry._tools
    tool_info = tool_registry._tools["test_func"]
    assert tool_info["function"] is test_func
    assert tool_info["description"] == "Add two numbers."
    assert tool_info["parameters"]["type"] == "object"
    # Both parameters should be in properties
    assert "a" in tool_info["parameters"]["properties"]
    assert "b" in tool_info["parameters"]["properties"]
    # 'a' should be in required parameters since it doesn't have a default
    assert "a" in tool_info["parameters"]["required"]
    # 'b' should not be in required parameters since it has a default
    assert "b" not in tool_info["parameters"].get("required", [])


def test_register_tool_with_name():
    """Test registering a tool with a custom name."""
    # Clear any existing tools
    tool_registry.clear()

    @tool
    def test_func():
        """Test function."""

    # Register with a custom name
    tool_registry.register(test_func, name="custom_name")

    assert "custom_name" in tool_registry._tools
    assert tool_registry._tools["custom_name"]["function"] is test_func


def test_get_tool():
    """Test getting a registered tool."""
    # Clear any existing tools
    tool_registry.clear()

    @tool
    def test_func():
        """Test function."""
        return "success"

    tool_info = tool_registry.get_tool("test_func")
    assert tool_info["function"] is test_func
    assert tool_info["function"]() == "success"


def test_get_nonexistent_tool():
    """Test getting a tool that doesn't exist."""
    # Clear any existing tools
    tool_registry.clear()
    assert tool_registry.get_tool("nonexistent") is None


def test_call_tool():
    """Test calling a registered tool."""
    # Clear any existing tools
    tool_registry.clear()

    @tool
    def add(a: int, b: int) -> int:
        """Add two numbers."""
        return a + b

    result = tool_registry.call_tool("add", {"a": 2, "b": 3})
    assert result == 5


def test_get_openai_tools():
    """Test getting tool schemas in OpenAI format."""
    # Clear any existing tools
    tool_registry.clear()

    @tool
    def test_func(a: int):
        """Test function."""

    schemas = tool_registry.get_openai_tools()
    assert len(schemas) == 1
    assert schemas[0]["type"] == "function"
    assert schemas[0]["function"]["name"] == "test_func"
    assert "parameters" in schemas[0]["function"]
    # The parameter 'a' should be in the schema
    assert "a" in schemas[0]["function"]["parameters"]["properties"]
    assert "a" in schemas[0]["function"]["parameters"]["required"]


def test_clear_tools():
    """Test clearing all registered tools."""
    # Clear any existing tools
    tool_registry.clear()

    @tool
    def test_func():
        pass

    assert len(tool_registry._tools) == 1  # The just registered function
    tool_registry.clear()
    assert len(tool_registry._tools) == 0
