import pygame


class Tile:
    name = None
    bg_img = None
    tile_pos = None
    associated_structure_pos = None
    has_structure = None
    structure = None

    def __init__(self, name, bg_img, tile_pos):
        self.tile_pos = tile_pos
        self.name = name
        self.bg_img = bg_img
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)

    def __str__(self):
        out_str = ""
        out_str += self.name + " Tile Pos:" + str(self.tile_pos[0]) + ", " + str(self.tile_pos[1]) + " Structure: " + self.structure.__str__()
        print(out_str)
        return out_str

    def set_structure(self, structure):
        self.structure = structure

    def get_structure(self):
        return self.structure


class NormalTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/normTile.png")
        self.name = "normTile"
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)


class ForestTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/forestTile.png")
        self.name = "forestTile"
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)


class MineTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/mineTile.png")
        self.name = "mineTile"
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)


class LakeTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/lakeTile.png")
        self.name = "lakeTile"
        self.tile_pos = tile_pos
        self.associated_structure_pos = (tile_pos[0] + 16, tile_pos[1] + 16)
