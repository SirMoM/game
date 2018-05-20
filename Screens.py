import pygame


class Screen(object):
    def __init__(self):
        print("New Screen")
        pygame.init()
        pygame.font.init()
        self.display = pygame.display.set_mode((200, 400))


class TileScreen(Screen):
    def __init__(self, tile):
        print("New TileScreen")
        print(tile)
