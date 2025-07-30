# -*- coding: utf-8 -*-
import inspect
from functools import wraps
from typing import (
    Any,
    AsyncGenerator,
    Dict,
    Iterable,
    Optional,
    TypeVar,
    Union,
)

from pydantic import BaseModel

from agentdev.tracing import Tracer, TraceType
from agentdev.tracing.dashscope_log import DashscopeLogHandler
from agentdev.utils.asyncio_util import aenumerate
from agentdev.utils.message_util import merge_incremental_chunk

T = TypeVar("T", covariant=True)


def trace(
    trace_type: Union[TraceType, str],
    tracer: Optional[Tracer] = Tracer(
        handlers=[DashscopeLogHandler(enable_console=True)],
    ),
) -> Any:
    if isinstance(trace_type, str):
        trace_type = TraceType(trace_type)

    def task_wrapper(func: Any) -> Any:

        async def async_exec(*args: Any, **kwargs: Any) -> Any:
            start_payload = _get_start_payload(args, kwargs)
            with tracer.event(
                trace_type,
                payload=start_payload,
                **kwargs,
            ) as event:
                kwargs = kwargs if kwargs is not None else {}
                kwargs["trace_event"] = event
                result = await func(*args, **kwargs)
                event.on_end(payload=_obj_to_dict(result))
                return result

        def sync_exec(*args: Any, **kwargs: Any) -> Any:
            start_payload = _get_start_payload(args, kwargs)
            with tracer.event(
                trace_type,
                payload=start_payload,
                **kwargs,
            ) as event:
                kwargs = kwargs if kwargs is not None else {}
                kwargs["trace_event"] = event
                result = func(*args, **kwargs)
                event.on_end(payload=_obj_to_dict(result))
                return result

        @wraps(func)
        async def async_iter_task(
            *args: Any,
            **kwargs: Any,
        ) -> AsyncGenerator[T, None]:
            start_payload = _get_start_payload(args, kwargs)
            with tracer.event(
                trace_type,
                payload=start_payload,
                **kwargs,
            ) as event:
                kwargs = kwargs if kwargs is not None else {}
                kwargs["trace_event"] = event
                cumulated = []

                async def iter_entry() -> AsyncGenerator[T, None]:
                    try:
                        async for i, resp in aenumerate(
                            func(*args, **kwargs),
                        ):  # type: ignore
                            if i == 0:
                                event.on_log(
                                    "",
                                    **{
                                        "step_suffix": "first_resp",
                                        "payload": resp.model_dump(),
                                    },
                                )
                            # todo: support more components
                            if len(resp.choices) > 0:
                                cumulated.append(resp)
                                if resp.choices[0].finish_reason is not None:
                                    if resp.choices[0].finish_reason == "stop":
                                        step_suffix = "last_resp"
                                    else:
                                        step_suffix = resp.choices[
                                            0
                                        ].finish_reason
                                    event.on_log(
                                        "",
                                        **{
                                            "step_suffix": step_suffix,
                                            "payload": resp.model_dump(),
                                        },
                                    )
                            elif resp.usage:
                                cumulated.append(resp)

                            yield resp
                    except Exception as e:
                        raise e
                    finally:
                        if cumulated:
                            merged_chunks = merge_incremental_chunk(cumulated)
                            if merged_chunks:
                                event.on_end(
                                    payload=merged_chunks.model_dump(),
                                )

                try:
                    async for resp in iter_entry():
                        yield resp

                except Exception as e:
                    raise e

        @wraps(func)
        def iter_task(*args: Any, **kwargs: Any) -> Iterable[T]:
            start_payload = _get_start_payload(args, kwargs)
            with tracer.event(
                trace_type,
                payload=start_payload,
                **kwargs,
            ) as event:
                cumulated = []
                try:
                    kwargs = kwargs if kwargs is not None else {}
                    kwargs["trace_event"] = event
                    for i, resp in enumerate(func(*args, **kwargs)):
                        if i == 0:
                            event.on_log(
                                "",
                                **{
                                    "step_suffix": "first_resp",
                                    "payload": resp.model_dump(),
                                },
                            )
                        # todo: support more components
                        if len(resp.choices) > 0:
                            cumulated.append(resp)
                            if resp.choices[0].finish_reason is not None:
                                if resp.choices[0].finish_reason == "stop":
                                    step_suffix = "last_resp"
                                else:
                                    step_suffix = resp.choices[0].finish_reason
                                event.on_log(
                                    "",
                                    **{
                                        "step_suffix": step_suffix,
                                        "payload": resp.model_dump(),
                                    },
                                )
                        elif resp.usage:
                            cumulated.append(resp)

                        yield resp
                except Exception as e:
                    raise e
                finally:
                    if cumulated:
                        merged_chunks = merge_incremental_chunk(cumulated)
                        if merged_chunks:
                            event.on_end(payload=merged_chunks.model_dump())

        if inspect.isasyncgenfunction(func):
            return async_iter_task
        elif inspect.isgeneratorfunction(func):
            return iter_task
        elif inspect.iscoroutinefunction(func):
            return async_exec
        else:
            return sync_exec

    return task_wrapper


def _get_start_payload(args: Any, kwargs: Any) -> Dict:
    dict_args = {}
    if isinstance(args, tuple) and len(args) > 1:
        dict_args = _obj_to_dict(args[1:])

    dict_kwargs = _obj_to_dict(kwargs)
    dict_kwargs = {
        key: value
        for key, value in dict_kwargs.items()
        if not key.startswith("trace_")
    }

    merged = {}
    if dict_args:
        if isinstance(dict_args, list):
            for item in dict_args:
                if isinstance(item, dict):
                    merged.update(item)
        elif isinstance(dict_args, dict):
            merged.update(dict_args)

    if dict_kwargs:
        merged.update(dict_kwargs)

    return merged


def _obj_to_dict(obj: Any) -> Any:
    if isinstance(obj, (str, int, float, bool, type(None))):
        return obj
    elif isinstance(obj, dict):
        return {k: _obj_to_dict(v) for k, v in obj.items()}  # obj
    elif isinstance(obj, (list, set, tuple)):
        return [_obj_to_dict(item) for item in obj]
    elif isinstance(obj, BaseModel):
        return obj.model_dump()
    else:
        result = None
        try:
            result = str(obj)
        except Exception as e:
            print(f"{obj} str method failed with error: {e}")
        return result
