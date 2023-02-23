from discordmenu.embed.components import EmbedFooter
from discordmenu.embed.view_state import ViewState
from discordmenu.intra_message_state import IntraMessageState
from tsutils.query_settings.query_settings import QuerySettings

from tsutils.tsubaki.links import CLOUDFRONT_URL, MonsterImage

TSUBAKI_FLOWER_ICON_URL = CLOUDFRONT_URL + '/tsubaki/tsubakiflower.png'


def embed_footer():
    return EmbedFooter('Requester may click the reactions below to switch tabs')


# Don't type state in case a cog makes its own local state type and it's not discord-menu ViewState
def embed_footer_with_state(state, *, image_url=None, text=None, qs: QuerySettings = None):
    if image_url is None:
        # don't overwrite specified important images e.g. in link mirror
        if qs is not None and qs.favcard is not None:
            if qs.favcard != 0:
                # use 0 as the setting for "I want to go back to the flower icon" after having
                # previously selected a favcard
                image_url = MonsterImage.icon(qs.favcard)
    if image_url is None:
        image_url = TSUBAKI_FLOWER_ICON_URL
    if text is None:
        text = 'Requester may click the reactions below to switch tabs'

    url = IntraMessageState.serialize(image_url, state.serialize())
    return EmbedFooter(
        text,
        icon_url=url)
