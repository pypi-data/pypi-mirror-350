# -*- coding: utf-8 -*-
import json
from abc import ABC
from typing import (
    Any,
    Dict,
    TypeVar,
)

from pydantic import BaseModel

# A type variable bounded by BaseModel, meaning it can represent BaseModel or
# any subclass of it.
ComponentArgsT = TypeVar("ComponentArgsT", bound=BaseModel, contravariant=True)
ComponentReturnT = TypeVar("ComponentReturnT", bound=BaseModel, covariant=True)


class BaseComponent(ABC):
    """Base component object to capture class names. use namespace to track
    during serialize"""

    def __str__(self) -> str:
        if hasattr(self, "model_dump_json"):
            return self.model_dump_json()
        elif hasattr(self, "name") and hasattr(self, "description"):
            info = {
                "name": self.name,
                "description": self.description,
            }
            return json.dumps(info)
        else:
            return str(self)

    def to_dict(self, **kwargs: Any) -> Dict[str, Any]:
        if kwargs:
            data = self.model_dump(**kwargs)
        else:
            data = {}
        data["namespace"] = self.get_namespace()
        return data

    def to_json(self, **kwargs: Any) -> str:
        data = self.to_dict(**kwargs)
        return json.dumps(data)

    @classmethod
    def get_namespace(cls) -> list[str]:
        """Get the namespace of the object.

        For example, if the class is
        `agentdev.component.internal.dashscopesearch`, then the
        namespace is ["agentdev", "component", "internal", "dashscopesearch"]
        """
        return cls.__module__.split(".")

    @classmethod
    def __get_pydantic_core_schema__(
        cls,
        source_type: Any,
        handler: Any,
    ) -> Any:
        from pydantic_core import core_schema

        return core_schema.any_schema()
