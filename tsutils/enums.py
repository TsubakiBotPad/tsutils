from enum import Enum

from discord.ext.commands import BadArgument


class Server(Enum):
    COMBINED = "COMBINED"
    JP = "JP"
    NA = "NA"
    KR = "KR"

    @classmethod
    async def convert(cls, ctx, argument):
        if argument.upper() == ('JP', 'JA'):
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


class EvoToFocus(Enum):
    newest = 0
    naprio = 1


class AltEvoSort(Enum):
    dfs = 0
    numerical = 1


class ChildMenuType(Enum):
    IdMenu = 0
    NaDiffMenu = 1
    AwakeningList = 2


class LsMultiplier(Enum):
    lsdouble = 0
    lssingle = 1


class CardPlusModifier(Enum):
    plus0 = 0
    plus297 = 1


class EvoGrouping(Enum):
    splitevos = 0
    groupevos = 1
