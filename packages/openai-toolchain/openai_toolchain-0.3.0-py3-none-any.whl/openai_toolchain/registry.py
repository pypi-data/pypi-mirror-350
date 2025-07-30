"""Tool registry for managing and calling registered tools."""

import inspect
import logging
from collections.abc import Callable, MutableMapping
from typing import Any, Dict, List, Optional, Type, TypeVar, Union, get_type_hints

T = TypeVar("T", bound=Callable[..., Any])

_logger = logging.getLogger(__name__)


class ToolError(Exception):
    """Base exception for tool-related errors."""


class ToolRegistry:
    """Singleton registry for AI tools with automatic schema generation."""

    _instance: Optional["ToolRegistry"] = None
    _initialized: bool = False

    def __new__(cls) -> "ToolRegistry":
        if cls._instance is None:
            instance = super().__new__(cls)
            cls._instance = instance
        return cls._instance

    def __init__(self) -> None:
        if not getattr(self, "_initialized", False):
            self._tools: Dict[str, Dict[str, Any]] = {}
            self._initialized = True

    def register(
        self,
        func: Optional[T] = None,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        non_ai_params: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Union[Callable[[T], T], T]:
        """Register a function as a tool.

        Can be used as a decorator with or without arguments.

        Args:
            func: The function to register (automatically passed when used as decorator)
            name: Optional custom name for the tool
            description: Optional description for the tool
            **kwargs: Additional tool metadata

        Returns:
            The decorated function or a decorator
        """

        def decorator(f: T) -> T:
            tool_name = name or f.__name__
            tool_description = description or (f.__doc__ or "").strip()

            # Initialize local non_ai_params list
            local_non_ai_params = (
                non_ai_params.copy() if non_ai_params is not None else []
            )

            if local_non_ai_params:
                non_ai_param_joined = "\\n- ".join(local_non_ai_params)
                tool_description += f"""

                Non-AI parameters (do not use these):
                {non_ai_param_joined}
                """

            # Extract parameter information
            sig = inspect.signature(f)
            parameters: Dict[str, Any] = {}
            required: List[str] = []
            type_hints = get_type_hints(f)

            for param_name, param in sig.parameters.items():
                if param_name == "self" or param_name in local_non_ai_params:
                    continue

                param_type = type_hints.get(param_name, str)
                param_info = self._get_parameter_info(param, param_type)
                parameters[param_name] = param_info

                if param.default == inspect.Parameter.empty:
                    required.append(param_name)

            # Create the tool schema with proper typing
            tool_schema: Dict[str, Any] = {
                "type": "function",
                "function": {
                    "name": tool_name,
                    "description": tool_description,
                    "parameters": {
                        "type": "object",
                        "properties": parameters,
                    },
                },
            }

            if required:
                # Explicitly type the parameters dictionary
                function_params = tool_schema["function"]["parameters"]
                if isinstance(function_params, MutableMapping):
                    function_params["required"] = required

            # Store the tool
            self._tools[tool_name] = {
                "function": f,
                "schema": tool_schema,
                "metadata": kwargs,
            }

            return f

        if func is not None:
            return decorator(func)
        return decorator

    def _get_parameter_info(
        self,
        param: inspect.Parameter,
        param_type: Type[Any],
    ) -> Dict[str, Any]:
        """Get parameter information for the schema.

        Args:
            param: The parameter to get info for
            param_type: The type of the parameter

        Returns:
            Dictionary containing parameter schema information
        """
        param_info: Dict[str, Any] = {}

        # Handle different parameter types
        if param_type in (str, int, float, bool):
            param_info["type"] = param_type.__name__
        elif param_type == list:
            param_info.update({"type": "array", "items": {"type": "string"}})
        elif param_type == dict:
            param_info["type"] = "object"
        else:
            param_info["type"] = "string"

        # Add description if available
        if param.annotation != inspect.Parameter.empty:
            param_info["description"] = str(param.annotation)

        # Add default value if available
        if param.default != inspect.Parameter.empty:
            param_info["default"] = param.default

        return param_info

    def _get_type_name(self, type_: Type[Any]) -> str:
        """Convert Python type to JSON schema type name.

        Args:
            type_: The Python type to convert

        Returns:
            String representing the JSON schema type
        """
        type_map = {
            str: "string",
            int: "integer",
            float: "number",
            bool: "boolean",
        }
        return type_map.get(type_, "string")

    def get_tool(self, name: str) -> Optional[Callable[..., Any]]:
        """Get a registered tool by name.

        Args:
            name: The name of the tool

        Returns:
            The registered function or None if not found
        """
        tool = self._tools.get(name)
        if tool is None:
            return None
        return tool.get("function")

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a registered tool by name with the given arguments.

        Args:
            name: The name of the tool to call
            arguments: The arguments to pass to the tool

        Returns:
            The result of the tool call

        Raises:
            ToolError: If the tool is not found or an error occurs during execution
        """
        tool = self._tools.get(name)
        if not tool:
            raise ToolError(f"Tool '{name}' not found")

        try:
            return tool["function"](**arguments)
        except Exception as e:
            _logger.error(f"Error calling tool '{name}': {e}", exc_info=True)
            raise ToolError(f"Error calling tool '{name}': {e}") from e

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """Get all registered tools in OpenAI format.

        Returns:
            List[Dict[str, Any]]: A list of tool definitions in OpenAI format
        """
        return [tool["schema"] for tool in self._tools.values() if "schema" in tool]

    def clear(self) -> None:
        """Clear all registered tools."""
        self._tools.clear()

    # Make the registry callable as a decorator
    tool = register
