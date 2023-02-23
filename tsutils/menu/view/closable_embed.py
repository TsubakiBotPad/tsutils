from discordmenu.embed.view_state import ViewState

from tsutils.query_settings.query_settings import QuerySettings


class ClosableEmbedViewState(ViewState):
    def __init__(self, original_author_id, menu_type, raw_query,
                 qs: QuerySettings, view_type, props):
        super().__init__(original_author_id, menu_type, raw_query)
        self.qs = qs
        self.view_type = view_type
        self.props = props
