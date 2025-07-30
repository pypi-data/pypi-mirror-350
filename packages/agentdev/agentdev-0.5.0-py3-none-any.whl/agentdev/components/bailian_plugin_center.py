# -*- coding: utf-8 -*-
import os
from typing import Any, Dict, List, Union

from pydantic import BaseModel, Field

from agentdev.base.component import Component
from agentdev.components.internal.clients.http_client import HttpClient
from agentdev.errors.service_errors import ToolSchemaCenterConnectionError
from agentdev.tracing import TraceType
from agentdev.tracing.wrapper import trace
from agentdev.utils.api_key_util import ApiNames, get_api_key
from agentdev.utils.utils import json_loads

api_url = os.getenv(
    "DASHSCOPE_ORCHERSTATOR",
    "http://ds-3047732a.1656375133437235.cn-beijing.pai-eas.aliyuncs.com/api"
    "/v1/",
)
api_auth = os.getenv("DASHSCOPE_ORCHERSTATOR_AUTH", "")

api_invoke_url = os.getenv(
    "DASHSCOPE_ORCHERSTATOR_INVOKE",
    "https://poc-dashscope.aliyuncs.com/api/v1/services/aigc/text-generation"
    "/generation",
)
model_name = os.getenv(
    "DASHSCOPE_PLUGIN_INVOKE_MODEL",
    "pre-pre_plugin_http_invoke",
)


class SearchPluginSchemaInput(BaseModel):
    """
    Input.
    """

    plugin_names: List[str] = Field(..., description="plugin names")
    request_id: str = Field(default="", description="request id")


class SearchPluginSchemaOutput(BaseModel):
    """
    Output.
    """

    output: dict = Field(..., description="search schema list as dict")


class BailianSearchPluginSchema(
    Component[SearchPluginSchemaInput, SearchPluginSchemaOutput],
):
    """
    Bailian Search PluginSchema component that could search schema on bailian
    """

    description: str = (
        "Bailian Search PluginSchema 可以查询插件的schema，用于插件执行"
    )
    name: str = "search_plugin_schema"

    @trace(TraceType.PLUGIN_CENTER)
    async def _arun(
        self,
        args: SearchPluginSchemaInput,
        **kwargs: Any,
    ) -> SearchPluginSchemaOutput:
        try:
            output = BailianSearchPluginSchema.get_plugin_schema_request(args)
            print(f"output:{output}")
            return SearchPluginSchemaOutput(output=output)
        except Exception as e:
            print(e)
            import traceback

            print(traceback.format_exc())
            return SearchPluginSchemaOutput(output={})

    @staticmethod
    def get_plugin_schema_request(
        search_input: SearchPluginSchemaInput,
    ) -> Dict[str, Any]:
        plugins_schema_list = dict()

        # get the dashscope plugin list
        dashscope_plugin_schema_list = (
            BailianSearchPluginSchema.plugin_schema_request(
                search_input=search_input,
            )
        )

        plugins_schema_list.update(dashscope_plugin_schema_list)
        return plugins_schema_list

    @staticmethod
    def plugin_schema_request(
        search_input: SearchPluginSchemaInput,
    ) -> Dict[str, Any]:
        tool_schema_headers = {
            "Content-Type": "application/json",
            "authorization": api_auth,
        }
        url = api_url + "plugin_schema"

        schema_http_client = HttpClient(url=url, headers=tool_schema_headers)

        body = {
            "headers": {
                "request_id": search_input.request_id,
            },
            "plugin_names": search_input.plugin_names,
        }

        http_results = schema_http_client.call(data=body).text

        try:
            http_results = json_loads(http_results)

            if str(http_results["header"]["status_code"]) != "200":
                error_message = (
                    "status_message"
                    + http_results["header"]["status_message"]
                    + "request id :"
                    + http_results["header"]["request_id"]
                )
                raise ToolSchemaCenterConnectionError(
                    f"fail to connect the dashscope schema center, "
                    f"error message is {error_message}",
                )

        except Exception:
            # e.g 直接返回auth fail
            raise ToolSchemaCenterConnectionError(
                f"fail to connect the dashscope schema center, "
                f"error message is {http_results}",
            )

        schema_list = http_results["data"]["output"]

        print("find plugin schema")

        return schema_list


class HeaderSchema(BaseModel):
    request_id: str = Field(default="", description="request id")
    plugin_name: str = Field(..., description="plugin name")
    attributes: Dict[str, Any] = Field(
        default={},
        description="plugin attributes",
    )
    user_id: str = Field(..., description="user id")


class PluginInput(BaseModel):
    """
    Input.
    """

    header: HeaderSchema = Field(..., description="header")
    openapi: dict = Field(..., description="api schema")


class PluginOutput(BaseModel):
    """
    Output.
    """

    output: Union[str, Dict] = Field(..., description="plugin do result")


class BailianPlugin(Component[PluginInput, PluginOutput]):
    """
    Bailian Plugin component that could  execute plugin on bailian
    """

    description: str = "Bailian Plugin 根据插件schema 执行插件"
    name: str = "plugin"

    @trace(TraceType.PLUGIN_CENTER)
    async def _arun(self, args: PluginInput, **kwargs: Any) -> PluginOutput:

        try:
            output = BailianPlugin.plugin_request(args, **kwargs)
            print(f"output:{output}")
            return PluginOutput(output=output)
        except Exception as e:
            print(e)
            import traceback

            print(traceback.format_exc())
            return PluginOutput(output={})

    @staticmethod
    def plugin_request(
        plugin_input: PluginInput,
        **kwargs: Any,
    ) -> Dict[str, Any]:

        tool_schema_headers = {
            "Content-Type": "application/json",
            "authorization": api_auth,
        }
        url = api_url + "plugin"

        http_client = HttpClient(url=url, headers=tool_schema_headers)

        body = {
            "header": plugin_input.header.dict(),
            "openapi": BailianPlugin.replace_example_with_value(
                plugin_input.openapi,
            ),
        }

        http_results = http_client.call(data=body).text

        try:
            http_results = json_loads(http_results)

            if str(http_results["header"]["status_code"]) != "200":
                error_message = (
                    "status_message"
                    + http_results["header"]["status_message"]
                    + "request id :"
                    + http_results["header"]["request_id"]
                )
                raise ToolSchemaCenterConnectionError(
                    f"fail to connect the dashscope plugin center, "
                    f"error message is {error_message}",
                )

        except Exception:
            # e.g 直接返回auth fail
            raise ToolSchemaCenterConnectionError(
                f"fail to connect the dashscope plugin center, "
                f"error message is {http_results}",
            )

        output = http_results["data"]["output"]

        print(f"plugin output{output}")

        return output

    @staticmethod
    def replace_example_with_value(data: Any) -> Any:
        """
        Recursively replace 'example' fields with 'value' fields in
            the given data.

        :param data: The data to process (can be a dict, list, or other types).
        :return: The processed data with 'example' fields replaced by 'value'
            fields.
        """
        if isinstance(data, dict):
            new_data = {}
            for key, value in data.items():
                if key == "example":
                    new_data["value"] = value
                else:
                    new_data[key] = BailianPlugin.replace_example_with_value(
                        value,
                    )
            print(f"new_data{new_data}")
            return new_data
        elif isinstance(data, list):
            return [
                BailianPlugin.replace_example_with_value(item) for item in data
            ]
        else:
            return data


class PluginInvokeInput(BaseModel):
    """
    Input.
    """

    tool_id: str = Field(..., description="the name of plugin")
    user_id: str = Field(..., description="user id")
    plugin_attributes: Dict = Field(
        ...,
        description="plugin attributes, the input of plugin",
    )


class PluginInvokeOutput(BaseModel):
    """
    Output.
    """

    output: Union[str, Dict] = Field(..., description="plugin do result")


class BailianPluginInvoke(Component[PluginInvokeInput, PluginInvokeOutput]):
    """
    Dashscope PluginInvoke component that recalling user info on bailian
    """

    description: str = "Bailian PluginInvoke 插件单独执行api，使用需要加白"
    name: str = "plugin_invoke"

    @trace(TraceType.PLUGIN_CENTER)
    async def _arun(
        self,
        args: PluginInvokeInput,
        **kwargs: Any,
    ) -> PluginInvokeOutput:

        try:
            output = BailianPluginInvoke.plugin_request(args, **kwargs)
            print(f"output:{output}")
            return PluginInvokeOutput(output=output)
        except Exception as e:
            print(e)
            import traceback

            print(traceback.format_exc())
            return PluginInvokeOutput(output={})

    @staticmethod
    def plugin_request(
        plugin_input: PluginInvokeInput,
        **kwargs: Any,
    ) -> Dict[str, Any]:
        try:
            token = get_api_key(ApiNames.dashscope_api_key, **kwargs)
        except AssertionError:
            raise ValueError("Please set valid DASHSCOPE_API_KEY!")

        tool_schema_headers = {
            "Content-Type": "application/json",
            "authorization": token,
        }
        body = {"model": model_name, "input": plugin_input.dict()}
        http_client = HttpClient(
            url=api_invoke_url,
            headers=tool_schema_headers,
        )

        http_results = http_client.call(data=body).text
        try:
            http_results = json_loads(http_results)

            if str(http_results["output"]["header"]["statusCode"]) != "200":
                error_message = (
                    "status_message"
                    + http_results["output"]["header"]["statusMessage"]
                    + "request id :"
                    + http_results["output"]["header"]["requestId"]
                )
                raise ToolSchemaCenterConnectionError(
                    f"fail to connect the dashscope plugin center, "
                    f"error message is {error_message}",
                )

        except Exception:
            # e.g 直接返回auth fail
            raise ToolSchemaCenterConnectionError(
                f"fail to connect the dashscope plugin center, "
                f"error message is {http_results}",
            )

        output = http_results["output"]["output"]

        print(f"plugin output{output}")

        return output
