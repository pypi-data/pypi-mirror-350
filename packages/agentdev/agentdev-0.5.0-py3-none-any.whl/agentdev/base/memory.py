# -*- coding: utf-8 -*-
from abc import abstractmethod
from enum import Enum
from typing import Any, Generic

from .__base import BaseComponent, ComponentArgsT, ComponentReturnT
from ..tracing.wrapper import trace


class MemoryOperation(str, Enum):
    ADD = "add"
    GET = "get"
    GET_ALL = "get_all"
    SEARCH = "search"
    RESET = "reset"


class Memory(BaseComponent, Generic[ComponentArgsT, ComponentReturnT]):

    @trace("memory")
    async def arun(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        if hasattr(args, "operation_type"):
            operation_type = args.operation_type
        else:
            raise ValueError("operation_type is required")
        if operation_type == MemoryOperation.ADD:
            return await self.add(args, **kwargs)
        elif operation_type == MemoryOperation.GET_ALL:
            return await self.get_all(args, **kwargs)
        elif operation_type == MemoryOperation.SEARCH:
            return await self.search(args, **kwargs)
        elif operation_type == MemoryOperation.RESET:
            return await self.reset(args, **kwargs)
        else:
            raise ValueError(f"Invalid operation type: {operation_type}")

    @abstractmethod
    async def add(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        """
        Create a new memory. store the messages to memory
        """
        raise NotImplementedError("add method must be implemented")

    @abstractmethod
    async def get(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        """
        List memories by filters
        """
        raise NotImplementedError("add method must be implemented")

    @abstractmethod
    async def get_all(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        """
        List all memories.
        """
        raise NotImplementedError("get_all method must be implemented")

    @abstractmethod
    async def search(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        """
        Search for memories with query string and filters
        """
        raise NotImplementedError("search method must be implemented")

    @abstractmethod
    async def reset(
        self,
        args: ComponentArgsT,
        **kwargs: Any,
    ) -> ComponentReturnT:
        """
        Reset or  Delete all memories.
        """
        raise NotImplementedError("reset method must be implemented")
