# -*- coding: utf-8 -*-
import pytest

from agentdev.components.local_memory import (
    LocalMemory,
    MemoryInput,
    MemoryOperation,
    SimpleChatStore,
)
from agentdev.schemas.message_schemas import UserPromptMessage


@pytest.fixture
def chat_store():
    return SimpleChatStore()


@pytest.fixture
def memory():
    return LocalMemory()


def test_set_and_get_messages(chat_store):
    key = "test_key"
    messages = [UserPromptMessage(content="Hello, world!")]
    chat_store.set_messages(key, messages)
    retrieved_messages = chat_store.get_messages(key)
    assert messages == retrieved_messages


def test_add_message(chat_store):
    key = "test_key"
    message = UserPromptMessage(content="Hello, again!")
    chat_store.add_message(key, message)
    assert message in chat_store.get_messages(key)


def test_delete_messages(chat_store):
    key = "test_key"
    messages = [UserPromptMessage(content="Hello, world!")]
    chat_store.set_messages(key, messages)
    deleted_messages = chat_store.delete_messages(key)
    assert messages == deleted_messages
    assert (
        chat_store.get_messages(key) == []
    ), "Messages should be empty after deletion"


def test_delete_message(chat_store):
    key = "test_key"
    messages = [
        UserPromptMessage(content="Hello world", name=None),
        UserPromptMessage(content="Hello again", name=None),
    ]
    chat_store.set_messages(key, messages)
    deleted_message = chat_store.delete_message(key, 0)
    assert (
        messages[0] == deleted_message
    ), "Deleted message should match the first message"
    assert chat_store.get_messages(key) == [
        messages[1],
    ], "Remaining messages should match the second message"


def test_delete_last_message(chat_store):
    key = "test_key"
    messages = [
        UserPromptMessage(content="Hello world", name=None),
        UserPromptMessage(content="Hello again", name=None),
    ]
    chat_store.set_messages(key, messages)
    last_message = chat_store.delete_last_message(key)
    assert (
        messages[-1] == last_message
    ), "Deleted last message should match the last message"
    assert chat_store.get_messages(key) == [
        messages[0],
    ], "Remaining messages should match the first message"


@pytest.mark.asyncio
async def test_put_and_get_all(memory):
    message = UserPromptMessage(content="Hello, world", name=None)
    await memory.add(
        MemoryInput(
            operation_type=MemoryOperation.ADD,
            run_id="test_run_id",
            messages=[message],
        ),
    )
    all_messages = memory.chat_store.get_messages("test_run_id")
    assert message in all_messages


@pytest.mark.asyncio
async def test_set_and_reset(memory):
    messages = [
        UserPromptMessage(content="Hello, world", name=None),
        UserPromptMessage(content="Hello, again", name=None),
    ]
    await memory.add(
        MemoryInput(
            operation_type=MemoryOperation.ADD,
            run_id="test_run_id",
            messages=messages,
        ),
    )
    all_messages = memory.chat_store.get_messages("test_run_id")
    assert messages == all_messages
    await memory.reset(
        MemoryInput(
            operation_type=MemoryOperation.RESET,
            run_id="test_run_id",
            messages=[],
        ),
    )
    assert memory.chat_store.get_messages("test_run_id") == []


@pytest.mark.asyncio
async def test_arun(memory):
    messages = [
        UserPromptMessage(content="Hello, world", name=None),
        UserPromptMessage(content="Hello, again", name=None),
    ]
    await memory.arun(
        MemoryInput(
            operation_type=MemoryOperation.ADD,
            run_id="test_run_id",
            messages=messages,
        ),
    )
    all_messages = memory.chat_store.get_messages("test_run_id")
    assert messages == all_messages
    await memory.arun(
        MemoryInput(
            operation_type=MemoryOperation.RESET,
            run_id="test_run_id",
            messages=[],
        ),
    )
    assert memory.chat_store.get_messages("test_run_id") == []
