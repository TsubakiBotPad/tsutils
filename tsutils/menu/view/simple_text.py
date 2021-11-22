from typing import List

from discordmenu.embed.components import EmbedMain
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState

from tsutils.menu.components.footers import embed_footer_with_state

from tsutils.menu.components.config import UserConfig


class SimpleTextViewState(ViewState):
    def __init__(self, original_author_id, menu_type, raw_query,
                 color, message,
                 extra_state=None):
        super().__init__(original_author_id, menu_type, raw_query,
                         extra_state=extra_state)
        self.message = message
        self.color = color

    def serialize(self):
        ret = super().serialize()
        ret.update({
            'message': self.message,
        })
        return ret

    @classmethod
    async def deserialize(cls, _dbcog, user_config: UserConfig, ims: dict):
        original_author_id = ims['original_author_id']
        menu_type = ims['menu_type']
        raw_query = ims.get('raw_query')
        return cls(original_author_id, menu_type, raw_query, user_config.color, ims.get('message'),
                   extra_state=ims)


class SimpleTextView:
    VIEW_TYPE = 'SimpleText'

    @staticmethod
    def embed(state: SimpleTextViewState):
        return EmbedView(
            EmbedMain(
                color=state.color,
                description=state.message
            ),
            embed_footer=embed_footer_with_state(state),
        )
