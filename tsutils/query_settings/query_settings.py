import random
import re
from enum import Enum, EnumMeta
from typing import Any, Dict

import discord

from tsutils.enums import Server
from tsutils.query_settings.enums import EvoToFocus, AltEvoSort, ChildMenuType, LsMultiplier, CardPlusModifier, \
    EvoGrouping, CardModeModifier, CardLevelModifier, MonsterLinkTarget
from tsutils.query_settings.validators import InvalidArgument, EmbedColor

SETTINGS_REGEX = re.compile(r'(?:--|—)(\w+)(?::{(.+?)})?')


class QuerySettings:
    SERIALIZED_VALUES = ['server', 'evosort', 'child_menu_type', 'lsmultiplier', 'cardplus', 'evogrouping',
                         'cardmode', 'cardlevel', 'linktarget', 'embedcolor']
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
        'linktarget': MonsterLinkTarget,
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
        'ilmina': MonsterLinkTarget.ilmina,
        'padindex': MonsterLinkTarget.padindex,
        'chesterip': MonsterLinkTarget.padindex,
    }
    NAMES_TO_VALIDATORS = {
        'embedcolor': EmbedColor,
    }

    def __init__(self, *,
                 na_prio: EvoToFocus = EvoToFocus.naprio,
                 server: Server = Server.COMBINED,
                 evosort: AltEvoSort = AltEvoSort.dfs,
                 child_menu_type: ChildMenuType = ChildMenuType.IdMenu,
                 lsmultiplier: LsMultiplier = LsMultiplier.lsdouble,
                 cardplus: CardPlusModifier = CardPlusModifier.plus297,
                 evogrouping: EvoGrouping = EvoGrouping.groupevos,
                 cardmode: CardModeModifier = CardModeModifier.solo,
                 cardlevel: CardLevelModifier = CardLevelModifier.lv110,
                 linktarget: MonsterLinkTarget = MonsterLinkTarget.padindex,

                 embedcolor: str = "0",
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
        self.linktarget = linktarget

        self.embedcolor = embedcolor

    @classmethod
    async def extract_raw(cls, user: discord.User, bot, query: str) -> "QuerySettings":
        return cls.extract(await cls._get_flags(user, bot), query)

    @classmethod
    def extract(cls, fm_flags: Dict[str, Any], query: str) -> "QuerySettings":
        fm_flags = fm_flags.copy()
        for key, value in fm_flags.items():
            if not isinstance(value, Enum):
                setting = QuerySettings.NAMES_TO_ENUMS.get(key)
                if isinstance(setting, EnumMeta):
                    fm_flags[key] = setting(value)

        for setting, data in re.findall(SETTINGS_REGEX, query.lower()):
            if setting in cls.SETTINGS_TO_ENUMS:
                value = cls.SETTINGS_TO_ENUMS[setting]
                key = cls.ENUMS_TO_NAMES[type(value)]
                fm_flags[key] = value
            elif setting in cls.NAMES_TO_VALIDATORS:
                try:
                    fm_flags[setting] = cls.NAMES_TO_VALIDATORS[setting].convert(data)  # noqa
                except InvalidArgument:
                    pass
        return QuerySettings(**fm_flags)

    def serialize(self: "QuerySettings") -> Dict[str, Any]:
        ret = {}
        for key in self.SERIALIZED_VALUES:
            setting = getattr(self, key)
            if setting:
                if key in self.NAMES_TO_ENUMS.keys():
                    ret[key] = setting.value
                else:
                    ret[key] = setting
        return ret

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "QuerySettings":
        enumdata = {}
        for key, value in data.items():
            if key in cls.NAMES_TO_ENUMS:
                enumdata[key] = cls.NAMES_TO_ENUMS[key](value)  # noqa
            elif key in cls.NAMES_TO_VALIDATORS:
                enumdata[key] = value
            else:
                raise KeyError(f"Invalid key: {key}")
        return QuerySettings(**enumdata)

    @staticmethod
    async def _get_flags(user: discord.User, bot) -> Dict[str, Any]:
        return await bot.get_cog("DBCog").config.user(user).fm_flags()

    def get_embedcolor(self):
        if self.embedcolor is None:
            return discord.Color.default()
        elif self.embedcolor == "random":
            return discord.Color(random.randint(0x000000, 0xffffff))
        else:
            return discord.Color(self.embedcolor)
