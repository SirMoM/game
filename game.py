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
    FPS = 60
    level = None

    def __init__(self):
        self.millis = 0
        self.playtime = 0
        self.running = True
        print("New Game")
        pygame.init()
        pygame.font.init()  # TODO as
        self.my_font = pygame.font.SysFont('Comic Sans MS', 30)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((500, 500))
        self.screen.fill(Color.grey)
        self.every_sek = pygame.USEREVENT + 1

    def execute(self):
        while self.running:
            self.on_event()

            self.on_loop()

            self.render_on_loop(self.level)

    def on_event(self):
        for event in pygame.event.get():

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos

                print("Click: ", pos)
                for tile in self.level.mapAsTileRows:
                    if tile.get_rect().collidepoint(pos):
                        print(tile.get_rect())
                        print(tile)
                        print("##############################")
                    else:
                        print("no")

            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self.running = True
                pygame.quit()
                sys.exit()

    def on_loop(self):
        # Time
        pygame.time.set_timer(self.every_sek, 100)
        self.millis = self.clock.tick(self.FPS)
        # self.clock.tick_busy_loop()
        self.playtime += self.millis / 1000

        for struct in self.level.structures:
            if type(struct) is Structures.LumberJack:
                self.level.wood += struct.resources_per_loop
            elif type(struct) is Structures.Quarry:
                self.level.stone += struct.resources_per_loop
            elif type(struct) is Structures.IronMine:
                self.level.iron += struct.resources_per_loop

    def render_on_loop(self, level):
        """:type level: Level"""

        self.screen.fill(Color.grey)
        str_caption = "%.f FPS %.f Playtime" % (self.clock.get_fps(), self.playtime)
        pygame.display.set_caption(str_caption)

        self.render_reassures_bar()

        for tile in level.mapAsTileRows:
            self.screen.blit(tile.bg_img, tile.tile_pos)

            # Draw ggf. structures
            if tile.structure:
                self.screen.blit(tile.structure.structure_img, tile.associated_structure_pos)

        pygame.display.flip()

    def render_reassures_bar(self):
        if self.level.wood > 0:
            self.screen.blit(pygame.image.load("textures/resources/wood.png"), (10, 10))
            str_anz_wood = ": %.f" % self.level.wood
            text_surface = self.my_font.render(str_anz_wood, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 5))

        if self.level.stone > 0:
            self.screen.blit(pygame.image.load("textures/resources/stone2.png"), (10, 42))
            str_anz_stone = ": %.f" % self.level.stone
            text_surface = self.my_font.render(str_anz_stone, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 42))

        if self.level.iron > 0:
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

    def __init__(self, save_game_path):
        self.structuresAsRowArray = []
        self.mapAsRowArray = []

        self.saveGame = open(save_game_path, "r")

        save_game_as_string = self.saveGame.read()

        sg = json.loads(save_game_as_string)

        print("Miscellaneous: ", sg[self.mapVar][self.miscVar])

        for rows in sg[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])

        if self.structuresVar in sg:
            for r in sg[self.structuresVar]:
                self.structuresAsRowArray.append(r["row"])

        print("structuresAsRowArray: ", self.structuresAsRowArray)

        self.level = Level(self.structuresAsRowArray, self.mapAsRowArray)

    def get_level(self):
        return self.level


def create_tile(shortcut, pos):
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


def create_structure(shortcut):
    # type: () -> Structures
    if shortcut == Structures.LumberJack.shortcut:
        return Structures.LumberJack()
    elif shortcut == Structures.Quarry.shortcut:
        return Structures.Quarry()
    elif shortcut == Structures.IronMine.shortcut:
        return Structures.IronMine()
    else:
        return False


class Level:
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


if __name__ == '__main__':
    map1 = "level.map"
    map2 = "level2.map"
    game = Game()
    lp = LevelParser("save_game.json")
    game.level = lp.get_level()
    game.execute()
