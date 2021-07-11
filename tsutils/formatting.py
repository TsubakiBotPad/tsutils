import re
import unicodedata

# https://gist.github.com/ryanmcgrath/982242
# UNICODE RANGE : DESCRIPTION
# 3000-303F : punctuation
# 3040-309F : hiragana
# 30A0-30FF : katakana
# FF00-FFEF : Full-width roman + half-width katakana
# 4E00-9FAF : Common and uncommon kanji
#
# Non-Japanese punctuation/formatting characters commonly used in Japanese text
# 2605-2606 : Stars
# 2190-2195 : Arrows
# u203B     : Weird asterisk thing
import discord

JA_REGEX_STR = (r'[\u3000-\u303F]|[\u3040-\u309F]|[\u30A0-\u30FF]|[\uFF00-\uFFEF]'
                r'|[\u4E00-\u9FAF]|[\u2605-\u2606]|[\u2190-\u2195]|\u203B')
JA_REGEX = re.compile(JA_REGEX_STR)


def contains_ja(txt: str) -> bool:
    return bool(JA_REGEX.search(txt))


def normalize_server_name(server: str) -> str:
    server = server.upper()
    return 'NA' if server == 'US' else server


def is_valid_image_url(url: str) -> bool:
    url = url.lower()
    return url.startswith('http') and (url.endswith('.png') or url.endswith('.jpg'))


def extract_image_url(m: discord.Message) -> str:
    if is_valid_image_url(m.content):
        return m.content
    if m.attachments and len(m.attachments) and is_valid_image_url(m.attachments[0].url):
        return m.attachments[0].url
    return None


def rmdiacritics(string: str) -> str:
    """ Return the base character of char, by "removing" any
    diacritics like accents or curls and strokes and the like.
    """
    output = ''
    for c in string:
        try:
            desc = unicodedata.name(c)
            cutoff = desc.find(' WITH ')
            if cutoff != -1:
                desc = desc[:cutoff]
            output += unicodedata.lookup(desc)
        except (KeyError, ValueError):
            output += c
    return re.sub("[\u201c\u201d]", '"', output)


def clean_global_mentions(content: str) -> str:
    """Wipes out mentions to @everyone and @here."""
    return re.sub(r'(@)(\w)', '\\g<1>\u200b\\g<2>', content)


def strip_right_multiline(txt: str) -> str:
    """Useful for prettytable output where there are a lot of right spaces."""
    return '\n'.join([x.strip() for x in txt.splitlines()])
