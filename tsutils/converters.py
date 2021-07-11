import re
from typing import TYPE_CHECKING
from discord.ext.commands import Converter, BadArgument
import discord

if TYPE_CHECKING:
    CaseInsensitiveRole = discord.Role
else:
    class CaseInsensitiveRole(Converter):
        async def convert(self, ctx, argument) -> discord.Role:
            match = re.match(r'(?:<@&)?(\d{15,20})>?$', argument)
            if match and ctx.guild.get_role(int(match.group(1))):
                return ctx.guild.get_role(int(match.group(1)))

            roles = {role for role in ctx.guild.roles if role.name == argument} or \
                    {role for role in ctx.guild.roles if role.name.lower() == argument.lower()}

            if len(roles) == 1:
                return roles.pop()
            if len(roles) == 0:
                raise BadArgument(f"No role matched {argument}")

            highest_prio = max(roles, key=lambda r: r.position)
            await ctx.send(f"Warning: More than one candidate found: {', '.join(r.mention for r in roles)}"
                           f" for input `{argument}`. We matched {highest_prio.mention}.",
                           allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))
            return highest_prio
