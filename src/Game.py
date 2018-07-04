# -*- coding: utf-8 -*-
import json
import os
import random
import sys

import pygame
import pygbutton

from src import Screens, Tiles, Structures
from src import config as cfg
from src.Utilities import ColorRGB

__author__ = "Noah Ruben"
__version__ = "0.1"

parent_dir = os.path.dirname(os.getcwd())


class Level:
    mapAsTileRows = []
    structures = []
    constructions = []
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
    show_territory = False
    FPS = 60
    level = None
    windows = []
    songs = []
    buttons = []
    music_volume = 100
    playtime = 0
    millis = 0
    resources_event_id = 25
    construction_event_id = 26
    game_icon = os.path.join(parent_dir, "textures/tiles/mountainTile.png")

    def __init__(self):
        print("New Game")
        pygame.mixer.init()
        pygame.font.init()
        pygame.init()

        self.load_settings()

        self.running = True
        self.pause = False
        self.clock = pygame.time.Clock()

        pygame.display.set_icon(pygame.image.load(self.game_icon))

        self.screen = pygame.display.set_mode((500, 500))
        self.screen.fill(ColorRGB.grey)

        self.comic_sans_30 = pygame.font.SysFont('Comic Sans MS', 30)
        self.boxy_bold_20 = pygame.font.Font(os.path.join(parent_dir, "textures/utils/fonts/Boxy-Bold.ttf"), 20)
        self.thor_20 = pygame.font.Font(os.path.join(parent_dir, "textures/utils/fonts/Thor.ttf"), 30)

        self.init_bg_music()

        self.buttons.append(pygbutton.PygButton((450, 0, 50, 30), 'T'))

    def execute(self):
        pygame.time.set_timer(self.resources_event_id, 1000)
        while self.running:
            if self.pause:
                for event in pygame.event.get():
                    if event.type == self.resources_event_id:
                        pygame.time.set_timer(self.resources_event_id, 1000)
                    elif event.type == pygame.QUIT:
                        self.running = False
                        pygame.quit()
                        sys.exit()

                self.play_music(self.music_volume)
                self.update_windows()

            else:
                self.on_event()
                self.on_loop()
                self.render_on_loop(self.level)

        pygame.mixer.music.stop()
        pygame.display.quit()

    def on_event(self):
        for event in pygame.event.get():
            if event.type == self.resources_event_id:
                pygame.time.set_timer(self.resources_event_id, 1000)
                for structure in self.level.structures:
                    if type(structure) is Structures.LumberJack:
                        self.level.wood += structure.resources_per_loop
                        print(self.level.wood)
                    if type(structure) is Structures.LumberJackTierTwo:
                        self.level.wood += structure.resources_per_loop
                        print(self.level.wood)
                    elif type(structure) is Structures.Quarry:
                        self.level.stone += structure.resources_per_loop
                    elif type(structure) is Structures.IronMine:
                        self.level.iron += structure.resources_per_loop

            if event.type == self.construction_event_id:
                for construction in self.level.constructions:
                    print(construction)
                    construction.build_tick()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
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

            for button in self.buttons:
                if 'click' in button.handleEvent(event):
                    self.show_territory = not self.show_territory

            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def on_loop(self):
        # Time
        self.millis = self.clock.tick(self.FPS)
        self.playtime += self.millis / 1000
        self.play_music(self.music_volume)

    def render_on_loop(self, level: Level):
        """:type level: Level"""

        self.screen.fill(ColorRGB.grey)
        str_caption = "%.f FPS %.f Playtime" % (self.clock.get_fps(), self.playtime)
        pygame.display.set_caption(str_caption)

        self.update_windows()

        self.render_reassures_bar()

        for button in self.buttons:
            button.draw(self.screen)

        for row in level.mapAsTileRows:
            for tile in row:
                self.screen.blit(tile.bg_img, tile.tile_pos)

                if tile.is_in_territory and self.show_territory:
                    self.screen.blit(pygame.image.load(tile.green_boarder), tile.tile_pos)

                # Draw ggf. structures
                if tile.structure is not None:
                    self.screen.blit(tile.structure.structure_img, tile.associated_structure_pos)

        pygame.display.flip()

    def update_windows(self):
        for window in self.windows:
            if window.is_active:
                window.update()
            else:
                self.windows.remove(window)

    def render_reassures_bar(self):
        if self.level.wood >= 1:
            self.screen.blit(pygame.image.load(os.path.join(parent_dir, "textures/resources/wood.png")), (10, 10))
            str_anz_wood = ": %.f" % self.level.wood
            text_surface = self.boxy_bold_20.render(str_anz_wood, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 15))

        if self.level.stone >= 1:
            self.screen.blit(pygame.image.load(os.path.join(parent_dir, "textures/resources/stone2.png")), (10, 42))
            str_anz_stone = ": %.f" % self.level.stone
            text_surface = self.thor_20.render(str_anz_stone, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 42))

        if self.level.iron >= 1:
            self.screen.blit(pygame.image.load(os.path.join(parent_dir, "textures/resources/iron.png")), (10, 74))
            str_anz_iron = ": %.f" % self.level.iron
            text_surface = self.comic_sans_30.render(str_anz_iron, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 74))

    def close(self):
        self.running = False
        for window in self.windows:
            try:
                window.close()
            except BaseException:
                print("Oops!  That was already closed")

    def play_music(self, volume):
        pygame.mixer.music.set_volume(float(volume))
        if not pygame.mixer.music.get_busy():
            self.current_song_id = random.randint(0, self.songs.__len__() - 1)
            print(self.songs[self.current_song_id])
            pygame.mixer.music.load(self.songs[self.current_song_id])
            pygame.mixer.music.play()

    def init_bg_music(self):
        self.songs.append(os.path.join(parent_dir, "sounds/music/Glorious_Morning_Waterflame.mp3"))
        # add more musik ?

    def load_settings(self):
        self.music_volume = cfg.get_value(cfg.sound_section, cfg.music_volume_option)


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

        self.save_game_file = open(os.path.join(parent_dir, save_game_path), "r")

        save_game_as_string = self.save_game_file.read()

        save_game_as_json_object = json.loads(save_game_as_string)

        print("Miscellaneous: ", save_game_as_json_object[self.mapVar][self.miscVar])
        print("Season: ", save_game_as_json_object[self.mapVar][self.seasonVar])
        print("Resources: ", save_game_as_json_object[self.resourcesVar])

        for rows in save_game_as_json_object[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])

        if self.structuresVar in save_game_as_json_object:
            for r in save_game_as_json_object[self.structuresVar]:
                self.structuresAsRowArray.append(r["row"])

        self.level = Level()

        pos_y = 40
        pos_x = 100

        for row_index in range(0, self.mapAsRowArray.__len__()):
            pos_y += 40
            temp_array = []
            temp_array.clear()
            for tile_shortcut_index in range(0, self.mapAsRowArray[row_index].__len__()):
                pos_x += 40
                if self.structuresAsRowArray:
                    temp_structure = create_structure(self.structuresAsRowArray[row_index][tile_shortcut_index])
                    temp_array.append(create_tile(self.mapAsRowArray[row_index][tile_shortcut_index], (pos_x, pos_y),
                                                  (row_index, tile_shortcut_index),
                                                  structure=temp_structure))
                    self.level.structures.append(temp_structure)
                else:
                    temp_array.append(create_tile(self.mapAsRowArray[row_index][tile_shortcut_index], (pos_x, pos_y),
                                                  (row_index, tile_shortcut_index)))

            for tile in temp_array:
                print(tile)

            pos_x = 100
            self.level.mapAsTileRows.append(temp_array)

        for row in self.level.mapAsTileRows:
            for tile in row:
                if tile.structure is not None and type(tile.structure) == Structures.Castle:
                    tile.structure.create_territory(tile=tile, level=self.level)

        # set the level resources
        self.level.wood = save_game_as_json_object[self.resourcesVar][self.woodVar]
        self.level.stone = save_game_as_json_object[self.resourcesVar][self.stoneVar]
        self.level.iron = save_game_as_json_object[self.resourcesVar][self.ironVar]

        self.save_game_file.close()

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
        self.save_game_file = open(os.path.join(parent_dir, self.save_game_path), "w")

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

        for row in self.level.mapAsTileRows:
            temp_tile_shortcut_array = []
            temp_structures_shortcut_array = []
            temp_tile_shortcut_array.clear()
            temp_structures_shortcut_array.clear()
            for tile in row:
                temp_tile_shortcut_array.append(tile.shortcut)
                if tile.structure:
                    temp_structures_shortcut_array.append(tile.structure.shortcut)
                else:
                    temp_structures_shortcut_array.append("N")

            json_obj[self.mapVar][self.terrainVar].append(self.create_row(temp_tile_shortcut_array))
            json_obj[self.structuresVar].append(self.create_row(temp_structures_shortcut_array))

        json_obj[self.resourcesVar][self.woodVar] = self.level.wood
        json_obj[self.resourcesVar][self.stoneVar] = self.level.stone
        json_obj[self.resourcesVar][self.ironVar] = self.level.iron

        json.dump(json_obj, self.save_game_file)
        self.save_game_file.close()

    def create_row(self, row_inhalt):
        row_json_object = json.loads('{"row" : []}')
        row_json_object[self.rowVar] = row_inhalt
        return row_json_object


class Construction:
    def __init__(self, level, where: tuple, structure_name, time: int):
        pygame.time.set_timer(Game.construction_event_id, 1000)
        self.level = level
        self.where_to_build = where
        self.time_till_completion = time

        self.tile = self.level.mapAsTileRows[self.where_to_build[0]][self.where_to_build[1]]
        self.structure = create_structure(structure_name)
        self.time = self.structure.build_time

        self.hammering = pygame.mixer.Sound(os.path.join(parent_dir, "sounds/effects/hammering.wav"))
        self.hammering.play(1, fade_ms=1000)


    def build_tick(self):
        if (self.level.wood - self.structure.build_costs[0]) >= 0 and (
                self.level.stone - self.structure.build_costs[1]) >= 0 and (
                self.level.iron - self.structure.build_costs[2]) >= 0:
            self.time_till_completion -= 1
            self.level.wood -= self.structure.build_costs[0]
            self.level.stone -= self.structure.build_costs[1]
            self.level.iron -= self.structure.build_costs[2]
        else:
            print("Could not work, not enough items")

        if self.time_till_completion == 0:
            self.build_done()

    def build_done(self):
        if self.tile.structure is not None:
            self.level.structures.remove(self.tile.structure)

        self.tile.structure = self.structure
        self.tile.construction = None
        self.level.structures.append(self.structure)
        self.level.constructions.remove(self)

        self.hammering.fadeout(1000)

        if type(self.structure) is Structures.Castle:
            self.structure.create_territory(self.tile, self.level)

    def __str__(self):
        return str(self.time_till_completion) + " successful workdays till completion of the " + self.structure.name


def create_tile(shortcut: str, pos: tuple, rel_pos, structure=None):
    if shortcut == Tiles.NormalTile.shortcut:
        temp = Tiles.NormalTile(pos, rel_pos)
        temp.set_structure(structure)
        return temp
    elif shortcut == Tiles.ForestTile.shortcut:
        temp = Tiles.ForestTile(pos, rel_pos)
        temp.set_structure(structure)
        return temp
    elif shortcut == Tiles.MineTile.shortcut:
        temp = Tiles.MineTile(pos, rel_pos)
        temp.set_structure(structure)
        return temp
    elif shortcut == Tiles.LakeTile.shortcut:
        temp = Tiles.LakeTile(pos, rel_pos)
        temp.set_structure(structure)
        return temp
    elif shortcut == Tiles.MountainTile.shortcut:
        temp = Tiles.MountainTile(pos, rel_pos)
        temp.set_structure(structure)
        return temp
    else:
        print("There went something wrong for creating the Tile")
        return Tiles.NormalTile(pos, rel_pos)


def create_structure(shortcut: str):
    # type: () -> Structures.Structure
    if shortcut == Structures.LumberJack.shortcut or shortcut == Structures.LumberJack.name:
        return Structures.LumberJack()
    if shortcut == Structures.LumberJackTierTwo.shortcut or shortcut == Structures.LumberJackTierTwo.name:
        return Structures.LumberJackTierTwo()
    elif shortcut == Structures.Quarry.shortcut or shortcut == Structures.Quarry.name:
        return Structures.Quarry()
    elif shortcut == Structures.IronMine.shortcut or shortcut == Structures.IronMine.name:
        return Structures.IronMine()
    elif shortcut == Structures.Castle.shortcut or shortcut == Structures.Castle.name:
        return Structures.Castle()
    else:
        return None
