import os
import sys

from cleo.commands.command import Command
from cleo.exceptions import CleoCommandNotFoundError
from cleo.loaders.command_loader import CommandLoader

from elenchos.helper.XmlHelper import XmlHelper


class ElenchosCommandLoader(CommandLoader):
    """
    Lazily command loader for Élenchos.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self):
        """
        Object constructor.
        """
        self.__command: dict[str, str] = ElenchosCommandLoader.__load_commands()

    # ------------------------------------------------------------------------------------------------------------------
    @property
    def names(self) -> list[str]:
        """
        Returns the names of all commands.
        """
        return list(self.__command.keys())

    # ------------------------------------------------------------------------------------------------------------------
    def has(self, name: str) -> bool:
        """
        Returns whether a command exists.

        :param name :The name of the command.
        """
        return name in self.__command

    # ------------------------------------------------------------------------------------------------------------------
    def get(self, name: str) -> Command:
        """
        Returns a command given its name.

        :param name: The name of the command.
        """
        if name not in self.__command:
            raise CleoCommandNotFoundError(name)

        parts = self.__command[name].split('.')
        class_name = parts.pop()
        module_name = '.'.join(parts)

        module_instance = __import__(module_name, fromlist=class_name)
        class_object = getattr(module_instance, class_name)

        return class_object()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __load_commands() -> dict[str, str]:
        """
        Lazily loads all commands from the XML commands file.
        """
        home = os.path.dirname(os.path.dirname(sys.modules[__name__].__file__))
        path = os.path.join(home, 'commands.xml')

        # Load all plugin commands.
        commands = XmlHelper.read_commands(path) if os.path.exists(path) else {}

        # Add build in commands.
        commands['gather-commands'] = 'elenchos.command.GatherCommandsCommand.GatherCommandsCommand'

        return commands

# ----------------------------------------------------------------------------------------------------------------------
