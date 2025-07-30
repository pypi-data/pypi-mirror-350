# -*- coding: utf-8 -*-
import json
import os
from typing import Any, Dict, List, Union

import dashscope
import requests
from pydantic import BaseModel, Field

from agentdev.base.component import Component
from agentdev.schemas.bailian_message_schemas import (
    IntentionOptions,
    PromptMessage,
)
from agentdev.tracing import TraceType
from agentdev.tracing.wrapper import trace

INTENTION_MODEL_NAME = os.getenv(
    "INTENTION_MODEL_NAME",
    "search_fus,news_intent_model",
)
INTENTION_CENTER_URL = os.getenv(
    "INTENTION_CENTER_URL",
    "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation"
    "/generation",
)
INTENTION_CENTER_NAME = os.getenv(
    "INTENTION_CENTER_NAME",
    "planning-router-serving-prod-tob",
)

default_intention_service_models = [
    model.strip() for model in INTENTION_MODEL_NAME.split(",")
]


class IntentionInput(BaseModel):
    """
    Intention Input
    """

    messages: List[Union[PromptMessage, Dict]] = Field(
        ...,
        description="user query in the format of Message",
    )
    intention_options: Union[IntentionOptions, Dict] = Field(
        default=IntentionOptions(),
        description="Rag options",
    )
    intention_service_models: List[str] = Field(
        default=default_intention_service_models,
        description="intention service models",
    )


class IntentionOutput(BaseModel):
    labels: List[str] = Field(description="The labels of the intention")


class IntentionCenter(Component[IntentionInput, IntentionOutput]):
    """
    Intention center
    """

    description = "意图中心组件，提供聚合意图识别服务。"
    name = "intention"

    @trace(TraceType.INTENTION)
    async def _arun(
        self,
        args: IntentionInput,
        **kwargs: Any,
    ) -> IntentionOutput:
        if not isinstance(args.intention_options, IntentionOptions):
            args.intention_options = IntentionOptions(**args.intention_options)
        # tracer = kwargs.get('tracer', get_tracer())
        payload = IntentionCenter.generate_intention_payload(args)
        dashscope_api_key = kwargs.get(
            "api_key",
            os.getenv("DASHSCOPE_API_KEY", dashscope.api_key),
        )
        if not dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY is not set")

        header = {
            "Content-Type": "application/json",
            "Accept-Encoding": "utf-8",
            "Authorization": "Bearer " + dashscope_api_key,
        }
        payload["model"] = INTENTION_CENTER_NAME

        kwargs["context"] = {"payload": payload}
        try:
            response = requests.post(
                INTENTION_CENTER_URL,
                headers=header,
                json=payload,
            )
            response_data = response.text
            response_json = json.loads(response_data)
            result = response_json["output"]["labels"]
            return IntentionOutput(labels=result)
        except Exception as e:
            print(e)
            import traceback

            print(traceback.format_exc())
            return IntentionOutput(labels=["general"])

    @staticmethod
    def generate_intention_payload(intention_input: IntentionInput) -> Dict:
        intention_service_models = intention_input.intention_service_models
        intention_options = intention_input.intention_options
        parameters = {
            "models": intention_service_models,
            "search_params": {
                "white_list": intention_options.white_list,
                "black_list": intention_options.black_list,
                "search_model": intention_options.search_model,
                "intensity": intention_options.intensity,
            },
            **(
                {"intervene_params": {"scene_id": intention_options.scene_id}}
                if intention_options.scene_id
                else {}
            ),
        }

        is_content_list = False
        for message in intention_input.messages:
            if isinstance(message.content, list):
                is_content_list = True
                break
        if is_content_list:
            for i, message in enumerate(intention_input.messages):
                content = ""
                if isinstance(message.content, list):
                    for content_item in message.content:
                        if isinstance(content_item, str):
                            content += f"\n\n{content_item}"
                        elif content_item.text:
                            content += f"\n\n{content_item.text}"
                    intention_input.messages[i].content = content

        messages = [
            message.model_dump(
                exclude={"name", "tool_calls", "function_call", "plugin_call"},
            )
            for message in intention_input.messages
        ]
        payload = {"input": {"messages": messages}, "parameters": parameters}

        return payload
