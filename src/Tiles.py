"""
This module holds all Tiles for the game.

Import
------
    os
        used to get the parent_dir
    random
        used to get a random element from a list
    pygame
        the game engine for the game
    logging
        basic python logging
    Structures
        for type hinting
    Game
        for type hinting
    Tuple
        for type hinting
    Surface
        for type hinting

"""
import logging
import os
import random
from typing import Tuple

import pygame
from pygame import Surface

from src.Game import Construction
from src.Structures import Structure

parent_dir = os.path.dirname(os.getcwd())

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(os.path.join(os.path.dirname(os.getcwd()), "logs/GameLog.log"))
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


class Tile:
    name: str = None
    bg_img: Surface = None
    img_path: str
    tile_pos: Tuple[int, int] = None
    associated_structure_pos: Tuple[int, int] = None
    has_structure: bool = False
    structure: bool = False
    shortcut: str = "D"
    rel_pos_tuple: Tuple[int, int] = ()
    is_in_territory: bool = False
    construction: Construction = None
    x_offset: int = 16
    y_offset: int = 16
    green_boarder: str = os.path.join(parent_dir, "textures/utils/greenBoarder.png")

    def __init__(self, name: str, bg_img: Surface, img_path: str, tile_pos: Tuple[int, int],
                 rel_pos: Tuple[int, int]) -> None:
        self.name = name
        self.tile_pos = tile_pos
        self.bg_img = bg_img
        self.img_path = img_path
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)

    def __str__(self) -> str:
        out_str = self.name
        return out_str

    def set_structure(self, structure: Structure) -> None:
        self.has_structure = True
        self.structure = structure

    def get_structure(self) -> Structure:
        return self.structure

    def set_new_pos(self, tile_pos: Tuple[int, int]) -> None:
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + self.x_offset, tile_pos[1] + self.y_offset)

    def is_point_in_tile(self, x_pos: int, y_pos: int):
        if self.tile_pos[0] + 32 > x_pos > self.tile_pos[0]:
            if self.tile_pos[1] + 32 > y_pos > self.tile_pos[1]:
                return True
            else:
                return False
        else:
            return False


class NormalTile(Tile):
    shortcut: str = "N"
    name: str = "Normal Ground"
    img_path: str = os.path.join(parent_dir, "textures/tiles/normTile.png")
    x_offset: int = 0
    y_offset: int = 0

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0], tile_pos[1])
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)


class ForestTile(Tile):
    shortcut: str = "F"
    name: str = "Forrest"
    img_path: str = os.path.join(parent_dir, "textures/tiles/forestTile.png")

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.img_path = random.choice([os.path.join(parent_dir, "textures/tiles/forestTile.png"),
                                       os.path.join(parent_dir, "textures/tiles/forestTile2.png")])
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos
        logger.debug("Just created a " + self.name)


class MineTile(Tile):
    shortcut: str = "PM"  # Potential Mine
    name: str = "Mine"
    img_path: str = os.path.join(parent_dir, "textures/tiles/mineTile.png")
    x_offset: int = 8
    y_offset: int = 8

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1] + 8)
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)


class LakeTile(Tile):
    shortcut: str = "L"
    name: str = "Lake"
    img_path: str = os.path.join(parent_dir, "textures/tiles/lakeTile.png")

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)


class MountainTile(Tile):
    shortcut: str = "M"
    name: str = "Mountain"
    img_path: str = os.path.join(parent_dir, "textures/tiles/mountainTile.png")
    x_offset: int = 8
    y_offset: int = 0

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1])
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)
