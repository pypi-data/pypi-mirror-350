"""OpenAI Toolchain - A Python library for working with OpenAI's function calling API."""

from .client import OpenAIClient
from .tools import ToolError, tool, tool_registry

__version__ = "0.2.0"
__all__ = ["ToolError", "tool", "OpenAIClient", "tool_registry"]
