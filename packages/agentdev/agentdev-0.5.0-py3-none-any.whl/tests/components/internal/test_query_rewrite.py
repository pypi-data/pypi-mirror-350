# -*- coding: utf-8 -*-
import asyncio
import pytest
from copy import deepcopy

from agentdev.components.internal.query_rewriter import (
    QueryConvolutionComponent,
    QueryConvolutionInput,
    QueryConvolutionOutput,
    QueryRewriterComponent,
    QueryRewriterInput,
    QueryRewriterOutput,
)
from agentdev.schemas.message_schemas import PromptMessage

messages = [
    PromptMessage(content="今天天气如何？", role="user"),
    PromptMessage(content="今天天气非常不错", role="assistant"),
    PromptMessage(content="魅族最新Flyme介绍", role="user"),
]
query_rewrite = QueryRewriterInput(messages=messages)
query_rewrite_conv = QueryConvolutionInput(messages=messages)


@pytest.fixture
def tester_query_rewrite_component(mocker):
    # Create an instance of QueryRewrite
    query_rewrite_component = QueryRewriterComponent()
    return query_rewrite_component


@pytest.fixture
def tester_query_rewrite_conv_component(mocker):
    # Create an instance of QueryRewrite
    query_rewrite_conv_component = QueryConvolutionComponent()
    return query_rewrite_conv_component


@pytest.mark.asyncio
async def test_arun_basic(tester_query_rewrite_component):
    # Mock input data

    # Call the arun method
    result = await tester_query_rewrite_component.arun(query_rewrite)

    # Assert the result is an instance of SearchOutput
    assert isinstance(result, QueryRewriterOutput)


@pytest.mark.asyncio
async def test_arun_conv(tester_query_rewrite_conv_component):
    # Mock input data

    # Call the arun method
    result = await tester_query_rewrite_conv_component.arun(query_rewrite_conv)

    # Assert the result is an instance of SearchOutput
    assert isinstance(result, QueryConvolutionOutput)
