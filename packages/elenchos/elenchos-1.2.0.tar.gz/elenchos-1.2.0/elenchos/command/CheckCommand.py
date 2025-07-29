import abc
from abc import ABC

from cleo.commands.command import Command


class CheckCommand(Command, ABC):
    """
    Abstract parent command for all check commands.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __set_style(self) -> None:
        """
        Sets the output format style used by Élenchos.
        """
        # Style for file system objects (e.g., file and directory names).
        self.add_style('fso', fg='green', options=['bold'])

        # Style for errors.
        self.add_style('error', fg='red', options=['bold'])

        # Style for notices.
        self.add_style('notice', fg='yellow')

        # Style for titles.
        self.add_style('title', fg='yellow')

    # ------------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def _handle(self) -> int:
        """
        Executes this command. This method must be implemented by concrete instances of a check command.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def handle(self) -> int:
        """
        Executes this command.
        """
        self.__set_style()

        return self._handle()

# ----------------------------------------------------------------------------------------------------------------------
