# -*- coding: utf-8 -*-
"""
This is the module responsible for all things that happen in the game

Import
------
    json
        for loading and saving a level
    random

    sys

    pygame

    pygbutton

"""
import json
import random
import sys
from typing import Tuple, List

import pygame
import pygbutton
from pygame.mixer import Sound

from src import Screens, Tiles, Structures
from src import config as cfg
from src.Structures import StructureException, Structure
from src.Utilities import ColorRGB, get_system_path_from_relative_path


class Level:
    """
    This Class represents a level which can be played.
    """
    # TODO TILE, Construction Typ hint
    mapAsTileRows: List = []
    structures: List[Structure] = []
    constructions: List = []
    wood: int = 0
    stone: int = 0
    iron: int = 0

    def resources_as_string(self) -> str:
        """
        A formatted way for the resources of the level

        Returns
        -------
        :return all resources as a String
        """
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
    width: int = 1000
    height: int = 1000
    x_offset: int = 200
    y_offset: int = 100
    running: bool = False
    FPS: int = 60
    level: Level
    windows = []
    songs = []
    buttons = []
    music_volume: int
    effects_volume: int
    playtime: int = 0
    millis: int = 0
    resources_event_id: int = 25
    construction_event_id: int = 26
    game_icon: str = get_system_path_from_relative_path("textures/tiles/mountainTile.png")

    def __init__(self, level: Level):
        # TODO logger.info("NEW GAME")
        pygame.mixer.init()
        pygame.font.init()
        pygame.init()

        pygame.key.set_repeat(75, 25)
        self.level = level

        self.load_settings()

        self.running = True
        self.pause = False
        self.clock = pygame.time.Clock()
        self.current_song_id = -1
        pygame.display.set_icon(pygame.image.load(self.game_icon))

        # self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

        self.comic_sans_30 = pygame.font.SysFont('Comic Sans MS', 30)
        self.boxy_bold_25 = pygame.font.Font(get_system_path_from_relative_path("textures/utils/fonts/Boxy-Bold.ttf"),
                                             25)
        self.thor_20 = pygame.font.Font(get_system_path_from_relative_path("textures/utils/fonts/Thor.ttf"), 30)

        self.screen.fill(ColorRGB.grey)

        self.init_bg_music()
        self.init_buttons()

        self.renderer: GameRender = GameRender(self.level, self.screen)

    def execute(self) -> None:
        """
        The main loop for the game.
        """
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
                self.render_on_loop()

        pygame.mixer.music.stop()
        pygame.display.quit()

    def on_event(self) -> None:
        """
        Handles all events in the game
        """
        for event in pygame.event.get():
            if event.type == self.resources_event_id:
                pygame.time.set_timer(self.resources_event_id, 1000)
                for structure in self.level.structures:
                    if type(structure) is Structures.LumberJack:
                        self.level.wood += structure.resources_per_loop
                        # TODO logger.info("Wood addes: " + self.level.wood.__str__())
                    if type(structure) is Structures.LumberJackTierTwo:
                        self.level.wood += structure.resources_per_loop
                        # TODO logger.info("Wood added: " + self.level.wood.__str__())
                    elif type(structure) is Structures.Quarry:
                        self.level.stone += structure.resources_per_loop
                        # TODO logger.info("Stone added: " + self.level.stone.__str__())
                    elif type(structure) is Structures.IronMine:
                        self.level.iron += structure.resources_per_loop
                        # TODO logger.info("Iron added: " + self.level.iron.__str__())

            if event.type == self.construction_event_id:
                for construction in self.level.constructions:
                    # # TODO logger.info(construction)
                    construction.build_tick()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    xPos, yPos = pygame.mouse.get_pos()
                    # TODO logger.info("Clicked at: " + xPos.__str__() + " ," + yPos.__str__())

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
                        # TODO logger.info("button: " + button._caption)
                        pass

            if event.type == pygame.VIDEORESIZE:
                old_width, old_height = self.width, self.height
                self.width = event.w
                self.height = event.h
                dif_width, dif_height = self.width - old_width, self.height - old_height
                pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

                for button in self.buttons:
                    newrect = button._propGetRect().move(dif_width, dif_height)
                    button._propSetRect(newrect)

            # quit if the quit button was pressed
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

    def on_loop(self) -> None:
        """
        All the game logic per loop
        :return:
        """
        # Time
        self.millis = self.clock.tick(self.FPS)
        self.playtime += self.millis / 1000
        self.play_music(self.music_volume)

    def render_on_loop(self) -> None:
        """
        This manages all the rendering for the game
        """
        self.screen.fill(ColorRGB.grey)
        str_caption = "Gloria! \t \t %.f FPS %.f Playtime" % (self.clock.get_fps(), self.playtime)
        pygame.display.set_caption(str_caption)

        self.update_windows()

        # TODO redo the buttons in the Randerer Class
        for button in self.buttons:
            button.draw(self.screen)

        # self.renderer.levelToRender = level
        self.renderer.render()

        pygame.display.flip()

    def update_windows(self) -> None:
        """
        Updates all TK Windows in the List windows
        """
        for window in self.windows:
            if window.is_active:
                window.update()
            else:
                self.windows.remove(window)

    def close(self) -> None:
        """
        This function shuts the game down
        """
        self.running = False
        for window in self.windows:
            try:
                window.close()
            except BaseException:
                # TODO logger.error("Oops!  That was already closed")
                pass

    def play_music(self, volume) -> None:
        """
         Plays music randomly
        :param volume: the volume at which the music is played
        """
        pygame.mixer.music.set_volume(float(volume))
        if not pygame.mixer.music.get_busy():
            self.current_song_id = random.randint(0, self.songs.__len__() - 1)
            # TODO logger.info("Song playing" + self.songs[self.current_song_id])
            pygame.mixer.music.load(self.songs[self.current_song_id])
            pygame.mixer.music.play()

    def init_bg_music(self) -> None:
        """
        registers all Paths for the music!
        """
        # TODO Auto scan  the musik library
        # TODO add more musik ?
        self.songs.append(get_system_path_from_relative_path("sounds/music/Glorious_Morning_Waterflame.mp3"))
        self.songs.append(get_system_path_from_relative_path("sounds/music/Mid-Air_Machine_-_Untamed_Wings.mp3"))

    def load_settings(self) -> None:
        """
            Loads the settings form the config File
        """
        self.music_volume = cfg.get_value(cfg.sound_section, cfg.music_volume_option)
        self.effects_volume = cfg.get_value(cfg.sound_section, cfg.sfx_volume_option)

    def init_buttons(self) -> None:
        """
        creates all the on screen buttons for the game
        """
        self.buttons.append(pygbutton.PygButton((self.width - 50, 0, 50, 50), 'T', font=self.boxy_bold_25))
        self.buttons.append(
            pygbutton.PygButton((self.width - 150, self.height - 200, 50, 50), '<', font=self.boxy_bold_25))
        self.buttons.append(
            pygbutton.PygButton((self.width - 100, self.height - 250, 50, 50), '^', font=self.boxy_bold_25))
        self.buttons.append(
            pygbutton.PygButton((self.width - 100, self.height - 150, 50, 50), 'v', font=self.boxy_bold_25))
        self.buttons.append(
            pygbutton.PygButton((self.width - 50, self.height - 200, 50, 50), '>', font=self.boxy_bold_25))


class LevelParser:
    mapVar: str = "map"
    terrainVar: str = "terrain"
    rowVar: str = "row"
    miscVar: str = "misc"
    structuresVar: str = "structures"
    seasonVar: str = "season"
    resourcesVar: str = "resources"
    woodVar: str = "wood"
    stoneVar: str = "stone"
    ironVar: str = "iron"

    def __init__(self, save_game_path: str):
        self.structuresAsRowArray = []
        self.mapAsRowArray = []

        self.save_game_file = open(get_system_path_from_relative_path(save_game_path), "r")

        save_game_as_string = self.save_game_file.read()

        save_game_as_json_object = json.loads(save_game_as_string)

        # TODO logger.info("Miscellaneous: " + save_game_as_json_object[self.mapVar][self.miscVar])
        # TODO logger.info("Season: " + save_game_as_json_object[self.mapVar][self.seasonVar])
        # TODO logger.info("Resources: " + save_game_as_json_object[self.resourcesVar].__str__())

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
                try:
                    temp_structure: Structure = create_structure(
                        self.structuresAsRowArray[row_index][tile_shortcut_index])
                except StructureException:
                    # TODO log the exception
                    temp_structure = None

                temp_tile: Tiles.Tile = create_tile(self.mapAsRowArray[row_index][tile_shortcut_index], (pos_x, pos_y),
                                                    (row_index, tile_shortcut_index), structure=temp_structure)

                # create_tile(self.mapAsRowArray[row_index][tile_shortcut_index], (pos_x, pos_y), (row_index, tile_shortcut_index))
                temp_array.append(temp_tile)
                if temp_structure is not None:
                    self.level.structures.append(temp_structure)


            pos_x = Game.x_offset
            self.level.mapAsTileRows.append(temp_array)

        for row in self.level.mapAsTileRows:
            for tile in row:
                if tile.get_structure() is not None and type(tile.get_structure) == Structures.Castle:
                    tile.get_structure().create_territory(tile=tile, level=self.level)

        # set the level resources
        self.level.wood = save_game_as_json_object[self.resourcesVar][self.woodVar]
        self.level.stone = save_game_as_json_object[self.resourcesVar][self.stoneVar]
        self.level.iron = save_game_as_json_object[self.resourcesVar][self.ironVar]

        self.save_game_file.close()

    def get_level(self) -> Level:
        """
        gives you the level
        :return: The level resulting from the Level-Parser
        """
        return self.level


class LevelWriter(object):
    mapVar: str = "map"
    terrainVar: str = "terrain"
    rowVar: str = "row"
    miscVar: str = "misc"
    structuresVar: str = "structures"
    seasonVar: str = "season"
    resourcesVar: str = "resources"
    woodVar: str = "wood"
    stoneVar: str = "stone"
    ironVar: str = "iron"

    def __init__(self, filename: str, level: Level):
        self.filename = filename
        self.level = level
        self.save_game_path = "saves/" + filename + ".json"
        self.save_game_file = open(get_system_path_from_relative_path(self.save_game_path), "w")

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
                if tile.get_structure():
                    temp_structures_shortcut_array.append(tile.get_structure().shortcut)
                else:
                    temp_structures_shortcut_array.append("N")

            json_obj[self.mapVar][self.terrainVar].append(self.create_row(temp_tile_shortcut_array))
            json_obj[self.structuresVar].append(self.create_row(temp_structures_shortcut_array))

        json_obj[self.resourcesVar][self.woodVar] = self.level.wood
        json_obj[self.resourcesVar][self.stoneVar] = self.level.stone
        json_obj[self.resourcesVar][self.ironVar] = self.level.iron

        json.dump(json_obj, self.save_game_file)
        self.save_game_file.close()

    def create_row(self, row_content) -> json:
        """
        Creates a json object from row-values

        :param row_content: the value of a row
        :return: A json object of the row
        """
        row_json_object = json.loads('{"row" : []}')
        row_json_object[self.rowVar] = row_content
        return row_json_object


class Construction:
    """
        This represents a construction on a Tile.
    """
    level: Level
    where_to_build: Tuple[int, int]
    # TODO TYPE Hinting
    tile = None
    structure: Structure
    time_till_completion: int
    time: int
    hammering: Sound

    def __init__(self, game: Game, where: tuple, structure_name: str):
        pygame.time.set_timer(Game.construction_event_id, 1000)
        self.level = game.level
        self.where_to_build = where

        self.tile = self.level.mapAsTileRows[self.where_to_build[0]][self.where_to_build[1]]
        self.structure = create_structure(structure_name)
        self.time_till_completion = self.structure.build_time
        self.time = self.structure.build_time

        self.hammering = pygame.mixer.Sound(get_system_path_from_relative_path("sounds/effects/hammering.wav"))
        self.hammering.set_volume(float(game.effects_volume))
        self.hammering.play(-1)

    def build_tick(self) -> None:
        """
        A iteration of the building process.
        """
        if (self.level.wood - self.structure.build_costs[0]) >= 0 and (
                self.level.stone - self.structure.build_costs[1]) >= 0 and (
                self.level.iron - self.structure.build_costs[2]) >= 0:
            self.time_till_completion -= 1
            self.level.wood -= self.structure.build_costs[0]
            self.level.stone -= self.structure.build_costs[1]
            self.level.iron -= self.structure.build_costs[2]
        else:
            pass
            # TODO logger.info("Could not work, not enough resources")

        if self.time_till_completion == 0:
            self.build_done()

    def build_done(self):
        """
        Completes a construction.
        """
        if self.tile.get_structure() is not None:
            self.level.structures.remove(self.tile.structure)

        self.tile.set_structure(self.structure)
        self.tile.construction = None
        self.level.structures.append(self.structure)
        self.level.constructions.remove(self)

        self.hammering.fadeout(1000)

        if type(self.structure) is Structures.Castle:
            self.structure.create_territory(self.tile, self.level)

    def __str__(self):
        return str(self.time_till_completion) + " successful workdays till completion of the " + self.structure.name


# TODO is pos rly needed
# TODO type hinting tile
def create_tile(shortcut: str, pos: Tuple[int, int], rel_pos: Tuple[int, int], structure=None):
    """
    This method creates a Tile based on the identifying shortcut.

    Parameter
    ---------
    :param shortcut: The shortcut which the Tile is based on
    :param pos: the absolute position of the Tile
    :param rel_pos: the relative position of the Tile
    :param structure: The Structure of the Tile

    Returns
    -------
    :return: A Tile
    """
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
        # TODO logger.error("There went something wrong for creating the Tile")
        return Tiles.NormalTile(pos, rel_pos)


def create_structure(shortcut: str) -> Structure:
    """
    This method creates a Tile based on the identifying shortcut.

    Parameter
    ---------
    :param shortcut: The shortcut which the identifies the Structure to create


    Returns
    -------
    :return: A Structure

    Raises
    ------
    :raises: StructureException: if no Structure could be created
    """
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
        raise StructureException("Could not create a Structure")


class GameRender:
    """
        This class is for rendering the game.
    """
    show_territory: bool = False
    y_rendering_pos: int = 0
    x_rendering_pos: int = 0

    y_anchor_pos: int = 250
    x_anchor_pos: int = 200

    y_offset: int = 33
    x_offset: int = 33

    resource_boarder_gap: int = 150

    comic_sans_30 = pygame.font.SysFont('Comic Sans MS', 30)
    boxy_bold_25 = pygame.font.Font(get_system_path_from_relative_path("textures/utils/fonts/Boxy-Bold.ttf"), 25)
    thor_20 = pygame.font.Font(get_system_path_from_relative_path("textures/utils/fonts/Thor.ttf"), 30)

    def __init__(self, level: Level, screen):
        # TODO logger.info("DAS IST EIN TEST info DAS SOLLTE FUNSEN")
        self.levelToRender = level
        self.screen = screen

    def toggle_territory_visibility(self) -> None:
        """
        this toggels if the Territory borders should be shown.
        """
        self.show_territory = not self.show_territory

    def render(self) -> None:
        """
        The main rendering method.
        To render the game only this should be called.
        """
        self._render_map()
        self._resource_bar()

    def _render_map(self) -> None:
        """
            renders the Tiles and Structures and gives them their new positions
        """
        for row in self.levelToRender.mapAsTileRows:
            for tile in row:
                self.y_rendering_pos = tile.rel_pos_tuple[0] * self.y_offset + self.y_anchor_pos
                self.x_rendering_pos = tile.rel_pos_tuple[1] * self.x_offset + self.x_anchor_pos

                # TODO logger.debug(("y_rendering_pos", self.y_rendering_pos, "x_rendering_pos", self.x_rendering_pos))

                tile.set_new_pos((self.x_rendering_pos, self.y_rendering_pos))
                self.screen.blit(tile.bg_img, (self.x_rendering_pos, self.y_rendering_pos))

                if tile.is_in_territory is True and self.show_territory is True:
                    self.screen.blit(pygame.image.load(tile.green_boarder), tile.tile_pos)

                # Draw ggf. structures
                if tile.get_structure() is not None:
                    self.screen.blit(tile.get_structure().structure_img, tile.associated_structure_pos)

    def _resource_bar(self) -> None:
        """
        renders the overlay of the ressources
        """
        if self.levelToRender.wood >= 1:
            self.screen.blit(pygame.image.load(get_system_path_from_relative_path("textures/resources/wood.png")),
                             (10, 10))
            str_anz_wood = ": %.f" % self.levelToRender.wood
            text_surface = self.boxy_bold_25.render(str_anz_wood, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 15))

        if self.levelToRender.stone >= 1:
            self.screen.blit(pygame.image.load(get_system_path_from_relative_path("textures/resources/stone2.png")),
                             (10, 42))
            str_anz_stone = ": %.f" % self.levelToRender.stone
            text_surface = self.boxy_bold_25.render(str_anz_stone, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 42))

        if self.levelToRender.iron >= 1:
            self.screen.blit(pygame.image.load(get_system_path_from_relative_path("textures/resources/iron.png")),
                             (10, 74))
            str_anz_iron = ": %.f" % self.levelToRender.iron
            text_surface = self.boxy_bold_25.render(str_anz_iron, False, (0, 0, 0))
            self.screen.blit(text_surface, (52, 74))

    def move_map_up(self) -> None:
        """
        moves the map 25 pixels up
        """
        self.y_anchor_pos -= 25

    def move_map_down(self) -> None:
        """
        moves the map 25 pixels down
        """
        self.y_anchor_pos += 25

    def move_map_left(self) -> None:
        """
        moves the map 25 pixels left
        """
        self.x_anchor_pos -= 25

    def move_map_right(self) -> None:
        """
        moves the map 25 pixels right
        """
        self.x_anchor_pos += 25
