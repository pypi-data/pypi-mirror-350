# -*- coding: utf-8 -*-
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class CopilotTool(BaseModel):
    tool_id: Optional[str] = Field(default=None, alias="toolId")
    tool_type: Optional[str] = Field(default=None, alias="toolType")
    user_defined_params: Optional[Dict] = Field(
        default=None,
        alias="userDefinedParams",
    )


class CopilotIntent(BaseModel):
    name: Optional[str] = Field(default=None, alias="name")


class CopilotModels(BaseModel):
    name: Optional[str] = Field(default=None, alias="name")
    type: Optional[str] = Field(default=None, alias="type")
    parameters: Optional[Dict] = Field(default=None, alias="parameters")


class CopilotModelOptions(BaseModel):
    generation: Optional[CopilotModels] = None
    fc: Optional[CopilotModels] = None
    custom_fc: Optional[CopilotModels] = Field(default=None, alias="customFc")


class CopilotConfig(BaseModel):
    tools: Optional[List[CopilotTool]] = None
    intents: Optional[List[CopilotIntent]] = None
    instruction: Optional[str] = None
    intent_routing: Optional[Dict] = None
    model_options: Optional[CopilotModelOptions] = Field(
        default=None,
        alias="modelOptions",
    )
    data_inspection: Optional[str] = None


class Copilot(BaseModel):
    """copilot definition"""

    id: str
    name: str
    type: int
    description: Optional[str] = None
    config: Optional[CopilotConfig] = {}
