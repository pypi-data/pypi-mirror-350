# -*- coding: utf-8 -*-
import asyncio
from typing import (
    Any,
    AsyncGenerator,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Sequence,
    Union,
)

from openai.types.chat import ChatCompletion, ChatCompletionChunk

from agentdev.base.component import Component
from agentdev.mcp_utils.server import MCPServer
from agentdev.models.llm import BaseLLM
from agentdev.schemas.message_schemas import (
    AssistantPromptMessage,
    Parameters,
    PromptMessage,
    PromptMessageFunction,
    PromptMessageRole,
    ToolCall,
    ToolCallFunction,
    ToolPromptMessage,
    create_chat_completion_chunk,
)
from agentdev.tracing.wrapper import trace
from agentdev.utils.message_util import merge_incremental_chunk


async def execute_tool_call(
    tool_calls: List[Union[ToolCall, Dict]],
    tools: Optional[Mapping[str, Union[Component, Callable]]] = None,
    **kwargs: Any,
) -> Dict[str, Any]:
    """
    Execute tool call
    Args:
        tool_calls: the object of ToolCall or dict,
            typically generated from llm response
        tools: the availble callable or component that used to execute
        **kwargs:

    Returns:

    """
    result = {}

    if not tool_calls or not tools:
        return result

    # convert tool_call to ToolCall Object
    formatted_tool_calls = [
        ToolCall(**tool_call) if isinstance(tool_call, dict) else tool_call
        for tool_call in tool_calls
    ]

    async def process_tool_call(tool_call: ToolCall) -> None:
        tool_name = tool_call.function.name
        tool = tools.get(tool_name)
        kwargs["tool_name"] = tool_name
        if tool:
            parameters = tool.verify_args(tool_call.function.arguments)
            tool_response = await tool.arun(parameters, **kwargs)
        else:
            tool_response = None
        result[tool_name] = BaseLLM.transform_response(tool_response)

    await asyncio.gather(
        *[process_tool_call(tool_call) for tool_call in formatted_tool_calls],
    )

    return result


async def execute_tool_call_from_message(
    response: Union[ChatCompletion, ChatCompletionChunk],
    tools: Optional[Mapping[str, Union[Component, Callable]]] = None,
    **kwargs: Any,
) -> List[PromptMessage]:
    """
    Execute function calls in the response.

    Args:
        response: The chat response to process.
        tools: A dictionary of available tools.

    Returns:
        List[PromptMessage]: The list of prompt messages.
    """
    if response.choices[0].finish_reason != "tool_calls":
        return []

    response_message = (
        response.choices[0].delta
        if isinstance(response, ChatCompletionChunk)
        else response.choices[0].message
    )
    tool_calls = response_message.tool_calls

    if not tool_calls or not tools:
        return []
    tool_calls = (
        [
            ToolCall(
                index=tool_call.index,
                id=tool_call.id,
                type=tool_call.type,
                function=ToolCallFunction(**tool_call.function.__dict__),
            )
            for tool_call in tool_calls
        ]
        if tool_calls
        else None
    )
    request_messages: List[PromptMessage] = []
    assistant_response = AssistantPromptMessage(tool_calls=tool_calls)
    if response_message.content:
        assistant_response.content = response_message.content

    request_messages.append(assistant_response)

    tool_call_results = await execute_tool_call(tool_calls, tools, **kwargs)

    for tool_name in tool_call_results:
        request_messages.append(
            ToolPromptMessage(
                content=tool_call_results[tool_name],
                tool_call_id=response.id,
                name=tool_name,
            ),
        )

    return request_messages


def check_available_tools(
    tools: Optional[Sequence[Union[PromptMessageFunction, Dict]]] = None,
    available_components: Optional[
        Dict[str, Union[Component, Callable]]
    ] = None,
) -> Dict[str, Component]:
    """
    return a new dict that include the components with tools name
    Args:
        tools:
        available_components:

    Returns:

    """
    tool_names = []
    if tools:
        for item in tools:
            if isinstance(item, PromptMessageFunction):
                tool_names.append(item.function.name)
            elif isinstance(item, dict):
                tool_names.append(item["function"]["name"])
        result: Dict[str, Any] = {
            k: v for k, v in available_components.items() if k in tool_names
        }
        return result
    else:
        return {}


@trace("function_call_loop")
async def function_call_loop(
    model: str,
    model_cls: BaseLLM,
    messages: List[PromptMessage],
    parameters: Optional[Parameters] = None,
    available_components: Optional[
        Dict[str, Union[Component, Callable]]
    ] = None,
    mcp_servers: Optional[List[MCPServer]] = None,
    **kwargs: Any,
) -> AsyncGenerator[ChatCompletionChunk | None, Any]:

    if mcp_servers:
        from agentdev.utils.mcp_util import MCPUtil

        components = await MCPUtil.get_all_tools(mcp_servers)
        tools = [
            {"type": "function", "function": comp.function_schema.model_dump()}
            for comp in components
        ]

        # update parameters
        base_params = {
            "tools": tools,
            "stream_options": {"include_usage": True},
        }
        if parameters is not None:
            base_params["tools"].extend(parameters.tools)
        parameters = Parameters(**base_params)

        # update available components
        available_components = {
            **(available_components or {}),
            **{comp.name: comp for comp in components},
        }

    allow_incremental_tools_message = kwargs.pop(
        "allow_incremental_tools_message",
        True,
    )
    # no need to valid tools before calling llm
    valid_components = check_available_tools(
        parameters.tools,
        available_components,
    )
    usage_chunks = []

    while True:
        response = model_cls.astream_unwrapped(
            model=model,
            stream=True,
            messages=messages,
            parameters=parameters,
            **kwargs,
        )
        is_more_request = False
        cumulated = []
        async for resp in response:
            if resp.usage:
                usage_chunks.append(resp)
                continue
            if not resp.choices:
                continue
            # if not allow_incremental_tools_message is True, we should not to
            # yield the response
            if not allow_incremental_tools_message and (
                resp.choices[0].delta.tool_calls
                or resp.choices[0].finish_reason == "tool_calls"
            ):
                pass
            else:
                yield resp

            cumulated.append(resp)

            if (
                len(resp.choices) > 0
                and resp.choices[0].finish_reason == "tool_calls"
            ):
                cumulated_resp = merge_incremental_chunk(cumulated)
                if not allow_incremental_tools_message:
                    cumulated_resp.choices[0].delta.role = (
                        PromptMessageRole.ASSISTANT.value
                    )
                    yield cumulated_resp

                tool_response: List[PromptMessage] = (
                    await execute_tool_call_from_message(
                        cumulated_resp,
                        valid_components,
                        **kwargs,
                    )
                )
                # the first response is from the assistant, the others are from
                # the tool calls
                if len(tool_response) > 1:
                    is_more_request = True
                    # TODO: only support one tool response
                    yield create_chat_completion_chunk(
                        message=tool_response[1],
                        model_name=model,
                        finish_reason=None,
                    )
                messages.extend(tool_response)

        if not is_more_request:
            break

    if len(usage_chunks) > 0:
        yield merge_incremental_chunk(usage_chunks)
