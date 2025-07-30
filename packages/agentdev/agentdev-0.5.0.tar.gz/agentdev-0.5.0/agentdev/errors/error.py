# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field


class BailianError(Exception):
    """
    Base error class for the SDK.
    """

    _name: str = "InternalServerError"
    _code: int = 500
    _message: str = "InternalServerError from Bailian service."
    _type: str = "InternalServerError"
    _request_id: str = ""

    @property
    def name(self) -> str:
        # Gather _name from all classes in MRO that are subclasses of BaseError
        return self._name

    def set_request_id(self, request_id: str) -> None:
        self._request_id = request_id

    @property
    def request_id(self) -> str:
        return self._request_id

    @property
    def code(self) -> int:
        return int(str(self._code)[0:3])

    @property
    def type(self) -> str:
        return self._type

    @property
    def message(self) -> str:
        result = self._message
        if self._request_id != "":
            result = f"{result} with request id {self._request_id}"
        return result

    def __init__(self, *args: str) -> None:
        substring = "{}"
        # for those with pre-defined format whose message will not be replaced
        if substring in self._message:
            self._message = self._message.format(*args)
        # for those whose message will be replaced by the input message
        else:
            if len(args) > 0 and isinstance(args[0], str):
                self._message = args[0]


class ErrorModel(BaseModel):
    name: str = Field(..., description="Error message")
    code: Optional[int] = Field(None, description="Error code")
    message: str = Field(..., description="Error message")

    @classmethod
    def from_exception(cls, exc: BailianError) -> "ErrorModel":
        return cls(
            message=exc.message,
            code=exc.code,
            name=exc.name,
        )
