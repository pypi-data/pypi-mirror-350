# -*- coding: utf-8 -*-
import os
import pytest
from unittest.mock import patch

from agentdev.components.bailian_rag import (
    BailianRag,
    PromptMessage,
    RagInput,
    RagOutput,
)


@pytest.fixture
def rag_component():
    return BailianRag()


def test_arun_success(rag_component):
    messages = [
        {
            "role": "system",
            "content": """
你是一位经验丰富的手机导购，任务是帮助客户对比手机参数，分析客户需求，推荐个性化建议。
# 知识库
请记住以下材料，他们可能对回答问题有帮助。
${documents}
""",
        },
        {"role": "user", "content": "有什么可以推荐的2000左右手机？"},
    ]

    # Prepare input data
    input_data = RagInput(
        messages=messages,
        workspace_id="llm-vcvpy43k0y1w2aes",
        rag_options={"pipeline_ids": ["0tgx5dbmv1"]},
        rest_token=2000,
    )

    # Call the _arun method
    result = rag_component.run(input_data)

    # Assertions to verify the result
    assert isinstance(result, RagOutput)
    assert isinstance(result.rag_result, str)
    assert isinstance(result.messages, list)
    assert isinstance(result.messages[0], PromptMessage)
