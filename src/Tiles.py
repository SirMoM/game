import os
import random
import pygame

import logging

from src import Structures, Game

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
    name = None
    bg_img = None
    img_path: str
    tile_pos = None
    associated_structure_pos = None
    has_structure = False
    structure = False
    shortcut: str = "D"
    rect = None
    rel_pos_tuple = ()
    is_in_territory = False
    construction: Game.Construction = None
    x_offset : int = 16
    y_offset : int = 16
    green_boarder = os.path.join(parent_dir, "textures/utils/greenBoarder.png")

    def __init__(self, name, bg_img, img_path, tile_pos, rel_pos):
        self.name = name
        self.tile_pos = tile_pos
        self.bg_img = bg_img
        self.img_path = img_path
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)

    def __str__(self):
        out_str = self.name
        return out_str

    def set_structure(self, structure: Structures.Structure):
        self.has_structure = True
        self.structure = structure

    def get_structure(self) -> Structures:
        return self.structure

    def set_new_pos(self, tile_pos):
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + self.x_offset, tile_pos[1] + self.y_offset)

    def is_point_in_tile(self, xPos, yPos):
        if self.tile_pos[0] + 32 > xPos > self.tile_pos[0]:
            if self.tile_pos[1] + 32 > yPos > self.tile_pos[1]:
                return True
            else:
                return False
        else:
            return False


class NormalTile(Tile):
    shortcut = "N"
    name = "Normal Ground"
    img_path = os.path.join(parent_dir, "textures/tiles/normTile.png")
    x_offset: int = 0
    y_offset: int = 0

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0], tile_pos[1])
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)


class ForestTile(Tile):
    shortcut = "F"
    name = "Forrest"
    img_path = os.path.join(parent_dir, "textures/tiles/forestTile.png")

    def __init__(self, tile_pos, rel_pos):
        self.img_path = random.choice([os.path.join(parent_dir, "textures/tiles/forestTile.png"),
                                       os.path.join(parent_dir, "textures/tiles/forestTile2.png")])
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos
        logger.debug("Just created a " + self.name)


class MineTile(Tile):
    shortcut = "PM"  # Potential Mine
    name = "Mine"
    img_path = os.path.join(parent_dir, "textures/tiles/mineTile.png")
    x_offset: int = 8
    y_offset: int = 8

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1] + 8)
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)


class LakeTile(Tile):
    shortcut = "L"
    name = "Lake"
    img_path = os.path.join(parent_dir, "textures/tiles/lakeTile.png")

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)


class MountainTile(Tile):
    shortcut = "M"
    name = "Mountain"
    img_path = os.path.join(parent_dir, "textures/tiles/mountainTile.png")
    x_offset: int = 8
    y_offset: int = 0

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1])
        self.rel_pos_tuple = rel_pos

        logger.debug("Just created a " + self.name)
