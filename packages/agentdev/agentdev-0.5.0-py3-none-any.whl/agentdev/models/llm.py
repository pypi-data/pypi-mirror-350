# -*- coding: utf-8 -*-
import json
import os
from typing import (
    Any,
    AsyncGenerator,
    AsyncIterable,
    Dict,
    Generator,
    Generic,
    List,
    Optional,
    Sequence,
    Type,
    TypeVar,
    Union,
    cast,
)

import instructor
from openai import AsyncOpenAI, OpenAI
from openai.types.chat import ChatCompletion, ChatCompletionChunk
from pydantic import BaseModel

from agentdev.base.model import AIModel, ModelType
from agentdev.constants import BASE_URL, DEFAULT_SYSTEM
from agentdev.schemas.bailian_message_schemas import (
    BailianMessage,
)
from agentdev.schemas.message_schemas import (
    AssistantPromptMessage,
    AudioMessageContent,
    BailianMessageContent,
    ImageMessageContent,
    Parameters,
    PromptMessage,
    PromptMessageRole,
    SystemPromptMessage,
    TextMessageContent,
    ToolPromptMessage,
    UserPromptMessage,
)
from agentdev.tracing import TraceType
from agentdev.tracing.wrapper import trace

MessageT = TypeVar("MessageT", bound=PromptMessage, contravariant=True)
ParamsT = TypeVar("ParamsT", bound=Parameters, contravariant=True)
StructReturnT = TypeVar("StructReturnT", bound=BaseModel, contravariant=True)
LlmReturnT = TypeVar(
    "LlmReturnT",
    bound=Union[
        ChatCompletion,
        ChatCompletionChunk,
        AsyncGenerator[ChatCompletionChunk, Any],
        BaseModel,
        AsyncGenerator[BaseModel, Any],
    ],
    covariant=True,
)


class BaseLLM(AIModel, Generic[MessageT, ParamsT, StructReturnT, LlmReturnT]):
    """
    Base class for LLM (Language Model) implementations.

    This class provides a generic interface for different types of LLMs and
    ensures that they can be used in a consistent manner. It defines the `run`
    method with multiple overloads to support different input types and a
    generic return type.
    """

    client: Optional[
        Union[OpenAI, AsyncOpenAI, instructor.client.Instructor]
    ] = None

    def __init__(self, **kwargs: Any):
        """
        Abstract method to initialize the LLM with generic prompt messages and
        parameters.

        """
        super().__init__(model_type=ModelType.LLM, **kwargs)
        client = kwargs.get("client", None)
        if not client:
            self.client = self.get_client(**kwargs)
        else:
            self.client = client

    def model_dump_json(self) -> str:
        info = {"model_type": str(self.model_type), "client": str(self.client)}
        return json.dumps(info)

    @classmethod
    def get_client(
        cls,
        api_key: str = os.getenv("DASHSCOPE_API_KEY", ""),
        base_url: str = BASE_URL,
        **kwargs: Any,
    ) -> Union[OpenAI, AsyncOpenAI]:
        """
        Get a llm client from openai compatible service
        Args:
            api_key:  api key of the openai compatible service
            base_url: base url for the openai compatible service

        Returns:

        """

        if not api_key:
            raise ValueError(
                "DASHSCOPE_API_KEY is not set, or Other OPENAI compatible "
                "api-key is not set",
            )
        _client = AsyncOpenAI(api_key=api_key, base_url=base_url)
        return _client

    @classmethod
    def from_instructor_client(cls, **kwargs: Any) -> "BaseLLM":
        _client = cls.get_client(**kwargs)
        _client = instructor.from_openai(_client)
        return cls(client=_client, **kwargs)

    async def arun(
        self,
        model: str,
        messages: Sequence[Union[MessageT, Dict]],
        parameters: Union[ParamsT, Dict] = None,
        response_model: Optional[Type[StructReturnT]] = None,
        **kwargs: Any,
    ) -> LlmReturnT:
        """
        Main method to run the LLM with the given prompt messages and
        parameters.

        Args:
           Args:
            model: model name messages (List[MessageT]): The prompt messages.
            parameters (ParamsT): The parameters for the LLM. response_model
            (Optional[StructReturnT]): used for structured output **kwargs:
            Other arguments if needed

        Returns:
            LlmReturnT: The completion result.
        """
        # update the api key if passed
        api_key = kwargs.get("api_key", None)

        if api_key:
            # is_instructor = isinstance(self.client,
            # instructor.client.Instructor) and response_model
            self.client = AsyncOpenAI(api_key=api_key, base_url=BASE_URL)
            if response_model:
                self.client = instructor.from_openai(self.client)

        # support dict message
        if isinstance(messages[0], dict):
            formatted_messages: List[PromptMessage] = [
                PromptMessage(**message) for message in messages
            ]
        else:
            formatted_messages = messages

        # support dict parameters
        if isinstance(parameters, dict):
            parameters: Parameters = Parameters(**parameters)

        if (
            len(formatted_messages) > 0
            and formatted_messages[0].role != PromptMessageRole.SYSTEM.value
        ):
            # insert the system message
            formatted_messages.insert(
                0,
                SystemPromptMessage(content=DEFAULT_SYSTEM),
            )

        extra_model_kwargs = {}

        # make sure the parameters is an openai parameters
        if parameters and type(parameters) is not Parameters:
            parameters = Parameters(
                **parameters.model_dump(exclude_none=True, exclude_unset=True),
            )
        parameters = (
            parameters.model_dump(exclude_none=True, exclude_unset=True)
            if parameters
            else {}
        )

        response_format = parameters.get("response_format")
        if response_format:
            if response_format == "json_schema":
                json_schema = parameters.get("json_schema")
                if not json_schema:
                    raise ValueError(
                        "Must define JSON Schema when the response format is json_schema",  # noqa E501
                    )
                try:
                    schema = json.loads(json_schema)
                except Exception:
                    raise ValueError(
                        f"not correct json_schema format: {json_schema}",
                    )
                parameters.pop("json_schema")
                parameters["response_format"] = {
                    "type": "json_schema",
                    "json_schema": schema,
                }
            else:
                parameters["response_format"] = {"type": response_format}

        dict_messages: List[Any] = [
            self._convert_prompt_message_to_dict(m) for m in formatted_messages
        ]

        if response_model:
            # TODO: response model is used for structured output,
            #  not compatible with function calling for now
            extra_model_kwargs["response_model"] = response_model
            # todo: change from create_partial to create, double check
            response = await self.client.chat.completions.create(
                model=model,
                stream=False,
                messages=dict_messages,
                **parameters,
                **extra_model_kwargs,
            )
        else:
            response = await self.client.chat.completions.create(
                model=model,
                stream=False,
                messages=dict_messages,
                **parameters,
                **extra_model_kwargs,
            )
        return response

    @trace(TraceType.LLM)
    async def astream(
        self,
        model: str,
        messages: Sequence[Union[MessageT, Dict]],
        parameters: ParamsT = None,
        response_model: Optional[Type[StructReturnT]] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[ChatCompletionChunk, Any]:
        responses = await self._astream(
            model=model,
            messages=messages,
            parameters=parameters,
            response_model=response_model,
            **kwargs,
        )

        async for response in responses:
            yield response

    async def astream_unwrapped(
        self,
        model: str,
        messages: Sequence[Union[PromptMessage, Dict]],
        parameters: ParamsT = None,
        response_model: Optional[Type[StructReturnT]] = None,
        **kwargs: Any,
    ) -> AsyncGenerator[ChatCompletionChunk, Any]:
        responses = await self._astream(
            model=model,
            messages=messages,
            parameters=parameters,
            response_model=response_model,
            **kwargs,
        )

        async for response in responses:
            yield response

    async def _astream(
        self,
        model: str,
        messages: Sequence[Union[MessageT, Dict]],
        parameters: ParamsT = None,
        response_model: Optional[Type[StructReturnT]] = None,
        **kwargs: Any,
    ) -> LlmReturnT:
        """
        Main method to run the LLM with the given prompt messages and
        parameters.

        Args:
           Args:
            model: model name
            messages (List[MessageT]): The prompt messages.
            parameters (ParamsT): The parameters for the LLM.
            response_model (Optional[StructReturnT]): used for structured
            output
            **kwargs: Other arguments if needed

        Returns:
            LlmReturnT: The completion result.
        """
        # update the api key
        api_key = kwargs.get("api_key", None)
        if api_key:
            is_instructor = isinstance(
                self.client,
                instructor.client.Instructor,
            )
            self.client = AsyncOpenAI(api_key=api_key, base_url=BASE_URL)
            if is_instructor:
                self.client = instructor.from_openai(self.client)

        # support dict message
        if isinstance(messages[0], dict):
            formatted_messages: List[PromptMessage] = [
                PromptMessage(**message) for message in messages
            ]
        else:
            formatted_messages = messages

        if (
            len(formatted_messages) > 0
            and formatted_messages[0].role != PromptMessageRole.SYSTEM.value
        ):
            # insert the system message
            formatted_messages.insert(
                0,
                SystemPromptMessage(content=DEFAULT_SYSTEM),
            )

        extra_model_kwargs = {}

        # make sure the parameters is an openai parameters
        if parameters and type(parameters) is not Parameters:
            parameters = Parameters(
                **parameters.model_dump(exclude_none=True, exclude_unset=True),
            )

        parameters = (
            parameters.model_dump(exclude_none=True, exclude_unset=True)
            if parameters
            else {}
        )
        parameters.pop("stream")
        parameters["stream_options"] = {"include_usage": True}

        response_format = parameters.get("response_format")
        if response_format:
            if response_format == "json_schema":
                json_schema = parameters.get("json_schema")
                if not json_schema:
                    raise ValueError(
                        "Must define JSON Schema when the response format is json_schema",  # noqa E501
                    )
                try:
                    schema = json.loads(json_schema)
                except Exception:
                    raise ValueError(
                        f"not correct json_schema format: {json_schema}",
                    )
                parameters.pop("json_schema")
                parameters["response_format"] = {
                    "type": "json_schema",
                    "json_schema": schema,
                }
            elif "type" not in response_format:
                parameters["response_format"] = {"type": response_format}

        dict_messages: List[Any] = [
            self._convert_prompt_message_to_dict(m) for m in formatted_messages
        ]

        if response_model:
            # TODO: response model is used for structured output,
            #  not compatible with function calling for now
            extra_model_kwargs["response_model"] = response_model
            response = self.client.chat.completions.create_partial(
                model=model,
                stream=True,
                messages=dict_messages,
                **parameters,
                **extra_model_kwargs,
            )
        else:
            response = await self.client.chat.completions.create(
                model=model,
                stream=True,
                messages=dict_messages,
                **parameters,
                **extra_model_kwargs,
            )
        return response

    @staticmethod
    def transform_response(response: Any) -> str:

        def dump_json_str(obj: Any) -> str:
            """
            Converts an object to a JSON string.
            """
            return json.dumps(
                dump_json(obj),
                ensure_ascii=False,
                default=lambda x: str(x),
            )

        def dump_json(obj: Any) -> Any:
            if isinstance(obj, dict):
                return {k: dump_json(v) for k, v in obj.items()}
            elif isinstance(obj, (tuple, list)):
                return [dump_json(v) for v in obj]
            elif isinstance(obj, BaseModel):
                return obj.model_dump(exclude_unset=True, exclude_none=True)
            elif isinstance(obj, (AsyncGenerator, Generator, AsyncIterable)):
                return str(obj)
            else:
                return obj

        if isinstance(response, str):
            return response
        elif isinstance(response, dict):
            return json.dumps(response, ensure_ascii=False)
        elif isinstance(response, BaseModel):
            return response.model_dump_json(
                exclude_none=True,
                exclude_unset=True,
            )
        else:
            return dump_json_str(response)

    def _convert_prompt_message_to_dict(
        self,
        message: PromptMessage,
    ) -> Dict[str, Any]:
        """
        Convert PromptMessage to dict for OpenAI API
        """
        message_dict: Dict[str, Any] = {}
        if isinstance(message, UserPromptMessage) or isinstance(
            message,
            BailianMessage,
        ):
            if isinstance(message.content, str):
                message_dict = {"role": "user", "content": message.content}
            elif isinstance(message.content, list):
                sub_messages = []
                for message_content in message.content:
                    if isinstance(message_content, TextMessageContent):
                        sub_messages.append(message_content.model_dump())
                    elif isinstance(message_content, ImageMessageContent):
                        sub_message_dict = {
                            "type": "image_url",
                            "image_url": {
                                "url": message_content.image_url.url,
                                "detail": message_content.image_url.detail.value,  # noqa E501
                            },
                        }
                        sub_messages.append(sub_message_dict)
                    elif isinstance(message_content, AudioMessageContent):
                        data_split = message_content.data.split(";base64,")
                        audio_format = data_split[0]
                        base64_data = data_split[1]
                        sub_message_dict = {
                            "type": "input_audio",
                            "input_audio": {
                                "data": base64_data,
                                "format": audio_format,
                            },
                        }
                        sub_messages.append(sub_message_dict)
                    elif isinstance(message_content, BailianMessageContent):
                        sub_message_dict = {}
                        if message_content.text:
                            sub_message_dict = {
                                "type": "text",
                                "text": message_content.text,
                            }
                        elif message_content.image:
                            sub_message_dict = {
                                "type": "image_url",
                                "image_url": {
                                    "url": message_content.image,
                                },
                            }
                        elif message_content.audio:
                            data_split = message_content.audio.split(
                                ";base64,",
                            )
                            audio_format = data_split[0]
                            base64_data = data_split[1]
                            sub_message_dict = {
                                "type": "input_audio",
                                "input_audio": {
                                    "data": base64_data,
                                    "format": audio_format,
                                },
                            }
                        sub_messages.append(sub_message_dict)

                message_dict = {"role": "user", "content": sub_messages}
        elif isinstance(message, AssistantPromptMessage):
            message = cast(AssistantPromptMessage, message)
            message_dict = {"role": "assistant", "content": message.content}
            if message.tool_calls:
                # message_dict["tool_calls"]=[tool_call.dict() for tool_call in
                #                               message.tool_calls]
                function_call = message.tool_calls[0]
                message_dict["function_call"] = {
                    "name": function_call.function.name,
                    "arguments": function_call.function.arguments,
                }
        elif isinstance(message, SystemPromptMessage):
            message = cast(SystemPromptMessage, message)
            if isinstance(message.content, list):
                text_contents = filter(
                    lambda c: isinstance(c, TextMessageContent),
                    message.content,
                )
                message.content = "".join(c.data for c in text_contents)
            message_dict = {"role": "system", "content": message.content}
        elif isinstance(message, ToolPromptMessage):
            message = cast(ToolPromptMessage, message)
            # message_dict = {
            #     "role": "tool",
            #     "content": message.content,
            #     "tool_call_id": message.tool_call_id
            # }
            message_dict = {
                "role": "function",
                "content": message.content,
                "name": message.tool_call_id,
            }
        elif isinstance(message, PromptMessage) and message.role in [
            "system",
            "function",
            "user",
            "assistant",
        ]:
            # in the case pass in a plain PromptMessage
            message_dict = {
                "role": message.role,
                "content": message.model_dump()["content"],
            }
        else:
            raise ValueError(f"Got unknown type {message}")

        if message.name:
            message_dict["name"] = message.name

        return message_dict

    def _convert_messages_to_prompt(self, messages: List[MessageT]) -> str:
        im_start = "<|im_start|>"
        im_end = "<|im_end|>"
        system_content = ""

        if isinstance(messages[0], SystemPromptMessage):
            if isinstance(messages[0].content, list):
                for c in messages[0].content:
                    if isinstance(c, TextMessageContent) or isinstance(
                        c,
                        BailianMessageContent,
                    ):
                        system_content += c.text or ""
            elif isinstance(messages[0].content, str):
                system_content = messages[0].content
        system_messages = [
            m for m in messages[1:] if isinstance(m, SystemPromptMessage)
        ]
        if system_messages:
            for m in system_messages:
                if isinstance(m.content, list):
                    for c in m.content:
                        if isinstance(c, TextMessageContent) or isinstance(
                            c,
                            BailianMessageContent,
                        ):
                            system_content += c.text or ""
                elif isinstance(m.content, str):
                    system_content += m.content
        prompt = (
            f"{im_start}{SystemPromptMessage.role}\n{system_content}{im_end}"
        )
        for message in messages[:-1]:
            if isinstance(message, UserPromptMessage):
                prompt += (
                    f"{im_start}{UserPromptMessage.role}\n"
                    f"{message.content}{im_end}"
                )
            elif isinstance(message, AssistantPromptMessage):
                prompt += (
                    f"{im_start}{AssistantPromptMessage.role}\n"
                    f"{message.content}{im_end}"
                )
            elif isinstance(message, ToolPromptMessage):
                # TODO: need to double check the logic here
                pass
            else:
                raise ValueError(f"Got unknown type {message}")
        return prompt
