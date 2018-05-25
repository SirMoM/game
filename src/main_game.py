# -*- coding: utf-8 -*-
import sys
import json
from typing import List

from src import Screens, Tiles, Structures
import pygame
from src.Utilities import ColorRGB

__author__ = "Noah Ruben"
__version__ = "0.1"


class Level(object):
    mapAsTileRows = []
    structures = []
    wood = 0
    stone = 0
    iron = 0

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
                for row in self.level.mapAsTileRows:
                    for tile in row:
                        if tile.is_point_in_tile(xPos, yPos):
                            tile_screen = Screens.TileScreen(self.level, tile)
                            self.windows.append(tile_screen)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    this = self
                    self.windows.append(Screens.InGameMenu(this))

            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self.running = True
                pygame.quit()
                sys.exit()

    def on_loop(self):
        # Time
        self.millis = self.clock.tick(self.FPS)
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
                # if type(window) is Screens.InGameMenu:
                self.windows.remove(window)

        self.render_reassures_bar()

        for row in level.mapAsTileRows:
            for tile in row:
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
    resourcesVar = "resources"
    woodVar = "wood"
    stoneVar = "stone"
    ironVar = "iron"

    def __init__(self, save_game_path: str):
        self.structuresAsRowArray = []
        self.mapAsRowArray = []

        self.saveGame = open(save_game_path, "r")

        save_game_as_string = self.saveGame.read()

        save_game_as_json_object = json.loads(save_game_as_string)

        print("Miscellaneous: ", save_game_as_json_object[self.mapVar][self.miscVar])
        print("Season: ", save_game_as_json_object[self.mapVar][self.seasonVar])
        print("Resources: ", save_game_as_json_object[self.resourcesVar])

        for rows in save_game_as_json_object[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])
        print("mapAsRowArray: ", self.mapAsRowArray)

        if self.structuresVar in save_game_as_json_object:
            for r in save_game_as_json_object[self.structuresVar]:
                self.structuresAsRowArray.append(r["row"])
        print("structuresAsRowArray: ", self.structuresAsRowArray)

        self.level = Level()

        pos_y = 40
        pos_x = 100

        for row_index in range(0, self.mapAsRowArray.__len__()):
            pos_y += 40
            temp_array = []
            temp_array.clear()
            for tile_shortcut_index in range(0, self.mapAsRowArray[row_index].__len__()):
                pos_x += 40
                temp_array.append(create_tile(self.mapAsRowArray[row_index][tile_shortcut_index], (pos_x, pos_y),
                                              structure=create_structure(
                                                  self.structuresAsRowArray[row_index][tile_shortcut_index])))
            pos_x = 100
            self.level.mapAsTileRows.append(temp_array)

        rowCounter = 0
        tileCounter = 0
        for row in self.structuresAsRowArray:
            rowCounter += 1
            for shortcut_structure in row:
                temp_structure = create_structure(shortcut_structure)
                self.level.structures.append(temp_structure)
                # self.level.mapAsTileRows[rowCounter][tileCounter].set_structure(temp_structure)
                tileCounter += 1

        # set the level resources
        self.level.wood = save_game_as_json_object[self.resourcesVar][self.woodVar]
        self.level.stone = save_game_as_json_object[self.resourcesVar][self.stoneVar]
        self.level.iron = save_game_as_json_object[self.resourcesVar][self.ironVar]

    def get_level(self) -> Level:
        return self.level


class LevelWriter(object):
    mapVar = "map"
    terrainVar = "terrain"
    rowVar = "row"
    miscVar = "misc"
    structuresVar = "structures"
    seasonVar = "season"
    resourcesVar = "resources"
    woodVar = "wood"
    stoneVar = "stone"
    ironVar = "iron"

    def __init__(self, filename: str, level: Level):
        self.filename = filename
        self.level = level
        self.save_game_path = "saves/" + filename + ".json"
        self.saveGame = open(self.save_game_path, "w")

        row_json_object = json.loads('{"row" : []}')

        level_as_json_string = '{' \
                               '"' + self.structuresVar + '": [],' \
                                                          '"' + self.mapVar + '": {' \
                                                                              '"' + self.terrainVar + '": [],' \
                                                                                                      '"' + self.miscVar + '": "None",' \
                                                                                                                           '"' + self.seasonVar + '": "Summer"},' \
                                                                                                                                                  '"' + self.resourcesVar + '": {' \
                                                                                                                                                                            '"' + self.woodVar + '": 0,' \
                                                                                                                                                                                                 '"' + self.stoneVar + '": 0,' \
                                                                                                                                                                                                                       '"' + self.ironVar + '": 0}' \
                                                                                                                                                                                                                                            '}'
        json_obj = json.loads(level_as_json_string)

        print(self.level.mapAsTileRows)

        for row in self.level.mapAsTileRows:
            print(row)
            temp = []
            temp.clear()
            for tiles in row:
                temp.append(tiles.shortcut)
            json_obj[self.mapVar][self.terrainVar].append(self.create_row(temp))

        print()

        json.dump(json_obj, self.saveGame)

    def create_row(self, row_inhalt):
        row_json_object = json.loads('{"row" : []}')
        row_json_object[self.rowVar] = row_inhalt
        return row_json_object


def create_tile(shortcut: str, pos: tuple, structure: Structures.Structure = None):
    # type: () -> Tile
    if shortcut == Tiles.NormalTile.shortcut:
        return Tiles.NormalTile(pos)
    elif shortcut == Tiles.ForestTile.shortcut:
        temp = Tiles.ForestTile(pos)
        temp.set_structure(structure)
        return temp
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
