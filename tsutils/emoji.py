import re
from typing import Sequence, Union

import discord

SendableEmoji = Union[str, discord.Emoji]
ReceivableEmoji = Union[SendableEmoji, discord.PartialEmoji]

YES_EMOJI = '\N{WHITE HEAVY CHECK MARK}'
NO_EMOJI = '\N{CROSS MARK}'

def char_to_emoji(c: str) -> SendableEmoji:
    """Casts individual characters & the integer 10 as emojis"""
    c = str(c).lower()
    if '0' <= c <= '9':
        names = {
            '0': '0\N{COMBINING ENCLOSING KEYCAP}',
            '1': '1\N{COMBINING ENCLOSING KEYCAP}',
            '2': '2\N{COMBINING ENCLOSING KEYCAP}',
            '3': '3\N{COMBINING ENCLOSING KEYCAP}',
            '4': '4\N{COMBINING ENCLOSING KEYCAP}',
            '5': '5\N{COMBINING ENCLOSING KEYCAP}',
            '6': '6\N{COMBINING ENCLOSING KEYCAP}',
            '7': '7\N{COMBINING ENCLOSING KEYCAP}',
            '8': '8\N{COMBINING ENCLOSING KEYCAP}',
            '9': '9\N{COMBINING ENCLOSING KEYCAP}',
            '10': '\N{KEYCAP TEN}'
        }
        return names[c]
    if c < 'a' or c > 'z':
        return c

    base = ord('\N{REGIONAL INDICATOR SYMBOL LETTER A}')
    adjustment = ord(c) - ord('a')
    return chr(base + adjustment)


def fix_emojis_for_server(emoji_list: Sequence[discord.Emoji], msg_text: str) -> str:
    """Finds 'emoji-looking' substrings in msg_text and corrects them.

    If msg_text has something like '<:emoji_1_derp:13242342343>' and the server
    contains an emoji named :emoji_2_derp: then it will be swapped out in
    the message.

    This corrects an issue where a padglobal alias is created in one server
    with an emoji, but it has a slightly different name in another server.
    """
    # Find all emoji-looking things in the message
    matches = re.findall(r'<:[0-9a-z_]+:\d{18}>', msg_text, re.IGNORECASE)
    if not matches:
        return msg_text

    # For each unique looking emoji thing
    for m in set(matches):
        # Create a regex for that emoji replacing the digit
        m_re = re.sub(r'\d', r'&', m).rstrip("~")
        for em in emoji_list:
            # If the current emoji matches the regex, force a replacement
            emoji_code = str(em)
            if re.match(m_re, emoji_code, re.IGNORECASE):
                msg_text = re.sub(m_re, emoji_code, msg_text, flags=re.IGNORECASE)
                break
    return msg_text


def replace_emoji_names_with_code(emoji_list: Sequence[discord.Emoji], msg_text: str) -> str:
    """Finds emoji-name substrings in msg_text and corrects them.

    If msg_text has something like ':emoji_1_derp:' and emoji_list contains
    an emoji named 'emoji_1_derp' then the value will replaced with the full
    emoji id.

    This allows a padglobal admin without nitro to create entries with emojis
    from other servers.
    """
    # First strip down actual emojis to just the names
    msg_text = re.sub(r'<(:[0-9a-z_]+:)\d{18}>', r'\1', msg_text, flags=re.IGNORECASE)

    # Find all emoji-looking things in the message
    matches = re.findall(r':[0-9a-z_]+:', msg_text, re.IGNORECASE)
    if not matches:
        return msg_text

    # For each unique looking emoji thing
    finished_names = []
    for m in set(matches):
        emoji_name = m.strip(':')
        for e in emoji_list:
            if e.name == emoji_name and e.name not in finished_names:
                finished_names.append(e.name)
                msg_text = msg_text.replace(m, str(e))
    return msg_text
