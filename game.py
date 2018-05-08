# -*- coding: utf-8 -*-
import sys
import json

__author__ = "Noah Ruben"
__version__ = "v1.0"

import pygame


class Color:
    def __init__(self):
        print("This is a Utility Class DO NOT create a Object")

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    purple = (150, 43, 186)
    grey = (200, 200, 200)


class Game:
    running = False
    FPS = 61

    def __init__(self):
        self.millis = None
        self.playtime = None
        self.running = True
        print("New Game")
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500, 500))
        self.screen.fill(Color.grey)

    def execute(self, level):
        while self.running:

            for event in pygame.event.get():
                self.on_Event(event)

            self.on_Loop()

            self.render_on_loop(level)

    def on_Event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def on_Loop(self):
        # Time
        self.millis = self.clock.tick(self.FPS)
        self.playtime = self.millis / 1000

    def render_on_loop(self, level):
        self.screen.fill(Color.grey)
        str = "%.f FPS" % self.clock.get_fps()
        pygame.display.set_caption(str)
        pygame.display.flip()
        self.screen.blit(level)


class LevelParser:
    mapVar = "map"
    terrainVar = "terrain"
    rowVar = "row"
    miscVar = "misc"

    structuresVar = "structures"

    def __init__(self):
        self.structuresAsRowArray = []
        self.mapAsRowArray = []

        self.mapFile = open("level.map", "r")
        self.saveGame = open("save_game.json", "r")

        map_As_String = self.mapFile.read()
        save_Game_As_String = self.saveGame.read()

        level = json.loads(map_As_String)
        sg = json.loads(save_Game_As_String)

        print "Miscellaneous: ", level[self.mapVar][self.miscVar]
        print "Terrain: ", level[self.mapVar][self.terrainVar]
        print "Structures: ", sg[self.structuresVar]

        for rows in level[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])

        for r in sg[self.structuresVar]:
            self.structuresAsRowArray.append(r["row"])

        self.level = Level(self.structuresAsRowArray, self.mapAsRowArray)

    def get_Level(self):
        return self.level


class Tile:
    name = None
    has_structure = None
    bg_img = None
    tile_pos = None

    def __init__(self):
        pass


class NormalTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("pic/normTile.png")
        self.name = "normTile"
        self.tile_pos = tile_pos


class ForestTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("pic/forestTile.png")
        self.name = "forestTile"
        self.tile_pos = tile_pos


def createTile(shortcut):
    # type: (String) -> Tile
    if shortcut == "N":
        return NormalTile()
    elif shortcut == "W":
        return ForestTile()


class Level:
    mapAsTileRows = []
    structures = []

    def __init__(self, save_game, map_rows):
        for row in map_rows:
            for shortcut in row:
                self.mapAsTileRows.append(createTile(shortcut))
        for structure in save_game:
            self.structures.append(structure)

        print "mapAsTileRows: ", self.mapAsTileRows
        print "structures: ", self.structures

    def __str__(self):
        str_names = ""  # type: str
        for row in self.mapAsTileRows:
            str_names += row.name + ", "

        return str_names


if __name__ == '__main__':
    game = Game()
    lp = LevelParser()
    game.execute(lp.get_Level())
