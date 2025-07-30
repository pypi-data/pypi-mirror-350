# -*- coding: utf-8 -*-
import json
import types
from inspect import Parameter, signature
from pydantic import BaseModel, create_model
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Type,
    TypedDict,
    Union,
    get_type_hints,
)

from agentdev.schemas.message_schemas import (
    ParametersSchema,
    PromptMessageTool,
)


def schema_type_to_typing(schema_property: Dict[str, Any]) -> Any:
    """Convert a JSON schema property to a Python typing annotation."""
    schema_type = schema_property.get("type", "any")

    if schema_type == "string":
        if "enum" in schema_property:
            return Literal[tuple(schema_property["enum"])]
        return str
    elif schema_type == "integer":
        return int
    elif schema_type == "number":
        return float
    elif schema_type == "boolean":
        return bool
    elif schema_type == "array":
        items_schema = schema_property.get("items", {})
        item_type = schema_type_to_typing(items_schema)
        return list(item_type)
    elif schema_type == "object":
        if "properties" in schema_property:
            # Create a TypedDict for the object
            properties = {}
            for prop_name, prop_schema in schema_property[
                "properties"
            ].items():
                properties[prop_name] = schema_type_to_typing(prop_schema)
            class_name = schema_property.get(
                "title",
                "CustomTypedDict",
            )  # Use types.new_class() instead of type()
            namespace = {"__annotations__": properties}
            return types.new_class(
                class_name,
                (TypedDict,),
                {},
                lambda ns: ns.update(namespace),
            )
        else:
            return Dict[str, Any]
    else:  # "any" or unknown types
        return Any


def function_schema_to_typing(schema: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convert a function call schema to Python typing annotations with default
        values.
    Returns format: {'key_name': (type, default_value)} or
        {'key_name': (type, ...)}
    if no default
    """
    annotations = {}

    parameters = schema
    if parameters.get("type") != "object":
        return {}
    properties = parameters.get("properties", {})
    required = parameters.get("required", [])

    for param_name, param_schema in properties.items():
        param_type = schema_type_to_typing(param_schema)
        # Check if parameter has a default value specified in schema
        if "default" in param_schema:
            default_value = param_schema["default"]
        # If not required, use None as default
        elif param_name not in required:
            default_value = None
        # If required, use ... to indicate no default value
        else:
            default_value = ...
        annotations[param_name] = (param_type, default_value)

    # Add return type if available
    if "returns" in schema:
        returns_schema = schema["returns"]
        returns_type = schema_type_to_typing(returns_schema)
        annotations["return"] = (
            returns_type,
            ...,
        )  # Return type doesn't have a default value
    return annotations


def function_tool(
    _func: Callable = None,
    *,
    name_override: str = None,
    description_override: str = None,
    schema_override: ParametersSchema = None,
) -> Callable:

    def decorator(func: Callable) -> Callable:
        """
        Decorator to add Component-like functionality to any function.

        Adds:
        - function_schema: A schema representation of the function.
        - arun: An asynchronous version of the function.
        - verify_args: A method to validate function arguments.
        """

        # Generate Pydantic model for argument validation
        func_annotations = get_type_hints(func)
        sig = signature(func)
        fields = {}

        if schema_override is None:
            for name, param in sig.parameters.items():
                if name == "return":
                    continue
                typ = func_annotations.get(name, Any)
                if param.default is Parameter.empty:
                    # Required parameter
                    fields[name] = (typ, ...)
                else:
                    # Optional parameter, set default value
                    fields[name] = (typ, param.default)
        else:
            fields = function_schema_to_typing(schema_override.model_dump())
        args_model: Type[BaseModel] = create_model(
            f"{func.__name__}Args",
            **fields,
        )

        def generate_function_schema(
            schema: Union[Dict, ParametersSchema] = None,
        ) -> PromptMessageTool:
            properties = {}
            required = []
            for name, field in args_model.model_fields.items():
                properties[name] = {
                    "type": (
                        field.annotation.__name__
                        if hasattr(field.annotation, "__name__")
                        else str(field.annotation)
                    ),
                }
                if field.is_required():
                    required.append(name)

            if schema is None:
                parameters = ParametersSchema(
                    type="object",
                    properties=properties,
                    required=required,
                )
            else:
                parameters = schema

            return PromptMessageTool(
                name=(
                    name_override
                    if name_override is not None
                    else func.__name__
                ),
                description=description_override or (func.__doc__ or ""),
                parameters=parameters,
            )

        def run(*args: Any, **kwargs: Any) -> Any:
            # Validate arguments
            if args:
                validated_args = verify_args(args[0])
            else:
                validated_args = verify_args(kwargs)
            # Call the original function with validated arguments
            return func(**validated_args)

        async def arun(*args: Any, **kwargs: Any) -> Any:
            # Call the original function with validated arguments
            if args:
                validated_args = verify_args(args[0])
            else:
                validated_args = verify_args(kwargs)
            # Call the original function with validated arguments
            return await func(**validated_args)

        def verify_args(args: Dict[str, Any]) -> Dict[str, Any]:
            try:
                if isinstance(args, str):
                    args_dict = json.loads(args)
                elif isinstance(args, BaseModel):
                    args_dict = args.model_dump()
                else:
                    args_dict = args

                validated_args = args_model(**args_dict)
                return validated_args.model_dump(exclude_none=True)
            except json.JSONDecodeError as e:
                raise ValueError(f"Invalid JSON format: {e}")
            except Exception as e:
                raise ValueError(f"Invalid arguments: {e}")

        # Return a new function object that wraps the original function
        wrapper = func  # Use run as the main entry point
        wrapper.arun = arun
        wrapper.run = run
        wrapper.verify_args = verify_args
        wrapper.function_schema = generate_function_schema(schema_override)

        return wrapper

    if _func is None:
        # If called with arguments, return the decorator
        return decorator
    else:
        # If called without arguments, apply directly
        return decorator(_func)


def tool_function_factory(
    schema: Union[Dict, PromptMessageTool],
    actual_func: Callable,
    **factory_kwargs: Any,
) -> Callable:
    """
    Create a tool function based on the given schema.

    Args:
        schema (dict): The schema definition of the tool
        actual_func(Callable): The actual function to execute
    Returns:
        function: The function generated according to the schema
    """
    if isinstance(schema, Dict):
        schema = PromptMessageTool(**schema)
    tool_name = schema.name
    tool_description = schema.description
    input_schema = schema.parameters
    required_properties = input_schema.get("required", [])

    async def generated_tool(**kwargs: Any) -> Any:
        """Function generated by schema."""
        # Validate required parameters
        for prop in required_properties:
            if prop not in kwargs:
                raise ValueError(f"Missing required property: {prop}")
        extra_kwargs = factory_kwargs.copy()
        return await actual_func(
            tool_name=tool_name,
            tool_params=kwargs,
            **extra_kwargs,
        )

    # Generate function docstring
    generated_tool.__doc__ = f"{tool_description}"
    generated_tool.__name__ = tool_name

    return function_tool(
        generated_tool,
        schema_override=ParametersSchema(**input_schema),
    )
