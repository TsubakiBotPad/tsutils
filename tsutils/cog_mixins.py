from abc import abstractmethod
from typing import Callable, Optional

import redbot.core.commands as commands
from discord.ext.commands import Cog
from redbot.core.commands import Command

from .helper_classes import CogABCMeta


class PreferenceMixin(metaclass=CogABCMeta):
    @abstractmethod
    def setup(self) -> None: ...

    @abstractmethod
    async def get_mixin_data(self, user_id: int) -> Optional[str]: ...

    @abstractmethod
    async def delete_mixin_data(self, requester: str, user_id: int) -> None: ...


class MixinCommand:
    def __init__(self, function: Callable, parent: Optional[str] = None, **kwargs):
        self.function = function
        self.parent = parent
        self.kwargs = kwargs

    def setup(self, cog: Cog, parent: Optional[Command] = None) -> None:
        parent = parent or self.parent or commands
        if isinstance(parent, str):
            parent = getattr(cog, parent)
        command = parent.command(**self.kwargs)(self.function)
        add_command_to_cog(command, cog)


class MixinGroup:
    def __init__(self, function: Callable, parent: Optional[str] = None, **kwargs):
        self.function = function
        self.parent = parent
        self.kwargs = kwargs
        self.children = []

    def command(self, **kwargs) -> Callable[[Callable], MixinCommand]:
        def _decorator(func: Callable) -> MixinCommand:
            child = MixinCommand(func, **kwargs)
            self.children.append(child)
            return child

        return _decorator

    def group(self, **kwargs) -> Callable[[Callable], "MixinGroup"]:
        def _decorator(func: Callable) -> MixinGroup:
            child = MixinGroup(func, **kwargs)
            self.children.append(child)
            return child

        return _decorator

    def setup(self, cog: Cog, parent: Optional[Command] = None) -> None:
        parent = parent or self.parent or commands
        if isinstance(parent, str):
            parent = getattr(cog, parent)
        group = parent.group(**self.kwargs)(self.function)
        add_command_to_cog(group, cog)
        for child in self.children:
            child.setup(cog, group)


def add_command_to_cog(command: Command, cog: Cog) -> None:
    command.cog = cog
    cog.__cog_commands__ = (*cog.__cog_commands__, command)
    setattr(cog, command.callback.__name__, command)

    lookup = {cmd.qualified_name: cmd for cmd in cog.__cog_commands__}

    parent = command.parent
    if parent is not None:
        parent = lookup[parent.qualified_name]
        parent.remove_command(command.name)
        parent.add_command(command)


def mixin_command(parent: Optional[str], **kwargs) -> Callable[[Callable], MixinCommand]:
    def _decorator(func: Callable) -> MixinCommand:
        return MixinCommand(func, parent, **kwargs)

    return _decorator


def mixin_group(parent: Optional[str], **kwargs) -> Callable[[Callable], MixinGroup]:
    def _decorator(func: Callable) -> MixinGroup:
        return MixinGroup(func, parent, **kwargs)

    return _decorator
