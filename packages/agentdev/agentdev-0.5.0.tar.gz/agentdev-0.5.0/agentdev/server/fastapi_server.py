# -*- coding: utf-8 -*-
import json
import uuid
from contextlib import asynccontextmanager
from typing import Any, Callable, Tuple, Type

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.datastructures import QueryParams
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import StreamingResponse
from uvicorn.main import run

from agentdev.schemas.llm_schemas import BailianRequestBody, RequestType
from agentdev.schemas.message_schemas import (
    create_error_response,
    create_success_result,
)

"""
TODO:
1. support multiple endpoint register
2. support local and remote on dashscope
2.1 request and response for local and dashscope
2.2 header specific
3. error handler for bad request

"""


class FastApiServer:

    def __init__(
        self,
        func: Callable,
        endpoint_path: str,
        request_model: Type[RequestType] = None,
        response_type: str = "sse",
        **kwargs: Any,
    ) -> None:

        @asynccontextmanager
        async def lifespan(app: FastAPI) -> Any:
            # TODO: add lifespan before start
            yield
            # TODO: add lifespan after finish

        self.func = func
        self.request_model = request_model
        self.endpoint_path = endpoint_path
        self.response_type = response_type  # 可选值: 'sse', 'json', 'text'
        self.app = FastAPI(lifespan=lifespan)
        self._add_middleware()
        self._add_router()
        self._add_health()

    def _add_health(self) -> None:

        @self.app.get("/readiness")
        async def readiness() -> str:
            if getattr(self.app.state, "is_ready", True):
                return "success"
            raise HTTPException(
                status_code=500,
                detail="Application is not ready",
            )

        @self.app.get("/liveness")
        async def liveness() -> str:
            if getattr(self.app.state, "is_healthy", True):
                return "success"
            raise HTTPException(
                status_code=500,
                detail="Application is not healthy",
            )

    def _add_middleware(self) -> None:

        @self.app.middleware("http")
        async def bailian_custom_router(
            request: Request,
            call_next: Callable,
        ) -> Response:
            response: Response = await call_next(request)
            return response

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def _add_router(self) -> None:

        async def _get_request_info(
            request: Request,
        ) -> Tuple[QueryParams, RequestType]:
            body = await request.body()
            request_body = json.loads(body.decode("utf-8")) if body else {}
            request_body_obj = self.request_model.model_validate(request_body)

            query_params = request.query_params
            return query_params, request_body_obj

        def _get_request_id(request_body_obj: RequestType) -> str:
            if (
                isinstance(request_body_obj, BailianRequestBody)
                and request_body_obj.header.request_id
            ):
                request_id = request_body_obj.header.request_id
            else:
                request_id = str(uuid.uuid4())
            return request_id

        @self.app.post(self.endpoint_path)
        async def main(request: Request) -> StreamingResponse:
            query_params, request_body_obj = await _get_request_info(
                request=request,
            )
            request_id = _get_request_id(request_body_obj)

            generator = self.func(request=request_body_obj)

            async def stream_generator() -> Any:
                try:
                    async for output in generator:
                        yield f"data: {create_success_result(request_id=request_id, output=output)}\n\n"  # noqa E501
                except Exception as e:
                    yield (
                        f"data: "
                        f"{create_error_response(request_id=request_id, error=e)}\n\n"  # noqa E501
                    )  # noqa E501

            media_type = {
                "sse": "text/event-stream",
                "json": "application/x-ndjson",
                "text": "text/plain",
            }.get(self.response_type, "text/event-stream")

            return StreamingResponse(
                stream_generator(),
                media_type=media_type,
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                },
            )

    def run(self, *args: Any, **kwargs: Any) -> None:
        run(app=self.app, **kwargs)
