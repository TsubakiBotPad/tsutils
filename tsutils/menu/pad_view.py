from abc import abstractmethod, ABCMeta
from typing import List, Optional, Dict, Any

from discord import Colour
from discordmenu.embed.components import EmbedMain, EmbedField, EmbedFooter, EmbedThumbnail, EmbedBodyImage
from discordmenu.embed.view import EmbedView
from discordmenu.embed.view_state import ViewState
from tsutils.menu.components.config import UserConfig

from tsutils.menu.components.footers import embed_footer_with_state
from tsutils.query_settings.query_settings import QuerySettings


class PadViewState(ViewState):
    def __init__(self, original_author_id, menu_type, raw_query, query, qs: QuerySettings, extra_state):
        super().__init__(original_author_id, menu_type, raw_query, extra_state=extra_state)
        self.query = query
        self.qs = qs

    def serialize(self) -> Dict[str, Any]:
        ret = super().serialize()
        ret.update({
            'query': self.query,
            'qs': self.qs.serialize(),
        })
        return ret

    @classmethod
    async def deserialize(cls, dbcog, user_config: UserConfig, ims: dict):
        return cls(ims['original_author_id'], ims['menu_type'], ims['raw_query'],
                   ims['query'], QuerySettings.deserialize(ims.get('qs')), ims
                   )


class PadView(metaclass=ABCMeta):
    VIEW_TYPE = 'Pad'

    @classmethod
    def embed_color(cls, state: PadViewState) -> Colour:
        return state.qs.embedcolor

    @classmethod
    @abstractmethod
    def embed_title(cls, state: PadViewState) -> Optional[str]:
        ...

    @classmethod
    @abstractmethod
    def embed_url(cls, state: PadViewState) -> Optional[str]:
        ...

    @classmethod
    def embed_thumbnail(cls, state: PadViewState) -> Optional[EmbedThumbnail]:
        return None

    @classmethod
    def embed_footer(cls, state: PadViewState) -> Optional[EmbedFooter]:
        return embed_footer_with_state(state, qs=state.qs)

    @classmethod
    @abstractmethod
    def embed_fields(cls, state: PadViewState) -> List[EmbedField]:
        ...

    @classmethod
    def embed_body_image(cls, state: PadViewState) -> Optional[EmbedBodyImage]:
        return None

    @classmethod
    def embed(cls, state: PadViewState) -> EmbedView:
        return EmbedView(
            EmbedMain(
                color=cls.embed_color(state),
                title=cls.embed_title(state),
                url=cls.embed_url(state)
            ),
            embed_thumbnail=cls.embed_thumbnail(state),
            embed_footer=cls.embed_footer(state),
            embed_body_image=cls.embed_body_image(state),
            embed_fields=cls.embed_fields(state)
        )
