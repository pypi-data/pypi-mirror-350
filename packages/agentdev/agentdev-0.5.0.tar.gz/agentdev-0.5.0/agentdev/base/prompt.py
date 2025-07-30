# -*- coding: utf-8 -*-
import re
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from jinja2 import Environment, meta
from pydantic import BaseModel

from agentdev.schemas.message_schemas import (
    AssistantPromptMessage,
    PromptMessage,
    SystemPromptMessage,
    ToolPromptMessage,
    UserPromptMessage,
)
from .__base import BaseComponent

DEFAULT_KNOWLEDGE_TEMPLATE = """## 来自 {source} 的内容：

```
{content}
```"""

ArgsT = TypeVar("ArgsT", bound=BaseModel, contravariant=True)
ReturnT = TypeVar(
    "ReturnT",
    bound=Union[List[PromptMessage], str],
    covariant=True,
)


class PromptTemplate(BaseComponent, Generic[ArgsT, ReturnT]):

    def __init__(
        self,
        template: Union[
            str,
            List[Dict[str, str]],
        ] = DEFAULT_KNOWLEDGE_TEMPLATE,
        template_format: str = "f-string",
        prefix: str = "",
        postfix: str = "",
    ):
        """
        The constructor for PromptTemplate Args:
            template: the template for a single prompt template_format: the
            format of the template ('jinja2', 'f-string', or 'interpolation')
            prefix: prefix for multiple prompts postfix: postfix for multiple
            prompts
        """
        if template_format not in ["jinja2", "f-string", "interpolation"]:
            raise ValueError(
                "Supported template formats are 'jinja2', "
                "'f-string', and 'interpolation'.",
            )
        self.template_format = template_format
        self.env = Environment() if template_format == "jinja2" else None

        if not isinstance(template, str) and not isinstance(template, list):
            raise ValueError(
                "Template must be either a string or a "
                "list of message dictionaries.",
            )
        self.template = template
        self.prefix = prefix
        self.postfix = postfix

    @classmethod
    def from_template(
        cls,
        template: Union[str, List[Dict[str, str]]],
        template_format: str = "jinja2",
        prefix: str = "",
        postfix: str = "",
    ) -> "PromptTemplate":
        return cls(template, template_format, prefix, postfix)

    def format_from_context_providers(
        self,
        context_providers: Dict[str, ArgsT],
    ) -> str:
        """
        This method is only for system prompt with string not for message yet
        Args:
            context_providers:

        Returns: str prompt

        """
        output = self.prefix
        if context_providers:
            for provider_info in context_providers.values():
                if provider_info:
                    formatted_prompt = self.format_prompt(provider_info)
                    if formatted_prompt is not None:
                        output += "/n/n"
                        output += formatted_prompt

        output += self.postfix
        return output

    def format(self, args: ArgsT) -> Union[List[PromptMessage], str]:
        """
        The main method to format
        Args:
            args: BaseModel as input

        Returns:

        """
        if isinstance(self.template, str):
            return self.format_prompt(args) or ""
        else:
            return self.format_message(args)

    async def arun(
        self,
        args: ArgsT,
        **kwargs: Any,
    ) -> Union[List[PromptMessage], str]:
        return self.format(args)

    def format_prompt(self, args: ArgsT) -> Optional[str]:
        if not isinstance(self.template, str):
            raise ValueError(
                "This template is for messages. Use format_message() instead.",
            )
        return self._format_template(self.template, args)

    def format_message(self, args: ArgsT) -> List[PromptMessage]:

        if not isinstance(self.template, list):
            raise ValueError(
                "This template is not for messages. Use format() instead.",
            )

        formatted_messages = []
        for msg in self.template:
            role = msg["role"]
            content = self._format_template(msg["content"], args)

            if role == "system":
                formatted_message = SystemPromptMessage(content=content)
            elif role == "user":
                formatted_message = UserPromptMessage(content=content)
            elif role == "assistant":
                formatted_message = AssistantPromptMessage(content=content)
            elif role == "tool":
                formatted_message = ToolPromptMessage(
                    content=content,
                    tool_call_id=msg.get("tool_call_id", ""),
                )
            else:
                raise ValueError(f"Unsupported role: {role}")

            formatted_messages.append(formatted_message)

        return formatted_messages

    def _format_template(
        self,
        template: str,
        model_instance: Union[Dict, BaseModel],
    ) -> Optional[str]:
        self._validate_template_with_model(template, model_instance.__class__)
        model_dict = (
            model_instance.model_dump()
            if isinstance(model_instance, BaseModel)
            else model_instance
        )
        model_dict = self.process_value_into_str(model_dict)
        if self.template_format == "jinja2":
            template_obj = self.env.from_string(template)
            return template_obj.render(**model_dict)
        elif self.template_format == "f-string":
            return template.format(**model_dict)
        elif self.template_format == "interpolation":
            variables = self._get_interpolation_variables(template)
            rendered_template = template
            for var_name in variables:
                var_value = str(getattr(model_instance, var_name))
                rendered_template = rendered_template.replace(
                    f"${{{var_name}}}",
                    var_value,
                )
            return rendered_template
        else:
            raise ValueError(
                f"Unsupported template format: {self.template_format}",
            )

    @staticmethod
    def process_value_into_str(model_dict: Dict) -> Dict:
        processed_model = {}
        for item in model_dict.keys():
            if isinstance(model_dict[item], str):
                processed_model[item] = model_dict[item]
            if isinstance(model_dict[item], list):
                if len(model_dict[item]) > 0 and isinstance(
                    model_dict[item][0],
                    str,
                ):
                    processed_model[item] += "\n".join(model_dict[item])
            if isinstance(model_dict[item], BaseModel):
                processed_model[item] = model_dict[item].model_dump_json()
            if isinstance(model_dict[item], dict):
                value = ""
                for k, v in model_dict[item].items():
                    value += k + ":" + v + "\n"
                processed_model[item] = value
        return processed_model

    def _validate_template_with_model(
        self,
        template: str,
        model_class: Type[BaseModel],
    ) -> None:
        if self.template_format == "jinja2":
            template_variables = self._get_jinja2_variables(template)
        elif self.template_format == "f-string":
            template_variables = self._get_fstring_variables(template)
        elif self.template_format == "interpolation":
            template_variables = self._get_interpolation_variables(template)

        model_fields = set(model_class.model_fields.keys())

        missing_fields = template_variables - model_fields
        if missing_fields:
            raise ValueError(
                f"Template variables not found in model: {missing_fields}",
            )

        unused_fields = model_fields - template_variables
        if unused_fields:
            print(
                f"Warning: Model fields not used in template: {unused_fields}",
            )

    def _get_jinja2_variables(self, template: str) -> set:
        ast = self.env.parse(template)
        return meta.find_undeclared_variables(ast)

    def _get_fstring_variables(self, template: str) -> set:
        pattern = r"\{([^}]+)\}"
        return set(re.findall(pattern, template))

    def _get_interpolation_variables(self, template: str) -> set:
        pattern = r"\$\{([^}]+)\}"
        return set(re.findall(pattern, template))
