import random
import re
from enum import EnumMeta
from typing import Any, Dict

import discord
from discord.ext.commands import Bot

from tsutils.enums import Server
from tsutils.query_settings.converters import EmbedColor, InvalidArgument
from tsutils.query_settings.enums import AltEvoSort, CardLevelModifier, CardModeModifier, CardPlusModifier, \
    ChildMenuType, EvoGrouping, EvoToFocus, LsMultiplier, MonsterLinkTarget, OrModifierPriority, ShowHelp

SETTINGS_REGEX = re.compile(r'(?:--|—)(\w+)(?::(?:({)|)((?(2)[^}]+|\S+)))?')


class QuerySettings:
    # properties that need to be retained by the menu after a monster has been found
    # anything that's used only for the purpose of locating a monster/list of monsters once does not need to be here
    SERIALIZED_NAMES = ['server', 'evosort', 'child_menu_type', 'lsmultiplier', 'cardplus', 'evogrouping',
                        'cardmode', 'cardlevel', 'linktarget', 'embedcolor', 'showhelp']

    NAMES_TO_ENUMS: Dict[str, EnumMeta] = {
        'na_prio': EvoToFocus,
        'ormod_prio': OrModifierPriority,
        'server': Server,
        'evosort': AltEvoSort,
        'child_menu_type': ChildMenuType,
        'lsmultiplier': LsMultiplier,
        'cardplus': CardPlusModifier,
        'evogrouping': EvoGrouping,
        'cardmode': CardModeModifier,
        'cardlevel': CardLevelModifier,
        'linktarget': MonsterLinkTarget,
        'showhelp': ShowHelp,
    }
    NAMES_TO_CONVERTERS = {
        'embedcolor': EmbedColor,
    }
    SETTINGS_TO_ENUMS = {
        # not serialized
        "naprio": EvoToFocus.naprio,
        "newest": EvoToFocus.newest,
        "orfirst": OrModifierPriority.orfirst,
        "orlast": OrModifierPriority.orlast,
        # serialized
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
        'help': ShowHelp.help,
        'content': ShowHelp.content,
    }

    ENUMS_TO_NAMES = {v: k for k, v in NAMES_TO_ENUMS.items()}

    def __init__(self, *,
                 na_prio: EvoToFocus = EvoToFocus.naprio,
                 ormod_prio: OrModifierPriority = OrModifierPriority.orlast,
                 server: Server = Server.COMBINED,
                 evosort: AltEvoSort = AltEvoSort.dfs,
                 child_menu_type: ChildMenuType = ChildMenuType.IdMenu,
                 lsmultiplier: LsMultiplier = LsMultiplier.lsdouble,
                 cardplus: CardPlusModifier = CardPlusModifier.plus297,
                 evogrouping: EvoGrouping = EvoGrouping.groupevos,
                 cardmode: CardModeModifier = CardModeModifier.solo,
                 cardlevel: CardLevelModifier = CardLevelModifier.lv110,
                 linktarget: MonsterLinkTarget = MonsterLinkTarget.padindex,
                 showhelp: ShowHelp = ShowHelp.content,

                 embedcolor: str = "0",
                 ):
        self.na_prio = na_prio
        self.ormod_prio = ormod_prio
        self.server = server
        self.evosort = evosort
        self.child_menu_type = child_menu_type
        self.lsmultiplier = lsmultiplier
        self.cardplus = cardplus
        self.evogrouping = evogrouping
        self.cardmode = cardmode
        self.cardlevel = cardlevel
        self.linktarget = linktarget
        self.showhelp = showhelp

        self._embedcolor = embedcolor

    @property
    def embedcolor(self) -> discord.Color:
        if not self._embedcolor:
            return discord.Color.default()
        if self._embedcolor == "random":
            return discord.Color(random.randint(0x000000, 0xffffff))
        else:
            return discord.Color(int(self._embedcolor))

    @classmethod
    def extract(cls, fm_flags: Dict[str, Any], query: str, *, force_valid: bool = False) \
            -> "QuerySettings":
        """Combine a user's fm_flags and a query string to create a new QuerySettings object"""
        settings = {}

        for name, value in fm_flags.items():
            if name in cls.NAMES_TO_ENUMS:
                settings[name] = cls.NAMES_TO_ENUMS[name](value)
            elif name in cls.NAMES_TO_CONVERTERS:
                settings[name] = value

        for setting, _, data in re.findall(SETTINGS_REGEX, query.lower()):
            if setting in cls.SETTINGS_TO_ENUMS:
                value = cls.SETTINGS_TO_ENUMS[setting]
                name = cls.ENUMS_TO_NAMES[value.__class__]
                settings[name] = value
            elif setting in cls.NAMES_TO_CONVERTERS:
                try:
                    settings[setting] = cls.NAMES_TO_CONVERTERS[setting].parse(data)
                except InvalidArgument:
                    if force_valid:
                        raise

        return cls(**settings)

    @classmethod
    async def extract_raw(cls, user: discord.User, bot: Bot, query: str, *, force_valid: bool = False) \
            -> "QuerySettings":
        dbcog: Any = bot.get_cog("DBCog")
        if dbcog is None:
            fm_flags = {}
        else:
            fm_flags = await dbcog.config.user(user).fm_flags()

        return cls.extract(fm_flags, query, force_valid=force_valid)

    def serialize(self) -> Dict[str, Any]:
        ret = {}
        for key in self.SERIALIZED_NAMES:
            if key in self.NAMES_TO_ENUMS:
                ret[key] = getattr(self, key).value
            elif key in self.NAMES_TO_CONVERTERS:
                # Internally, converter names start with a '_'
                ret[key] = getattr(self, '_' + key)
        return ret

    @classmethod
    def deserialize(cls, data: Dict[str, Any]) -> "QuerySettings":
        enumdata = {}
        for key, value in data.items():
            if key in cls.NAMES_TO_ENUMS:
                enumdata[key] = cls.NAMES_TO_ENUMS[key](value)
            elif key in cls.NAMES_TO_CONVERTERS:
                enumdata[key] = value
            else:
                raise KeyError(f"Invalid key: {key}")
        return QuerySettings(**enumdata)

    @staticmethod
    def strip(cls, query: str) -> str:
        return re.sub(r' +', ' ', re.sub(r'(--|—)\w+(:{.+?}|:\S+)?', ' ', query))
