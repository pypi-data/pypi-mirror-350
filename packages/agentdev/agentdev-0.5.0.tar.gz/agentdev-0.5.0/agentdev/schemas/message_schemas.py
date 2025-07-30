# -*- coding: utf-8 -*-
import json
import time
import uuid
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from openai.types.chat import ChatCompletion, ChatCompletionChunk
from openai.types.chat.chat_completion_stream_options_param import (
    ChatCompletionStreamOptionsParam,
)
from pydantic import BaseModel, Field, model_validator
from typing_extensions import Annotated, Literal

from agentdev.errors import BailianError


def generate_tool_call_id(prefix: str = "call_") -> str:
    #  generate a random uuid
    random_uuid = uuid.uuid4()
    # replace uuid to string and remove '-', then get latest 22 characters
    random_part = str(random_uuid).replace("-", "")[:22]
    # add prefix
    tool_call_id = f"{prefix}{random_part}"
    return tool_call_id


class ToolChoiceInputFunction(BaseModel):
    name: str


class ToolChoice(BaseModel):
    type: str
    function: ToolChoiceInputFunction


class ParametersSchema(BaseModel):
    type: str
    properties: Dict[str, Any]
    required: Optional[List[str]]


class PromptMessageTool(BaseModel):
    """
    Model class for prompt message tool.
    """

    name: str
    description: str
    parameters: Union[Dict[str, Any], ParametersSchema]


class PromptMessageFunction(BaseModel):
    """
    Model class for prompt message function.
    """

    type: str = "function"
    function: PromptMessageTool


class PromptMessageRole(Enum):
    """
    Enum class for prompt message.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

    @classmethod
    def value_of(cls, value: str) -> "PromptMessageRole":
        """
        Get value of given mode.

        :param value: mode value
        :return: mode
        """
        for mode in cls:
            if mode.value == value:
                return mode
        raise ValueError(f"invalid prompt message type value {value}")


class PromptMessageContentType(Enum):
    """
    Enum class for prompt message content type.
    """

    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"


class BailianMessageContent(BaseModel):
    """
    only for qwen on dashscope
    """

    text: Union[str, None] = None
    image: Union[str, None] = None
    audio: Union[str, None] = None
    video: Union[str, List[str], None] = None
    box: Union[str, None] = None
    file_path: str = Field(None, alias="file")

    # qwen2-vl
    noteId: Union[str, None] = None
    noteTag: Union[str, None] = None
    min_pixels: Union[int, None] = None
    max_pixels: Union[int, None] = None
    fps: Union[float, None] = None


class ImageMessageContent(BaseModel):

    class ImageUrlDetail(BaseModel):
        """
        Model class for image prompt message content.
        """

        class DETAIL(Enum):
            LOW = "low"
            HIGH = "high"
            AUTO = "auto"

        url: str
        detail: DETAIL = DETAIL.LOW

    type: Literal["image_url"]
    image_url: ImageUrlDetail


class TextMessageContent(BaseModel):
    type: Literal["text"]
    text: str


class AudioMessageContent(BaseModel):

    class InputAudioDetail(BaseModel):
        """
        Model class for image prompt message content.
        """

        base64_data: str = Field(
            default="",
            description="the base64 data of multi-modal file",
        )
        format: str = Field(
            default="mp3",
            description="The format of the encoded audio data.  supports "
            "'wav' and 'mp3'.",
        )

        @property
        def data(self) -> str:
            return f"data:{self.format};base64,{self.base64_data}"

    type: Literal["input_audio"]
    input_audio: InputAudioDetail


ChatCompletionMessage = Annotated[
    Union[TextMessageContent, ImageMessageContent, AudioMessageContent],
    Field(discriminator="type"),
]


class ToolCallFunction(BaseModel):
    """
    Model class for assistant prompt message tool call function.
    """

    name: str
    arguments: str

    # for bailian open source
    output: Optional[str] = None


class ToolCall(BaseModel):
    """
    Model class for assistant prompt message tool call.
    """

    index: int = 0
    id: str
    type: Optional[str] = None
    function: ToolCallFunction


class PromptMessage(BaseModel):
    """
    Model class for prompt message.
    """

    role: str
    content: Union[
        str | List[ChatCompletionMessage] | List[BailianMessageContent]
    ] = None
    name: Optional[str] = None


class UserPromptMessage(PromptMessage):
    """
    Model class for user prompt message.
    """

    role: str = PromptMessageRole.USER.value


class AssistantPromptMessage(PromptMessage):
    """
    Model class for assistant prompt message.
    """

    role: str = PromptMessageRole.ASSISTANT.value
    tool_calls: Optional[List[ToolCall]] = None
    function_call: Optional[ToolCall] = None
    plugin_call: Optional[ToolCall] = None


class SystemPromptMessage(PromptMessage):
    """
    Model class for system prompt message.
    """

    role: str = PromptMessageRole.SYSTEM.value


class ToolPromptMessage(PromptMessage):
    """
    Model class for tool prompt message.
    """

    role: str = PromptMessageRole.TOOL.value
    tool_call_id: str

    def is_empty(self) -> bool:
        """
        Check if prompt message is empty.

        :return: True if prompt message is empty, False otherwise
        """
        if not super().is_empty() and not self.tool_call_id:
            return False

        return True


class ResponseFormat(BaseModel):

    class JsonSchema(BaseModel):
        name: str
        description: Union[str, None] = None
        schema_param: dict = Field(None, alias="schema")
        strict: Union[bool, None] = False

    type: Literal["text", "json_object", "json_schema"] = "text"
    json_schema: Optional[JsonSchema] = None

    @model_validator(mode="before")
    def validate_schema(cls, values: dict) -> dict:
        if not isinstance(values, dict) or "type" not in values:
            raise ValueError(f"Json schem not valid with type {type(values)}")
        format_type = values.get("type")
        json_schema = values.get("json_schema")

        if format_type in ["text", "json_object"] and json_schema is not None:
            raise ValueError(
                f"Json schem is not allowed for type {format_type}",
            )

        if format_type == "json_schema":
            if json_schema is None:
                raise ValueError(
                    f"Json schem is required for type {format_type}",
                )
        return values


class Parameters(BaseModel):
    """
    General Parameters for LLM
    """

    top_p: Optional[float] = None
    temperature: Optional[float] = None

    frequency_penalty: Optional[float] = None
    presence_penalty: Optional[float] = None

    max_tokens: Optional[int] = None

    stop: Optional[Union[Optional[str], List[str]]] = None
    stream: bool = True
    stream_options: Optional[ChatCompletionStreamOptionsParam] = None

    tools: Optional[List[Union[PromptMessageFunction, Dict]]] = None
    tool_choice: Optional[Union[str, ToolChoice]] = None
    parallel_tool_calls: bool = False

    logit_bias: Optional[Dict[str, int]] = None
    top_logprobs: Optional[int] = None
    logprobs: Optional[bool] = None

    n: Optional[int] = Field(default=1, ge=1, le=5)
    seed: Optional[int] = None

    response_format: Optional[Union[ResponseFormat, str]] = ResponseFormat(
        type="text",
    )


def get_message_content(message: PromptMessage) -> Optional[str]:
    if isinstance(message.content, list):
        for item in message.content:
            if isinstance(item, BailianMessageContent):
                return item.text
            else:
                if isinstance(item, TextMessageContent):
                    return item.text
                elif isinstance(item, ImageMessageContent) or isinstance(
                    item,
                    AudioMessageContent,
                ):
                    continue
                else:
                    return None
        return None
    else:
        return message.content


def create_chat_completion(
    message: PromptMessage,
    model_name: str,
    id: str = "",
    finish_reason: Optional[str] = None,
) -> ChatCompletion:
    # Create Choice object
    choice = {
        "finish_reason": finish_reason,
        "index": 0,
        "message": message.model_dump(),
        "logprobs": None,
    }

    # Construct ChatCompletion object
    return ChatCompletion(
        id=id,  # Generate unique ID
        choices=[choice],  # List containing at least one Choice
        created=int(time.time()),  # Current timestamp
        model=model_name,  # Adjust based on actual model used
        object="chat.completion",  # Fixed literal value
        # Optional fields below
        service_tier=None,
        system_fingerprint=None,
        usage=None,
    )


def create_chat_completion_chunk(
    message: PromptMessage,
    model_name: str,
    id: str = "",
    finish_reason: Optional[str] = None,
) -> ChatCompletionChunk:
    # Create Choice object for chunk
    choice = {
        "finish_reason": finish_reason,
        "index": 0,
        "logprobs": None,
        "delta": message.model_dump(),
    }

    # Construct ChatCompletionChunk object
    return ChatCompletionChunk(
        id=id,  # Generate unique ID
        choices=[choice],  # List containing at least one Choice
        created=int(time.time()),  # Current timestamp
        model=model_name,  # Adjust based on actual model used
        object="chat.completion.chunk",  # Fixed literal value
        # Optional fields below
        service_tier=None,
        system_fingerprint=None,
        usage=None,
    )


def is_json_string(s: Union[str, Dict, BaseModel, None]) -> bool:
    try:
        obj = json.loads(s)  # type: ignore[arg-type]
        if isinstance(obj, (dict, list)):
            return True
        return False
    except Exception:
        return False


def create_success_result(
    request_id: str,
    output: Union[str, Dict, BaseModel, None] = None,
) -> str:
    if output:
        if is_json_string(output):
            result = json.loads(output)  # type: ignore[arg-type]
        elif isinstance(output, str):
            result = {"output": output}
        elif isinstance(output, dict):
            result = output
        elif isinstance(output, BaseModel):
            result = output.model_dump()
        else:
            result = {"output": str(output)}
    else:
        result = {}

    result["request_id"] = request_id

    return json.dumps(result, ensure_ascii=False)


def create_error_response(request_id: str, error: Exception) -> str:
    new_error = error
    if not isinstance(error, BailianError):
        new_error = BailianError(str(error))

    result = {
        "request_id": request_id,
        "error": {
            "code": new_error.code,
            "type": new_error.type,
            "name": new_error.name,
            "message": new_error.message,
        },
    }

    return json.dumps(result, ensure_ascii=False)


def create_dashscope_success_response(
    request_id: str,
    header: Union[Dict, BaseModel, None] = None,
    payload: Union[str, Dict, BaseModel, None] = None,
    finished: bool = False,
) -> str:
    if header:
        header_dict = (
            header if isinstance(header, dict) else header.model_dump()
        )
    else:
        header_dict = {}

    if payload:
        if is_json_string(payload):
            payload_dict = json.loads(payload)  # type: ignore[arg-type]
        elif isinstance(payload, str):
            payload_dict = {"output": payload}
        elif isinstance(payload, dict):
            payload_dict = payload
        elif isinstance(payload, BaseModel):
            payload_dict = payload.model_dump()
        else:
            payload_dict = {"output": str(payload)}
    else:
        payload_dict = {}

    header_dict.update(
        {
            "status_code": 200,
            "status_type": "Success",
            "status_name": "Success",
            "status_message": "success",
            "finished": finished,
            "request_id": request_id,
        },
    )

    result = {"header": header_dict, "payload": payload_dict}

    return json.dumps(result, ensure_ascii=False)


def create_dashscope_error_response(
    request_id: str,
    error: Exception,
    header: Union[Dict, BaseModel, None] = None,
) -> str:
    new_error = error
    if not isinstance(error, BailianError):
        new_error = BailianError(str(error))

    if header:
        header_dict = (
            header if isinstance(header, dict) else header.model_dump()
        )
    else:
        header_dict = {}

    header_dict.update(
        {
            "request_id": request_id if request_id else new_error.request_id,
            "status_code": new_error.code,
            "status_type": new_error.type,
            "status_name": new_error.name,
            "status_message": new_error.message,
            "finished": True,
        },
    )

    result = {"header": header_dict, "payload": {}}

    return json.dumps(result, ensure_ascii=False)
