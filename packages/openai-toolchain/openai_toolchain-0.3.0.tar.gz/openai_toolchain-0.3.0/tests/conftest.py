"""Pytest configuration and fixtures for tests."""

import pytest

from openai_toolchain.tools import ToolRegistry


@pytest.fixture()
def tool_registry():
    """Fixture that provides a clean tool registry for each test."""
    # Create a new registry
    registry = ToolRegistry()
    # Clear any existing tools
    registry._tools = {}
    return registry
