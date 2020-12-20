import discord.ext
from redbot.core import commands


def auth_check(perm, default=False):
    def check(ctx):
        if ctx.author.id in ctx.bot.owner_ids:
            return True
        authcog = ctx.bot.get_cog("GlobalAdmin")
        if not authcog:
            return default
        return authcog.settings.get_perm(ctx.author.id, perm, default=default)

    return commands.check(check)


def make_non_gatekeeping_check(condition, failmessage):
    def non_gatekeep_check(**kwargs):
        def decorator(command):
            @command.before_invoke
            async def hook(instance, ctx):
                if not condition(ctx, **kwargs):
                    await ctx.send(failmessage.format(ctx))
                    raise discord.ext.commands.CheckFailure()

            return command

        return decorator

    return non_gatekeep_check


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
