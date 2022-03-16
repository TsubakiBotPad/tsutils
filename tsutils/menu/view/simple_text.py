from typing import List

from discordmenu.embed.components import EmbedMain
from discordmenu.embed.view import EmbedView
from tsutils.query_settings.query_settings import QuerySettings

from tsutils.menu.components.config import UserConfig
from tsutils.menu.components.footers import embed_footer_with_state
from tsutils.menu.view.view_state_base import ViewStateBase


class SimpleTextViewState(ViewStateBase):
    def __init__(self, original_author_id, menu_type, raw_query,
                 query_settings: QuerySettings, message,
                 reaction_list: List[str] = None,
                 extra_state=None):
        super().__init__(original_author_id, menu_type, raw_query,
                         reaction_list=reaction_list, extra_state=extra_state)
        self.message = message
        self.query_settings = query_settings

    def serialize(self):
        ret = super().serialize()
        ret.update({
            'message': self.message,
            'query_settings': self.query_settings.serialize(),
        })
        return ret

    @classmethod
    async def deserialize(cls, _dbcog, user_config: UserConfig, ims: dict):
        original_author_id = ims['original_author_id']
        menu_type = ims['menu_type']
        raw_query = ims.get('raw_query')
        query_settings = QuerySettings.deserialize(ims.get('query_settings'))
        return cls(original_author_id, menu_type, raw_query, query_settings, ims.get('message'),
                   reaction_list=ims.get('reaction_list'), extra_state=ims)


class SimpleTextView:
    VIEW_TYPE = 'SimpleText'

    @staticmethod
    def embed(state: SimpleTextViewState):
        return EmbedView(
            EmbedMain(
                color=state.query_settings.embedcolor,
                description=state.message
            ),
            embed_footer=embed_footer_with_state(state),
        )
