import asyncio


def async_to_sync(awaitable):
    """Run your async code in sync mode"""
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(awaitable)


def sync_to_async(func):
    """Run your sync code in async mode"""

    async def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper
