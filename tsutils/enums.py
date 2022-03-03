from enum import Enum

from discord.ext.commands import BadArgument


class Server(Enum):
    COMBINED = "COMBINED"
    JP = "JP"
    NA = "NA"
    KR = "KR"

    @classmethod
    async def convert(cls, ctx, argument):
        if argument.upper() in ('JP', 'JA'):
            return Server.JP
        elif argument.upper() in ('NA', 'EN', 'US'):
            return Server.NA
        elif argument.upper() in ('KR', 'KO'):
            return Server.KR
        else:
            raise BadArgument(f"Unable to convert server `{argument}`")


class StarterGroup(Enum):
    RED = 0
    BLUE = 1
    GREEN = 2

    @classmethod
    async def convert(cls, ctx, argument):
        if 'RED'.startswith(argument.upper()):
            return StarterGroup.RED
        elif 'BLUE'.startswith(argument.upper()):
            return StarterGroup.BLUE
        elif 'GREEN'.startswith(argument.upper()):
            return StarterGroup.GREEN
        else:
            raise BadArgument(f"Unable to convert group `{argument}`")
