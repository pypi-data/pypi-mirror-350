# -*- coding: utf-8 -*-
import asyncio
import pytest
import uuid

from agentdev.base.memory import MemoryOperation
from agentdev.components.local_memory import MemoryInput
from agentdev.components.redis_memory import RedisChatStore, RedisMemory
from agentdev.schemas.message_schemas import PromptMessage


@pytest.fixture(scope="function")
def redis_store():
    # Use a test db (db=15) to avoid polluting real data
    store = RedisChatStore(
        user="default",
        password="123456",
        host="localhost",
        port=6379,
        db=0,
        key_prefix="test_memory:",
        expire_seconds=60,
    )
    yield store
    # Cleanup all test keys after each test
    for key in store.redis.scan_iter("test_memory:*"):
        store.redis.delete(key)


@pytest.fixture
def run_id():
    return f"test_run_{uuid.uuid4()}"


@pytest.fixture
def sample_messages():
    return [
        PromptMessage(role="user", content="Hello"),
        PromptMessage(role="assistant", content="Hi, how can I help you?"),
        PromptMessage(role="user", content="Tell me a joke."),
    ]


@pytest.fixture
def redis_memory():
    # 用测试db，避免污染正式数据
    memory = RedisMemory(
        host="localhost",
        port=6379,
        db=0,
        user="default",
        password="123456",
        key_prefix="test_memory:",
        expire_seconds=60,
    )
    yield memory
    # 清理
    for key in memory.chat_store.redis.scan_iter("test_memory:*"):
        memory.chat_store.redis.delete(key)


def test_add_and_get_message(redis_store, run_id):
    msg = PromptMessage(role="user", content="Hello")
    redis_store.add_message(run_id, msg)
    messages = redis_store.get_messages(run_id)
    assert len(messages) == 1
    assert messages[0].role == "user"
    assert messages[0].content == "Hello"


def test_add_messages_and_get(redis_store, run_id, sample_messages):
    redis_store.add_messages(run_id, sample_messages)
    messages = redis_store.get_messages(run_id)
    assert len(messages) == len(sample_messages)
    for m1, m2 in zip(messages, sample_messages):
        assert m1.role == m2.role
        assert m1.content == m2.content


def test_get_messages_with_dialogue_round(
    redis_store,
    run_id,
    sample_messages,
):
    redis_store.add_messages(run_id, sample_messages)
    messages = redis_store.get_messages(run_id, filters={"dialogue_round": 2})
    assert len(messages) == 2
    assert messages[0].content == sample_messages[1].content
    assert messages[1].content == sample_messages[2].content


def test_delete_messages(redis_store, run_id, sample_messages):
    redis_store.add_messages(run_id, sample_messages)
    redis_store.delete_messages(run_id)
    messages = redis_store.get_messages(run_id)
    assert messages == []


def test_redis_memory_add_and_get(redis_memory, run_id, sample_messages):
    input_data = MemoryInput(
        operation_type=MemoryOperation.ADD,
        run_id=run_id,
        messages=sample_messages,
    )
    asyncio.run(redis_memory.add(input_data))
    get_input = MemoryInput(
        operation_type=MemoryOperation.GET,
        run_id=run_id,
    )
    result = asyncio.run(redis_memory.get(get_input))
    assert len(result.messages) == len(sample_messages)
    for m1, m2 in zip(result.messages, sample_messages):
        assert m1.role == m2.role
        assert m1.content == m2.content


def test_redis_memory_get_all(redis_memory, run_id, sample_messages):
    input_data = MemoryInput(
        operation_type=MemoryOperation.ADD,
        run_id=run_id,
        messages=sample_messages,
    )
    asyncio.run(redis_memory.add(input_data))
    get_all_input = MemoryInput(
        operation_type=MemoryOperation.GET_ALL,
        run_id=run_id,
    )
    result = asyncio.run(redis_memory.get_all(get_all_input))
    assert len(result.messages) == len(sample_messages)


def test_redis_memory_search(redis_memory, run_id, sample_messages):
    input_data = MemoryInput(
        operation_type=MemoryOperation.ADD,
        run_id=run_id,
        messages=sample_messages,
    )
    asyncio.run(redis_memory.add(input_data))
    search_input = MemoryInput(
        operation_type=MemoryOperation.SEARCH,
        run_id=run_id,
        messages=[PromptMessage(role="user", content="joke")],
        filters={},
    )
    result = asyncio.run(redis_memory.search(search_input))
    assert any("joke" in m.content for m in result.messages)


def test_redis_memory_reset(redis_memory, run_id, sample_messages):
    input_data = MemoryInput(
        operation_type=MemoryOperation.ADD,
        run_id=run_id,
        messages=sample_messages,
    )
    asyncio.run(redis_memory.add(input_data))
    reset_input = MemoryInput(
        operation_type=MemoryOperation.RESET,
        run_id=run_id,
    )
    asyncio.run(redis_memory.reset(reset_input))
    get_input = MemoryInput(
        operation_type=MemoryOperation.GET,
        run_id=run_id,
    )
    result = asyncio.run(redis_memory.get(get_input))
    assert result.messages == []
