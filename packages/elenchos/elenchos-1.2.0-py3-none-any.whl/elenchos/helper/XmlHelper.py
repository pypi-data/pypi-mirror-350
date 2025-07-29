from pathlib import Path
from typing import Dict

from lxml import etree


class XmlHelper:
    """
    Utility class for reading and writing XML command files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def read_commands(filename: str) -> dict[str, str]:
        """
        Reads a commands' XML file.

        :param filename: The path to the commands XML file.
        """
        commands = {}

        doc = etree.parse(filename)
        xpath = '/commands/command'
        elements = doc.xpath(xpath)
        for element in elements:
            name = str(element.xpath('@name')[0])
            module = element.text
            commands[name] = module

        return commands

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def write_commands(filename: str, commands: Dict[str, str]) -> None:
        """
        Writes a commands XML file.

        :param filename: The path to the commands XML file.
        :param commands: The commands. A map from command name to class name.
        """
        root = etree.Element('commands')
        for name, command in commands.items():
            element = etree.Element('command')
            element.attrib['name'] = name
            element.text = command
            root.append(element)

        path = Path(filename)
        path.write_bytes(etree.tostring(root, pretty_print=True))

# ----------------------------------------------------------------------------------------------------------------------
