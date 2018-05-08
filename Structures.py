import pygame


class Structure:
    name = None
    has_structure = None
    bg_img = None
    structure_pos = None

    def __init__(self, name, bg_img, structure_pos):
        self.structure_pos = structure_pos
        self.name = name
        self.bg_img = bg_img


class LumberJack(Structure):
    def __init__(self, structure_pos):
        self.bg_img = pygame.image.load("textures/structures/lumberJack.png")
        self.name = "Lumber Jack"
        self.structure_pos = structure_pos
