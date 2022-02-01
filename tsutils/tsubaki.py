from discordmenu.emoji.emoji_cache import emoji_cache

CLOUDFRONT_URL = "https://d30r6ivozz8w2a.cloudfront.net"
MEDIA_PATH = CLOUDFRONT_URL + '/media/'
ICON_TEMPLATE = MEDIA_PATH + 'icons/{0:05d}.png'
RPAD_PIC_TEMPLATE = MEDIA_PATH + 'portraits/{0:05d}.png?cachebuster=2'
VIDEO_TEMPLATE = MEDIA_PATH + 'animated_portraits/{0:05d}.mp4'
GIF_TEMPLATE = MEDIA_PATH + 'animated_portraits/{0:05d}.gif'
ORB_SKIN_TEMPLATE = MEDIA_PATH + 'orb_skins/jp/{0:03d}.png'
ORB_SKIN_CB_TEMPLATE = MEDIA_PATH + 'orb_skins/jp/{0:03d}cb.png'


def number_emoji_small(num: int):
    return emoji_cache.get_emoji(f"bullet_{num}")


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
