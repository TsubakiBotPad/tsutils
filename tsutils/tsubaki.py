from typing import Any, Optional

from discord import User
from redbot.core import commands
from redbot.core.bot import Red

from .helper_functions import make_non_gatekeeping_check

CLOUDFRONT_URL = "https://d30r6ivozz8w2a.cloudfront.net"


def auth_check(perm, default=False):
    def check(ctx):
        if ctx.author.id in ctx.bot.owner_ids:
            return True
        authcog = ctx.bot.get_cog("GlobalAdmin")
        if not authcog:
            return default
        return authcog.settings.get_perm(ctx.author.id, perm, default=default)

    return commands.check(check)


def _is_donor(ctx, only_patron=False):
    if ctx.author.id in ctx.bot.owner_ids:
        return True
    donationcog = ctx.bot.get_cog("Donations")
    if not donationcog:
        return False
    return donationcog.is_donor(ctx, only_patron)


is_donor = make_non_gatekeeping_check(
    _is_donor,
    ("Sorry, but this is a Donor Only command.  Learn "
     "more about donation via `{0.prefix}donate`")
)


async def get_user_preference(bot: Red, user: User, pref: str) -> Optional[Any]:
    cog: Any = bot.get_cog("UserPreferences")
    if not cog:
        return None
    return await cog.config.user(user).get_raw(pref)
