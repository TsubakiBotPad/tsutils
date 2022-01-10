from discordmenu.emoji.emoji_cache import emoji_cache

CLOUDFRONT_URL = "https://d30r6ivozz8w2a.cloudfront.net"


def number_emoji_small(num: int):
    return emoji_cache.get_emoji(f"bullet_{num}")
