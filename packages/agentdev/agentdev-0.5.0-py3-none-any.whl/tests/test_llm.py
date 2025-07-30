# -*- coding: utf-8 -*-
import pytest
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from pydantic import BaseModel
from typing import Optional

from agentdev.models.llm import BaseLLM
from agentdev.schemas.message_schemas import Parameters, UserPromptMessage
from agentdev.tracing import Tracer
from agentdev.tracing.dashscope_log import DashscopeLogHandler


# This testing require DASHSCOPE_API_KEY environment variable to be set


class User(BaseModel):
    name: Optional[str]
    age: Optional[int]


@pytest.fixture
def user_text_message():
    return UserPromptMessage(content="创建一个角色")


@pytest.fixture
def user_openai_vl_message():
    content_list = [
        {"type": "text", "text": "这张图是什么内容。"},
        {
            "type": "image_url",
            "image_url": {
                "url": "https://bailian-cn-beijing.oss-cn-beijing.aliyuncs"
                ".com/einstein.png",
            },
        },
    ]
    return UserPromptMessage(content=content_list)


@pytest.fixture
def user_bailian_vl_message():
    content_list = [
        {
            "text": "这张图是什么内容。",
        },
        {
            "image": "https://bailian-cn-beijing.oss-cn-beijing.aliyuncs.com"
            "/einstein.png",
        },
    ]
    return UserPromptMessage(content=content_list)


@pytest.fixture
def llm():
    return BaseLLM()


@pytest.mark.asyncio
async def test_vl_arun(user_openai_vl_message, llm):
    """Test arun method"""
    chunks = []
    async for chunk in llm.astream(
        model="qwen-vl-plus",
        messages=[user_openai_vl_message],
    ):
        chunks.append(chunk)
        print("astream chunk:", chunk)

    assert len(chunks) > 0
    assert isinstance(chunks[0], ChatCompletionChunk)


@pytest.mark.asyncio
async def test_bailian_vl_arun(user_bailian_vl_message, llm):
    """Test arun method"""
    chunks = []
    async for chunk in llm.astream(
        model="qwen-vl-plus",
        messages=[user_bailian_vl_message],
    ):
        chunks.append(chunk)
        print("astream chunk:", chunk)

    assert len(chunks) > 0
    assert isinstance(chunks[0], ChatCompletionChunk)


@pytest.mark.asyncio
async def test_text_arun(user_text_message, llm):
    """Test arun method"""
    result = await llm.arun(model="qwen-turbo", messages=[user_text_message])
    assert isinstance(result, ChatCompletion)
    assert result.choices[0].message.content is not None
    assert isinstance(result.choices[0].message.content, str)


@pytest.mark.asyncio
async def test_text_astream(user_text_message, llm):
    """Test astream method"""
    chunks = []
    parameters = Parameters(stream_options={"include_usage": True})
    async for chunk in llm.astream(
        model="qwen-max",
        messages=[user_text_message],
        parameters=parameters,
    ):
        chunks.append(chunk)
        print("astream chunk:", chunk)

    assert len(chunks) > 0
    assert isinstance(chunks[0], ChatCompletionChunk)


@pytest.mark.asyncio
async def test_structured_output(user_text_message):
    """Test structured output with response_model"""
    llm = BaseLLM.from_instructor_client()
    chunks = []
    output = None

    async for chunk in llm.astream(
        model="qwen-max",
        messages=[user_text_message],
        response_model=User,
    ):
        chunks.append(chunk)
        output = chunk

    assert len(chunks) > 0
    assert isinstance(output, User)
