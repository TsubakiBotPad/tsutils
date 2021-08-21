from typing import Any

from discord import User
from redbot.core import commands
from redbot.core.bot import Red


def auth_check(perm: str, default: bool = False):
    def check(ctx):
        if ctx.author.id in ctx.bot.owner_ids:
            return True
        authcog = ctx.bot.get_cog("GlobalAdmin")
        if not authcog:
            return default
        return authcog.settings.get_perm(ctx.author.id, perm, default=default)

    return commands.check(check)


def has_perm(perm: str, user: User, bot: Red, default: bool = False) -> bool:
    if user.id in bot.owner_ids:
        return True
    authcog: Any = bot.get_cog("GlobalAdmin")
    if not authcog:
        return default
    return authcog.settings.get_perm(user.id, perm, default=default)
