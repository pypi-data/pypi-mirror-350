# -*- coding: utf-8 -*-
import pytest
from pydantic import BaseModel

from agentdev.base.prompt import PromptTemplate
from agentdev.constants import DEFAULT_SYSTEM


class MyModel(BaseModel):
    name: str
    what: str
    unused_field: str = "This field is not used in the template"


jinja2_template = "给我讲一个关于{{name}}的{{what}}故事"
prompt_jinja2 = PromptTemplate.from_template(
    jinja2_template,
    template_format="jinja2",
)

fstring_template = "给我讲一个关于{name}的{what}故事"
prompt_fstring = PromptTemplate.from_template(
    fstring_template,
    template_format="f-string",
)

raw_empty_template = DEFAULT_SYSTEM
prompt_raw = PromptTemplate.from_template(
    raw_empty_template,
    template_format="f-string",
)

message_template = [
    {"role": "system", "content": "你是一个故事生成器。"},
    {"role": "user", "content": "给我讲一个关于{{name}}的{{what}}故事"},
]
prompt_message = PromptTemplate.from_template(
    message_template,
    template_format="jinja2",
)

interpolation_template = "给我讲一个关于${name}的${what}故事"
prompt_interpolation = PromptTemplate.from_template(
    interpolation_template,
    template_format="interpolation",
)


def test_raw_format():
    value = MyModel(name="狗剩", what="高兴")
    result = prompt_raw.format(value)
    assert result == result


def test_jinja2_format():
    value = MyModel(name="狗剩", what="高兴")
    result = prompt_jinja2.format(value)
    assert result == "给我讲一个关于狗剩的高兴故事"


def test_fstring_format():
    value = MyModel(name="狗剩", what="高兴")
    result = prompt_fstring.format(value)
    assert result == "给我讲一个关于狗剩的高兴故事"


def test_message_format():
    value = MyModel(name="狗剩", what="高兴")
    messages = prompt_message.format_message(value)
    expected_messages = [
        {"role": "system", "content": "你是一个故事生成器。"},
        {"role": "user", "content": "给我讲一个关于狗剩的高兴故事"},
    ]
    for msg, exp_msg in zip(messages, expected_messages):
        assert msg.role == exp_msg["role"]
        assert msg.content == exp_msg["content"]


def test_invalid_model():

    class InvalidModel(BaseModel):
        name: str
        invalid_field: str

    with pytest.raises(ValueError):
        prompt_jinja2.format(InvalidModel(name="狗剩", invalid_field="测试"))


def test_interpolation_format():
    value = MyModel(name="狗剩", what="高兴")
    result = prompt_interpolation.format(value)
    assert result == "给我讲一个关于狗剩的高兴故事"
