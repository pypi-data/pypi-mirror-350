# -*- coding: utf-8 -*-
import pytest

from agentdev.components.bailian_plugin_center import (
    BailianPlugin,
    BailianPluginInvoke,
    BailianSearchPluginSchema,
    PluginInput,
    PluginInvokeInput,
    PluginInvokeOutput,
    PluginOutput,
    SearchPluginSchemaInput,
    SearchPluginSchemaOutput,
)


@pytest.fixture
def search_plugin_schema_component():
    return BailianSearchPluginSchema()


def test_arun_search_plugin_schema_success(search_plugin_schema_component):
    # Prepare input data
    input_data = SearchPluginSchemaInput(
        plugin_names=["pre-code_interpreter"],
        reqquest_id="",
    )

    # Call the _arun method
    result = search_plugin_schema_component.run(input_data)

    # Assertions to verify the result
    assert isinstance(result, SearchPluginSchemaOutput)
    assert isinstance(result.output, dict)


@pytest.fixture
def plugin_component():
    return BailianPlugin()


def test_arun_plugin_success(plugin_component):
    header = {
        "request_id": "",
        "plugin_name": "pre-code_interpreter",
        "user_id": "205608228479407843",
        "plugin_attributes": {},
        "attributes": {"X-DashScope-EUID": ""},
    }
    openapi = {
        "openapi": "3.0.3",
        "info": {
            "title": "python代码执行器",
            "description": "python代码执行器",
            "version": "v1.0.7",
        },
        "servers": [{"url": "127.0.0.1:8000", "description": ""}],
        "paths": {
            "/run_code": {
                "post": {
                    "parameters": [],
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "required": ["header", "payload"],
                                    "type": "object",
                                    "properties": {
                                        "header": {
                                            "required": ["request_id"],
                                            "type": "object",
                                            "properties": {
                                                "request_id": {
                                                    "type": "string",
                                                    "description": "请求id",
                                                    "example": "",
                                                    "exampleSetFlag": True,
                                                    "types": ["string"],
                                                },
                                            },
                                            "exampleSetFlag": False,
                                            "types": ["object"],
                                        },
                                        "payload": {
                                            "required": ["input, files"],
                                            "type": "object",
                                            "properties": {
                                                "input": {
                                                    "type": "string",
                                                    "description": "待执行的代码",
                                                    "example": "```py\n# Calculating 10 to the power of 4\nresult = 10 ** "  # noqa E501
                                                    "4\nresult\n```",
                                                    "exampleSetFlag": True,
                                                    "types": ["string"],
                                                    "default": "",
                                                },
                                                "files": {
                                                    "type": "array",
                                                    "description": "需要上传的文件",  # noqa E501
                                                    "value": [],
                                                    "exampleSetFlag": True,
                                                    "items": {
                                                        "type": "string",
                                                        "exampleSetFlag": False,  # noqa E501
                                                        "types": ["string"],
                                                    },
                                                    "types": ["array"],
                                                    "default": [""],
                                                },
                                            },
                                            "exampleSetFlag": False,
                                            "types": ["object"],
                                        },
                                    },
                                    "exampleSetFlag": False,
                                    "types": ["object"],
                                },
                                "exampleSetFlag": False,
                            },
                        },
                        "required": True,
                    },
                },
            },
        },
    }
    # Prepare input data
    input_data = PluginInput(header=header, openapi=openapi)

    # Call the _arun method
    result = plugin_component.run(input_data)

    # Assertions to verify the result
    assert isinstance(result, PluginOutput)


def test_arun_plugin_calculator_success(plugin_component):
    header = {
        "request_id": "",
        "plugin_name": "pre-calculator",
        "user_id": "205608228479407843",
    }
    openapi = {
        "openapi": "3.0.1",
        "info": {
            "title": "Calculator",
            "description": "A plugin that use calculator.",
            "version": "v1",
        },
        "servers": [{"url": "http://localhost:8080"}],
        "paths": {
            "/api": {
                "post": {
                    "summary": "math calculation",
                    "operationId": "calculate",
                    "requestBody": {
                        "content": {
                            "application/json": {
                                "schema": {
                                    "required": ["header", "payload"],
                                    "type": "object",
                                    "properties": {
                                        "header": {
                                            "type": "object",
                                            "properties": {
                                                "request_id": {
                                                    "type": "string",
                                                    "exampleSetFlag": False,
                                                    "types": ["string"],
                                                    "value": "十乘四",
                                                },
                                            },
                                            "exampleSetFlag": False,
                                            "types": ["object"],
                                        },
                                        "payload": {
                                            "type": "object",
                                            "properties": {
                                                "input": {
                                                    "type": "object",
                                                    "properties": {
                                                        "text": {
                                                            "type": "string",
                                                            "description": "输入的要计算的文本，可以用中文或者数字，比如10/5、十乘四",  # noqa E501
                                                            "value": "十乘四",
                                                            "exampleSetFlag": True,  # noqa E501
                                                            "types": [
                                                                "string",
                                                            ],
                                                        },
                                                    },
                                                    "exampleSetFlag": False,
                                                    "types": ["object"],
                                                },
                                            },
                                            "exampleSetFlag": False,
                                            "types": ["object"],
                                        },
                                    },
                                    "exampleSetFlag": False,
                                    "types": ["object"],
                                },
                                "exampleSetFlag": False,
                            },
                        },
                        "required": True,
                    },
                    "responses": {
                        "200": {"description": "OK"},
                        "400": {"description": "INVALID_PARAMETER"},
                        "500": {"description": "INTERNAL_ERROR"},
                    },
                },
            },
        },
        "components": {
            "schemas": {
                "InputBody": {
                    "required": ["header", "payload"],
                    "type": "object",
                    "properties": {
                        "header": {
                            "type": "object",
                            "properties": {
                                "request_id": {
                                    "type": "string",
                                    "exampleSetFlag": False,
                                    "types": ["string"],
                                },
                            },
                            "exampleSetFlag": False,
                            "types": ["object"],
                        },
                        "payload": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "object",
                                    "properties": {
                                        "text": {
                                            "type": "string",
                                            "description": "输入的要计算的文本，可以用中文或者数字，比如10/5、十乘四",  # noqa E501
                                            "value": "十乘四",
                                            "exampleSetFlag": True,
                                            "types": ["string"],
                                        },
                                    },
                                    "exampleSetFlag": False,
                                    "types": ["object"],
                                },
                            },
                            "exampleSetFlag": False,
                            "types": ["object"],
                        },
                    },
                    "exampleSetFlag": False,
                    "types": ["object"],
                },
            },
            "extensions": {},
        },
    }
    # Prepare input data
    input_data = PluginInput(header=header, openapi=openapi)

    # Call the _arun method
    result = plugin_component.run(input_data)

    # Assertions to verify the result
    assert isinstance(result, PluginOutput)


@pytest.fixture
def plugin_invoke_component():
    return BailianPluginInvoke()


def test_arun_plugin_invoke_success(plugin_invoke_component):
    # plugin_attributes = {
    #     "header": {
    #         "request_id": ""
    #     },
    #     "payload": {
    #         "input": "\na = 1\nb = 6\n"
    #     }
    # }
    plugin_attributes = {
        "header": {"request_id": ""},
        "payload": {
            "input": "\nimport matplotlib.pyplot as plt\n\n# Data to "
            "plot\nlabels = '茶叶', '生丝'\nsizes = [70, 30]\n\n# "
            "Plot\nfig1, ax1 = plt.subplots()\nax1.pie(sizes, "
            "labels=labels, autopct='%1.1f%%', "
            "startangle=90)\nax1.axis('equal')  # Equal aspect "
            "ratio ensures that pie is drawn as a "
            "circle.\n\nplt.show()\n",
        },
    }
    # Prepare input data
    input_data = PluginInvokeInput(
        tool_id="pre-code_interpreter",
        user_id="205608228479407842",
        plugin_attributes=plugin_attributes,
    )

    # Call the _arun method
    result = plugin_invoke_component.run(input_data)

    # Assertions to verify the result
    assert isinstance(result, PluginInvokeOutput)
    print(result.output)
