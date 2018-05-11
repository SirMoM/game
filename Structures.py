import pygame


class Structure:
    name = None
    structure_img = None

    def __init__(self, name, img):
        self.name = name
        self.structure_img = img

    def __str__(self):
        out_str = ""
        out_str += self.name + self.structure_img.__str__()
        return out_str


class LumberJack(Structure):
    def __init__(self):
        self.structure_img = pygame.image.load("textures\structures\lumberJack.png")
        self.name = "Lumber Jack"
