from typing import Any, Optional

from discord import User
from redbot.core.bot import Red


async def get_user_preference(bot: Red, user: User, pref: str) -> Optional[Any]:
    """Gets a user's preference from UserPreferences cog"""
    if pref in ('timezone',):
        raise ValueError("Invalid preference.  Use the cog method to get this.")

    cog: Any = bot.get_cog("UserPreferences")
    if cog is None:
        return None
    return await cog.config.user(user).get_raw(pref)
