import pygame


class Structure:
    name = None
    bg_img = None

    def __init__(self, name, bg_img):
        self.name = name
        self.bg_img = bg_img

    def __str__(self):
        out_str = ""
        out_str += self.name
        return out_str


class LumberJack(Structure):
    def __init__(self):
        self.bg_img = pygame.image.load("textures/structures/lumberJack.png")
        self.name = "Lumber Jack"
