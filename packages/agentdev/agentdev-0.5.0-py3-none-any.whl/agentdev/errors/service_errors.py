# -*- coding: utf-8 -*-
from .error import BailianError


class MissingParameter(BailianError):
    _name = "MissingParameter"
    _code = 400
    _message = "The request failed because it is missing required parameters"
    _type: str = "BadRequest"


class InvalidParameter(BailianError):
    _name = "InvalidParameter"
    _code = 400
    _message = "A parameter specified in the request is not valid"
    _type: str = "BadRequest"


class RateLimitExceeded(BailianError):
    _name = "RateLimitExceeded"
    _code = 429
    _message = "The Requests Per Minute(RPM) limit for your account has been exceeded."  # noqa E501
    _type: str = "TooManyRequests"


class SensitiveContentDetected(BailianError):
    _name = "SensitiveContentDetected"
    _code = 400
    _message = "The request failed because the input text may contain sensitive information."  # noqa E501
    _type: str = "BadRequest"


class AuthenticationError(BailianError):
    _name = "AuthenticationError"
    _code = 401
    _message = "The API key in the request is missing or invalid."
    _type: str = "Unauthorized"


class AccessDenied(BailianError):
    _name = "AccessDenied"
    _code = 403
    _message = "The request failed because you do not have access to the requested resource."  # noqa E501
    _type: str = "Forbidden"


class Unknown(BailianError):
    _name = "Unknown"
    _code = 500
    _message = "Unknown error"
    _type: str = "InternalServerError"


class ModelServingError(BailianError):
    _name = "ModelServingError"
    _code = 500
    _message = "The request cannot be processed at this time because the model serving error"  # noqa E501
    _type: str = "InternalServerError"


class APITimeoutError(BailianError):
    _name = "APITimeoutError"
    _code = 500
    _message = "Request timed out"
    _type: str = "InternalServerError"


class InputUnknownError(InvalidParameter):
    _message = "An unknown error occurred due to an unsupported input format."


class UserError(BailianError):
    _name = "UserError"
    _code = 400
    _type: str = "BadRequest"

    def __init__(self, message: str):
        super().__init__(message)
        self._message = message


# All Internal error during Plugin calling part are set to code 50006
# Use the following 50006 status code plug-in center to reply and do not
# change it.
class InternalPlugError(BailianError):
    _code = 50006
    _name = "InternalPlugError"
    _message = "Internal Error during Plug calling."


class ToolSchemaCenterConnectionError(InternalPlugError):
    _name = "Tool Schema Center Connection Error"
    _message = "Fail to connect schema center"
