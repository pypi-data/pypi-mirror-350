from typing import Awaitable
import asyncio


__all__ = (
    'async_to_sync',
)


def async_to_sync(awaitable: Awaitable):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(awaitable)
