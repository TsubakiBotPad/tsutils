import re
from abc import ABC, abstractmethod

from discord.ext.commands import BadArgument


class InvalidArgument(BadArgument):
    pass


class Validator(ABC):
    def __new__(cls, *args, **kwargs):
        raise TypeError("Validators cannot be instantiated")
    
    @classmethod
    @abstractmethod
    def convert(cls, arg: str) -> str:
        ...


class Color(Validator):
    COLORS = {
        'blue': 0x3498db,
        'blurple': 0x7289da,
        'dark_blue': 0x206694,
        'dark_gold': 0xc27c0e,
        'dark_gray': 0x607d8b,
        'dark_green': 0x1f8b4c,
        'dark_grey': 0x607d8b,
        'dark_magenta': 0xad1457,
        'dark_orange': 0xa84300,
        'dark_purple': 0x71368a,
        'dark_red': 0x992d22,
        'dark_teal': 0x11806a,
        'dark_theme': 0x36393f,
        'darker_gray': 0x546e7a,
        'darker_grey': 0x546e7a,
        'default': 0x000000,
        'gold': 0xf1c40f,
        'green': 0x2ecc71,
        'greyple': 0x99aab5,
        'light_gray': 0x979c9f,
        'light_grey': 0x979c9f,
        'lighter_gray': 0x95a5a6,
        'lighter_grey': 0x95a5a6,
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
    def convert(cls, arg: str) -> str:
        if arg in cls.COLORS:
            return str(cls.COLORS[arg])
        elif re.match(r"^#?[0-9a-fA-F]{6}$", arg):
            return str(int(arg.lstrip("#"), 16))
        else:
            raise InvalidArgument("Invalid color!  Valid colors are any hexcode and:\n" + ", ".join(cls.COLORS))
