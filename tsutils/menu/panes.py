emoji_buttons = {
    'home': '\N{HOUSE BUILDING}',
    'reset': '\N{WHITE MEDIUM STAR}',
}


class MenuPanes:
    INITIAL_EMOJI = emoji_buttons['home'],
    DATA = {}
    HIDDEN_EMOJIS = []

    @classmethod
    def emoji_names(cls):
        """Return all emoji names. If an emoji is specified as a tuple with fallback(s), returns a tuple."""
        return [k for k, v in cls.DATA.items() if k not in cls.HIDDEN_EMOJIS]

    @classmethod
    def all_emoji_names(cls):
        """
        Return all valid emoji names, including fallbacks.
        In particular, the length of the list returned by this method is not guaranteed to be
        the same as the length of the list returned by `emoji_names`, and so this should only
        be used for validity checking.
        """
        ret = []
        for k, v in cls.DATA.items():
            if k in cls.HIDDEN_EMOJIS:
                continue
            if isinstance(k, str):
                ret.append(k)
            elif isinstance(k, tuple):
                # case when a fallback is provided
                ret += k
        return ret

    @classmethod
    def transitions(cls):
        ret = {}
        for k, v in cls.DATA.items():
            if v[0] is None:
                continue
            if isinstance(k, str):
                ret[k] = v[0]
            elif isinstance(k, tuple):
                # case when a fallback is provided
                ret.update({_: v[0] for _ in k})
        return ret

    @classmethod
    def pane_types(cls):
        return {v[1]: v[0] for k, v in cls.DATA.items() if v[1] and v[1] not in cls.HIDDEN_EMOJIS}

    @classmethod
    def respond_to_emoji_with_parent(cls, emoji: str):
        """Only defined for menus that support children"""
        if cls.DATA.get(emoji) is None:
            return None
        return cls.DATA[emoji][0] is not None

    @classmethod
    def respond_to_emoji_with_child(cls, emoji: str):
        """Only defined for menus that support children"""
        if cls.DATA.get(emoji) is None:
            return None
        return cls.DATA[emoji][2] is not None

    @classmethod
    def get_child_data_func(cls, emoji: str):
        """Only defined for menus that support children"""
        if cls.DATA.get(emoji) is None:
            return None
        return cls.DATA[emoji][2]
