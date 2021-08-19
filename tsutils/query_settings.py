import re
from enum import Enum
from typing import Any, Dict

from .enums import AltEvoSort, CardPlusModifier, ChildMenuType, EvoGrouping, EvoToFocus, LsMultiplier, Server

SETTINGS_REGEX = re.compile(r'(?:--|—)(\w+)(?::{(.+?)})?')


class QuerySettings:
    SERIALIZED_VALUES = ['server', 'evosort', 'child_menu_type', 'lsmultiplier', 'cardplus', 'evogrouping']
    NAMES_TO_ENUMS = {
        'na_prio': EvoToFocus,
        'server': Server,
        'evosort': AltEvoSort,
        'child_menu_type': ChildMenuType,
        'lsmultiplier': LsMultiplier,
        'cardplus': CardPlusModifier,
        'evogrouping': EvoGrouping,
    }
    ENUMS_TO_NAMES = {v: k for k, v in NAMES_TO_ENUMS.items()}
    SETTINGS_TO_ENUMS = {
        "na": Server.NA,
        "allservers": Server.COMBINED,
        "dfs": AltEvoSort.dfs,
        "numerical": AltEvoSort.numerical,
        "nadiff": ChildMenuType.NaDiffMenu,
        "nadiffs": ChildMenuType.NaDiffMenu,
        "awakening": ChildMenuType.AwakeningList,
        "awakenings": ChildMenuType.AwakeningList,
        'lsdouble': LsMultiplier.lsdouble,
        'lssingle': LsMultiplier.lssingle,
        'lss': LsMultiplier.lssingle,
        'plus0': CardPlusModifier.plus0,
        'plus297': CardPlusModifier.plus297,
        'splitevos': EvoGrouping.splitevos,
        'groupevos': EvoGrouping.groupevos,
    }

    def __init__(self,
                 na_prio: EvoToFocus = EvoToFocus.naprio,
                 server: Server = Server.COMBINED,
                 evosort: AltEvoSort = AltEvoSort.dfs,
                 child_menu_type: ChildMenuType = ChildMenuType.IdMenu,
                 lsmultiplier: LsMultiplier = LsMultiplier.lsdouble,
                 cardplus: CardPlusModifier = CardPlusModifier.plus297,
                 evogrouping: EvoGrouping = EvoGrouping.splitevos,
                 ):
        self.na_prio = na_prio
        self.server = server
        self.evosort = evosort
        self.child_menu_type = child_menu_type
        self.lsmultiplier = lsmultiplier
        self.cardplus = cardplus
        self.evogrouping = evogrouping

    @classmethod
    def extract(cls, fm_flags: Dict[str, Any], query: str) -> "QuerySettings":
        fm_flags = fm_flags.copy()
        for key, value in fm_flags.items():
            if not isinstance(value, Enum):
                fm_flags[key] = QuerySettings.NAMES_TO_ENUMS[key](value)  # noqa

        for setting, data in re.findall(SETTINGS_REGEX, query.lower()):
            if setting not in cls.SETTINGS_TO_ENUMS:
                continue
            value = cls.SETTINGS_TO_ENUMS[setting]
            key = cls.ENUMS_TO_NAMES[type(value)]
            fm_flags[key] = value

        return QuerySettings(**fm_flags)

    def serialize(self: "QuerySettings") -> Dict[str, Any]:
        return {v: getattr(self, v).value for v in self.SERIALIZED_VALUES}

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> "QuerySettings":
        enumdata = {}
        for key, value in data.items():
            enumdata[key] = QuerySettings.NAMES_TO_ENUMS[key](value)  # noqa

        return QuerySettings(**enumdata)
