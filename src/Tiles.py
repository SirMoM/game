import os
import pygame
from src import Structures

parent_dir = os.path.dirname(os.getcwd())


class Tile:
    name = None
    bg_img = None
    img_path: str
    tile_pos = None
    associated_structure_pos = None
    has_structure = False
    structure = False
    shortcut = "D"
    rect = None
    rel_pos_tuple = ()

    def __init__(self, name, bg_img, img_path, tile_pos, rel_pos):
        self.tile_pos = tile_pos
        self.name = name
        self.bg_img = bg_img
        self.img_path = img_path
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos

    def __str__(self):
        out_str = ""
        out_str += self.name + " Rel Pos:" + str(self.rel_pos_tuple[0]) + ", " + str(
            self.rel_pos_tuple[1]) + " Structure: " + self.structure.__str__()
        return out_str

    def set_structure(self, structure: Structures.Structure):
        self.has_structure = True
        self.structure = structure

    def get_structure(self) -> Structures:
        return self.structure

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

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos


class ForestTile(Tile):
    shortcut = "F"
    name = "Forrest"
    img_path = os.path.join(parent_dir, "textures/tiles/forestTile.png")

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos


class MineTile(Tile):
    shortcut = "PM"  # Potential Mine
    name = "Mine"
    img_path = os.path.join(parent_dir, "textures/tiles/mineTile.png")

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1] + 8)
        self.rel_pos_tuple = rel_pos


class LakeTile(Tile):
    shortcut = "L"
    name = "Lake"
    img_path = os.path.join(parent_dir, "textures/tiles/lakeTile.png")

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos


class MountainTile(Tile):
    shortcut = "M"
    name = "Mountain"
    img_path = os.path.join(parent_dir, "textures/tiles/mountainTile.png")

    def __init__(self, tile_pos, rel_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1] + 16)
        self.rel_pos_tuple = rel_pos
