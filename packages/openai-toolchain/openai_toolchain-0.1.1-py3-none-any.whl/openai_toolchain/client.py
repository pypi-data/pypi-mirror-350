"""OpenAI client for interacting with the API with tool support."""

import json
import logging
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    TypedDict,
    Union,
    cast,
)

from openai import OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionMessageParam

from .tools import tool_registry


# Define custom types for better type checking
class MessageDict(TypedDict, total=False):
    """Dictionary representing a chat message."""

    role: str
    content: str
    name: Optional[str]
    tool_call_id: Optional[str]


# Define a type for tool definitions
ToolDefinition = Dict[str, Any]  # Simplified for now, can be made more specific


# Define a type for the response from the OpenAI API
class ChatResponse(TypedDict, total=False):
    """Type for the response from the OpenAI API."""

    choices: List[Dict[str, Any]]
    # Add other fields as needed


_logger = logging.getLogger(__name__)

MessageRole = Literal["system", "user", "assistant", "tool"]


class OpenAIClient:
    """Client for interacting with the OpenAI API with tool support."""

    def __init__(
        self,
        api_key: str,
        base_url: str = "https://api.openai.com/v1",
        default_model: str = "gpt-4",
        **client_kwargs: Any,
    ) -> None:
        """Initialize the OpenAI client.

        Args:
            api_key: Your OpenAI API key
            base_url: Base URL for the API (defaults to OpenAI's API)
            default_model: Default model to use for completions
            **client_kwargs: Additional arguments to pass to the OpenAI client
        """
        self.client = OpenAI(api_key=api_key, base_url=base_url, **client_kwargs)
        self.default_model = default_model

    def chat(
        self,
        messages: Sequence[MessageDict],
        model: Optional[str] = None,
        tools: Optional[Sequence[Union[ToolDefinition, str]]] = None,
        tool_choice: str = "auto",
        **kwargs: Any,
    ) -> ChatCompletion:
        """Send a chat completion request with optional tool support.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            model: Model to use (defaults to the client's default model)
            tools: List of tool definitions or tool names (defaults to all registered tools)
            tool_choice: How the model should handle tool calls
            **kwargs: Additional arguments for the completion

        Returns:
            The chat completion response
        """
        model = model or self.default_model

        # Get tools from the singleton registry if not provided
        tool_schemas: List[ToolDefinition] = []
        if tools is None:
            tool_schemas = tool_registry.get_openai_tools()
        elif tools and isinstance(tools[0], str):
            all_tools = tool_registry.get_openai_tools()
            tool_schemas = [
                tool
                for tool in all_tools
                if tool.get("function", {}).get("name") in tools
            ]
        else:
            # Cast to List[ToolDefinition] since we know the type
            tool_schemas = list(cast(Sequence[ToolDefinition], tools))

        # Convert messages to the correct format
        openai_messages: List[ChatCompletionMessageParam] = [
            self._convert_message(msg) for msg in messages
        ]

        # Make the API call
        response = self.client.chat.completions.create(
            model=model,
            messages=openai_messages,
            tools=tool_schemas if tool_schemas else None,
            tool_choice=tool_choice if tool_schemas else None,
            **kwargs,
        )

        return response

    def chat_with_tools(
        self,
        messages: Sequence[MessageDict],
        tools: Optional[Sequence[str]] = None,
        model: Optional[str] = None,
        max_tool_calls: int = 5,
        **kwargs: Any,
    ) -> str:
        # Convert messages to a list for mutation
        conversation: List[MessageDict] = list(messages)
        """Send a chat completion request and handle tool calls automatically.

        This will automatically execute tool calls and include their results
        in subsequent API calls until the model returns a final response.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            tools: List of tool names to use (None for all registered tools)
            model: Model to use (defaults to the client's default model)
            max_tool_calls: Maximum number of tool call rounds to allow
            **kwargs: Additional arguments for the completion

        Returns:
            The final assistant message content

        Raises:
            RuntimeError: If the maximum number of tool calls is exceeded
        """
        # Conversation is now a list that we can mutate
        tool_call_count = 0

        # Get tools from the singleton registry
        tool_schemas = [
            tool
            for tool in tool_registry.get_openai_tools()
            if not tools or tool.get("function", {}).get("name") in tools
        ]

        while tool_call_count < max_tool_calls:
            # Get the next response from the model
            response = self.chat(
                conversation,
                model=model or self.default_model,
                tools=tool_schemas or None,
                tool_choice="auto" if tool_schemas else "none",
                **kwargs,
            )

            message = response.choices[0].message

            # If there are no tool calls, we're done
            if not hasattr(message, "tool_calls") or not message.tool_calls:
                return message.content or ""

            # Process tool calls
            tool_call_count += 1
            for tool_call in message.tool_calls:
                function = tool_call.function

                # Execute the tool
                try:
                    result = tool_registry.call_tool(
                        function.name,
                        json.loads(function.arguments),
                    )
                    result_str = (
                        json.dumps(result) if not isinstance(result, str) else result
                    )
                except Exception as e:
                    result_str = f"Error: {e!s}"

                # Add the tool response to the conversation
                conversation.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": function.name,
                        "content": result_str,
                    },
                )

        raise RuntimeError(f"Maximum number of tool calls ({max_tool_calls}) exceeded")

    def _convert_message(self, message: MessageDict) -> ChatCompletionMessageParam:
        """Convert a message dictionary to the proper ChatCompletionMessageParam type."""
        role = message.get("role")
        content = message.get("content", "")

        if role == "system":
            return {"role": "system", "content": content}
        elif role == "user":
            return {"role": "user", "content": content}
        elif role == "assistant":
            return {"role": "assistant", "content": content}
        elif role == "tool":
            return {
                "role": "tool",
                "tool_call_id": message.get("tool_call_id", ""),
                "name": message.get("name", ""),
                "content": content,
            }
        elif role == "function":
            return {
                "role": "function",
                "name": message.get("name", ""),
                "content": content,
            }
        else:
            # Default to user message if role is not recognized
            return {"role": "user", "content": str(message)}
