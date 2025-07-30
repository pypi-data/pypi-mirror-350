# -*- coding: utf-8 -*-
from abc import abstractmethod
from enum import Enum
from typing import Any

from .__base import BaseComponent

"""
Support different model type and mainly support llm model
"""


class ModelType(Enum):
    LLM = "llm"
    TEXT_EMBEDDING = "text-embedding"
    RERANK = "rerank"
    SPEECH2TEXT = "speech2text"
    MODERATION = "moderation"
    TTS = "tts"
    TEXT2IMG = "text2img"


class AIModel(BaseComponent):
    model_type: ModelType

    def __init__(self, model_type: ModelType, **kwargs: Any):
        self.model_type = model_type

    @abstractmethod
    async def arun(self, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError
