# -*- coding: utf-8 -*-
from typing import AsyncIterable, AsyncIterator, Tuple, TypeVar

T = TypeVar("T")


async def aenumerate(
    asequence: AsyncIterable[T],
    start: int = 0,
) -> AsyncIterator[Tuple[int, T]]:
    """Asynchronously enumerate an async iterator from a given start value"""
    n = start
    async for elem in asequence:
        yield n, elem
        n += 1
