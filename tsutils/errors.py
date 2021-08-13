from discord.ext.commands import CommandError


class IndexNotLoaded(KeyError):
    pass


class NoAPIKeyException(CommandError):
    def __init__(self, fix_command=None, *args):
        if fix_command is not None:
            super().__init__(f"API key not found.  Set it with `{fix_command}`", *args)
        else:
            super().__init__(None, *args)


class BadAPIKeyException(ClientInlineTextException):
    def __init__(self, fix_command=None, *args):
        if fix_command is not None:
            super().__init__(f"Invalid API key.  Fix it with `{fix_command}`", *args)
        else:
            super().__init__(None, *args)
