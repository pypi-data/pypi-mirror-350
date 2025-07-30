# -*- coding: utf-8 -*-
from mcp.types import CallToolResult
from mcp.types import Tool as MCPTool
from pydantic import BaseModel, create_model
from typing import Any, Type

from agentdev.base.component import Component
from agentdev.errors.service_errors import UserError
from agentdev.mcp_utils.server import MCPServer


class MCPUtil:

    @classmethod
    async def get_all_tools(
        cls,
        servers: list["MCPServer"],
    ) -> list[Component]:
        """Get all MCP tools from a list of MCP servers."""
        tools = []
        tool_names: set[str] = set()
        for server in servers:
            server_tools = await cls.get_tools(server)
            server_tool_names = {tool.name for tool in server_tools}
            if len(server_tool_names & tool_names) > 0:
                raise UserError(
                    f"Duplicate tool names found across MCP servers: "
                    f"{server_tool_names & tool_names}",
                )
            tool_names.update(server_tool_names)
            tools.extend(server_tools)

        return tools

    @classmethod
    async def get_tools(cls, server: "MCPServer") -> list[Component]:
        """Get all MCP tools from an MCP server."""
        tools = await server.list_tools()
        return [cls._create_mcp_component(tool, server) for tool in tools]

    @classmethod
    def _create_mcp_args_model(cls, mcp_tool: MCPTool) -> Type[BaseModel]:
        """
        Dynamically create a Pydantic model class from a MCP tool

        Args:
            mcp_tool: The MCP tool received from the MCP server

        Returns:
            A new Pydantic model class for tool arguments
        """
        type_map = {
            "string": str,
            "integer": int,
            "number": float,
            "boolean": bool,
            "array": list,
            "object": dict,
        }

        properties = mcp_tool.inputSchema.get("properties", {})
        required = mcp_tool.inputSchema.get("required", [])

        field_definitions = {}
        for field_name, field_schema in properties.items():
            field_type = field_schema.get("type", "Any")
            field_type = type_map.get(field_type, Any)

            # Define if field is optional based on required list and default
            # value
            if field_name in required:
                field_definitions[field_name] = (field_type, ...)
            else:
                default_value = field_schema.get("default", None)
                field_definitions[field_name] = (field_type, default_value)

        # Create model that inherits from BaseModel
        return create_model(f"{mcp_tool.name}Args", **field_definitions)

    @classmethod
    def _create_mcp_component(
        cls,
        mcp_tool: MCPTool,
        server: "MCPServer",
        **kwargs: Any,
    ) -> Component:
        """
        Dynamically create a Component class from a MCP tool

        Args:
            mcp_tool: The MCP tool received from the MCP server

        Returns:
            A new Component class for the MCP tool
        """
        tool_name = mcp_tool.name
        tool_desc = mcp_tool.description or "No description provided."
        tool_args_model: Type[BaseModel] = cls._create_mcp_args_model(mcp_tool)

        class MCPToolComponent(Component[tool_args_model, CallToolResult]):  # type: ignore[valid-type] # noqa E501
            name = tool_name
            description = tool_desc

            async def _arun(
                self,
                args: tool_args_model,  # type: ignore[valid-type]
                **kwargs: Any,
            ) -> CallToolResult:
                call_tool_result = await server.call_tool(
                    self.name,
                    args.model_dump(),
                )
                return call_tool_result

        return MCPToolComponent()
