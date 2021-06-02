from enum import Enum

class Server(Enum):
    COMBINED = "COMBINED"
    JP = "JP"
    NA = "NA"
    KR = "KR"


# These are True and False for backwards compatablility.  More values can be added.
class EvoToFocus(Enum):
    newest = 0
    naprio = 1


class AltEvoSort(Enum):
    gungho = 0
    numerical = 1
