import glob
import os
import sys
from typing import Dict

from cleo.io.outputs.output import Verbosity

from elenchos.command.CheckCommand import CheckCommand
from elenchos.helper.XmlHelper import XmlHelper


class GatherCommandsCommand(CheckCommand):
    """
    A command to gather all Élenchos commands.
    """
    name = 'gather-commands'
    description = 'Gathers all installed Élenchos commands.'

    # ------------------------------------------------------------------------------------------------------------------
    def _handle(self) -> int:
        """
        Executes this command.
        """
        commands = self.__gather_commands()
        self.__write_commands(commands)

        return 0

    # ------------------------------------------------------------------------------------------------------------------
    def __gather_commands(self) -> Dict[str, str]:
        """
        Gathers commands from site packages.
        """
        commands = {}
        home = os.path.dirname(os.path.dirname(sys.modules[__name__].__file__))
        target_path = os.path.realpath(os.path.join(home, 'commands.xml'))
        folders = list(filter(lambda x: x.endswith('site-packages'), sys.path))

        for folder in folders:
            self.io.write_line('Scanning folder <fso>{}</fso>'.format(folder), verbosity=Verbosity.VERBOSE)
            paths = glob.glob(os.path.join(folder, '**/commands.xml'), recursive=True)
            for path in paths:
                path = os.path.realpath(path)
                if path != target_path:
                    self.io.write_line('Reading <fso>{}</fso>'.format(path), verbosity=Verbosity.VERBOSE)
                    commands.update(XmlHelper.read_commands(path))

        return dict(sorted(commands.items()))

    # ------------------------------------------------------------------------------------------------------------------
    def __write_commands(self, commands: Dict[str, str]) -> None:
        """
        Writes commands to a commands' XML file.

        :param commands: The commands.
        """
        home = os.path.dirname(os.path.dirname(sys.modules[__name__].__file__))
        path = os.path.realpath(os.path.join(home, 'commands.xml'))
        self.io.write_line('Writing <fso>{}</fso>'.format(path), verbosity=Verbosity.VERBOSE)
        XmlHelper.write_commands(path, commands)

# ----------------------------------------------------------------------------------------------------------------------
