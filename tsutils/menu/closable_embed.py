from discordmenu.embed.control import EmbedControl
from discordmenu.embed.menu import EmbedMenu

from tsutils.menu.components.panes import MenuPanes


class ClosableEmbedMenu:
    MENU_TYPE = 'ClosableEmbedMenu'
    message = None
    view_types = {}

    @staticmethod
    def menu():
        embed = EmbedMenu({}, ClosableEmbedMenu.message_control)
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
