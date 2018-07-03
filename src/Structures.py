import os

import pygame

from src import Tiles, Game

parent_dir = os.path.dirname(os.getcwd())


class Structure:
    resources_per_loop: float
    name: str
    structure_img: str
    shortcut = "D"
    resources_type: str
    build_costs = None

    def __init__(self, name, img):
        self.structure_img = img
        self.name = name

    def __str__(self):
        out_str = self.name + "Resource: " + self.resources_type
        return out_str

    @staticmethod
    def can_build(tile):
        return False


class LumberJack(Structure):
    resources_per_loop = 1.0
    shortcut = "LJ"
    resources_type = "Wood"
    name = "Lumber Jack"
    build_costs = 4, 0, 0
    build_time = 3

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures\structures\lumberJack.png"))

    @staticmethod
    def can_build(tile):
        if tile.structure is None and tile.shortcut is Tiles.ForestTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class LumberJackTierTwo(Structure):
    resources_per_loop = 2.0
    shortcut = "LJ2"
    resources_type = "Wood"

    name = "Lumber Jack T2"
    build_costs = 20, 10, 5
    build_time = 10

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/lumberJackTII.png"))

    @staticmethod
    def can_build(tile):
        if type(tile.structure) is LumberJack and tile.shortcut is Tiles.ForestTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class Quarry(Structure):
    resources_per_loop = 0.5
    shortcut = "Q"
    resources_type = "Stone"
    name = "Quarry"
    build_costs = 10, 0, 0
    build_time = 6

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/quarry.png"))

    @staticmethod
    def can_build(tile):
        if tile.structure is None and tile.shortcut is Tiles.MountainTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class IronMine(Structure):
    resources_per_loop = 0.3
    shortcut = "IM"
    resources_type = "Iron"
    name = "Iron Mine"

    build_costs = 8, 5, 0
    build_time = 5

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/ironMine.png"))

    @staticmethod
    def can_build(tile):
        if tile.structure is None and tile.shortcut is Tiles.MineTile.shortcut and tile.is_in_territory:
            return True
        else:
            return False


class Castle(Structure):
    resources_per_loop = 0.0
    resources_type = ""
    shortcut = "C"
    name = "Castle"
    build_costs = 10, 10, 10
    build_time = 10
    tile_range = 2
    tile = None
    level: Game.Level

    def __init__(self):
        self.structure_img = pygame.image.load(os.path.join(parent_dir, "textures/structures/castle.png"))

    def create_territory(self, tile, level: Game.Level):
        self.tile = tile
        self.level = level
        territory_start = []
        territory_end = []

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

        print("territory_start ", territory_start)
        print("territory_end ", territory_end)

        for i in range(territory_start[0], territory_end[0]):
            for j in range(territory_start[1], territory_end[1]):
                self.level.mapAsTileRows[i][j].is_in_territory = True

    @staticmethod
    def can_build(tile):
        if tile.structure is None and tile.shortcut is Tiles.NormalTile.shortcut:
            return True
        else:
            return False
