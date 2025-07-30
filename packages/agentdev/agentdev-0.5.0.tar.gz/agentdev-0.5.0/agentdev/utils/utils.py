# -*- coding: utf-8 -*-
import json
import json5


def process_json_str(s: str) -> dict:
    try:
        return json5.loads(s)
    except Exception:
        # json库对一些特殊unicode字符有支持, 同时设置 strict 可以绕过无法解析的字符，增加容错性
        return json.loads(s, strict=False)


def json_loads(s: str) -> dict:
    s = s.strip("\n")
    if s.startswith("```") and s.endswith("\n```"):
        s = "\n".join(s.split("\n")[1:-1])
    return process_json_str(s)
