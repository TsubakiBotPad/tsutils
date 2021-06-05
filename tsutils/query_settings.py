import re
from enum import Enum
from typing import Any, Dict

from tsutils.enums import Server, EvoToFocus, AltEvoSort, ChildMenuSelector

SETTINGS_REGEX = re.compile(r'(?:--|—)(\w+)(?::{(.+?)})?')


class QuerySettings:
    SERIALIZED_VALUES = ['server', 'evosort', 'menuselect']
    NAMES_TO_ENUMS = {
        'na_prio': EvoToFocus,
        'server': Server,
        'evosort': AltEvoSort,
        'menuselect': ChildMenuSelector,
    }
    ENUMS_TO_NAMES = {v: k for k, v in NAMES_TO_ENUMS.items()}
    SETTINGS_TO_ENUMS = {
        "na": Server.NA,
        "allservers": Server.COMBINED,
        "dfs": AltEvoSort.dfs,
        "numerical": AltEvoSort.numerical,
        "nadiff": ChildMenuSelector.NaDiffMenu,
        "awakenings": ChildMenuSelector.AwakeningList,
    }

    def __init__(self,
                 na_prio: EvoToFocus = EvoToFocus.naprio,
                 server: Server = Server.COMBINED,
                 evosort: AltEvoSort = AltEvoSort.dfs,
                 menuselect: ChildMenuSelector = ChildMenuSelector.IdMenu):
        self.na_prio = na_prio
        self.server = server
        self.evosort = evosort
        self.menuselect = menuselect

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
