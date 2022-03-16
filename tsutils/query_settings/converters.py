import re
from abc import ABCMeta, abstractmethod

from discord.ext.commands import BadArgument, Converter


class InvalidArgument(BadArgument):
    pass


class QSConverter(Converter, metaclass=ABCMeta):
    @classmethod
    async def convert(cls, ctx, arg: str) -> str:
        return cls.parse(arg)

    @classmethod
    @abstractmethod
    def parse(cls, arg: str) -> str:
        ...


class EmbedColor(QSConverter):
    COLORS = {
        'blue': 0x3498db,
        'blurple': 0x7289da,
        'dark blue': 0x206694,
        'dark gold': 0xc27c0e,
        'dark gray': 0x607d8b,
        'dark green': 0x1f8b4c,
        'dark grey': 0x607d8b,
        'dark magenta': 0xad1457,
        'dark orange': 0xa84300,
        'dark purple': 0x71368a,
        'dark red': 0x992d22,
        'dark teal': 0x11806a,
        'dark theme': 0x36393f,
        'darker gray': 0x546e7a,
        'darker grey': 0x546e7a,
        'default': 0x000000,
        'gold': 0xf1c40f,
        'green': 0x2ecc71,
        'greyple': 0x99aab5,
        'light gray': 0x979c9f,
        'light grey': 0x979c9f,
        'lighter gray': 0x95a5a6,
        'lighter grey': 0x95a5a6,
        'magenta': 0xe91e63,
        'orange': 0xe67e22,
        'pink': 0xffa1dd,
        'purple': 0x9b59b6,
        'red': 0xe74c3c,
        'teal': 0x1abc9c,

        'clear': 0,
        'random': 'random',
    }

    @classmethod
    def parse(cls, arg):
        arg = arg.strip().replace('_', ' ')
        if arg in cls.COLORS:
            return str(cls.COLORS[arg])
        elif re.match(r"^#?[0-9a-fA-F]{6}$", arg):
            return str(int(arg.lstrip("#"), 16))
        else:
            raise InvalidArgument(f"Invalid color: {arg}! Valid colors are any hexcode and {', '.join(cls.COLORS)}")
