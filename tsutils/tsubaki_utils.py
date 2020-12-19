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


def is_donor(only_patron=False):
    def check(ctx):
        if ctx.author.id in ctx.bot.owner_ids:
            return True
        donationcog = ctx.bot.get_cog("Donations")
        if not donationcog:
            return False
        return donationcog.is_donor(ctx, only_patron)

    return commands.check(check)
