"""
This module is used handle the config-file of the game

Import
------
    os
        used to get the config-file destination

    ConfigParser
        used to get easy access to the config-file
"""

import os
from configparser import ConfigParser

sound_section: str = "game.sound"
music_volume_option: str = "music_volume"
music_on_option: str = "music_on"
sfx_volume_option: str = "sfx_volume"
sfx_on_option: str = "sfx_on"

parent_dir: str = os.path.dirname(os.getcwd())
file_path: str = os.path.join(parent_dir, "config.cfg")


def set_value(config_section: str, config_to_set: str, value: str) -> None:
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(file_path)
    config_parser.set(config_section, config_to_set, value)
    config_parser.write(open(file_path, 'w'))


def get_value(config_section: str, config_to_set: str) -> str:
    config_parser: ConfigParser = ConfigParser()
    config_parser.read(file_path)
    return config_parser.get(config_section, config_to_set)
