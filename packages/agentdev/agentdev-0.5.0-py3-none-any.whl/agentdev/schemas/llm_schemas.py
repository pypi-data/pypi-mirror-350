# -*- coding: utf-8 -*-
from typing import List, Optional, TypeVar, Union

from openai.types.chat import ChatCompletion, ChatCompletionChunk
from pydantic import BaseModel, Extra, Field, field_validator

from agentdev.errors.error import BailianError, ErrorModel
from .bailian_message_schemas import (
    BailianMessage,
    BailianParameters,
    Parameters,
)


class Request(BaseModel):
    stream: bool = False


class Response(BaseModel):
    error: Optional[ErrorModel] = None

    @field_validator("error", mode="before")
    def validate_error(cls, v: Union[BailianError, ErrorModel]) -> ErrorModel:
        if isinstance(v, BailianError):
            return ErrorModel.from_exception(v)
        return v


RequestType = TypeVar("RequestType", bound=Request, contravariant=True)
ResponseType = TypeVar("ResponseType", bound=Response, covariant=True)


class BailianChatRequest(Request, Parameters):
    messages: List[BailianMessage]
    model: str


class BailianChatResponse(Response, ChatCompletion):
    pass


class BailianChatCompletionChunk(Response, ChatCompletionChunk):
    pass


class DashscopeChatRequest(Request):

    class DashscopeInput(BaseModel):
        messages: List[BailianMessage]

    model: str
    input: DashscopeInput
    parameters: BailianParameters


class DashscopeInnerUserMeta(BaseModel):
    visit_inner_model: Optional[str] = ""


class BailianAttributes(BaseModel):
    x_dashscope_euid: str = Field("", alias="X-DashScope-EUID")
    x_dashscope_euid_lower: str = Field("", alias="x-dashscope-euid")
    x_dashscope_datainspection: str = Field(
        "",
        alias="x-dashscope-datainspection",
    )
    x_dashscope_euid_api_key_id: str = Field("", alias="x-dashscope-apikeyid")
    x_dashscope_logging_consent: str = Field(
        "",
        alias="x-dashscope-loggingconsent",
    )
    x_dashscope_avgtpsrequestsnum: str = Field(
        "",
        alias="x-dashscope-avgtpsrequestsnum",
    )
    x_dashscope_apikeyloc: str = Field("", alias="x-dashscope-apikeyloc")
    x_dashscope_bwid: str = Field("", alias="x-dashscope-bwid")
    x_dashscope_inner_flow_control: str = Field(
        "",
        alias="x-dashscope-inner-flow-control",
    )
    x_dashscope_inner_request_priority: str = Field(
        "",
        alias="x-dashscope-inner-request-priority",
    )
    x_dashscope_uid: str = Field("", alias="x-dashscope-uid")
    x_dashscope_workspace: str = Field("", alias="x-dashscope-workspace")
    x_ds_request_priority: str = Field("", alias="x-ds-request-priority")
    x_dashscope_sse: str = Field("", alias="x-dashscope-sse")
    x_dashscope_inner_user_meta: DashscopeInnerUserMeta = (
        DashscopeInnerUserMeta()
    )
    app_id: Optional[str] = ""
    baggage: Optional[str] = ""
    model: Optional[str] = "default_model"
    subuser_id: Optional[str] = ""
    traceparent: Optional[str] = ""
    tracestate: Optional[str] = ""
    user_id: Optional[str] = "default_user_id"
    workspace_id: Optional[str] = ""

    class Config:
        # allow additional headers that are not defined in the model
        extra = Extra.allow
        populate_by_name = True


class BaseHeader(BaseModel):
    request_id: str
    service_id: str = ""
    task_id: str = ""
    attributes: dict = {}


class BailianHeader(BaseHeader):
    attributes: BailianAttributes = BailianAttributes()
    # model server request header's attributes.
    attributes_str: Optional[str] = None


class BailianRequestBody(Request):
    header: BailianHeader
    payload: DashscopeChatRequest
