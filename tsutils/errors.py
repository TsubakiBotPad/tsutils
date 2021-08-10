from discord.ext.commands import CommandError


class IndexNotLoaded(KeyError):
    pass


class NoAPIKeyException(CommandError):
    def __init__(self, fix_command=None, *args):
        if fix_command is not None:
            m = f"API keys not found.  Use `{fix_command}` to set them."
            super().__init__(m, *args)
        else:
            super().__init__(None, *args)
