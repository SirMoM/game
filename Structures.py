import pygame


class Structure:
    name = None
    has_structure = None
    bg_img = None
    tile_pos = None

    def __init__(self, name, bg_img, tile_pos):
        self.tile_pos = tile_pos
        self.name = name
        self.bg_img = bg_img


class LumberJack(Structure):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("pic/lumberJack.png")
        self.name = "Lumber Jack"
        self.tile_pos = tile_pos

