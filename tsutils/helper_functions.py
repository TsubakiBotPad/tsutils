import asyncio
import discord.ext
import errno
import os
import signal
from functools import wraps
from typing import Any, AsyncGenerator, Callable, Coroutine, Iterable, Mapping, Optional, TypeVar

Decorator = Callable[[Callable], Callable]
DecoratorFunction = Callable[..., Decorator]

R = TypeVar("R")


def timeout_after(seconds: int = 10,
                  error_message: str = os.strerror(errno.ETIME)) \
        -> Decorator:
    """A decorator to give a timeout to a synchronous function"""

    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


def corowrap(coro, loop):
    """Turns a Coroutine into a fake synchronous function for some reason???"""

    # TODO: Remove this.  Oh god, why would I write this???
    def func(*args, **kwargs):
        fut = asyncio.run_coroutine_threadsafe(coro, loop)
        try:
            fut.result()
        except Exception:
            pass

    return func


async def conditional_iterator(condition: Callable[[], Coroutine[None, None, Optional[R]]],
                               poll_interval: int = 0) \
        -> AsyncGenerator[R, None]:
    """An async generator that only yields when the condition is not None or False"""
    while True:
        value = await condition()
        if value is not None and value is not False:
            yield value
        await asyncio.sleep(poll_interval)


async def repeating_timer(seconds: int,
                          condition: Optional[Callable[[], bool]] = None,
                          start_immediately: bool = True) \
        -> AsyncGenerator[None, None]:
    """Yields every N seconds"""
    if condition is None:
        def condition():
            return True
    if start_immediately and condition():
        yield
    while condition():
        await asyncio.sleep(seconds)
        yield


def deepget(mapping: Mapping, keys: Iterable, default: Any) -> Any:
    """Get a value from deep in a nested Mapping returning the default if any of the keys are invalid"""
    o = mapping
    for key in keys:
        try:
            o = o[key]
        except KeyError:
            return default
    return o


def make_non_gatekeeping_check(condition: Callable[..., bool], failmessage: str) \
        -> DecoratorFunction:
    """Creates a check decorator that doesn't stop the a user from seeing a command.

    It only shows a "You don't have permission to use this" string (specified by failmessage)
    if an invalid user tries to use it.
    """

    def non_gatekeep_check(**kwargs):
        def decorator(command):
            @command.before_invoke
            async def hook(instance, ctx):
                if not condition(ctx, **kwargs):
                    await ctx.send(failmessage.format(ctx))
                    raise discord.ext.commands.CheckFailure()

            return command

        return decorator

    return non_gatekeep_check
