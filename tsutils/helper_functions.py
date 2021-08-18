import asyncio
import discord.ext
import errno
import os
import signal
from functools import wraps


def timeout_after(seconds=10, error_message=os.strerror(errno.ETIME)):
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
    def func(*args, **kwargs):
        fut = asyncio.run_coroutine_threadsafe(coro, loop)
        try:
            fut.result()
        except Exception:
            pass

    return func


def fawait(coro, loop):
    fut = asyncio.run_coroutine_threadsafe(coro, loop)
    try:
        fut.result()
    except Exception:
        pass


async def repeating_timer(seconds, condition=None, start_immediately=True):
    if condition is None:
        def condition():
            return True
    if start_immediately:
        yield
    while condition():
        await asyncio.sleep(seconds)
        yield


def deepget(mapping, keys, default):
    o = mapping
    for key in keys:
        try:
            o = o[key]
        except KeyError:
            return default
    return o


def make_non_gatekeeping_check(condition, failmessage):
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
