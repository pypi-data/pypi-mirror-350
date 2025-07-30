# -*- coding: utf-8 -*-
import asyncio
import pytest
from copy import deepcopy

from agentdev.components.internal.query_parsing import (
    ParsingInput,
    ParsingOutput,
    QueryParsingComponent,
)
from agentdev.schemas.message_schemas import PromptMessage

parsing_input = ParsingInput(
    query="周杰伦的双截棍",
    schema={"singer": "描述：歌手名", "song": "描述：歌名"},
)


@pytest.fixture
def tester_query_parsing_component(mocker):
    # Create an instance of QueryParsing
    query_parsing_component = QueryParsingComponent()
    return query_parsing_component


@pytest.mark.asyncio
async def test_arun_basic(tester_query_parsing_component):
    # Mock input data

    # Call the arun method
    result = await tester_query_parsing_component.arun(parsing_input)

    # Assert the result is an instance of ParsingOutput
    assert isinstance(result, ParsingOutput)
