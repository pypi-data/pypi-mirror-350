# -*- coding: utf-8 -*-
from agentdev.errors.error import BailianError
from agentdev.errors.service_errors import (
    AccessDenied,
    APITimeoutError,
    AuthenticationError,
    InvalidParameter,
    MissingParameter,
    ModelServingError,
    RateLimitExceeded,
    SensitiveContentDetected,
    Unknown,
)


def test_bailian_error():
    error = BailianError()
    assert error.name == "InternalServerError"
    assert error.code == 500
    assert error.message == "InternalServerError from Bailian service."


def test_error_with_request_id():
    error = MissingParameter()
    error.set_request_id("12345")
    assert error.name == "MissingParameter"
    assert error.code == 400
    assert (
        error.message
        == "The request failed because it is missing required parameters "
        "with request id 12345"
    )


def test_missing_parameter():
    error = MissingParameter()
    assert error.name == "MissingParameter"
    assert error.code == 400
    assert (
        error.message
        == "The request failed because it is missing required parameters"
    )


def test_invalid_parameter():
    error = InvalidParameter("some_parameter")
    assert error.name == "InvalidParameter"
    assert error.code == 400
    assert error.message == "some_parameter"


def test_rate_limit_exceeded():
    error = RateLimitExceeded()
    assert error.name == "RateLimitExceeded"
    assert error.code == 429
    assert (
        error.message
        == "The Requests Per Minute(RPM) limit for your account has been "
        "exceeded."
    )


def test_sensitive_content_detected():
    error = SensitiveContentDetected()
    assert error.name == "SensitiveContentDetected"
    assert error.code == 400
    assert (
        error.message
        == "The request failed because the input text may contain sensitive "
        "information."
    )


def test_authentication_error():
    error = AuthenticationError()
    assert error.name == "AuthenticationError"
    assert error.code == 401
    assert error.message == "The API key in the request is missing or invalid."


def test_access_denied():
    error = AccessDenied()
    assert error.name == "AccessDenied"
    assert error.code == 403
    assert (
        error.message
        == "The request failed because you do not have access to the "
        "requested resource."
    )


def test_unknown():
    error = Unknown()
    assert error.name == "Unknown"
    assert error.code == 500
    assert error.message == "Unknown error"


def test_model_serving_error():
    error = ModelServingError()
    assert error.name == "ModelServingError"
    assert error.code == 500
    assert (
        error.message
        == "The request cannot be processed at this time because the model "
        "serving error"
    )


def test_api_timeout_error():
    error = APITimeoutError()
    assert error.name == "APITimeoutError"
    assert error.code == 500
    assert error.message == "Request timed out"
