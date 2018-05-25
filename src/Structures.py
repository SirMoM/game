import pygame


class Structure:
    resources_per_loop: str
    name: str
    structure_img: str
    shortcut = "D"
    resources_type: str

    def __init__(self, name, img):
        self.structure_img = img
        self.name = name

    def __str__(self):
        out_str = self.name + "Resource: " + self.resources_type
        return out_str


class LumberJack(Structure):
    resources_per_loop = 1
    shortcut = "LJ"
    resources_type = "Wood"
    name = "Lumber Jack"

    def __init__(self):
        self.structure_img = pygame.image.load("textures\structures\lumberJack.png")


class Quarry(Structure):
    resources_per_loop = 0.5
    shortcut = "Q"
    resources_type = "Stone"
    name = "Quarry"

    def __init__(self):
        self.structure_img = pygame.image.load("textures/structures/quarry.png")


class IronMine(Structure):
    resources_per_loop = 0.3
    shortcut = "IM"
    resources_type = "Iron"
    name = "Iron Mine"

    def __init__(self):
        self.structure_img = pygame.image.load("textures/structures/ironMine.png")
