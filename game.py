# -*- coding: utf-8 -*-
import sys
import json

import Tiles
import Structures

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
        # quit if the quit button was pressed
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

        for structure in level.structures:
            self.screen.blit(structure.bg_img, structure.structure_pos)

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

        level_map = json.loads(map_As_String)
        sg = json.loads(save_Game_As_String)

        print "Miscellaneous: ", level_map[self.mapVar][self.miscVar]
        print "Save Game: ", sg["structures"]

        for rows in level_map[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])

        for r in sg[self.structuresVar]:
            self.structuresAsRowArray.append(r["row"])

        self.level = Level(self.structuresAsRowArray, self.mapAsRowArray)

    def get_Level(self):
        return self.level


def createTile(shortcut, pos):
    # type: (String) -> Tile
    if shortcut == "N":
        return Tiles.NormalTile(pos)
    elif shortcut == "W":
        return Tiles.ForestTile(pos)
    elif shortcut == "M":
        return Tiles.MineTile(pos)
    elif shortcut == "L":
        return Tiles.LakeTile(pos)


def createStructure(shortcut, pos):
    # type: (String) -> Structures
    if shortcut == "LJ":
        return Structures.LumberJack(pos)
    elif shortcut == "Filler":
        pass
    else:
        return False


class Level:
    mapAsTileRows = []
    structures = []
    pos_y = 40
    pos_x = 40

    def __init__(self, save_game, map_rows):
        for row in map_rows:
            self.pos_y += 40
            for shortcut_tile in row:
                self.pos_x += 40
                self.mapAsTileRows.append(createTile(shortcut_tile, (self.pos_x, self.pos_y)))
            self.pos_x = 40
        for shortcut_structure in save_game:
            tempStructure = createStructure(shortcut_structure, (self.pos_x, self.pos_y))
            if tempStructure:
                self.structures.append(tempStructure)

        # print "mapAsTileRows: ", self.mapAsTileRows
        print "Structures: ", self.structures

    def __str__(self):
        str_names = ""  # type: str
        for row in self.mapAsTileRows:
            str_names += row.name + ", "

        return str_names


if __name__ == '__main__':
    game = Game()
    lp = LevelParser()
    game.execute(lp.get_Level())
