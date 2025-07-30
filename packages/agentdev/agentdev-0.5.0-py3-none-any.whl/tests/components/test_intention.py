# -*- coding: utf-8 -*-
import pytest

from agentdev.components.bailian_intention_center import (
    IntentionCenter,
    IntentionInput,
    IntentionOutput,
)


@pytest.fixture
def intention_component():
    return IntentionCenter()


def test_arun_success(intention_component):
    # Mock API response
    messages = [{"role": "user", "content": "帮我查一下南京的天气？"}]

    # Prepare input
    input_data = IntentionInput(messages=messages)

    # Call _arun
    result = intention_component.run(input_data)

    # Verify result
    assert isinstance(result, IntentionOutput)
    assert "search" in result.labels
