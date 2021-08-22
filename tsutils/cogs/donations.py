from typing import Any

from redbot.core.commands import Context

from ..helper_functions import make_non_gatekeeping_check


def _is_donor(ctx: Context, only_patron: bool = False) -> bool:
    if ctx.author.id in ctx.bot.owner_ids:
        return True
    donationcog: Any = ctx.bot.get_cog("Donations")
    if not donationcog:
        return False
    return donationcog.is_donor(ctx, only_patron)


is_donor = make_non_gatekeeping_check(
    _is_donor,
    ("Sorry, but this is a Donor Only command.  Learn "
     "more about donation via `{0.prefix}donate`")
)
