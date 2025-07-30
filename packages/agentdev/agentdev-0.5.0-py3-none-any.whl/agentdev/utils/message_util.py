# -*- coding: utf-8 -*-
from openai.types.chat import ChatCompletionChunk
from typing import List, Optional

from agentdev.schemas.message_schemas import (
    ToolCall,
    ToolCallFunction,
    PromptMessageRole,
)


# TODO: add this for streaming structured output support later
def merge_incremental_chunk(
    responses: List[ChatCompletionChunk],
) -> Optional[ChatCompletionChunk]:
    """
    Convert an incremental chunk to a ChatCompletionChunk.
    """

    if len(responses) == 0:
        return None

    # get usage or finish reason
    merged = ChatCompletionChunk(**responses[-1].__dict__)

    # if the responses has usage info, then merge the finish reason chunk to
    # usage chunk
    if not merged.choices and len(responses) > 1:
        merged.choices = responses[-2].choices

    # might be multiple tool calls result
    tool_calls_dict = {}

    for resp in reversed(responses[:-1]):
        for i, j in zip(merged.choices, resp.choices):
            # jump the finish reason chunk
            if (i.delta.content is None and j.delta.content is not None) and (
                i.delta.tool_calls is None and j.delta.tool_calls is not None
            ):
                continue
            elif j.delta.role == PromptMessageRole.TOOL.value:
                continue
            # merge content
            elif not i.delta.content and isinstance(j.delta.content, str):
                i.delta.content = j.delta.content
            elif isinstance(i.delta.content, str) and isinstance(
                j.delta.content,
                str,
            ):
                i.delta.content = j.delta.content + i.delta.content

            # merge tool calls
            elif not i.delta.tool_calls and isinstance(
                j.delta.tool_calls,
                list,
            ):
                for tool_call in j.delta.tool_calls:
                    if tool_call.index not in tool_calls_dict:
                        tool_calls_dict[tool_call.index] = tool_call
                        # make sure function.arguments is a string
                        if not tool_call.function.arguments:
                            tool_calls_dict[
                                tool_call.index
                            ].function.arguments = ""
                    else:
                        if tool_call.id != "":
                            tool_calls_dict[tool_call.index].id = tool_call.id
                        if tool_call.function.name:
                            tool_calls_dict[tool_call.index].function.name = (
                                tool_call.function.name
                            )
                        if (
                            tool_call.function.arguments
                            and not tool_calls_dict[
                                tool_call.index
                            ].function.arguments.startswith("{")
                        ):
                            tool_calls_dict[
                                tool_call.index
                            ].function.arguments = (
                                tool_call.function.arguments
                                + tool_calls_dict[
                                    tool_call.index
                                ].function.arguments
                            )

        if merged.usage and resp.usage:
            merged.usage.prompt_tokens += resp.usage.prompt_tokens
            merged.usage.completion_tokens += resp.usage.completion_tokens
            merged.usage.total_tokens += resp.usage.total_tokens

    if tool_calls_dict:
        merged.choices[0].delta.tool_calls = [
            ToolCall(
                id=tool_call.id,
                type=tool_call.type,
                function=ToolCallFunction(**tool_call.function.__dict__),
            )
            for tool_call in tool_calls_dict.values()
        ]
    return merged
