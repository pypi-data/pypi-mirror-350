# -*- coding: utf-8 -*-
import copy
import uuid
from typing import Any, Dict, List, Optional, TypeVar, Union

from pydantic import BaseModel, Field, SerializeAsAny

from agentdev.base.memory import Memory, MemoryOperation
from agentdev.schemas.message_schemas import PromptMessage

MessageT = TypeVar("MessageT", bound=PromptMessage, contravariant=True)


class MemoryInput(BaseModel):
    operation_type: MemoryOperation
    run_id: Optional[str] = Field(
        description="Run id of the memory",
        default=str(uuid.uuid4()),
    )
    messages: Optional[Union[List[PromptMessage], str]] = Field(
        default=None,
        description="Messages to be used in the memory operation",
    )
    filters: Optional[Dict[str, Any]] = Field(
        description="Associated filters for the messages, such as run_id, "
        "agent_id, etc.",
        default=None,
    )


class MemoryOutput(BaseModel):
    infos: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Information about the memory operation result",
    )
    messages: Optional[List[PromptMessage]] = Field(
        default=[],
        description="Messages to be recalled",
    )
    summarization: Optional[str] = Field(
        default=None,
        description="Summarization of the messages",
    )


class SimpleChatStore(BaseModel):
    """Simple chat store. Async methods provide same functionality as sync
    methods in this class."""

    store: Dict[str, List[PromptMessage]] = Field(default_factory=dict)

    def set_messages(self, key: str, messages: List[MessageT]) -> None:
        """Set messages for a key."""
        self.store[key] = copy.deepcopy(messages)

    def get_messages(
        self,
        key: str,
        filters: Optional[Dict[str, Any]] = None,
    ) -> List[MessageT]:
        """Get messages for a key."""
        return self.store.get(key, [])

    def add_message(
        self,
        key: str,
        message: MessageT,
        idx: Optional[int] = None,
    ) -> None:
        """Add a message for a key."""
        message_buffer = copy.deepcopy(message)
        if idx is None:
            self.store.setdefault(key, []).append(message_buffer)
        else:
            self.store.setdefault(key, []).insert(idx, message_buffer)

    def delete_messages(self, key: str) -> Optional[List[MessageT]]:
        """Delete messages for a key."""
        if key not in self.store:
            return None
        return self.store.pop(key)

    def delete_message(self, key: str, idx: int) -> Optional[MessageT]:
        """Delete specific message for a key."""
        if key not in self.store:
            return None
        if idx >= len(self.store[key]):
            return None
        return self.store[key].pop(idx)

    def delete_last_message(self, key: str) -> Optional[MessageT]:
        """Delete last message for a key."""
        if key not in self.store:
            return None
        return self.store[key].pop()

    def get_keys(self) -> List[str]:
        """Get all keys."""
        return list(self.store.keys())

    def search(self, query: str, filters: Any) -> List[MessageT]:
        """Simple Chat Store not implement the search method"""
        return []

    # TODO add persist method


class LocalMemory(Memory[MemoryInput, Any]):
    """
    Manages the chat history for an agent.

    Attributes:
        max_token_limit (int): Maximum token limit for a message
        max_messages (Optional[int]): Maximum number of messages to keep in
        history.
        chat_store (Optional[SimpleChatStore]): A store of chat history.
    """

    max_token_limit: int = 2000
    max_messages: Optional[int] = None
    chat_store: SerializeAsAny[SimpleChatStore] = Field(
        default_factory=SimpleChatStore,
    )

    def __init__(
        self,
        chat_store: Optional[SerializeAsAny[SimpleChatStore]] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        if chat_store:
            self.chat_store = chat_store
        else:
            self.chat_store = SimpleChatStore()

    @staticmethod
    def generate_new_key() -> str:
        return str(uuid.uuid4())

    async def add(self, args: MemoryInput, **kwargs: Any) -> MemoryOutput:
        run_id = args.run_id
        messages = args.messages
        if not run_id or not messages:
            raise ValueError("run_id and message are required")
        if isinstance(messages, str):
            messages = [PromptMessage(content=messages, role="user")]
        for message in messages:
            if not isinstance(message, PromptMessage):
                raise ValueError("message must be a PromptMessage")
            self.chat_store.add_message(run_id, message)
            self._manage_overflow(run_id)
        return MemoryOutput(infos={"success": True})

    async def search(self, args: MemoryInput, **kwargs: Any) -> MemoryOutput:

        run_id = args.run_id
        filters = args.filters
        if not filters:
            raise ValueError("filters is required")

        if run_id:
            filters[run_id] = run_id

        if isinstance(args.messages, List):
            query = args.messages[-1].content
        elif isinstance(args.messages, str):
            query = args.messages
        else:
            raise ValueError("messages must be a List or str")
        if not run_id or not filters:
            raise ValueError("run_id and filters is required")
        return MemoryOutput(messages=self.chat_store.search(query, filters))

    async def get_all(self, args: MemoryInput, **kwargs: Any) -> MemoryOutput:
        run_id = args.get("run_id")
        if not run_id:
            raise ValueError("run_id is required")
        return MemoryOutput(messages=self.chat_store.get_messages(run_id))

    async def get(self, args: MemoryInput, **kwargs: Any) -> MemoryOutput:
        run_id = args.get("run_id")
        if not run_id:
            raise ValueError("run_id is required")
        return MemoryOutput(
            messages=self.chat_store.get_messages(
                run_id,
                filters=args.filters,
            ),
        )

    async def reset(self, args: MemoryInput, **kwargs: Any) -> MemoryOutput:
        run_id = args.run_id
        if not run_id:
            raise ValueError("run_id is required")
        self.chat_store.delete_messages(run_id)
        return MemoryOutput(infos={"success": True})

    def _manage_overflow(self, key: str) -> None:
        """
        Manages the chat history overflow based on max_messages constraint.
        """
        if self.max_messages is not None:
            current_messages = self.chat_store.get_messages(key)
            while len(current_messages) > self.max_messages:
                self.chat_store.delete_message(key, 0)

    # TODO： add token and length limit
