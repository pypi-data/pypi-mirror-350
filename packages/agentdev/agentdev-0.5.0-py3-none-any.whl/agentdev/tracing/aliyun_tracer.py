# -*- coding: utf-8 -*-
import os
import re
import time
from enum import Enum
from typing import Any, Dict

from aliyun.trace.aliyun_llm_trace import extract_from_remote
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
    OTLPSpanExporter as OTLPSpanGrpcExporter,
)
from opentelemetry.propagate import extract, inject
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import StatusCode

from .base import TracerHandler, TraceType


class MineType(str, Enum):
    TEXT = "text/plain"
    JSON = "application/json"


class AliyunTracerHandler(TracerHandler):

    def __init__(self, **kwargs: Any) -> None:
        resource = Resource(
            attributes={
                SERVICE_NAME: get_service_name(os.getenv("DS_SVC_NAME", "")),
                SERVICE_VERSION: "1.0.0",
                "source": "bailian-sdk-serving",
            },
        )
        provider = TracerProvider(resource=resource)
        span_exporter = BatchSpanProcessor(
            OTLPSpanGrpcExporter(
                endpoint=os.getenv("TRACE_ENDPOINT", ""),
                headers=f"Authentication="
                f"{os.getenv('TRACE_AUTHENTICATION', '')}",
            ),
        )
        provider.add_span_processor(span_exporter)
        trace.set_tracer_provider(provider)
        tracer_provider = trace.get_tracer_provider()
        self._tracer = trace.get_tracer(
            __name__,
            tracer_provider=tracer_provider,
        )
        self._span = None
        self._failed = False

    @staticmethod
    def set_trace_header(trace_header: Dict[str, Any]) -> None:
        extract_from_remote(trace_header)

    def get_context(self) -> Any:
        carrier = self.get_carrier()
        context = extract(carrier)
        return context

    @staticmethod
    def get_carrier() -> Any:
        carrier = {}
        inject(carrier)
        return carrier

    def get_tracer(self) -> Any:
        return self._tracer

    def on_start(
        self,
        event_type: TraceType,
        payload: Dict[str, Any],
        **kwargs: Any,
    ) -> None:

        if kwargs.get("trace_header"):
            self.set_trace_header(kwargs.pop("trace_header"))

        self._span = self._tracer.start_span(
            name=kwargs.get("trace_name", event_type),
            context=kwargs.get("trace_context", None),
            start_time=time.time_ns(),
            attributes={
                "gen_ai.span.kind": event_type.upper(),
                "gen_ai.response.id": payload.get("request_id", ""),
                "input.mine_type": MineType.JSON,
                "input.value": str(payload),
            },
        )

    def on_end(
        self,
        event_type: TraceType,
        start_payload: Dict[str, Any],
        end_payload: Dict[str, Any],
        start_time: float,
        **kwargs: Any,
    ) -> None:

        success = kwargs.get("success", True) and not self._failed
        self._span.set_attribute("output.mine_type", MineType.JSON)
        self._span.set_attribute("output.value", str(end_payload))
        self._span.set_status(
            status=StatusCode.OK if success else StatusCode.ERROR,
        )
        self._span.end(end_time=time.time_ns())

    def on_log(self, message: Any, **kwargs: Any) -> None:
        if message:
            self._span.set_attribute("message", str(message))
        if "step_suffix" in kwargs and "payload" in kwargs:
            self._span.set_attribute(
                "step." + kwargs["step_suffix"],
                str(kwargs["payload"]),
            )

    def on_error(
        self,
        event_type: TraceType,
        start_payload: Dict[str, Any],
        error: Exception,
        start_time: float,
        traceback_info: str,
        **kwargs: Any,
    ) -> None:
        self._failed = True
        self._span.set_status(
            status=StatusCode.ERROR,
            description=traceback_info,
        )
        if error:
            self._span.record_exception(error)


def get_service_name(ds_svc_name: str) -> str:
    pattern = r"deployment\.([^-]+(?:-[^-]+)*?)(?=-[^-]+-[^-]+$)"
    match = re.search(pattern, ds_svc_name)
    if match:
        return match.group(1)
    else:
        return ds_svc_name
