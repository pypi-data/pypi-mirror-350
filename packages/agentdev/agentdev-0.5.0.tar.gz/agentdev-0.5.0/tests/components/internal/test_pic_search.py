# -*- coding: utf-8 -*-
import asyncio
import pytest
from copy import deepcopy

from agentdev.components.internal.pic_searcher import (
    PicSearcher,
    PicSearchInput,
    PicSearchOutput,
)
from agentdev.schemas.message_schemas import PromptMessage

pic_search_input = PicSearchInput(query="拉布拉多图片")


@pytest.fixture
def tester_pic_search_component(mocker):
    # Create an instance of QueryParsing
    pic_search_component = PicSearcher()
    return pic_search_component


@pytest.mark.asyncio
async def test_arun_basic(tester_pic_search_component):
    # Mock input data

    # Call the arun method
    result = await tester_pic_search_component.arun(pic_search_input)

    # Assert the result is an instance of PicSearchOutput
    assert isinstance(result, PicSearchOutput)
