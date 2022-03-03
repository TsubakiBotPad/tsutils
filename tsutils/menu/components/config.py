import random

from discord import Color


def _user_color_to_discord_color(color):
    if color is None:
        return Color.default()
    elif color == "random":
        return Color(random.randint(0x000000, 0xffffff))
    else:
        return Color(color)


class UserConfig:
    def __init__(self, color):
        self.color = color


class BotConfig:
    @staticmethod
    async def get_user(config, user_id):
        user_config = config.user_from_id(user_id)
        user_color = await user_config.color()
        color = _user_color_to_discord_color(user_color)
        return UserConfig(color)
