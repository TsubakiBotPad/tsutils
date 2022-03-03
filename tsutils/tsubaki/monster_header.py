from typing import Optional

from discordmenu.embed.base import Box
from discordmenu.embed.text import LinkedText, Text

from tsutils.enums import Server
from tsutils.query_settings.query_settings import QuerySettings
from tsutils.tsubaki.custom_emoji import get_attribute_emoji_by_monster
from tsutils.tsubaki.links import MonsterLink


class MonsterHeader:
    @classmethod
    def menu_title(cls, m, *, is_tsubaki=False, is_jp_buffed=False,
                   use_emoji=False):
        return Text('{}{} {}'.strip().format(
            get_attribute_emoji_by_monster(m) if use_emoji else '',
            '\N{EARTH GLOBE AMERICAS}' if m.server_priority == Server.NA else '',
            cls._maybe_tsubaki(m, is_tsubaki=is_tsubaki, is_jp_buffed=bool(is_jp_buffed))))

    @classmethod
    def box_with_emoji(cls, m, *, link=True, prefix=None,
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
    def text_with_emoji(cls, m, *, prefix=None,
                        query_settings: Optional[QuerySettings] = None):
        return cls.box_with_emoji(m, link=False, prefix=prefix,
                                  query_settings=query_settings).to_markdown()

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
    def _maybe_tsubaki(cls, m, is_tsubaki, is_jp_buffed=False):
        """Returns the monster name as well as an `!` if the monster is Tsubaki

        To celebrate 1000 issues/PRs in our main Tsubaki repo, we added this easter egg! Yay!
        """
        tsubaki_punctuation = '!' if is_tsubaki else ''
        suffix = cls._jp_suffix(m, is_jp_buffed)
        return f'[{m.monster_no_na}] {m.name_en}{tsubaki_punctuation}{suffix}'
