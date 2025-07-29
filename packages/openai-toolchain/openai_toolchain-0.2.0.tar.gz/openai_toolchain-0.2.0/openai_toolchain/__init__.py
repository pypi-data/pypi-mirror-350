"""OpenAI Toolchain - A Python library for working with OpenAI's function calling API."""

from importlib.metadata import PackageNotFoundError, version

from .client import OpenAIClient
from .tools import ToolError, tool, tool_registry

try:
    __version__ = version("openai-toolchain")
except PackageNotFoundError:
    # package is not installed in development mode
    __version__ = "0.0.0"

__all__ = ["ToolError", "tool", "OpenAIClient", "tool_registry"]
