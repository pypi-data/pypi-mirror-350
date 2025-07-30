# -*- coding: utf-8 -*-
# mcp_wrapper.py
from typing import Any, Callable, Generic, Optional, Type, TypeVar

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel
from pydantic_core import PydanticUndefined

T = TypeVar("T", bound=BaseModel)
U = TypeVar("U", bound=BaseModel)


class MCPWrapper(Generic[T, U]):

    def __init__(self, mcp: FastMCP, component_class: Type):
        self.mcp = mcp
        self.component_class = component_class

    def wrap(
        self,
        name: str,
        description: str,
        method_name: str = "arun",
    ) -> Callable[..., Any]:
        component = self.component_class(name=name, description=description)

        def create_decorated_async_function(
            params: list[str],
            func_name: str = "wrapped_tool",
            decorator: Optional[Callable] = None,
        ) -> Callable[..., Any]:
            # Generate parameter list with type annotations
            params_types_with_default = []
            params_types_without_default = []

            for param in params:
                # Get field information from Pydantic model
                field_info = component.input_type.model_fields[param]
                # Extract type annotation
                param_type = field_info.annotation
                # Convert type to string representation
                if hasattr(param_type, "__name__"):
                    type_str = param_type.__name__
                    if type_str == "Optional":
                        if hasattr(param_type, "__args__"):
                            try:
                                type_str = param_type.__args__[0].__name__
                            except Exception:
                                type_str = ""
                        else:
                            type_str = ""
                else:
                    type_str = str(param_type)

                # Check for default value
                if field_info.default is not PydanticUndefined:
                    default_repr = repr(field_info.default)
                    if type_str == "":
                        param_line = f"{param} = {default_repr}"
                    else:
                        param_line = f"{param}: {type_str} = {default_repr}"
                    params_types_with_default.append(param_line)
                else:
                    if type_str == "":
                        param_line = f"{param}"
                    else:
                        param_line = f"{param}: {type_str}"
                    params_types_without_default.append(param_line)

            args_str_with_default = ", ".join(params_types_with_default)
            args_str_without_default = ", ".join(params_types_without_default)

            args_str = args_str_without_default
            if len(args_str_with_default) > 0:
                args_str += f", {args_str_with_default}"
            kwargs_code = (
                "{" + ", ".join([f"'{p}': {p}" for p in params]) + "}"
            )

            # dynamic generate functions
            code = f"""
async def {func_name}({args_str}):
    input_model = component.input_type(**{kwargs_code})
    method = getattr(component, method_name)
    result = await method(input_model)
    import json
    return json.dumps(result.model_dump(), ensure_ascii=False)
"""

            # make namespace for component
            namespace = {"component": component, "method_name": method_name}

            # generate code generation
            exec(code, namespace)

            raw_function = namespace[func_name]

            # apply decorator
            if decorator:
                return decorator(raw_function)
            return raw_function

        # define the mcp tool decorator
        tool_decorator = self.mcp.tool(
            name=component.name,
            description=component.description,
        )

        # wrap the tool with mcp decorator with respect of the component
        # input type
        wrapped_tool = create_decorated_async_function(
            params=component.input_type.model_fields.keys(),
            decorator=tool_decorator,
        )

        self.mcp._tool_manager._tools[component.name].parameters.update(
            component.function_schema.parameters.model_dump(),
        )
        return wrapped_tool


if __name__ == "__main__":
    from mcp.server.fastmcp import FastMCP

    from demos.components.create_component import SearchComponent

    # Create an MCP server
    mcp = FastMCP("ComponentDemo")

    # Wrap and add the SearchComponent
    search_wrapper = MCPWrapper(mcp, SearchComponent)
    search_wrapper.wrap("Search Component", "Search Component For Example")
    print(mcp._tool_manager._tools)
    print("MCP server is running...")
    mcp.run()
