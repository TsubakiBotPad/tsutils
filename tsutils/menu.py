import asyncio
import inspect

import discord


class EmojiUpdater(object):
    # a pass-through base class that does nothing to the emoji dictionary
    # or to the selected emoji
    def __init__(self, emoji_to_embed, **kwargs):
        self.emoji_dict = emoji_to_embed
        self.selected_emoji = None

    async def on_update(self, ctx, selected_emoji):
        self.selected_emoji = selected_emoji
        return True


class Menu():
    """Menu by https://github.com/Awoonar/Dusty-Cogs/blob/master/menu/menu.py"""

    def __init__(self, bot):
        self.bot = bot

        # Feel free to override this in your cog if you need to
        self.emoji = {
            0: "0⃣",
            1: "1⃣",
            2: "2⃣",
            3: "3⃣",
            4: "4⃣",
            5: "5⃣",
            6: "6⃣",
            7: "7⃣",
            8: "8⃣",
            9: "9⃣",
            10: "🔟",
            "next": "➡",
            "back": "⬅",
            "yes": "✅",
            "no": "❌",
        }

    # for use as an action
    async def reaction_delete_message(self, bot, ctx, message):
        await message.delete()

    async def custom_menu(self, ctx, emoji_to_message, selected_emoji, **kwargs):
        """Creates and manages a new menu
        Required arguments:
            Type:
                1- number menu
                2- confirmation menu
                3- info menu (basically menu pagination)
                4- custom menu. If selected, choices must be a list of tuples.
            Messages:
                Strings or embeds to use for the menu.
                Pass as a list for number menu
        Optional arguments:
            page (Defaults to 0):
                The message in messages that will be displayed
            timeout (Defaults to 15):
                The number of seconds until the menu automatically expires
            check (Defaults to default_check):
                The same check that wait_for_reaction takes
            is_open (Defaults to False):
                Whether or not the menu can take input from any user
            emoji (Defaults to self.emoji):
                A dictionary containing emoji to use for the menu.
                If you pass this, use the same naming scheme as self.emoji
            message (Defaults to None):
                The discord.Message to edit if present
            """
        return await self._custom_menu(ctx, emoji_to_message, selected_emoji, **kwargs)

    async def show_menu(self,
                        ctx,
                        message,
                        new_message_content):
        if message:
            if isinstance(new_message_content, discord.Embed):
                return await message.edit(embed=new_message_content)
            else:
                return await message.edit(content=new_message_content)
        else:
            if isinstance(new_message_content, discord.Embed):
                return await ctx.send(embed=new_message_content)
            else:
                return await ctx.send(new_message_content)

    async def _custom_menu(self, ctx, emoji_to_message, selected_emoji,
                           allowed_action=True, **kwargs):
        timeout = kwargs.get('timeout', 15)
        message = kwargs.get('message', None)

        reactions_required = not message
        new_message_content = emoji_to_message.emoji_dict[selected_emoji]
        if allowed_action:
            if not message:
                message = await self.show_menu(ctx, message, new_message_content)
            else:
                await self.show_menu(ctx, message, new_message_content)

        if reactions_required:
            async def addreactions():
                for e in emoji_to_message.emoji_dict:
                    try:
                        await message.add_reaction(e)
                    except discord.Forbidden:
                        pass

            asyncio.create_task(addreactions())

        def check(payload):
            def default_check(pl):
                return pl.user_id != self.bot.user.id and not (pl.guild_id and pl.member.bot)

            return (kwargs.get('check', default_check)(payload) and
                    str(payload.emoji.name) in list(emoji_to_message.emoji_dict.keys()) and
                    payload.user_id == ctx.author.id and
                    payload.message_id == message.id)

        if not message:
            raise ValueError(str((message, ctx)))

        try:
            p = await self.bot.wait_for('raw_reaction_add', check=check, timeout=timeout)
        except asyncio.TimeoutError:
            p = None

        if p is None:
            try:
                await message.clear_reactions()
            except discord.Forbidden:
                pass
            return message, new_message_content

        react_emoji = p.emoji.name
        react_action = emoji_to_message.emoji_dict[p.emoji.name]

        if inspect.iscoroutinefunction(react_action):
            message = await react_action(self.bot, ctx, message)
        elif inspect.isfunction(react_action):
            message = react_action(ctx, message)

        # user function killed message, quit
        if not message:
            return None, None

        try:
            if not isinstance(message.channel, discord.DMChannel):
                await message.remove_reaction(react_emoji, p.member)
        except discord.Forbidden:
            pass

        # update the emoji mapping however we need to, or just pass through and do nothing

        allowed_action = await emoji_to_message.on_update(ctx, react_emoji)
        return await self._custom_menu(
            ctx, emoji_to_message, emoji_to_message.selected_emoji,
            timeout=timeout,
            check=check,
            message=message,
            allowed_action=allowed_action)
