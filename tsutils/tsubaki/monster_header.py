from typing import Optional

from discordmenu.embed.base import Box
from discordmenu.embed.text import LinkedText, Text

from tsutils.enums import Server
from tsutils.query_settings import QuerySettings
from tsutils.tsubaki.emoji_map import get_attribute_emoji_by_monster
from tsutils.tsubaki.tsubaki import MonsterLink


class MonsterHeader:
    @classmethod
    def linked_box(cls, m, show_jp=False, query_settings: Optional[QuerySettings] = None):
        return cls.box(m, link=True, show_jp=show_jp, query_settings=query_settings)

    @classmethod
    def box(cls, m, link=False, show_jp=False,
            query_settings: Optional[QuerySettings] = None):
        msg = '[{}] {}{}'.format(
            m.monster_no_na,
            m.name_en,
            cls._jp_suffix(m) if show_jp else '')
        return LinkedText(msg, MonsterLink.header_link(m, query_settings=query_settings)) if link else Text(msg)

    @classmethod
    def header_plaintext(cls, m, is_tsubaki=False, is_jp_buffed=False,
                         use_emoji=False):
        return Text('{}{} {}'.strip().format(
            get_attribute_emoji_by_monster(m) if use_emoji else '',
            '\N{EARTH GLOBE AMERICAS}' if m.server_priority == Server.NA else '',
            cls._long_maybe_tsubaki(m, is_tsubaki, bool(is_jp_buffed))))

    @classmethod
    def text_with_emoji(cls, m, link=True, prefix=None,
                        query_settings: Optional[QuerySettings] = None):
        msg = f"{m.monster_no_na} - {m.name_en}"
        suffix = cls._jp_suffix(m, False, False)
        return Box(
            prefix,
            Text(get_attribute_emoji_by_monster(m)),
            LinkedText(msg, MonsterLink.header_link(m, query_settings=query_settings)) if link else Text(msg),
            Text(suffix) if suffix else None,
            delimiter=' '
        )

    @classmethod
    def _jp_suffix(cls, m, is_jp_buffed=False, subname_on_override=True):
        suffix = ""
        if m.roma_subname and (subname_on_override or m.name_en_override is None):
            suffix += ' [{}]'.format(m.roma_subname)
        if not m.on_na:
            suffix += ' (JP only)'
        if is_jp_buffed:
            suffix += ' (JP buffed)'
        return suffix

    @classmethod
    def _long_maybe_tsubaki(cls, m, is_tsubaki, is_jp_buffed=False):
        """Returns long_v2 as well as an `!` if the monster is Tsubaki

        To celebrate 1000 issues/PRs in our main Tsubaki repo, we added this easter egg! Yay!
        """
        return '[{}] {}{}{}'.format(
            m.monster_no_na,
            m.name_en,
            '!' if is_tsubaki else '',
            cls._jp_suffix(m, is_jp_buffed))
