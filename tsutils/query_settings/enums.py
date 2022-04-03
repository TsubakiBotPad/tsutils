from enum import Enum


class EvoToFocus(Enum):
    newest = 0
    naprio = 1


class OrModifierPriority(Enum):
    orfirst = True
    orlast = False


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


class CardModeModifier(Enum):
    solo = 0
    coop = 1


class CardLevelModifier(Enum):
    lvmax = 0
    lv110 = 1
    lv120 = 2


class MonsterLinkTarget(Enum):
    padindex = 0
    ilmina = 1


class ShowHelp(Enum):
    help = True
    content = False
