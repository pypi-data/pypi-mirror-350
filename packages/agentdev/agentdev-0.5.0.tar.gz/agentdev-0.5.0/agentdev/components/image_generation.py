# -*- coding: utf-8 -*-
import os
import uuid
from http import HTTPStatus
from typing import Any, Optional

from dashscope import ImageSynthesis
from pydantic import BaseModel, Field

from agentdev.base.component import Component
from agentdev.tracing import TraceType
from agentdev.tracing.wrapper import trace
from agentdev.utils.api_key_util import ApiNames, get_api_key


class ImageGenInput(BaseModel):
    """
    文生图Input
    """

    prompt: str = Field(
        ...,
        description="正向提示词，用来描述生成图像中期望包含的元素和视觉特点,超过800自动截断",
    )
    size: str = Field(
        default="1024*1024",
        description="输出图像的分辨率。默认值是1024*1024 最高可达200万像素",
    )
    n: int = Field(
        default=1,
        description="生成图片的数量。取值范围为1~4张 默认1",
    )


class ImageGenOutput(BaseModel):
    """
    文生图 Output.
    """

    results: list[str] = Field(title="Results", description="输出图片url 列表")
    request_id: Optional[str] = Field(
        default=None,
        title="Request ID",
        description="请求ID",
    )


class ImageGeneration(Component[ImageGenInput, ImageGenOutput]):
    """
    文生图调用.
    """

    name: str = "bailian_image_gen"
    description: str = (
        "AI绘画（图像生成）服务，输入文本描述和图像分辨率，返回根据文本信息绘制的图片URL。"
    )

    @trace(TraceType.IMAGE_GENERATION)
    async def arun(self, args: ImageGenInput, **kwargs: Any) -> ImageGenOutput:
        """
        同步调用文生图进行图片生成
        """
        request_id = kwargs.get("request_id", "")
        trace_event = kwargs.pop("trace_event", None)

        try:
            token = get_api_key(ApiNames.dashscope_api_key, **kwargs)
        except AssertionError:
            raise ValueError("Please set valid DASHSCOPE_API_KEY!")

        model_name = kwargs.get(
            "model_name",
            os.getenv("MODEL_NAME", "wanx2.1-t2i-turbo"),
        )
        res = ImageSynthesis.call(
            api_key=token,
            model=model_name,
            prompt=args.prompt,
            n=args.n,
            size=args.size,
        )

        if request_id == "":
            request_id = (
                res.request_id if res.request_id else str(uuid.uuid4())
            )

        if trace_event:
            trace_event.on_log(
                "",
                **{
                    "step_suffix": "results",
                    "payload": {
                        "request_id": request_id,
                        "image_query_result": res,
                    },
                },
            )
        results = []
        if res.status_code == HTTPStatus.OK:
            for result in res.output.results:
                results.append(result.url)
        return ImageGenOutput(results=results, request_id=request_id)


if __name__ == "__main__":
    import asyncio

    image_generation = ImageGeneration()

    image_gent_input = ImageGenInput(
        prompt="帮我画一个国宝熊猫",
        size="1024*1024",
    )

    async def main() -> None:
        image_gent_output = await image_generation.arun(image_gent_input)
        print(image_gent_output)
        print(image_generation.function_schema.model_dump())

    asyncio.run(main())
