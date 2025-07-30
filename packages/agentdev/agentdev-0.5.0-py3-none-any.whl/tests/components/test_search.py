# -*- coding: utf-8 -*-
import os
import pytest
from unittest.mock import patch

from agentdev.components.bailian_search import (
    BailianSearch,
    PromptMessage,
    SearchInput,
    SearchOptions,
    SearchOutput,
)


@pytest.fixture
def search_component():
    return BailianSearch()


def test_arun_success(search_component):
    messages = [{"role": "user", "content": "南京的天气如何？"}]

    # Prepare input data
    input_data = SearchInput(
        messages=messages,
        search_options=SearchOptions(search_strategy="standard"),
    )

    # Call the _arun method
    result = search_component.run(
        input_data,
        **{"user_id": "1202053544550233"},
    )

    # Assertions to verify the result
    assert isinstance(result, SearchOutput)
    assert isinstance(result.search_result, str)
    assert isinstance(result.search_info, dict)
