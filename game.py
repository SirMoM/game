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
                self.on_event(event)

            self.on_Loop()

            self.render_on_loop(level)

    def on_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    def on_Loop(self):
        # Time
        self.millis = self.clock.tick(self.FPS)
        self.playtime = self.millis / 1000

    def render_on_loop(self, level):
        """:type level: Level"""
        self.screen.fill(Color.grey)
        str_caption = "%.f FPS" % self.clock.get_fps()
        pygame.display.set_caption(str_caption)
        for tile in level.mapAsTileRows:
            self.screen.blit(tile.bg_img, tile.tile_pos)
        pygame.display.flip()


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

    def __init__(self, name, bg_img, tile_pos):
        self.tile_pos = tile_pos
        self.name = name
        self.bg_img = bg_img


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


class MineTile(Tile):
    def __init__(self, tile_pos):
        self.bg_img = pygame.image.load("pic/mineTile.png")
        self.name = "mineTile"
        self.tile_pos = tile_pos


def createTile(shortcut, pos):
    # type: (String) -> Tile
    if shortcut == "N":
        return NormalTile(pos)
    elif shortcut == "W":
        return ForestTile(pos)


class Level:
    mapAsTileRows = []
    structures = []
    pos_y = 20
    pos_x = 20

    def __init__(self, save_game, map_rows):
        for row in map_rows:
            self.pos_y += 20
            for shortcut in row:
                self.pos_x += 20
                self.mapAsTileRows.append(createTile(shortcut, (self.pos_x, self.pos_y)))
            self.pos_x = 20
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
