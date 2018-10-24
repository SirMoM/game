# -*- coding: utf-8 -*-
import json
import logging
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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler
handler = logging.FileHandler(os.path.join(parent_dir, "logs/GameLog.log"))
handler.setLevel(logging.INFO)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


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
        # TODO Do it right so someone can understand this output

        str_names = ""
        for row in self.mapAsTileRows:
            for tile in row:
                str_names += tile.__str__() + ", "
            str_names += "\n"
        return str_names


class Game:
    width = 1000
    height = 1000
    x_offset = 200
    y_offset = 100
    running = False
    show_territory = False
    FPS = 60
    level = None
    windows = []
    songs = []
    buttons = []
    music_volume = None
    effects_volume = None
    playtime = 0
    millis = 0
    resources_event_id = 25
    construction_event_id = 26
    game_icon = os.path.join(parent_dir, "textures/tiles/mountainTile.png")

    def __init__(self, level: Level):
        logger.info("NEW GAME")
        pygame.mixer.init()
        pygame.font.init()
        pygame.init()

        pygame.key.set_repeat(75, 25)
        self.level = level

        self.load_settings()

        self.running = True
        self.pause = False
        self.clock = pygame.time.Clock()

        pygame.display.set_icon(pygame.image.load(self.game_icon))

        # self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        self.comic_sans_30 = pygame.font.SysFont('Comic Sans MS', 30)
        self.boxy_bold_25 = pygame.font.Font(os.path.join(parent_dir, "textures/utils/fonts/Boxy-Bold.ttf"), 25)
        self.thor_20 = pygame.font.Font(os.path.join(parent_dir, "textures/utils/fonts/Thor.ttf"), 30)

        self.screen.fill(ColorRGB.grey)

        self.init_bg_music()

        self.buttons.append(pygbutton.PygButton((self.width - 50, 0, 50, 50), 'T', font=self.boxy_bold_25))

        self.buttons.append(
            pygbutton.PygButton((self.width - 150, self.height - 200, 50, 50), '<', font=self.boxy_bold_25))
        self.buttons.append(
            pygbutton.PygButton((self.width - 100, self.height - 250, 50, 50), '^', font=self.boxy_bold_25))
        self.buttons.append(
            pygbutton.PygButton((self.width - 100, self.height - 150, 50, 50), 'v', font=self.boxy_bold_25))
        self.buttons.append(
            pygbutton.PygButton((self.width - 50, self.height - 200, 50, 50), '>', font=self.boxy_bold_25))

        self.renderer: GameRender = GameRender(self.level, self.screen)

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
                        logger.info("Wood addes: " + self.level.wood.__str__())
                    if type(structure) is Structures.LumberJackTierTwo:
                        self.level.wood += structure.resources_per_loop
                        logger.info("Wood added: " + self.level.wood.__str__())
                    elif type(structure) is Structures.Quarry:
                        self.level.stone += structure.resources_per_loop
                        logger.info("Stone added: " + self.level.stone.__str__())
                    elif type(structure) is Structures.IronMine:
                        self.level.iron += structure.resources_per_loop
                        logger.info("Iron added: " + self.level.iron.__str__())

            if event.type == self.construction_event_id:
                for construction in self.level.constructions:
                    # logger.info(construction)
                    construction.build_tick()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    xPos, yPos = pygame.mouse.get_pos()
                    logger.info("Clicked at: " + xPos.__str__() + " ," + yPos.__str__())

                    for row in self.level.mapAsTileRows:
                        for tile in row:
                            if tile.is_point_in_tile(xPos, yPos):
                                tile_screen = Screens.TileScreen(self, tile)
                                self.windows.append(tile_screen)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    this = self
                    self.windows.append(Screens.InGameMenu(this))

                if event.key == pygame.K_w:
                    self.renderer.move_map_up()

                if event.key == pygame.K_s:
                    self.renderer.move_map_down()

                if event.key == pygame.K_a:
                    self.renderer.move_map_left()

                if event.key == pygame.K_d:
                    self.renderer.move_map_right()

            for button in self.buttons:
                if 'click' in button.handleEvent(event):

                    if button._propGetCaption() is "T":
                        self.renderer.toggle_territory_visibility()
                    if button._propGetCaption() is "^":
                        self.renderer.move_map_up()
                    if button._propGetCaption() is "v":
                        self.renderer.move_map_down()
                    if button._propGetCaption() is "<":
                        self.renderer.move_map_left()
                    if button._propGetCaption() is ">":
                        self.renderer.move_map_right()
                    else:
                        logger.info("button: " + button._caption)

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

        self.screen.fill(ColorRGB.grey)
        str_caption = "Gloria! \t \t %.f FPS %.f Playtime" % (self.clock.get_fps(), self.playtime)
        pygame.display.set_caption(str_caption)

        self.update_windows()

        # TODO redo the buttons in the Randerer Class
        for button in self.buttons:
            button.draw(self.screen)

        # self.renderer.levelToRender = level
        self.renderer.render()

        self.update_pygame_screen()

        pygame.display.flip()

    def update_windows(self):
        for window in self.windows:
            if window.is_active:
                window.update()
            else:
                self.windows.remove(window)

    def close(self):
        self.running = False
        for window in self.windows:
            try:
                window.close()
            except BaseException:
                logger.error("Oops!  That was already closed")

    def play_music(self, volume):
        pygame.mixer.music.set_volume(float(volume))
        if not pygame.mixer.music.get_busy():
            self.current_song_id = random.randint(0, self.songs.__len__() - 1)
            logger.info("Song playing" + self.songs[self.current_song_id])
            pygame.mixer.music.load(self.songs[self.current_song_id])
            pygame.mixer.music.play()

    def init_bg_music(self):
        # TODO Auto scan  the musik library
        # TODO add more musik ?
        self.songs.append(os.path.join(parent_dir, "sounds/music/Glorious_Morning_Waterflame.mp3"))
        self.songs.append(os.path.join(parent_dir, "sounds/music/Mid-Air_Machine_-_Untamed_Wings.mp3"))

    def load_settings(self):
        self.music_volume = cfg.get_value(cfg.sound_section, cfg.music_volume_option)
        self.effects_volume = cfg.get_value(cfg.sound_section, cfg.sfx_volume_option)

    def update_pygame_screen(self):
        self.width, self.height = pygame.display.Info().current_w, pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.update()


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

        logger.info("Miscellaneous: " + save_game_as_json_object[self.mapVar][self.miscVar])
        logger.info("Season: " + save_game_as_json_object[self.mapVar][self.seasonVar])
        logger.info("Resources: " + save_game_as_json_object[self.resourcesVar].__str__())

        for rows in save_game_as_json_object[self.mapVar][self.terrainVar]:
            self.mapAsRowArray.append(rows["row"])

        if self.structuresVar in save_game_as_json_object:
            for r in save_game_as_json_object[self.structuresVar]:
                self.structuresAsRowArray.append(r["row"])

        self.level = Level()

        pos_y = Game.y_offset
        pos_x = Game.y_offset

        for row_index in range(0, self.mapAsRowArray.__len__()):
            pos_y += 33
            temp_array = []
            temp_array.clear()
            for tile_shortcut_index in range(0, self.mapAsRowArray[row_index].__len__()):
                pos_x += 33
                if self.structuresAsRowArray:
                    temp_structure = create_structure(self.structuresAsRowArray[row_index][tile_shortcut_index])
                    temp_array.append(create_tile(self.mapAsRowArray[row_index][tile_shortcut_index], (pos_x, pos_y),
                                                  (row_index, tile_shortcut_index),
                                                  structure=temp_structure))
                    self.level.structures.append(temp_structure)
                else:
                    temp_array.append(create_tile(self.mapAsRowArray[row_index][tile_shortcut_index], (pos_x, pos_y),
                                                  (row_index, tile_shortcut_index)))

            pos_x = Game.x_offset
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
    def __init__(self, game: Game, where: tuple, structure_name):
        pygame.time.set_timer(Game.construction_event_id, 1000)
        self.level = game.level
        self.where_to_build = where

        self.tile = self.level.mapAsTileRows[self.where_to_build[0]][self.where_to_build[1]]
        self.structure = create_structure(structure_name)
        self.time_till_completion = self.structure.build_time
        self.time = self.structure.build_time

        self.hammering = pygame.mixer.Sound(os.path.join(parent_dir, "sounds/effects/hammering.wav"))
        self.hammering.set_volume(float(game.effects_volume))
        self.hammering.play(-1)

    def build_tick(self):
        if (self.level.wood - self.structure.build_costs[0]) >= 0 and (
                self.level.stone - self.structure.build_costs[1]) >= 0 and (
                self.level.iron - self.structure.build_costs[2]) >= 0:
            self.time_till_completion -= 1
            self.level.wood -= self.structure.build_costs[0]
            self.level.stone -= self.structure.build_costs[1]
            self.level.iron -= self.structure.build_costs[2]
        else:
            logger.info("Could not work, not enough resources")

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
        logger.error("There went something wrong for creating the Tile")
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


class GameRender:
    show_territory: bool = False
    y_rendering_pos: int = 0
    x_rendering_pos: int = 0

    y_anchor_pos: int = 250
    x_anchor_pos: int = 200

    y_offset: int = 33
    x_offset: int = 33

    resource_boarder_gap: int = 150

    comic_sans_30 = pygame.font.SysFont('Comic Sans MS', 30)
    boxy_bold_25 = pygame.font.Font(os.path.join(parent_dir, "textures/utils/fonts/Boxy-Bold.ttf"), 25)
    thor_20 = pygame.font.Font(os.path.join(parent_dir, "textures/utils/fonts/Thor.ttf"), 30)

    def __init__(self, level: Level, screen):
        logger.info("DAS IST EIN TEST info DAS SOLLTE FUNSEN")
        self.levelToRender = level
        self.screen = screen

    def toggle_territory_visibility(self):
        self.show_territory = not self.show_territory

    def render(self):
        self.render_map()
        self.resource_bar()

    def render_map(self):
        for row in self.levelToRender.mapAsTileRows:
            for tile in row:
                self.y_rendering_pos = tile.rel_pos_tuple[0] * self.y_offset + self.y_anchor_pos
                self.x_rendering_pos = tile.rel_pos_tuple[1] * self.x_offset + self.x_anchor_pos

                logger.debug(("y_rendering_pos", self.y_rendering_pos, "x_rendering_pos", self.x_rendering_pos))

                tile.set_new_pos((self.x_rendering_pos, self.y_rendering_pos))
                self.screen.blit(tile.bg_img, (self.x_rendering_pos, self.y_rendering_pos))

                if tile.is_in_territory is True and self.show_territory is True:
                    self.screen.blit(pygame.image.load(tile.green_boarder), tile.tile_pos)

                # Draw ggf. structures
                if tile.structure is not None:
                    self.screen.blit(tile.structure.structure_img, tile.associated_structure_pos)

    def resource_bar(self):
        if self.levelToRender.wood >= 1:
            self.screen.blit(pygame.image.load(os.path.join(parent_dir, "textures/resources/wood.png")), (10, 10))
            str_anz_wood = ": %.f" % self.levelToRender.wood
            text_surface = self.boxy_bold_25.render(str_anz_wood, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 15))

        if self.levelToRender.stone >= 1:
            self.screen.blit(pygame.image.load(os.path.join(parent_dir, "textures/resources/stone2.png")), (10, 42))
            str_anz_stone = ": %.f" % self.levelToRender.stone
            text_surface = self.boxy_bold_25.render(str_anz_stone, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 42))

        if self.levelToRender.iron >= 1:
            self.screen.blit(pygame.image.load(os.path.join(parent_dir, "textures/resources/iron.png")), (10, 74))
            str_anz_iron = ": %.f" % self.levelToRender.iron
            text_surface = self.boxy_bold_25.render(str_anz_iron, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 74))

    def move_map_up(self):
        self.y_anchor_pos -= 25

    def move_map_down(self):
        self.y_anchor_pos += 25

    def move_map_left(self):
        self.x_anchor_pos -= 25

    def move_map_right(self):
        self.x_anchor_pos += 25
