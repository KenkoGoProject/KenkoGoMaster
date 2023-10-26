import asyncio
from typing import Coroutine, TypeVar

T = TypeVar('T')


def __ensure_event_loop() -> None:
    try:
        asyncio.get_event_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())


def sync(coroutine: Coroutine[any, any, T]) -> T:
    """同步执行异步函数"""
    __ensure_event_loop()
    loop = asyncio.get_event_loop()
    return loop.create_task(coroutine) if loop.is_running() else loop.run_until_complete(coroutine)
