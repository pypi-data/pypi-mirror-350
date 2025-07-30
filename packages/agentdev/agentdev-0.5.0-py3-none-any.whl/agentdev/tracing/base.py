# -*- coding: utf-8 -*-
import time
import traceback
from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any, Dict, List

from .tracing_metric import TraceType


# Handler Interface
class TracerHandler(ABC):

    @abstractmethod
    def on_start(
        self,
        event_type: TraceType,
        payload: Dict[str, Any],
        **kwargs: Any,
    ) -> None:
        pass

    @abstractmethod
    def on_end(
        self,
        event_type: TraceType,
        start_payload: Dict[str, Any],
        end_payload: Dict[str, Any],
        start_time: float,
        **kwargs: Any,
    ) -> None:
        pass

    @abstractmethod
    def on_log(self, message: str, **kwargs: Any) -> None:
        pass

    @abstractmethod
    def on_error(
        self,
        event_type: TraceType,
        start_payload: Dict[str, Any],
        error: Exception,
        start_time: float,
        traceback_info: str,
        **kwargs: Any,
    ) -> None:
        pass


# 新增基础的LogHandler类
class BaseLogHandler(TracerHandler):

    import logging

    logger = logging.getLogger(__name__)

    def on_start(
        self,
        event_type: TraceType,
        payload: Dict[str, Any],
        **kwargs: Any,
    ) -> None:
        self.logger.info(f"Event {event_type} started with payload: {payload}")

    def on_end(
        self,
        event_type: TraceType,
        start_payload: Dict[str, Any],
        end_payload: Dict[str, Any],
        start_time: float,
        **kwargs: Any,
    ) -> None:
        self.logger.info(
            f"Event {event_type} ended with start payload: {start_payload}, "
            f"end payload: {end_payload}, duration: "
            f"{time.time() - start_time} seconds, kwargs: {kwargs}",
        )

    def on_log(self, message: str, **kwargs: Any) -> None:
        self.logger.info(f"Log: {message}")

    def on_error(
        self,
        event_type: TraceType,
        start_payload: Dict[str, Any],
        error: Exception,
        start_time: float,
        traceback_info: str,
        **kwargs: Any,
    ) -> None:
        self.logger.error(
            f"Error in event {event_type} with payload: {start_payload}, "
            f"error: {error}, "
            f"traceback: {traceback_info}, duration: "
            f"{time.time() - start_time} seconds, kwargs: {kwargs}",
        )


class Tracer:
    """
    Tracer class for logging events
    usage:
    with tracer.event(TraceType.LLM, payload) as event:
        event.log("message")
        ""...logic here...""
        end_payload = {xxx}
        # optional on_end call for additional payload and kwargs
        event.on_end(end_payload, if_success=True)
    """

    def __init__(self, handlers: List[TracerHandler]):
        self.handlers = handlers

    @contextmanager
    def event(
        self,
        event_type: TraceType,
        payload: Dict[str, Any],
        **kwargs: Any,
    ) -> Any:
        start_time = time.time()

        for handle in self.handlers:
            handle.on_start(event_type, payload, **kwargs)

        event_context = EventContext(
            self.handlers,
            event_type,
            start_time,
            payload,
        )
        try:
            yield event_context
        except Exception as e:
            traceback_info = traceback.format_exc()  # 获取traceback信息
            for handle in self.handlers:
                handle.on_error(
                    event_type,
                    payload,
                    e,
                    start_time,
                    traceback_info=traceback_info,
                )  # 传递traceback信息
            raise
        else:
            event_context._end(payload)

    def log(self, message: str, **kwargs: Any) -> None:
        for handle in self.handlers:
            handle.on_log(message, **kwargs)


class EventContext:

    def __init__(
        self,
        handlers: List[TracerHandler],
        event_type: TraceType,
        start_time: float,
        start_payload: Dict[str, Any],
    ) -> None:
        self.handlers = handlers
        self.event_type = event_type
        self.start_time = start_time
        self.start_payload = start_payload
        self.end_payload = {}
        self.kwargs = {}

    def on_end(self, payload: Dict[str, Any], **kwargs: Any) -> None:
        self.end_payload = payload
        self.kwargs = kwargs

    def on_log(self, message: str, **kwargs: Any) -> None:
        kwargs["event_type"] = self.event_type
        kwargs["start_time"] = self.start_time
        kwargs["start_payload"] = self.start_payload
        for handle in self.handlers:
            handle.on_log(message, **kwargs)

    def _end(self, start_payload: Dict[str, Any] = None) -> None:
        for handle in self.handlers:
            handle.on_end(
                self.event_type,
                start_payload,
                self.end_payload,
                self.start_time,
                **self.kwargs,
            )

    def set_trace_header(self, trace_header: Dict[str, Any]) -> None:
        if trace_header:
            from .aliyun_tracer import AliyunTracerHandler

            for handle in self.handlers:
                if isinstance(handle, AliyunTracerHandler):
                    AliyunTracerHandler.set_trace_header(trace_header)
