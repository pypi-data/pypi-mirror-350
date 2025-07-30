# -*- coding: utf-8 -*-
from typing import Dict, Type

from agentdev.base import Component
from .bailian_search_lite import BailianSearchLite
from .image_generation import ImageGeneration

components_for_mcp_server: Dict[str, Type[Component]] = {
    "bailian_image_gen": ImageGeneration,
    "bailian_web_search": BailianSearchLite,
}
