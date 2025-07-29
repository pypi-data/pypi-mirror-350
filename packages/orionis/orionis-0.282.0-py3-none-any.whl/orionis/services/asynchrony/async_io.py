import asyncio
from typing import Any, Coroutine, TypeVar, Union

T = TypeVar("T")

def run_coroutine(coro: Coroutine[Any, Any, T]) -> Union[T, asyncio.Future]:
    """
    Executes the given coroutine object, adapting to the current execution context.
    If there is an active event loop, it uses `asyncio.ensure_future` to schedule the coroutine.
    If there is no active event loop, it uses `asyncio.run` to run the coroutine directly.
    If the coroutine is already running, it returns a `Future` object that can be awaited.

    Parameters
    ----------
    coro : Coroutine[Any, Any, T]
        The coroutine object
    """
    from inspect import iscoroutine

    if not iscoroutine(coro):
        raise TypeError("Expected a coroutine object.")

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    if loop.is_running():
        return asyncio.ensure_future(coro)
    else:
        return loop.run_until_complete(coro)
