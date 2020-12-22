import asyncio
import io


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


class CtxIO(io.IOBase):
    def __init__(self, ctx):
        self.ctx = ctx
        super(CtxIO, self).__init__()

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
