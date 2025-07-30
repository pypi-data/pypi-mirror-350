# -*- coding: utf-8 -*-
import os
from enum import Enum
from typing import Any, Optional


class ApiNames(Enum):
    dashscope_api_key = "DASHSCOPE_API_KEY"


def get_api_key(
    api_enum: ApiNames,
    key: Optional[str] = None,
    **kwargs: Any,
) -> str:
    """

    Args:
        api_enum: enum of api name
        key: default key
        **kwargs: might contain the api name

    Returns:

    """
    api_key = ""
    if key is not None:
        if kwargs.get(api_enum.name, "") != "":
            if key != kwargs.get(api_enum.name):
                # use runtime key instead of init key
                api_key = kwargs.get(api_enum.name)
        else:
            api_key = key
    else:
        api_key = kwargs.get(api_enum.name, os.environ.get(api_enum.value, ""))

    assert api_key != "", f"{api_enum.name} must be acquired"
    return api_key
