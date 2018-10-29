"""
This module is used handle the config-file of the game

Import
------
    os
        used to get the config-file destination

    ConfigParser
        used to get easy access to the config-file

    get_system_path_from_relative_path
        used to get the config-file-path
"""

from configparser import ConfigParser

from src.Utilities import get_system_path_from_relative_path

sound_section: str = "game.sound"
music_volume_option: str = "music_volume"
music_on_option: str = "music_on"
sfx_volume_option: str = "sfx_volume"
sfx_on_option: str = "sfx_on"

file_path: str = get_system_path_from_relative_path("config.cfg")


def set_value(config_section: str, config_to_set: str, value: str) -> None:
    """
    Allows you to set a value in the config file.

    for config_section, config_to_set use the module variables.

    Parameters
    ----------
        :param config_section: Defines the config section which will be used to set a value
        :param config_to_set: The actual option to set
        :param value: the value to set as a String

    Return
    ------
        :return: a str which contains the full path to the File

    """
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(file_path)
    config_parser.set(config_section, config_to_set, value)
    config_parser.write(open(file_path, 'w'))


def get_value(config_section: str, config_to_set: str) -> str:
    """
    Gives you the value for an option.

    for config_section, config_to_set use the module variables.

    :param config_section: Defines the config section which will be used to set a value
    :param config_to_set: The actual option to set
    :return: the value for the option
    """
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(file_path)
    return config_parser.get(config_section, config_to_set)
