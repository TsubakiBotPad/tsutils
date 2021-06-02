import re
from enum import Enum
from typing import Any, Dict

from tsutils.enums import Server, SearchPriority, AltEvoSort

SETTINGS_REGEX = re.compile(r'(?:--|—)(\w+)(?::{(.+?)})?')


class QuerySettings:
    SERIALIZED_VALUES = ['server', 'evosort']
    NAMES_TO_ENUMS = {
        'na_prio': SearchPriority,
        'server': Server,
        'evosort': AltEvoSort,
    }

    def __init__(self,
                 na_prio: SearchPriority = SearchPriority.naprio,
                 server: Server = Server.COMBINED,
                 evosort: AltEvoSort = AltEvoSort.gungho):
        self.na_prio = na_prio
        self.server = server
        self.evosort = evosort

    @staticmethod
    def extract(fm_flags: Dict[str, Any], query: str) -> "QuerySettings":
        # TODO: Eventually remove this suite once we use Enums everywhere
        for key, value in fm_flags:
            if not isinstance(value, Enum):
                fm_flags[key] = QuerySettings.NAMES_TO_ENUMS[key](value)  # noqa

        for setting, data in re.findall(SETTINGS_REGEX, query):
            if setting == "na":
                fm_flags['server'] = Server.NA
            elif setting == "allservers":
                fm_flags['server'] = Server.COMBINED

            if setting in ("gungho", "normal"):
                fm_flags['evosort'] = AltEvoSort.gungho
            elif setting == "numerical":
                fm_flags['server'] = AltEvoSort.numerical

        return QuerySettings(**fm_flags)

    def serialize(self: "QuerySettings") -> Dict[str, Any]:
        return {v: getattr(self, v).value for v in self.SERIALIZED_VALUES}

    @staticmethod
    def deserialize(data: Dict[str, Any]) -> "QuerySettings":
        enumdata = {}
        for key, value in data.values():
            enumdata[key] = QuerySettings.NAMES_TO_ENUMS[key](value)  # noqa

        return QuerySettings(**data)
