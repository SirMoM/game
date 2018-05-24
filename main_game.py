# -*- coding: utf-8 -*-
import sys
import json

import Screens
import Tiles
import Structures
import pygame
from Utilities import ColorRGB

__author__ = "Noah Ruben"
__version__ = "0.1"


class Level(object):
    mapAsTileRows = []
    structures = []
    wood = 0
    stone = 0
    iron = 0

    def __init__(self, save_game, map_rows):
        pos_y = 40
        pos_x = 100
        for row in map_rows:
            pos_y += 40
            for shortcut_tile in row:
                pos_x += 40
                self.mapAsTileRows.append(create_tile(shortcut_tile, (pos_x, pos_y)))
            pos_x = 100

        counter = 0
        for shortcut_structure_array in save_game:
            for shortcut_structure in shortcut_structure_array:
                temp_structure = create_structure(shortcut_structure)
                self.structures.append(temp_structure)
                self.mapAsTileRows[counter].set_structure(temp_structure)
                counter += 1

    def resources_as_string(self):
        resources_str = "%.f Wood %.f Iron" % (self.wood, self.iron)
        return resources_str

    def __str__(self):
        str_names = ""  # type: str
        for row in self.mapAsTileRows:
            str_names += row.name + ", "
        return str_names


class Game:
    running = False
    FPS = 60
    level = None
    windows = []

    def __init__(self):
        self.millis = 0
        self.playtime = 0
        self.running = True
        print("New Game")
        pygame.init()
        pygame.font.init()
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500, 500))
        self.screen.fill(ColorRGB.grey)
        self.resources_tick = 25

    def execute(self):
        pygame.time.set_timer(self.resources_tick, 1000)

        while self.running:
            self.on_event()

            self.on_loop()

            self.render_on_loop(self.level)

    def on_event(self):
        for event in pygame.event.get():

            if event.type == self.resources_tick:
                pygame.time.set_timer(self.resources_tick, 1000)
                for structures in self.level.structures:
                    if type(structures) is Structures.LumberJack:
                        self.level.wood += structures.resources_per_loop
                    elif type(structures) is Structures.Quarry:
                        self.level.stone += structures.resources_per_loop
                    elif type(structures) is Structures.IronMine:
                        self.level.iron += structures.resources_per_loop

            if event.type == pygame.MOUSEBUTTONDOWN:
                xPos, yPos = pygame.mouse.get_pos()

                print("Click: ", xPos, yPos)
                for tile in self.level.mapAsTileRows:
                    if tile.is_point_in_tile(xPos, yPos):
                        tile_screen = Screens.TileScreen(self.level, tile)
                        self.windows.append(tile_screen)

            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self.running = True
                pygame.quit()
                sys.exit()

    def on_loop(self):
        # Time
        self.millis = self.clock.tick(self.FPS)
        # self.clock.tick_busy_loop()
        self.playtime += self.millis / 1000

    def render_on_loop(self, level: Level):
        """:type level: Level"""

        self.screen.fill(ColorRGB.grey)
        str_caption = "%.f FPS %.f Playtime" % (self.clock.get_fps(), self.playtime)
        pygame.display.set_caption(str_caption)

        for window in self.windows:
            if window.is_active:
                window.update()
            else:
                self.windows.remove(window)

        self.render_reassures_bar()

        for tile in level.mapAsTileRows:
            self.screen.blit(tile.bg_img, tile.tile_pos)

            # Draw ggf. structures
            if tile.structure:
                self.screen.blit(tile.structure.structure_img, tile.associated_structure_pos)

        pygame.display.flip()

    def render_reassures_bar(self):
        if self.level.wood >= 1:
            self.screen.blit(pygame.image.load("textures/resources/wood.png"), (10, 10))
            str_anz_wood = ": %.f" % self.level.wood
            text_surface = self.my_font.render(str_anz_wood, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 5))

        if self.level.stone >= 1:
            self.screen.blit(pygame.image.load("textures/resources/stone2.png"), (10, 42))
            str_anz_stone = ": %.f" % self.level.stone
            text_surface = self.my_font.render(str_anz_stone, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 42))

        if self.level.iron >= 1:
            self.screen.blit(pygame.image.load("textures/resources/iron.png"), (10, 74))
            str_anz_iron = ": %.f" % self.level.iron
            text_surface = self.my_font.render(str_anz_iron, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 74))


class LevelParser:
    mapVar = "map"
    terrainVar = "terrain"
    rowVar = "row"
    miscVar = "misc"
    structuresVar = "structures"
    seasonVar = "season"

    def __init__(self, save_game_path: str):
        self.structuresAsRowArray = []
        self.mapAsRowArray = []

        self.saveGame = open(save_game_path, "r")

        save_game_as_string = self.saveGame.read()

        save_game_as_json_object = json.loads(save_game_as_string)

        print("Miscellaneous: ", save_game_as_json_object[self.mapVar][self.miscVar])
        print("Season: ", save_game_as_json_object[self.mapVar][self.seasonVar])

        for rows in save_game_as_json_object[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])

        if self.structuresVar in save_game_as_json_object:
            for r in save_game_as_json_object[self.structuresVar]:
                self.structuresAsRowArray.append(r["row"])

        print("structuresAsRowArray: ", self.structuresAsRowArray)

        self.level = Level(self.structuresAsRowArray, self.mapAsRowArray)

    def get_level(self) -> Level:
        return self.level


def create_tile(shortcut: str, pos: tuple):
    # type: () -> Tile
    if shortcut == Tiles.NormalTile.shortcut:
        return Tiles.NormalTile(pos)
    elif shortcut == Tiles.ForestTile.shortcut:
        return Tiles.ForestTile(pos)
    elif shortcut == Tiles.MineTile.shortcut:
        return Tiles.MineTile(pos)
    elif shortcut == Tiles.LakeTile.shortcut:
        return Tiles.LakeTile(pos)
    elif shortcut == Tiles.MountainTile.shortcut:
        return Tiles.MountainTile(pos)
    else:
        print("There went something wrong for creating the Tile")
        return Tiles.NormalTile(pos)


def create_structure(shortcut: str):
    # type: () -> Structures
    if shortcut == Structures.LumberJack.shortcut:
        return Structures.LumberJack()
    elif shortcut == Structures.Quarry.shortcut:
        return Structures.Quarry()
    elif shortcut == Structures.IronMine.shortcut:
        return Structures.IronMine()
    else:
        return False
