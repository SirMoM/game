# -*- coding: utf-8 -*-
import sys
import json

import Tiles
import Structures
import pygame

from Tiles import Tile

__author__ = "Noah Ruben"
__version__ = "v1.0"


class Color:
    def __init__(self):
        print("This is a Utility Class DO NOT create a Object")

    black = (0, 0, 0)
    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    purple = (150, 43, 186)
    grey = (150, 150, 150)


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

            self.on_loop()

            self.render_on_loop(level)

    def on_event(self, event):
        # quit if the quit button was pressed
        if event.type == pygame.QUIT:
            self.running = True
            pygame.quit()
            sys.exit()

    def on_loop(self):
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

    def __init__(self, level_path, save_game_path):
        self.structuresAsRowArray = []
        self.mapAsRowArray = []

        self.mapFile = open(level_path, "r")
        self.saveGame = open(save_game_path, "r")

        map_as_string = self.mapFile.read()
        save_game_as_string = self.saveGame.read()

        level_map = json.loads(map_as_string)
        sg = json.loads(save_game_as_string)

        print("Miscellaneous: ", level_map[self.mapVar][self.miscVar])

        for rows in level_map[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])

        for r in sg[self.structuresVar]:
            self.structuresAsRowArray.append(r["row"])

        print(self.structuresAsRowArray)

        self.level = Level(self.structuresAsRowArray, self.mapAsRowArray)

    def get_level(self):
        return self.level


def create_tile(shortcut, pos):
    # type: () -> Tile
    if shortcut == "N":
        return Tiles.NormalTile(pos)
    elif shortcut == "W":
        return Tiles.ForestTile(pos)
    elif shortcut == "M":
        return Tiles.MineTile(pos)
    elif shortcut == "L":
        return Tiles.LakeTile(pos)


def create_structure(shortcut, pos):
    # type: () -> Structures
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
                self.mapAsTileRows.append(create_tile(shortcut_tile, (self.pos_x, self.pos_y)))
            self.pos_x = 40

        self.pos_y = 40
        self.pos_x = 40

        # TODO strukture pos in Tile auslagern ?
        # TODO how to get the tile?
        # TODO tile unabhäning ?
        counter = 0
        for shortcut_structure_array in save_game:
            for shortcut_structure in shortcut_structure_array:
                print("Counter: ", counter, "Item: ", shortcut_structure, self.mapAsTileRows[counter])
                self.mapAsTileRows[counter].set = create_structure(shortcut_structure, self.mapAsTileRows[counter].associated_structure_pos)
                counter += 1

        # print "mapAsTileRows: ", self.mapAsTileRows
        print("Structures: ", self.structures)

    def __str__(self):
        str_names = ""  # type: str
        for row in self.mapAsTileRows:
            str_names += row.name + ", "

        return str_names


if __name__ == '__main__':
    map1 = "level.map"
    map2 = "level2.map"
    game = Game()
    lp = LevelParser(map1, "save_game.json")
    game.execute(lp.get_level())
