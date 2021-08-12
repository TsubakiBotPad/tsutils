from redbot.core.commands import UserFeedbackCheckFailure


class IndexNotLoaded(KeyError):
    pass


class UserFeedbackException(UserFeedbackCheckFailure):  # TODO: Find another way to do this
    """An error that sends its message to the user instead of failing a command

    This error has nothing to do with checks, and only inherits from UserFeedbackCheckFailure
    because the Red bot instance automatically sends its message to the current
    channel when raised.
    """
    pass


class NoAPIKeyException(UserFeedbackException):
    def __init__(self, fix_command=None, *args):
        if fix_command is not None:
            m = f"API keys not found.  Use `{fix_command}` to set them."
            super().__init__(m, *args)
        else:
            super().__init__(None, *args)
