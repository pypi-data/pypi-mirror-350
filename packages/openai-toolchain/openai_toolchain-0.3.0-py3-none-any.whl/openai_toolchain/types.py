"""Type definitions for the OpenAI Toolchain."""

from typing import Any, Dict, List, Literal, TypedDict

# Type aliases
MessageRole = Literal["system", "user", "assistant", "tool", "function"]


class ToolFunction(TypedDict):
    """A function that can be called by the model."""

    name: str
    arguments: str


class ToolCall(TypedDict):
    """A tool call made by the model."""

    id: str
    type: Literal["function"]
    function: ToolFunction


class ToolResult(TypedDict):
    """The result of a tool call."""

    tool_call_id: str
    name: str
    content: str


# Type for message dictionaries
MessageDict = Dict[str, str]

# Type for tool schemas
ToolSchema = Dict[str, Any]

# Type for tool definitions in OpenAI format
OpenAITool = Dict[str, Any]

# Type for tool call results
ToolCallResult = Dict[str, Any]

# Type for chat completion messages
ChatMessage = Dict[str, str]
ChatMessages = List[ChatMessage]
