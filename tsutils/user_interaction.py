import asyncio
import re
from typing import Literal, Optional, List

import discord

from .emoji import SendableEmoji, YES_EMOJI, NO_EMOJI


async def send_repeated_consecutive_messages(ctx, message: str) -> discord.Message:
    """Edit the last message to include the string `x2` or more if would otherwise be repeated"""
    lmessage = await ctx.history().__anext__()
    fullmatch = re.escape(message) + r"(?: x(\d+))?"
    match = re.match(fullmatch, lmessage.content)
    if match and lmessage.author == ctx.bot.user:
        n = match.group(1) or "1"
        await lmessage.edit(content=message + " x" + str(int(n) + 1))
        return lmessage
    else:
        return await ctx.send(message)


async def get_user_confirmation(ctx, text: str,
                                yes_emoji: SendableEmoji = YES_EMOJI, no_emoji: SendableEmoji = NO_EMOJI,
                                timeout: int = 10) -> Literal[True, False, None]:
    msg = await ctx.send(text)
    asyncio.create_task(msg.add_reaction(yes_emoji))
    asyncio.create_task(msg.add_reaction(no_emoji))

    def check(reaction, user):
        return (str(reaction.emoji) in [yes_emoji, no_emoji]
                and user.id == ctx.author.id
                and reaction.message.id == msg.id)

    ret = False
    try:
        r, u = await ctx.bot.wait_for('reaction_add', check=check, timeout=timeout)
        if r.emoji == yes_emoji:
            ret = True
    except asyncio.TimeoutError:
        ret = None

    await msg.delete()
    return ret


async def get_user_reaction(ctx, text: str, *emoji: SendableEmoji, timeout: int = 10) -> Optional[SendableEmoji]:
    msg = await ctx.send(text)

    async def addreactions():
        for e in emoji:
            try:
                asyncio.create_task(msg.add_reaction(e))
            except (discord.Forbidden, discord.NotFound):
                pass

    asyncio.create_task(addreactions())

    def check(reaction, user):
        return (str(reaction.emoji) in emoji
                and user.id == ctx.author.id
                and reaction.message.id == msg.id)

    try:
        r, u = await ctx.bot.wait_for('reaction_add', check=check, timeout=timeout)
        ret = r.emoji
    except asyncio.TimeoutError:
        ret = None

    await msg.delete()
    return ret


async def await_and_remove(bot, react_msg: discord.Message, listen_user: discord.User,
                           delete_msgs: Optional[List[discord.Message]] = None,
                           emoji: SendableEmoji = NO_EMOJI, timeout: int = 15) -> None:
    """Remove a message when recieving an emoji reaction"""
    try:
        await react_msg.add_reaction(emoji)
    except Exception as e:
        # failed to add reaction, ignore
        return

    def check(payload):
        return str(payload.emoji.name) == emoji and \
               payload.user_id == listen_user.id and \
               payload.message_id == react_msg.id

    try:
        p = await bot.wait_for('add_reaction', check=check, timeout=timeout)
    except asyncio.TimeoutError:
        # Expected after {timeout} seconds
        p = None

    if p is None:
        try:
            await react_msg.remove_reaction(emoji, react_msg.guild.me)
        except Exception as e:
            # failed to remove reaction, ignore
            return
    else:
        msgs = delete_msgs or [react_msg]
        for m in msgs:
            await m.delete_message()


class StatusManager:
    """An asynchronous context manager to temporary modify the bot's status"""

    def __init__(self, bot, status: discord.Status = discord.Status.dnd):
        self.bot = bot
        self.newstatus = status
        self.oldstatus = None

    async def __aenter__(self) -> None:
        if not self.bot.guilds:
            return
        self.oldstatus = self.bot.guilds[0].me.status
        activity = self.bot.guilds[0].me.activity
        await self.bot.change_presence(activity=activity, status=self.newstatus)

    async def __aexit__(self, *args):
        if self.oldstatus is None \
                or not self.bot.guilds \
                or self.bot.guilds[0].me.status != self.newstatus:
            return
        activity = self.bot.guilds[0].me.activity
        await self.bot.change_presence(activity=activity, status=self.oldstatus)


def confirmation_message(msg: str) -> str:
    return f"{YES_EMOJI} {msg}"


async def send_confirmation_message(ctx, msg: str) -> discord.Message:
    return await ctx.send(confirmation_message(msg))


def cancellation_message(msg: str) -> str:
    return f"{NO_EMOJI} {msg}"


async def send_cancellation_message(ctx, msg: str) -> discord.Message:
    return await ctx.send(cancellation_message(msg))
