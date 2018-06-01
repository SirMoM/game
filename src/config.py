import os
import configparser

sound_section = "game.sound"

music_volume_option = "music_volume"
music_on_option = "music_on"
sfx_volume_option = "sfx_volume"
sfx_on_option = "sfx_on"

parent_dir = os.path.dirname(os.getcwd())
file_path = os.path.join(parent_dir, "config.cfg")


def set_value(config_section: str, config_to_set: str, value: str):
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)
    config_parser.set(config_section, config_to_set, value)
    config_parser.write(open(file_path, 'w'))


def get_value(config_section: str, config_to_set: str):
    config_parser = configparser.ConfigParser()
    config_parser.read(file_path)
    return config_parser.get(config_section, config_to_set)
