# -*- coding: utf-8 -*-
import json
import os
import pytest
import time
import traceback

from agentdev.tracing import create_handler, get_tracer
from agentdev.tracing.aliyun_tracer import AliyunTracerHandler
from agentdev.tracing.base import BaseLogHandler, Tracer, TraceType
from agentdev.tracing.dashscope_log import DashscopeLogHandler


def test_create_handler_default():
    """Test create_handler with default mode."""
    handlers = create_handler(eval_mode="default")
    assert len(handlers) == 1
    assert isinstance(handlers[0], BaseLogHandler)


@pytest.fixture
def log_dir(tmp_path):
    """Fixture to provide a temporary directory for logs."""
    return tmp_path / "logs"


def test_create_handler_dashscope_log(log_dir):
    """Test create_handler with dashscope_log mode."""
    handlers = create_handler(
        eval_mode="dashscope_log",
        log_level=20,
        log_dir=str(log_dir),
    )
    assert len(handlers) == 1
    handler = handlers[0]
    assert isinstance(handler, DashscopeLogHandler)

    # Check if log directory is created
    assert log_dir.exists(), f"Log directory '{log_dir}' does not exist"

    # Trigger on_start and verify log file content
    handler.on_start(
        event_type=TraceType.LLM,
        payload={"user_id": "test_user"},
    )
    info_log_file = log_dir / f"info.log.{os.getpid()}"
    assert (
        info_log_file.exists()
    ), f"Info log file '{info_log_file}' does not exist"

    with open(info_log_file, "r") as f:
        log_lines = f.readlines()
        assert len(log_lines) > 0, "No log entries found in info log file"
        log_entry = json.loads(log_lines[-1])
        assert log_entry["step"] == "llm_start", "Unexpected step in log entry"
        assert (
            log_entry["user_id"] == "test_user"
        ), "Unexpected user_id in log entry"

    # Trigger on_error and verify error log file content
    try:
        raise ValueError("Test error")
    except Exception as e:
        handler.on_error(
            event_type=TraceType.LLM,
            start_payload={"user_id": "test_user"},
            error=e,
            start_time=time.time(),
            traceback_info=traceback.format_exc(),
        )

    error_log_file = log_dir / f"error.log.{os.getpid()}"
    assert (
        error_log_file.exists()
    ), f"Error log file '{error_log_file}' does not exist"

    with open(error_log_file, "r") as f:
        log_lines = f.readlines()
        assert len(log_lines) > 0, "No log entries found in error log file"
        log_entry = json.loads(log_lines[-1])
        assert log_entry["step"] == "llm_error", "Unexpected step in log entry"
        assert (
            log_entry["code"] == "ValueError"
        ), "Unexpected error code in log entry"


def test_get_tracer():
    """Test get_tracer returns the same instance for the same eval_mode."""
    tracer1 = get_tracer(eval_mode="default")
    tracer2 = get_tracer(eval_mode="default")
    assert tracer1 is tracer2


def test_base_log_handler(caplog):
    """Test BaseLogHandler logs messages correctly."""
    caplog.set_level("INFO")
    handler = BaseLogHandler()
    handler.on_start(event_type=TraceType.LLM, payload={"key": "value"})
    handler.on_end(
        event_type=TraceType.LLM,
        start_payload={"key": "value"},
        end_payload={},
        start_time=0,
    )
    assert "Event llm started" in caplog.text
    assert "Event llm ended" in caplog.text


def test_tracer_event_context():
    """Test Tracer event context management."""
    tracer = Tracer(handlers=[BaseLogHandler()])
    with tracer.event(event_type=TraceType.LLM, payload={"key": "value"}):
        tracer.log(
            "Test message",
        )  # Use Tracer's log method instead of EventContext
    assert True  # Ensure no exceptions were raised


def test_tracer_custom_log():
    """Test Tracer custom log method."""
    tracer = Tracer(handlers=[DashscopeLogHandler(enable_console=True)])
    with tracer.event(
        event_type=TraceType.LLM,
        payload={"key": "value"},
    ) as event:
        tracer.log("msg1", **{"key1": "value1", "key2": {"key3": "value3"}})
        event.on_log(
            "msg2",
            **{"step_suffix": "last_resp", "payload": {"key": "value"}},
        )
    assert True


def test_aliyun_tracer():
    """Test Tracer custom log method."""
    tracer = Tracer(handlers=[AliyunTracerHandler()])

    trace_header = {"baggage": "", "traceparent": "", "tracestate": ""}

    with tracer.event(
        event_type=TraceType.LLM,
        payload={"key": "value"},
    ) as event:
        event.set_trace_header(trace_header)
        tracer.log("msg1", **{"key1": "value1", "key2": {"key3": "value3"}})
        event.on_log(
            "msg2",
            **{"step_suffix": "last_resp", "payload": {"key": "value"}},
        )
    assert True
