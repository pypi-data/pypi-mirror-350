# -*- coding: utf-8 -*-
class TraceType(str):
    """Callback manager event types.

    Attributes:
        LLM: Logs for the template and response of LLM calls.
        TOOL：Logs for the tool name and its arguments and
            the output of tool calls
        AGENT_STEP: Logs for the agent loop start and end?
    """

    # Officially supported event types
    LLM = "llm"
    TOOL = "tool"
    AGENT_STEP = "agent_step"
    SEARCH = "search"
    IMAGE_GENERATION = "image_generation"
    RAG = "rag"
    INTENTION = "intention"
    PLUGIN_CENTER = "plugin_center"

    def __init__(self, value: str):
        if not isinstance(value, str):
            raise ValueError(
                f"TraceType value must be a string, got {type(value)}",
            )
        self._value_ = value

    def __str__(self) -> str:
        return self._value_

    def __repr__(self) -> str:
        return f"TraceType({self._value_})"

    @classmethod
    def add_type(cls, name: str, value: str) -> None:
        if not isinstance(name, str) or not isinstance(value, str):
            raise ValueError("Name and value must be strings")
        if hasattr(cls, name):
            raise ValueError(f"TraceType {name} already exists")
        setattr(cls, name, cls(value))
