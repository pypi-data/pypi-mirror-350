# -*- coding: utf-8 -*-
import pytest

from agentdev.base.function_tool import function_tool, tool_function_factory
from agentdev.schemas.message_schemas import ParametersSchema


@function_tool
def get_weather(city: str) -> str:
    """Get the weather for a given city."""
    return f"The weather in {city} is sunny."


def test_function_schema():
    # Assert function schema structure
    assert get_weather.function_schema.name == "get_weather"
    assert (
        get_weather.function_schema.description
        == "Get the weather for a given city."
    )
    assert "city" in get_weather.function_schema.parameters.properties
    assert get_weather.function_schema.parameters.required == ["city"]


def test_argument_validation():
    # Valid arguments
    validated_args = get_weather.verify_args({"city": "Shanghai"})
    assert validated_args == {"city": "Shanghai"}

    # Invalid arguments
    try:
        get_weather.verify_args({"city": 123})  # city should be a string
        assert False, "Expected ValueError"
    except ValueError:
        pass


def test_async_execution():
    # Run the function asynchronously and assert result
    import asyncio

    async def run_test():
        result = await get_weather.arun(city="Beijing")
        return result

    result = asyncio.run(run_test())
    assert result == "The weather in Beijing is sunny."


def test_sync_execution():
    # Run the function asynchronously and assert result

    def run_test():
        result = get_weather.run({"city": "Beijing"})
        return result

    result = run_test()
    assert result == "The weather in Beijing is sunny."


def test_custom_name_and_description():

    @function_tool(
        name_override="custom_name",
        description_override="Custom description for testing.",
    )
    def custom_function(city: str) -> str:
        """Original docstring."""
        return f"The weather in {city} is sunny."

    # Assert custom name and description in function schema
    assert custom_function.function_schema.name == "custom_name"
    assert (
        custom_function.function_schema.description
        == "Custom description for testing."
    )
    assert "city" in custom_function.function_schema.parameters.properties
    assert custom_function.function_schema.parameters.required == ["city"]

    # Ensure original function behavior is preserved
    assert (
        custom_function(city="Shanghai") == "The weather in Shanghai is sunny."
    )


def test_default_name_and_description():

    @function_tool
    def default_function(city: str) -> str:
        """Default docstring."""
        return f"The weather in {city} is sunny."

    # Assert default name and description in function schema
    assert default_function.function_schema.name == "default_function"
    assert default_function.function_schema.description == "Default docstring."
    assert "city" in default_function.function_schema.parameters.properties
    assert default_function.function_schema.parameters.required == ["city"]


schema = {
    "name": "searchProduct",
    "description": "搜索商品信息",
    "parameters": {
        "type": "object",
        "properties": {
            "keyword": {"type": "string"},
            "maxResults": {"type": "integer"},
        },
        "required": ["keyword"],
        "additional_properties": False,
    },
}


def mock_func(**kwargs):
    return kwargs


@pytest.mark.asyncio
async def test_tool_factory():

    mock_tool_cls = tool_function_factory(
        schema,
        mock_func,
        **{"service_id": "123"},
    )
    assert mock_tool_cls.function_schema.name == schema["name"]
    assert mock_tool_cls.function_schema.description == schema["description"]
    assert mock_tool_cls.function_schema.parameters == ParametersSchema(
        **schema["parameters"],
    )

    results = mock_tool_cls(keyword="手机", maxResults=5)
    assert results == {
        "tool_name": schema["name"],
        "tool_params": {"keyword": "手机", "maxResults": 5},
        "service_id": "123",
    }

    results = await mock_tool_cls.arun(**{"keyword": "手机", "maxResults": 5})
    assert results == {
        "tool_name": schema["name"],
        "tool_params": {"keyword": "手机", "maxResults": 5},
        "service_id": "123",
    }
