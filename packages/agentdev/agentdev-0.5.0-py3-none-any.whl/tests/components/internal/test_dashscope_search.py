# -*- coding: utf-8 -*-
import asyncio
import pytest
from copy import deepcopy

from agentdev.components.internal.dashscope_search import (
    DashscopeSearch,
    SearchInput,
    SearchOutput,
)
from agentdev.schemas.message_schemas import PromptMessage

search_input = SearchInput(
    messages=[PromptMessage(content="魅族最新Flyme介绍", role="user")],
)


@pytest.fixture
def tester_search_component(mocker):
    # Create an instance of DashscopeSearch
    search_component = DashscopeSearch()
    return search_component


@pytest.mark.asyncio
async def test_arun_basic(tester_search_component):
    # Mock input data

    # Call the arun method
    result = await tester_search_component.arun(
        search_input,
        **{"is_local": True},
    )

    # Assert the result is an instance of SearchOutput
    assert isinstance(result, SearchOutput)
    assert len(result.search_result) > 0
    assert result.search_info == {}


@pytest.mark.asyncio
async def test_arun_basic_with_user_config(tester_search_component):
    # Mock input data

    # Call the arun method
    result = await tester_search_component.arun(
        search_input,
        **{"is_local": True, "user_id": "1999849738269549"},
    )

    # Assert the result is an instance of SearchOutput
    assert isinstance(result, SearchOutput)
    assert len(result.search_result) > 0
    assert result.search_info == {}


@pytest.mark.asyncio
async def test_arun_basic_with_search_options(tester_search_component):
    # Mock input data
    local_search_input = deepcopy(search_input)
    local_search_input.search_options.enable_source = True

    # Call the arun method
    result = await tester_search_component.arun(
        local_search_input,
        **{"is_local": True, "user_id": "1999849738269549"},
    )

    # Assert the result is an instance of SearchOutput
    assert isinstance(result, SearchOutput)
    assert len(result.search_result) > 0
    assert len(result.search_info.values()) > 0
