from redbot.core.commands import UserFeedbackCheckFailure


class IndexNotLoaded(KeyError):
    pass


class ClientInlineTextException(UserFeedbackCheckFailure):  # TODO: Find another way to do this
    """An error that sends its message to the user in the Discord client instead of
    failing a command and printing a message to the terminal/logger

    This error has nothing to do with checks, and only inherits from UserFeedbackCheckFailure
    because the Red bot instance automatically sends its message to the current
    channel when raised.
    """
    pass


class NoAPIKeyException(ClientInlineTextException):
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
