from enum import Enum


class SmartEqEnum(Enum):
    def __eq__(self, other):
        if isinstance(other, Enum):
            return self.name == other.name \
                   and self.value == other.value \
                   and self.__class__.__name__ == other.__class__.__name__
        return False

class Server(SmartEqEnum):
    COMBINED = "COMBINED"
    JP = "JP"
    NA = "NA"
    KR = "KR"


class EvoToFocus(SmartEqEnum):
    newest = 0
    naprio = 1


class AltEvoSort(SmartEqEnum):
    dfs = 0
    numerical = 1


class ChildMenuSelector(SmartEqEnum):
    IdMenu = 0
    NaDiffMenu = 1
    AwakeningList = 2
