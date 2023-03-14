import urllib.parse
from typing import Optional, Union

from tsutils.pad import get_pdx_id
from tsutils.query_settings.enums import MonsterLinkTarget
from tsutils.query_settings.query_settings import QuerySettings

# cachebreak is a bit zzz because python gets real mad when fstrings are combined and
# they only sometimes have text inside the brackets.
# see: https://stackoverflow.com/questions/46768088/valueerror-cannot-switch-from-manual-field-specification-to-automatic-field-num
# of course, this is not what we're doing, but still.

CLOUDFRONT_URL = "https://d30r6ivozz8w2a.cloudfront.net"
PICS_URL = "https://pics.tsubakibot.com/index.html"
MEDIA_PATH = CLOUDFRONT_URL + '/media/'
ICON_TEMPLATE = MEDIA_PATH + 'icons/{0:05d}'
REGULAR_SUFFIX = '.png'
CACHEBREAK_SUFFIX = '_{}.png'
ICON_PATH = ICON_TEMPLATE + CACHEBREAK_SUFFIX
RPAD_PIC_TEMPLATE = MEDIA_PATH + 'portraits/{0:05d}.png'
VIDEO_TEMPLATE = MEDIA_PATH + 'animated_portraits/{0:05d}.mp4'
GIF_TEMPLATE = MEDIA_PATH + 'animated_portraits/{0:05d}.gif'
HQ_GIF_TEMPLATE = MEDIA_PATH + 'animated_portraits/{0:05d}_hq.gif'
SPINE_TEMPLATE = PICS_URL + '?m={0:d}'
ORB_SKIN_TEMPLATE = MEDIA_PATH + 'orb_skins/jp/{0:03d}.png'
ORB_SKIN_CB_TEMPLATE = MEDIA_PATH + 'orb_skins/jp/{0:03d}cb.png'

INFO_PDX_TEMPLATE = 'http://www.puzzledragonx.com/en/monster.asp?n={}'
YT_SEARCH_TEMPLATE = 'https://www.youtube.com/results?search_query={}'
SKYOZORA_TEMPLATE = 'http://pad.skyozora.com/pets/{}'
ILMINA_TEMPLATE = 'https://ilmina.com/#/CARD/{}'
PADINDEX_TEMPLATE = 'https://pad.chesterip.cc/{}'


class MonsterImage:
    @staticmethod
    def icon(idx: int, cachebreak: Optional[Union[str, int]] = None):
        if cachebreak is None:
            return ICON_TEMPLATE.format(idx) + REGULAR_SUFFIX
        return ICON_TEMPLATE.format(idx) + CACHEBREAK_SUFFIX.format(cachebreak)

    @staticmethod
    def picture(monster_id: int):
        return RPAD_PIC_TEMPLATE.format(monster_id)

    @staticmethod
    def video(monster_id: int):
        return VIDEO_TEMPLATE.format(monster_id)

    @staticmethod
    def gif(monster_id: int):
        return GIF_TEMPLATE.format(monster_id)

    @staticmethod
    def hq_gif(monster_id: int):
        return HQ_GIF_TEMPLATE.format(monster_id)

    @staticmethod
    def spine(monster_id: int):
        return SPINE_TEMPLATE.format(monster_id)

    @staticmethod
    def orb_skin(monster_id: int):
        return ORB_SKIN_TEMPLATE.format(monster_id)

    @staticmethod
    def orb_skin_colorblind(monster_id: int):
        return ORB_SKIN_CB_TEMPLATE.format(monster_id)


class MonsterLink:
    @staticmethod
    def puzzledragonx(m):
        return INFO_PDX_TEMPLATE.format(get_pdx_id(m))

    @staticmethod
    def youtube_search(m):
        return YT_SEARCH_TEMPLATE.format(urllib.parse.quote(m.name_ja))

    @staticmethod
    def skyozora(m):
        return SKYOZORA_TEMPLATE.format(m.monster_no_jp)

    @staticmethod
    def ilmina(m):
        return ILMINA_TEMPLATE.format(m.monster_no_jp)

    @staticmethod
    def ilmina_skill(m):
        return "https://ilmina.com/#/SKILL/{}".format(m.active_skill.active_skill_id) if m.active_skill else None

    @staticmethod
    def padindex(m):
        return PADINDEX_TEMPLATE.format(m.monster_no_jp)

    @staticmethod
    def header_link(m, qs: Optional[QuerySettings] = None):
        if not m.on_na:
            return MonsterLink.padindex(m)
        elif not m.on_jp:
            return MonsterLink.ilmina(m)

        if qs is None or qs.linktarget == MonsterLinkTarget.padindex:
            return MonsterLink.padindex(m)
        else:
            return MonsterLink.ilmina(m)
