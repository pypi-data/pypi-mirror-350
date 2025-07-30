# -*- coding: utf-8 -*-
import json
import os
from typing import Any, Dict, List, Tuple, Union

import dashscope
import requests
from pydantic import BaseModel, Field

from agentdev.base.component import Component
from agentdev.schemas.bailian_message_schemas import (
    PromptMessage,
    RagOptions,
)
from agentdev.tracing import TraceType
from agentdev.tracing.wrapper import trace

RAG_URL = (
    "http://dashscope.aliyuncs.com/api/v1/indices/pipeline/retrieve_prompt"
)


class RagInput(BaseModel):
    """
    Search Input.
    """

    messages: List[Union[PromptMessage, Dict]] = Field(
        ...,
        description="user query in the format of Message",
    )
    rag_options: Union[RagOptions, Dict] = Field(
        default=RagOptions(),
        description="Rag options",
    )
    rest_token: int = Field(default=0, description="rest token")
    image_urls: List[str] = Field(default=[], description="image urls")
    workspace_id: str = Field(
        ...,
        description="user query in the format of Message",
    )


class RagOutput(BaseModel):
    """
    Search Input.
    """

    rag_result: str = Field(
        ...,
        description="Rag result in the format of string",
    )
    messages: List[PromptMessage] = Field(
        ...,
        description="user query in the format of Message "
        "with updated system prompt",
    )


class BailianRag(Component[RagInput, RagOutput]):
    """
    Dashscope Rag component that recalling user info on bailian
    """

    description: str = (
        "Bailian Rag可召回用户在百炼上的数据库中存储的信息，用于后续大模型生成使用。"
    )
    name: str = "rag"

    @trace(TraceType.RAG)
    async def _arun(self, args: RagInput, **kwargs: Any) -> RagOutput:
        """
        Run the Rag component with RagInput and return Ragoutput
        Args:
            args: in RagInput format that defined by user
            **kwargs:

        Returns: in the form of SearchOutput

        """
        #
        if not isinstance(args.rag_options, RagOptions):
            args.rag_options = RagOptions(**args.rag_options)
        # tracer = kwargs.get('tracer', get_tracer())

        payload, headers = BailianRag.generate_rag_request(args, **kwargs)

        kwargs["context"] = {
            "workspace_id": args.workspace_id,
            "payload": payload,
        }

        try:
            response = requests.post(RAG_URL, headers=headers, json=payload)
            response_data = response.text
            response_json = json.loads(response_data)
            result = response_json["data"][0]["text"]
            output_messages = BailianRag.update_system_prompt(args, result)
            return RagOutput(rag_result=result, messages=output_messages)
        except Exception as e:
            print(e)
            import traceback

            print(traceback.format_exc())
            return RagOutput(rag_result="", messages=args.messages)

    @staticmethod
    def generate_rag_request(
        rag_input: RagInput,
        **kwargs: Any,
    ) -> Tuple[Dict, Dict]:

        def _build_body(_rag_input: RagInput) -> dict:
            query_content = _rag_input.messages[-1].content
            history = [
                message.model_dump() for message in _rag_input.messages[:-1]
            ]
            _rag_options = _rag_input.rag_options

            data = {
                "image_list": _rag_input.image_urls,
                "pipeline_id_list": _rag_options.pipeline_ids,
                "file_id_list": _rag_options.file_ids,
                "query": query_content,
                "query_history": history,
                "prompt_max_token_length": [_rag_input.rest_token],
                "prompt_enable_citation": _rag_options.enable_citation,
                "enable_web_search": _rag_options.enable_web_search,
                "session_file_ids": _rag_options.session_file_ids,
                "system_prompt": next(
                    (
                        message.content
                        for message in _rag_input.messages
                        if message.role == "system"
                    ),
                    "",
                ),
            }

            if _rag_options.prompt_strategy == "top_k":
                data["prompt_strategy_name"] = "topk"
            else:
                data["prompt_strategy_name"] = _rag_options.prompt_strategy

            if _rag_options.prompt_strategy == "top_k":
                data["rerank_top_n"] = _rag_options.maximum_allowed_chunk_num

            data["dense_similarity_top_k"] = 100
            data["sparse_similarity_top_k"] = 100

            return data

        dashscope_api_key = kwargs.get(
            "api_key",
            os.getenv("DASHSCOPE_API_KEY", dashscope.api_key),
        )

        if not dashscope_api_key:
            raise ValueError("DASHSCOPE_API_KEY is not set")
        header = {
            "Content-Type": "application/json",
            "Accept-Encoding": "utf-8",
            "X-DashScope-WorkSpace": rag_input.workspace_id,
            "Authorization": "Bearer " + dashscope_api_key,
        }
        payload = _build_body(rag_input)
        return payload, header

    @staticmethod
    def update_system_prompt(
        rag_input: RagInput,
        rag_text: str,
    ) -> List[PromptMessage]:
        replaced_word = rag_input.rag_options.replaced_word
        messages = []
        for message in rag_input.messages:
            content = message.content
            if message.role == "system":
                if replaced_word in content:
                    content = content.replace(replaced_word, rag_text)
            messages.append(PromptMessage(role=message.role, content=content))
        return messages
