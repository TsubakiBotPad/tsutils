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
