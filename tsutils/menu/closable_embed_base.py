from discordmenu.embed.control import EmbedControl
from discordmenu.embed.menu import EmbedMenu

from tsutils.menu.components.panes import MenuPanes


class ClosableEmbedMenuBase:
    MENU_TYPE = 'ClosableEmbedMenu'
    message = None
    view_types = {}

    @classmethod
    def menu(cls):
        embed = EmbedMenu({}, cls.message_control)
        return embed

    @classmethod
    def message_control(cls, state):
        view = cls.view_types[state.view_type]
        return EmbedControl(
            [view.embed(state, state.props)],
            []
        )


class ClosableEmbedMenuPanes(MenuPanes):
    pass
