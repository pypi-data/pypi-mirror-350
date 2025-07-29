"""Tool registration and management for OpenAI function calling.

This module provides a registry for AI tools with automatic schema generation,
validation, and execution capabilities for use with OpenAI's function calling
API.
"""

import inspect
from collections.abc import MutableSequence
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Type,
    TypeVar,
    Union,
    cast,
    get_type_hints,
)

T = TypeVar("T", bound=Callable[..., Any])
F = TypeVar("F", bound=Callable[..., Any])


class ToolError(Exception):
    """Exception raised for errors in tool registration or execution.

    This exception is raised when there are issues with tool registration,
    schema generation, or during tool execution.
    """


class ToolRegistry:
    """Registry for AI tools with automatic schema generation.

    This class implements a singleton pattern to maintain a global registry
    of tools that can be called by the OpenAI API. It handles tool registration,
    schema generation, and tool execution.
    """

    _instance: Optional["ToolRegistry"] = None
    _tools: Dict[str, Dict[str, Any]]

    def __new__(cls) -> "ToolRegistry":
        """Create a new instance or return the existing singleton instance.

        Returns:
            ToolRegistry: The singleton instance of ToolRegistry.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._tools = {}
        return cls._instance

    def register(
        self,
        func: Optional[Callable[..., Any]] = None,
        *,
        name: Optional[str] = None,
        **kwargs: Any,
    ) -> Union[Callable[[F], F], F]:
        """Register a function as a tool.

        This method can be used as a decorator with or without arguments.
        It registers the function with the tool registry and generates
        the necessary OpenAPI schema for OpenAI function calling.

        Examples:
            >>> @tool_registry.register
            ... def my_tool(param: str) -> str:
            ...     return f"Processed {param}"
            >>> @tool_registry.register(name="custom_name")
            ... def another_tool():
            ...     pass

        Args:
            func: The function to register (automatically passed when used as decorator).
            name: Optional custom name for the tool. If not provided, the function's
                name will be used.
            **kwargs: Additional metadata to include with the tool registration.

        Returns:
            Callable: The decorated function or a decorator function if called without
                a function argument.

        Raises:
            ToolError: If there's an issue with the tool registration.
        """

        def decorator(f: F) -> F:
            tool_name = name or f.__name__
            tool_description = (f.__doc__ or "").strip()

            # Store the tool
            self._tools[tool_name] = {
                "function": f,
                "description": tool_description,
                "parameters": self._get_parameters_schema(f),
                "metadata": kwargs,
            }
            return f

        if func is not None:
            return decorator(cast(F, func))
        return decorator

    def _get_parameters_schema(self, func: Callable[..., Any]) -> Dict[str, Any]:
        """Generate OpenAPI schema for function parameters.

        This method inspects the function signature and type hints to generate
        a JSON Schema that describes the function's parameters in a format
        compatible with OpenAI's function calling API.

        Args:
            func (Callable): The function for which to generate the parameter schema.

        Returns:
            dict: A dictionary containing the OpenAPI schema for the function's
                parameters.

        Example:
            >>> def example(a: int, b: str = "default") -> None:
            ...     pass
            >>> schema = tool_registry._get_parameters_schema(example)
            >>> print(schema)
            {'type': 'object', 'properties': {'a': {'type': 'integer', 'description': ''}, 'b': {'type': 'string', 'description': '', 'default': 'default'}}, 'required': ['a']}  # noqa: E501
        """
        params: Dict[str, Any] = {
            "type": "object",
            "properties": {},
            "required": [],
        }
        sig = inspect.signature(func)
        type_hints = get_type_hints(func)

        for param_name, param in sig.parameters.items():
            # Skip 'self' and 'cls' parameters
            if param_name in ("self", "cls"):
                continue

            param_type = type_hints.get(param_name, str)
            param_schema = self._type_to_schema(param_type)
            param_schema["description"] = ""

            if param.default != inspect.Parameter.empty:
                param_schema["default"] = param.default
            else:
                required = params["required"]
                if isinstance(required, MutableSequence):
                    required.append(param_name)

            params["properties"][param_name] = param_schema

        return params

    def _get_parameter_info(
        self,
        param: inspect.Parameter,
        param_type: Type[Any],
    ) -> Dict[str, Any]:
        """Get parameter information for the schema.

        This method extracts the parameter's type, default value, and description
        to include in the OpenAPI schema.

        Args:
            param (inspect.Parameter): The parameter to extract information from.
            param_type (Type): The type of the parameter.

        Returns:
            dict: A dictionary containing the parameter's information.
        """
        param_info = {"type": self._type_to_schema(param_type)["type"]}

        # Add description if available
        if param.annotation != inspect.Parameter.empty:
            param_info["description"] = str(param.annotation)

        # Add default value if available
        if param.default != inspect.Parameter.empty:
            param_info["default"] = param.default

        return param_info

    def _type_to_schema(self, type_: Type[Any]) -> Dict[str, Any]:
        """Convert Python type to OpenAPI schema.

        This method maps Python types to their corresponding JSON Schema types.
        It handles basic types (str, int, float, bool) as well as generic
        types from the typing module (List, Dict, etc.).

        Args:
            type_ (Type): The Python type to convert to a schema.

        Returns:
            dict: A dictionary representing the JSON Schema for the type.

        Note:
            For complex or custom types, the type will be converted to a string
            representation in the schema. For more precise control over the schema,
            consider using Pydantic models or explicitly defining the schema.
        """
        if type_ is str:
            return {"type": "string"}
        elif type_ is int:
            return {"type": "integer"}
        elif type_ is float:
            return {"type": "number"}
        elif type_ is bool:
            return {"type": "boolean"}
        elif type_ is list or type_ is List:
            return {"type": "array", "items": {}}
        elif type_ is dict or type_ is Dict:
            return {"type": "object"}
        else:
            # For custom types or more complex types, default to string
            # and include the type name in the description
            type_name = getattr(type_, "__name__", str(type_))
            return {
                "type": "string",
                "description": f"Expected type: {type_name}",
                "x-python-type": type_name,
            }

    def get_tool(self, name: str) -> Optional[Dict[str, Any]]:
        """Get a registered tool by name.

        This method retrieves a tool's metadata and function from the registry.

        Args:
            name (str): The name of the tool to retrieve.

        Returns:
            dict or None: The tool's metadata and function, or None if not found.
        """
        return self._tools.get(name)

    def call_tool(self, name: str, arguments: Dict[str, Any]) -> Any:
        """Call a registered tool by name with the given arguments.

        This method executes a registered tool with the provided arguments and
        returns the result.

        Args:
            name (str): The name of the tool to call.
            arguments (dict): A dictionary of arguments to pass to the tool.

        Returns:
            Any: The result of the tool execution.

        Raises:
            ToolError: If the tool is not found or if there's an error during execution.
        """
        tool = self.get_tool(name)
        if not tool:
            raise ToolError(f"Tool '{name}' not found")

        try:
            return tool["function"](**arguments)
        except Exception as e:
            raise ToolError(f"Error calling tool '{name}': {e}") from e

    def get_openai_tools(self) -> List[Dict[str, Any]]:
        """Gets all registered tools in OpenAI function calling format.

        This method converts all registered tools to the format expected by the
        OpenAI API for function calling. The resulting list can be passed directly
        to the OpenAI API's `tools` parameter.

        Returns:
            list: A list of tools in OpenAI function calling format. Each tool is a
                dictionary with 'type' and 'function' keys, where 'function'
                contains the tool's name, description, and parameters schema.

        Example:
            >>> @tool_registry.register
            ... def get_weather(location: str) -> str:
            ...     return f"Weather in {location}: Sunny"
            >>> tools = tool_registry.get_openai_tools()
            >>> print(tools[0]['function']['name'])
            get_weather
        """
        tools = []
        for name, tool in self._tools.items():
            tools.append(
                {
                    "type": "function",
                    "function": {
                        "name": name,
                        "description": tool["description"],
                        "parameters": tool["parameters"],
                    },
                },
            )
        return tools

    def clear(self) -> None:
        """Clears all registered tools."""
        self._tools.clear()


# Global registry instance
tool_registry = ToolRegistry()


def tool(
    func_or_name: Optional[Union[Callable[..., Any], str]] = None, **kwargs: Any
) -> Union[Callable[[Callable[..., Any]], Callable[..., Any]], Callable[..., Any]]:
    """Register a function as a tool with the global registry.

    This decorator can be used with or without arguments to register a function
    as a tool with the global tool registry.

    Examples:
        >>> @tool
        ... def my_function():
        ...     pass

        >>> @tool("custom_name")
        ... def another_function():
        ...     pass
    """
    """Decorator to register a function as a tool.

    This decorator provides a convenient way to register functions as tools with
    the global tool registry. It can be used in several ways:

    1. As a simple decorator::


           @tool
           def my_function():
               pass

    2. With a custom name::


           @tool("custom_name")
           def my_function():
               pass

    3. With additional metadata::


           @tool(name="custom_name", category="weather")
           def get_weather():
               pass

    Args:
        func_or_name: Either the function to decorate, a string name for the tool,
            or None if using keyword arguments.
        **kwargs: Additional metadata to include with the tool registration.
            Common keys include 'name' for a custom tool name and 'description'
            to override the function's docstring.

    Returns:
        Callable: The decorated function or a decorator function if called with
            arguments.

    """
    if func_or_name is None or isinstance(func_or_name, str):
        # @tool or @tool("name")
        name = func_or_name
        return lambda f: tool_registry.register(f, name=name, **kwargs)
    else:
        # @tool without arguments
        return tool_registry.register(func_or_name, **kwargs)
