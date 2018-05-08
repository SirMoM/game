import pygame


class Tile:
    name = None
    has_structure = None
    bg_img = None
    tile_pos = None

    def __init__(self, name, bg_img, tile_pos):
        self.tile_pos = tile_pos
        self.name = name
        self.bg_img = bg_img


class NormalTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/normTile.png")
        self.name = "normTile"
        self.tile_pos = tile_pos


class ForestTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/forestTile.png")
        self.name = "forestTile"
        self.tile_pos = tile_pos


class MineTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/mineTile.png")
        self.name = "mineTile"
        self.tile_pos = tile_pos


class LakeTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("textures/tiles/lakeTile.png")
        self.name = "lakeTile"
        self.tile_pos = tile_pos
