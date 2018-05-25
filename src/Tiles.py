import pygame

from src import Structures


class Tile:
    name = None
    bg_img = None
    img_path: str
    tile_pos = None
    associated_structure_pos = None
    has_structure = False
    structure = None
    shortcut = "D"
    rect = None

    def __init__(self, name, bg_img, img_path, tile_pos):
        self.tile_pos = tile_pos
        self.name = name
        self.bg_img = bg_img
        self.img_path = img_path
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)

    def __str__(self):
        out_str = ""
        out_str += self.name + " Tile Pos:" + str(self.tile_pos[0]) + ", " + str(
            self.tile_pos[1]) + " Structure: " + self.structure.__str__()
        return out_str

    def set_structure(self, structure: Structures.Structure):
        self.has_structure = True
        self.structure = structure

    def get_structure(self) -> Structures:
        return self.structure

    def get_rect(self):
        return pygame.Rect(self.associated_structure_pos[0], self.associated_structure_pos[1],
                           self.associated_structure_pos[0] + 32,
                           self.associated_structure_pos[1] + 32)

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
    img_path = "textures/tiles/normTile.png"

    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)


class ForestTile(Tile):
    shortcut = "F"
    name = "Forrest"
    img_path = "textures/tiles/forestTile.png"

    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)


class MineTile(Tile):
    shortcut = "PM"  # Potential Mine
    name = "Mine"
    img_path = "textures/tiles/mineTile.png"

    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1] + 8)


class LakeTile(Tile):
    shortcut = "L"
    name = "Lake"
    img_path = "textures/tiles/lakeTile.png"

    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)


class MountainTile(Tile):
    shortcut = "M"
    name = "Mountain"
    img_path = "textures/tiles/mountainTile.png"

    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load(self.img_path)
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 8, tile_pos[1] + 16)