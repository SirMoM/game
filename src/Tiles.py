#!/usr/bin/python
# -*- coding: utf-8 -*-
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
import random
from typing import Tuple, ClassVar

import pygame
from pygame import Surface

from src.GameMechanics import Construction
from src.Structures import Structure
from src.Utilities import get_system_path_from_relative_path


class Tile:
    name: str = None
    bg_img: Surface = None
    img_path: str
    tile_pos: Tuple[int, int] = None
    associated_structure_pos: Tuple[int, int] = None
    has_structure: bool = False
    _structure: bool = False
    shortcut: str = "D"
    rel_pos_tuple: Tuple[int, int] = ()
    is_in_territory: bool = False
    construction: Construction = None
    x_offset: int = 16
    y_offset: int = 16
    green_boarder: str = get_system_path_from_relative_path("textures/utils/greenBoarder.png")

    def __init__(self, name: str, bg_img: Surface, img_path: str, tile_pos: Tuple[int, int],
                 rel_pos: Tuple[int, int]) -> None:
        self.name = name
        self.tile_pos = tile_pos
        self.bg_img = bg_img
        self.img_path = img_path
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos

        # TODO LOG logger.debug("Just created a " + self.name)

    def __str__(self) -> str:
        out_str = self.name
        return out_str

    def set_structure(self, structure: Structure) -> None:
        """
        Sets a _structure of a tile and turns the 'has_structure' flag true.

        :param structure: the _structure to set
        """
        self.has_structure = True
        self._structure: Structure = structure

    def get_structure(self) -> Structure:
        """
        Gets you the structure of the tile

        :return: the structure of the tile
        """
        return self._structure

    def set_new_pos(self, tile_pos: Tuple[int, int]) -> None:
        """
        Sets the absolute position of the Tile and updates the absolute position of where the structure
        should be rendered on the Tile

        :param tile_pos: the new absolute position to set
        """
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + self.x_offset, tile_pos[1] + self.y_offset)

    def is_point_in_tile(self, x_pos: int, y_pos: int) -> bool:
        """
        Tells you if a pair if coordinates is inside the tile.


        :param x_pos: the absolute x-Position
        :param y_pos: the absolute y-Position
        :return: if the coordinates are in the Tile
        """
        if self.tile_pos[0] + 32 > x_pos > self.tile_pos[0]:
            if self.tile_pos[1] + 32 > y_pos > self.tile_pos[1]:
                return True
            else:
                return False
        else:
            return False


class NormalTile(Tile):
    """
    The normal ground Tile.
    """
    shortcut: ClassVar[str] = "N"
    name: ClassVar[str] = "Normal Ground"
    img_path: ClassVar[str] = get_system_path_from_relative_path("textures/tiles/normTile.png")
    x_offset: int = 0
    y_offset: int = 0

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0], tile_pos[1])
        self.rel_pos_tuple = rel_pos

        # TODO LOG logger.debug("Just created a " + self.name)


class ForestTile(Tile):
    """
    A forest Tile.
    """
    shortcut: ClassVar[str] = "F"
    name: ClassVar[str] = "Forrest"
    img_path: ClassVar[str] = get_system_path_from_relative_path("textures/tiles/forestTile.png")

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.img_path = random.choice([get_system_path_from_relative_path("textures/tiles/forestTile.png"),
                                       get_system_path_from_relative_path("textures/tiles/forestTile2.png")])
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos
        # TODO LOG logger.debug("Just created a " + self.name)


class MineTile(Tile):
    """
    A Tile where a mine can be build.
    """
    shortcut: ClassVar[str] = "PM"  # Potential Mine
    name: ClassVar[str] = "Mine"
    img_path: ClassVar[str] = get_system_path_from_relative_path("textures/tiles/mineTile.png")
    x_offset: int = 8
    y_offset: int = 8

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        print(self.img_path)
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1] + 8)
        self.rel_pos_tuple = rel_pos

        # TODO LOG logger.debug("Just created a " + self.name)


class LakeTile(Tile):
    """
    The lake Tile.
    """
    shortcut: ClassVar[str] = "L"
    name: ClassVar[str] = "Lake"
    img_path: ClassVar[str] = get_system_path_from_relative_path("textures/tiles/lakeTile.png")

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos

        # TODO LOG logger.debug("Just created a " + self.name)


class MountainTile(Tile):
    """
    The mountain Tile
    """
    shortcut: ClassVar[str] = "M"
    name: ClassVar[str] = "Mountain"
    img_path: ClassVar[str] = get_system_path_from_relative_path("textures/tiles/mountainTile.png")
    x_offset: int = 8
    y_offset: int = 0

    def __init__(self, tile_pos: Tuple[int, int], rel_pos: Tuple[int, int]) -> None:
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1])
        self.rel_pos_tuple = rel_pos

        # TODO LOG logger.debug("Just created a " + self.name)
