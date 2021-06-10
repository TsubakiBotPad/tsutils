from enum import Enum


class Server(Enum):
    COMBINED = "COMBINED"
    JP = "JP"
    NA = "NA"
    KR = "KR"


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
