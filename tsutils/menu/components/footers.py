from discordmenu.embed.components import EmbedFooter
from discordmenu.embed.view_state import ViewState
from discordmenu.intra_message_state import IntraMessageState

from tsutils.tsubaki.links import CLOUDFRONT_URL

TSUBAKI_FLOWER_ICON_URL = CLOUDFRONT_URL + '/tsubaki/tsubakiflower.png'


def embed_footer():
    return EmbedFooter('Requester may click the reactions below to switch tabs')


def embed_footer_with_state(state: ViewState, *, image_url=None, text=None):
    if image_url is None:
        image_url = TSUBAKI_FLOWER_ICON_URL
    if text is None:
        text = 'Requester may click the reactions below to switch tabs'

    url = IntraMessageState.serialize(image_url, state.serialize())
    return EmbedFooter(
        text,
        icon_url=url)
