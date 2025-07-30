# -*- coding: utf-8 -*-
import os
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, StrictInt, field_validator, model_validator

from agentdev.errors.service_errors import InvalidParameter
from .message_schemas import (
    AssistantPromptMessage,
    Parameters,
    PromptMessage,
    PromptMessageFunction,
    SystemPromptMessage,
    ToolCall,
    UserPromptMessage,
)


class ToolType(Enum):
    PLUGIN = 0  # internal tool
    EXTERNAL_API = 1  # external tool
    BAILIAN_PLUGIN = 2  # plugin from bailian platform
    SYSTEM_PROMPT = 3  # only for system prompt
    USER_FUNCTION = 4  # function call only, execute on user side
    STUB_FUNCTION = 5  # virtual tool, has only name


class ToolMeta(BaseModel):
    id: Optional[str] = None
    type: Optional[ToolType] = ToolType.SYSTEM_PROMPT
    tool_name: str = None
    tool_schema: Optional[PromptMessageFunction] = None
    tool_call: Optional[ToolCall] = None
    result: Optional[Any] = None
    examples: Union[List[dict], None] = (
        None  # 输入样例，[{'query': '样例query', 'parameters': {'key1': 'value1'}}]
    )
    score: Optional[float] = None
    tool_object: Optional[Any] = None


class KnowledgeHolder(BaseModel):
    source: str
    content: str


class IntentionOptions(BaseModel):
    white_list: List[str] = []
    black_list: List[str] = []
    search_model: str = "search_v6"
    intensity: Optional[int] = None
    scene_id: Optional[str] = None


class SearchOptions(BaseModel):
    """
    Search Options on Bailian
    """

    enable_source: bool = False
    enable_citation: bool = False
    enable_readpage: bool = False
    enable_online_read: bool = False
    citation_format: str = "[<number>]"
    search_strategy: str = "standard"
    forced_search: bool = False
    prepend_search_result: bool = False
    enable_search_extension: bool = False
    item_cnt: int = 20000
    top_n: int = 0
    intention_options: Union[IntentionOptions, None] = IntentionOptions()


# 知识库拼装片段数范围 [1, 20]
PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MIN = os.getenv(
    "PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MIN",
    1,
)
PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MAX = os.getenv(
    "PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MAX",
    20,
)


class RagOptions(BaseModel):

    class FallbackOptions(BaseModel):
        default_response_type: Optional[str] = "llm"
        default_response: Optional[str] = ""

    replaced_word: str = "${documents}"
    pipeline_ids: Optional[List[str]] = []
    file_ids: Optional[List[str]] = []
    prompt_strategy: Optional[str] = "top_k"
    maximum_allowed_chunk_num: Optional[int] = 5
    maximum_allowed_length: Optional[int] = 2000
    enable_citation: bool = False
    fallback_options: Optional[FallbackOptions] = None
    enable_web_search: bool = False
    session_file_ids: Optional[List[str]] = []

    @field_validator("prompt_strategy")
    def prompt_strategy_check(cls, value: str) -> str:
        if value:
            value = value.lower()
            if value in ["topk", "top_K", "topK"]:
                return "top_k"
        return value

    @field_validator("maximum_allowed_chunk_num")
    def maximum_allowed_chunk_num_check(cls, value: int) -> int:
        if value < int(PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MIN) or value > int(
            PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MAX,
        ):
            raise KeyError(
                f"Range of maximum_allowed_chunk_num should be "
                f"[{PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MIN}, "
                f"{PARAM_MAXIMUM_ALLOWED_CHUNK_NUM_MAX}]",
            )
        return value


class BailianParameters(Parameters):
    """
    Parameters for Bailian only
    """

    repetition_penalty: Union[float, None] = None
    length_penalty: Union[float, None] = None

    top_k: Union[StrictInt, None] = None
    min_tokens: Optional[int] = None

    result_format: Literal["text", "message"] = "message"
    incremental_output: bool = False

    # Search
    enable_search: bool = False
    search_options: Optional[SearchOptions] = SearchOptions()

    # RAG
    enable_rag: bool = False  # rag of bailian assistant service
    rag_options: Union[RagOptions, None] = None
    selected_model: Optional[str] = "qwen-max"

    # Intention
    intention_options: Optional[IntentionOptions] = None

    # MCP Servers
    mcp_config_file: Optional[str] = None


class BailianMessage(PromptMessage):
    """
    Model class for bailian message.
    """

    role: str
    tool_calls: Optional[List[ToolCall]] = None
    function_call: Optional[ToolCall] = None
    plugin_call: Optional[ToolCall] = None
    tool_call_id: Optional[str] = None

    @classmethod
    def from_messages(
        cls,
        messages: List[
            Union[
                UserPromptMessage,
                AssistantPromptMessage,
                SystemPromptMessage,
            ]
        ],
    ) -> List["BailianMessage"]:
        """
        Convert a list of UserPromptMessage, AssistantPromptMessage,
        and SystemPromptMessage to a list of BailianMessage.

        :param messages: List of different types of prompt messages
        :return: List of BailianMessage
        """
        return [cls(**message.model_dump()) for message in messages]

    @classmethod
    @model_validator(mode="before")
    def validate_content(cls, v: Dict[str, Any]) -> Dict[str, Any]:
        role, content = v.get("role"), v.get("content")
        if not isinstance(content, str) and role != "user":
            raise InvalidParameter(
                f"content must be type of str when role is {role}",
            )

        tool_call_id = v.get("tool_call_id")
        if tool_call_id is not None and role != "tool":
            raise InvalidParameter(
                f"tool_call_id must be None when role is {role}",
            )

        tool_calls = v.get("tool_calls")
        if tool_calls is not None and role != "assistant":
            raise InvalidParameter(
                f"tool_calls must be None when role is {role}",
            )
        return v
