# -*- coding: utf-8 -*-
import pytest
from openai.types.chat import ChatCompletionChunk
from pydantic import BaseModel, Field
from typing import Any

from agentdev.base.component import Component
from agentdev.models.function_call import (
    function_call_loop,
    merge_incremental_chunk,
)
from agentdev.models.llm import BaseLLM
from agentdev.schemas.message_schemas import Parameters, UserPromptMessage


class SearchInput(BaseModel):
    """
    Search Input.
    """

    query: str = Field(..., title="Query")


class SearchOutput(BaseModel):
    """
    Search Output.
    """

    results: str


class SearchComponent(Component[SearchInput, SearchOutput]):
    """
    Search Component.
    """

    def model_dump_json(self):
        return "SearchComponent"

    async def _arun(self, args: SearchInput, **kwargs: Any) -> SearchOutput:
        """
        Run.
        """
        if "sf" in args.query.lower() or "san francisco" in args.query.lower():
            result = "It's 60 degrees and foggy."
        result = "It's 90 degrees and sunny."

        return SearchOutput(results=result)


search_component = SearchComponent(
    name="search_tool",
    description="search user query for latest information from website",
)


@pytest.fixture
def llm():
    return BaseLLM()


@pytest.fixture
def user_tool_call_message():
    return UserPromptMessage(content="杭州今天会下雨么？")


@pytest.fixture
def user_tool_call_parameters():
    tool_info = search_component.function_schema.model_dump()
    tools = [{"type": "function", "function": tool_info}]
    return Parameters(tools=tools, stream_options={"include_usage": True})


@pytest.mark.asyncio
async def test_function_call_arun(
    user_tool_call_message,
    user_tool_call_parameters,
    llm,
):
    """Test arun method"""
    chunks = []
    async for chunk in llm.astream(
        model="qwen-max",
        messages=[user_tool_call_message],
        parameters=user_tool_call_parameters,
    ):
        chunks.append(chunk)
        print("astream chunk:", chunk)
        if (
            len(chunk.choices) > 0
            and chunk.choices[0].finish_reason == "tool_calls"
        ):
            cumulated_resp = merge_incremental_chunk(chunks)
            assert len(cumulated_resp.choices[0].delta.tool_calls) > 0
            assert (
                cumulated_resp.choices[0]
                .delta.tool_calls[0]
                .function.arguments.count("query")
                > 0
            )
            assert (
                cumulated_resp.choices[0].delta.tool_calls[0].function.name
                == "search_tool"
            )
            print("cumulated_resp:", cumulated_resp)

    assert len(chunks) > 0
    assert isinstance(chunks[0], ChatCompletionChunk)


@pytest.mark.asyncio
async def test_function_call_loop_arun(
    user_tool_call_message,
    user_tool_call_parameters,
    llm,
):
    """Test arun method"""
    chunks = []
    async for chunk in function_call_loop(
        model_cls=llm,
        model="qwen-max",
        messages=[user_tool_call_message],
        parameters=user_tool_call_parameters,
        available_components={"search_tool": search_component},
    ):
        chunks.append(chunk)
        print("astream chunk:", chunk)

    assert len(chunks) > 0
    assert isinstance(chunks[0], ChatCompletionChunk)
