import urllib.parse
from typing import Optional

from tsutils.pad import get_pdx_id
from tsutils.query_settings.enums import MonsterLinkTarget
from tsutils.query_settings.query_settings import QuerySettings

CLOUDFRONT_URL = "https://d30r6ivozz8w2a.cloudfront.net"
MEDIA_PATH = CLOUDFRONT_URL + '/media/'
ICON_TEMPLATE = MEDIA_PATH + 'icons/{0:05d}.png'
RPAD_PIC_TEMPLATE = MEDIA_PATH + 'portraits/{0:05d}.png?cachebuster=2'
VIDEO_TEMPLATE = MEDIA_PATH + 'animated_portraits/{0:05d}.mp4'
GIF_TEMPLATE = MEDIA_PATH + 'animated_portraits/{0:05d}.gif'
ORB_SKIN_TEMPLATE = MEDIA_PATH + 'orb_skins/jp/{0:03d}.png'
ORB_SKIN_CB_TEMPLATE = MEDIA_PATH + 'orb_skins/jp/{0:03d}cb.png'

INFO_PDX_TEMPLATE = 'http://www.puzzledragonx.com/en/monster.asp?n={}'
YT_SEARCH_TEMPLATE = 'https://www.youtube.com/results?search_query={}'
SKYOZORA_TEMPLATE = 'http://pad.skyozora.com/pets/{}'
ILMINA_TEMPLATE = 'https://ilmina.com/#/CARD/{}'
PADINDEX_TEMPLATE = 'https://pad.chesterip.cc/{}'


class MonsterImage:
    @staticmethod
    def icon(idx: int):
        return ICON_TEMPLATE.format(idx)

    @staticmethod
    def picture(monster_id: int):
        return RPAD_PIC_TEMPLATE.format(monster_id)

    @staticmethod
    def video(monster_no_jp: int):
        return VIDEO_TEMPLATE.format(monster_no_jp)

    @staticmethod
    def gif(monster_no_jp: int):
        return GIF_TEMPLATE.format(monster_no_jp)

    @staticmethod
    def orb_skin(orb_skin_id: int):
        return ORB_SKIN_TEMPLATE.format(orb_skin_id)

    @staticmethod
    def orb_skin_colorblind(orb_skin_id: int):
        return ORB_SKIN_CB_TEMPLATE.format(orb_skin_id)


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
    def header_link(m, query_settings: Optional[QuerySettings] = None):
        if not m.on_na:
            return MonsterLink.padindex(m)
        if query_settings is None:
            return MonsterLink.padindex(m)
        return MonsterLink.padindex(m) \
            if query_settings.linktarget == MonsterLinkTarget.padindex \
            else MonsterLink.ilmina(m)
