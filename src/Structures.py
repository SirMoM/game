import os
from typing import ClassVar, List

import pygame

from src import Tiles, GameMechanics

parent_dir = os.path.dirname(os.getcwd())


class Structure(object):
    resources_per_loop: float
    name: str
    structure_img: str
    shortcut: ClassVar[str] = "D"
    resources_type: str
    build_costs = None

    def __init__(self, name, img):
        self.structure_img = img
        self.name = name

    def __str__(self):
        out_str = self.name + "Resource: " + self.resources_type
        return out_str

    @staticmethod
    def can_build(tile) -> bool:
        """
            This method checks if this structure can be build ontop this Tile

            Parameter
            ---------
            :param tile: the tile which has to be compatible

            Returns
            -------
            :return bool: true if this can be build.
        """
        return False


class LumberJack(Structure):
    resources_per_loop: float = 1.0
    shortcut: ClassVar[str] = "LJ"
    resources_type: ClassVar[str] = "Wood"
    name: ClassVar[str] = "Lumber Jack"
    build_costs = 4, 0, 0
    build_time: int = 3

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures\structures\lumberJack.png"))

    @staticmethod
    def can_build(tile) -> bool:
        """
            This method checks if this structure can be build ontop this Tile

            Parameter
            ---------
            :param tile: the tile which has to be compatible

            Returns
            -------
            :return bool: true if this can be build.
        """
        if tile.get_structure() is None and tile.shortcut is Tiles.ForestTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class LumberJackTierTwo(Structure):
    resources_per_loop: ClassVar[float] = 2.0
    shortcut: ClassVar[str] = "LJ2"
    resources_type: ClassVar[str] = "Wood"

    name: ClassVar[str] = "Lumber Jack T2"
    build_costs = 20, 10, 5
    build_time: ClassVar[int] = 10

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/lumberJackTII.png"))

    @staticmethod
    def can_build(tile) -> bool:
        """
            This method checks if this structure can be build ontop this Tile

            Parameter
            ---------
            :param tile: the tile which has to be compatible

            Returns
            -------
            :return bool: true if this can be build.
        """
        if type(
                tile.get_structure()) is LumberJack and tile.shortcut is Tiles.ForestTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class Quarry(Structure):
    resources_per_loop: ClassVar[int] = 0.5
    shortcut: ClassVar[str] = "Q"
    resources_type: ClassVar[str] = "Stone"
    name: ClassVar[str] = "Quarry"
    build_costs = 10, 0, 0
    build_time: ClassVar[int] = 6

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/quarry.png"))

    @staticmethod
    def can_build(tile) -> bool:
        """
            This method checks if this structure can be build ontop this Tile

            Parameter
            ---------
            :param tile: the tile which has to be compatible

            Returns
            -------
            :return bool: true if this can be build.
        """
        if tile.get_structure() is None and tile.shortcut is Tiles.MountainTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class IronMine(Structure):
    resources_per_loop: ClassVar[float] = 0.3
    shortcut: ClassVar[str] = "IM"
    resources_type: ClassVar[str] = "Iron"
    name: ClassVar[str] = "Iron Mine"

    build_costs = 8, 5, 0
    build_time: ClassVar[int] = 5

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/ironMine.png"))

    @staticmethod
    def can_build(tile) -> bool:
        """
            This method checks if this structure can be build ontop this Tile

            Parameter
            ---------
            :param tile: the tile which has to be compatible

            Returns
            -------
            :return bool: true if this can be build.
        """
        if tile.get_structure() is None and tile.shortcut is Tiles.MineTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class Castle(Structure):
    resources_per_loop: ClassVar[float] = 0.0
    resources_type = None
    shortcut: ClassVar[str] = "C"
    name: ClassVar[str] = "Castle"
    build_costs = 5, 5, 5
    build_time: int = 10
    tile_range: ClassVar[int] = 2
    tile = None  # type: Tiles.Tile
    level = None  # type: GameMechanics.Level

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/castle.png"))

    # TODO Level Hinting for params
    def create_territory(self, tile, level) -> None:
        self.tile = tile
        self.level = level
        territory_start: List[int, int] = []
        territory_end: List[int, int] = []

        territory_end.append(self.tile.rel_pos_tuple[0] + self.tile_range + 1)
        territory_end.append(self.tile.rel_pos_tuple[1] + self.tile_range + 1)
        territory_start.append(self.tile.rel_pos_tuple[0] - self.tile_range)
        territory_start.append(self.tile.rel_pos_tuple[1] - self.tile_range)

        if territory_end[0] > self.level.mapAsTileRows[tile.rel_pos_tuple[0]].__len__():
            territory_end[0] = self.level.mapAsTileRows[tile.rel_pos_tuple[0]].__len__()
        if territory_end[1] > self.level.mapAsTileRows[tile.rel_pos_tuple[1]].__len__():
            territory_end[1] = self.level.mapAsTileRows[tile.rel_pos_tuple[1]].__len__()

        if territory_start[0] < 0:
            territory_start[0] = 0
        if territory_start[1] < 0:
            territory_start[1] = 0

        # TODO LOG this its kinda important
        print("territory_start ", territory_start)
        print("territory_end ", territory_end)

        for i in range(territory_start[0], territory_end[0]):
            for j in range(territory_start[1], territory_end[1]):
                self.level.mapAsTileRows[i][j].is_in_territory = True

    @staticmethod
    def can_build(tile) -> bool:
        """
            This method checks if this structure can be build ontop this Tile

            Parameter
            ---------
            :param tile: the tile which has to be compatible

            Returns
            -------
            :return bool: true if this can be build.
        """
        if tile.get_structure() is None and tile.shortcut is Tiles.NormalTile.shortcut:
            return True
        else:
            return False


class StructureException(BaseException):
    """
    An exception for everything that can go wrong with Structures.
    """

    shortcut: str

    def __init__(self, message: str, shortcut=None):
        # Call the base class constructor with the parameters it needs
        super().__init__(message)
        self.shortcut = shortcut
