from abc import abstractmethod, ABCMeta
from typing import List, Optional, Dict, Any, Union

from discord import Colour
from discordmenu.embed.base import Box
from discordmenu.embed.components import EmbedMain, EmbedField, EmbedFooter, EmbedThumbnail, EmbedBodyImage, EmbedAuthor
from discordmenu.embed.view import EmbedView

from tsutils.menu.components.config import UserConfig
from tsutils.menu.components.footers import embed_footer_with_state
from tsutils.query_settings.query_settings import QuerySettings


# We don't subclass from ViewState becuase otherwise we'll get a billion lint warnings
# that deserialize doesn't match the default method signature, and the benefit isn't
# even that much
class PadViewState:
    def __init__(self, original_author_id, menu_type, raw_query, query, qs: QuerySettings, extra_state):
        self.extra_state = extra_state or {}
        self.menu_type = menu_type
        self.original_author_id = original_author_id
        self.raw_query = raw_query
        self.query = query
        self.qs = qs

    def serialize(self) -> Dict[str, Any]:
        ret = {
            'raw_query': self.raw_query,
            'menu_type': self.menu_type,
            'original_author_id': self.original_author_id,
            'query': self.query,
            'qs': self.qs.serialize(),
        }
        ret.update(self.extra_state)
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
    def embed_title(cls, state: PadViewState) -> Optional[str]:
        return None

    @classmethod
    def embed_url(cls, state: PadViewState) -> Optional[str]:
        return None

    @classmethod
    def embed_thumbnail(cls, state: PadViewState) -> Optional[EmbedThumbnail]:
        return None

    @classmethod
    def embed_footer(cls, state: PadViewState) -> Optional[EmbedFooter]:
        return embed_footer_with_state(state, qs=state.qs)

    @classmethod
    def embed_fields(cls, state: PadViewState) -> List[EmbedField]:
        return []

    @classmethod
    def embed_body_image(cls, state: PadViewState) -> Optional[EmbedBodyImage]:
        return None

    @classmethod
    def embed_description(cls, state: PadViewState) -> Optional[Union[Box, str]]:
        return None

    @classmethod
    def embed_author(cls, state: PadViewState) -> Optional[EmbedAuthor]:
        return None

    @classmethod
    def embed(cls, state: PadViewState) -> EmbedView:
        return EmbedView(
            EmbedMain(
                color=cls.embed_color(state),
                title=cls.embed_title(state),
                url=cls.embed_url(state),
                description=cls.embed_description(state)
            ),
            embed_author=cls.embed_author(state),
            embed_thumbnail=cls.embed_thumbnail(state),
            embed_footer=cls.embed_footer(state),
            embed_body_image=cls.embed_body_image(state),
            embed_fields=cls.embed_fields(state)
        )
