import pygame


class Structure:
    resources_per_loop = None
    name = None
    structure_img = None
    shortcut = "D"

    def __init__(self, name, img):
        self.name = name
        self.structure_img = img

    def __str__(self):
        out_str = ""
        out_str += self.name + self.structure_img.__str__()
        return out_str


class LumberJack(Structure):
    resources_per_loop = 1 / 60
    shortcut = "LJ"

    def __init__(self):
        self.structure_img = pygame.image.load("textures\structures\lumberJack.png")
        self.name = "Lumber Jack"


class Quarry(Structure):
    resources_per_loop = 1 / 120
    shortcut = "Q"

    def __init__(self):
        self.structure_img = pygame.image.load("textures/structures/quarry.png")
        self.name = "Quarry"
