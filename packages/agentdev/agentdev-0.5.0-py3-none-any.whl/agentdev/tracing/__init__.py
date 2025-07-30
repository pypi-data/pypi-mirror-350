# -*- coding: utf-8 -*-
from typing import Any, List, Union

from .base import BaseLogHandler, Tracer, TracerHandler
from .tracing_metric import TraceType


def create_handler(
    eval_mode: Union[str, List] = "default",
    **eval_params: Any,
) -> List[TracerHandler]:
    if isinstance(eval_mode, str):
        eval_mode = [eval_mode]
    handlers: List[TracerHandler] = []
    if "default" in eval_mode:
        handlers.append(BaseLogHandler())
    elif "aliyun_tracer" in eval_mode:
        from .aliyun_tracer import AliyunTracerHandler

        handlers.append(AliyunTracerHandler(**eval_params))
    elif "dashscope_log" in eval_mode:
        from .dashscope_log import DashscopeLogHandler

        handlers.append(DashscopeLogHandler(**eval_params))
    return handlers


_tracer_instances = {}


def get_tracer(
    eval_mode: Union[str, List] = "default",
    **eval_params: Any,
) -> Tracer:
    global _tracer_instances  # noqa F824
    if isinstance(eval_mode, str):
        eval_mode = [eval_mode]
    eval_mode_key = tuple(eval_mode)  # 使用元组作为字典键
    if eval_mode_key not in _tracer_instances:
        handlers = create_handler(eval_mode, **eval_params)
        _tracer_instances[eval_mode_key] = Tracer(handlers)
    return _tracer_instances[eval_mode_key]
