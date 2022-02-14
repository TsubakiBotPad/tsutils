import asyncio
import io
import logging
from abc import ABCMeta

from discord.ext.commands import CogMeta

from .enums import Server
from .errors import IndexNotLoaded


class aobject(object):
    """Base class to allow for asynchronous __init__"""

    # noinspection PyTypeChecker
    # noinspection PyMethodParameters
    async def __anew__(cls, *args, **kwargs):
        self = super().__new__(cls)
        await self.__init__(*args, **kwargs)
        return self

    async def __ainit__(self, *args, **kwargs):
        pass

    __new__ = __anew__
    __init__ = __ainit__


class DuplicateFilter(logging.Filter):
    def __init__(self):
        super().__init__()
        self.last_log = None

    def filter(self, record):
        current_log = (record.module, record.levelno, record.msg)
        if current_log != self.last_log:
            self.last_log = current_log
            return True
        return False


class CogABCMeta(ABCMeta, CogMeta):
    """A metaclass that implements ABCMeta and CogMeta"""


class CtxIO(io.IOBase):
    def __init__(self, ctx):
        super().__init__()
        self.ctx = ctx

    def read(self):
        raise io.UnsupportedOperation("read")

    def write(self, data):
        asyncio.ensure_future(self.ctx.send(data))


class DummyObject(dict):
    def __init__(self, item=None, **kwargs):
        if item is None:
            item = {}
        item.update(kwargs)
        super().__init__(item)
        self.__dict__ = item

    def __getattr__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


class IndexDict(dict):
    def __getattribute__(self, name):
        try:
            super().__getattribute__(name)
        except KeyError:
            if isinstance(name, Server):
                raise IndexNotLoaded("Index not yet loaded")
            raise
