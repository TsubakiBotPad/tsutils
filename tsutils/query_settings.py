import re
from enum import Enum
from typing import Any, Dict

from tsutils.enums import Server, EvoToFocus, AltEvoSort, ChildMenuType, LsMultiplier, CardPlusModifier, \
    EvoGrouping, CardModeModifier, CardLevelModifier

SETTINGS_REGEX = re.compile(r'(?:--|—)(\w+)(?::{(.+?)})?')


class QuerySettings:
    SERIALIZED_VALUES = ['server', 'evosort', 'child_menu_type', 'lsmultiplier', 'cardplus', 'evogrouping',
                         'cardmode', 'cardlevel']
    NAMES_TO_ENUMS = {
        'na_prio': EvoToFocus,
        'server': Server,
        'evosort': AltEvoSort,
        'child_menu_type': ChildMenuType,
        'lsmultiplier': LsMultiplier,
        'cardplus': CardPlusModifier,
        'evogrouping': EvoGrouping,
        'cardmode': CardModeModifier,
        'cardlevel': CardLevelModifier,
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
        'solo': CardModeModifier.solo,
        'coop': CardModeModifier.coop,
        'lvmax': CardLevelModifier.lvmax,
        'lv110': CardLevelModifier.lv110,
        'lv120': CardLevelModifier.lv120,
    }
    SETTINGS_WITH_DATA_NAMES = []

    def __init__(self,
                 na_prio: EvoToFocus = EvoToFocus.naprio,
                 server: Server = Server.COMBINED,
                 evosort: AltEvoSort = AltEvoSort.dfs,
                 child_menu_type: ChildMenuType = ChildMenuType.IdMenu,
                 lsmultiplier: LsMultiplier = LsMultiplier.lsdouble,
                 cardplus: CardPlusModifier = CardPlusModifier.plus297,
                 evogrouping: EvoGrouping = EvoGrouping.groupevos,
                 cardmode: CardModeModifier = CardModeModifier.solo,
                 cardlevel: CardLevelModifier = CardLevelModifier.lv110,
                 ):
        self.na_prio = na_prio
        self.server = server
        self.evosort = evosort
        self.child_menu_type = child_menu_type
        self.lsmultiplier = lsmultiplier
        self.cardplus = cardplus
        self.evogrouping = evogrouping
        self.cardmode = cardmode
        self.cardlevel = cardlevel

    @classmethod
    def extract(cls, fm_flags: Dict[str, Any], query: str) -> "QuerySettings":
        fm_flags = fm_flags.copy()
        for key, value in fm_flags.items():
            if not isinstance(value, Enum):
                fm_flags[key] = QuerySettings.NAMES_TO_ENUMS[key](value)  # noqa

        for setting, data in re.findall(SETTINGS_REGEX, query.lower()):
            if setting in cls.SETTINGS_TO_ENUMS:
                value = cls.SETTINGS_TO_ENUMS[setting]
                key = cls.ENUMS_TO_NAMES[type(value)]
                fm_flags[key] = value
            elif setting in cls.SETTINGS_WITH_DATA_NAMES:
                fm_flags[setting] = data
        return QuerySettings(**fm_flags)

    def serialize(self: "QuerySettings") -> Dict[str, Any]:
        return {v: getattr(self, v).value for v in self.SERIALIZED_VALUES}

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> "QuerySettings":
        enumdata = {}
        for key, value in data.items():
            enumdata[key] = QuerySettings.NAMES_TO_ENUMS[key](value)  # noqa

        return QuerySettings(**enumdata)
