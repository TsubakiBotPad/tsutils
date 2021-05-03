from discordmenu.embed.components import EmbedFooter
from discordmenu.embed.view_state import ViewState
from discordmenu.intra_message_state import IntraMessageState

TSUBAKI_FLOWER_ICON_URL = 'https://d1kpnpud0qoyxf.cloudfront.net/tsubaki/tsubakiflower.png'


def embed_footer():
    return EmbedFooter('Requester may click the reactions below to switch tabs')


def embed_footer_with_state(state: ViewState, image_url=TSUBAKI_FLOWER_ICON_URL):
    url = IntraMessageState.serialize(image_url, state.serialize())
    return EmbedFooter(
        'Requester may click the reactions below to switch tabs',
        icon_url=url)
