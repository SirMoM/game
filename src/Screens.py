#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module contains all Screens for the game.
The Screens are basically classes for Tkinter.

Import
------

    inspect
        to get all Structures from a the Structures-module

    os
        for managing the save files
    sys
        to get all Structures from a the Structures-module
    tkinter
        to create the Screens
"""
import inspect
import os
import sys
import tkinter
from typing import List

from src import GameMechanics, Structures
from src import config as cfg
from src.Utilities import ColorHex, get_system_path_from_relative_path


class Textfield:
    """
        A wrapper class for an tkinter.Entry
    """

    def __init__(self, screen, side=None, pad_y=None, pad_x=None):
        self.entry = tkinter.Entry(screen)
        self.entry.pack(side=side, pady=pad_y, padx=pad_x)

    def get_user_input(self) -> str:
        """
            the user-input from the textfield

            Returns
            -------
                str
                    the value from the textfield
        """
        return self.entry.get()

    def mark_false_input(self, text):
        """marks the textfield input als false"""
        self.entry["bg"] = ColorHex.red
        self.entry.delete(0, len(self.entry.get()))
        self.entry.insert(0, text)


def get_all_structures():
    """
    Returns
    -------
        List
            a list of all structures in the structures module
    """
    structures = []
    for name, obj in inspect.getmembers(sys.modules[Structures.__name__]):
        if inspect.isclass(obj):
            if issubclass(obj, Structures.Structure):
                structures.append(obj)

    return structures


class TileScreen:
    """
    The Tile screen
    """

    def __init__(self, game, tile):
        # TODO LOG logger.debug("Opend a Tile screen with a" + tile.__str__() + "Tile")
        self.game = game
        self.level = game.level
        self.tile = tile
        self.is_active = True

        self.construction_label = None
        self.overview_frame = None

        self.top_level = tkinter.Tk()
        self.top_level.title(tile.name)
        self.top_level.geometry("450x450")
        self.top_level.protocol("WM_DELETE_WINDOW", self.close)

        self.tile_img = MyImage(self.top_level, self.tile.img_path)
        self.tile_img.create_image(tkinter.TOP, 200, 200)

        self.create_overview_frame()
        self.top_level.focus_force()

    def close(self) -> None:
        """
            closes the screen
        """
        self.is_active = False
        self.top_level.destroy()

    def update(self) -> None:
        """
            updates the Screen
        """
        if self.tile.construction is not None:
            self.construction_label["text"] = self.tile.construction.__str__()
        elif self.construction_label is not None and self.tile.construction is None:
            self.construction_label.forget()

        self.top_level.update()

    def create_overview_frame(self) -> None:
        """
            Lay's out all the components of the Tile-screen
        """
        distance = 10

        self.overview_frame = tkinter.Frame(self.top_level)
        self.overview_frame.pack(fill=tkinter.BOTH, ipady=10, pady=5, expand=True)

        structure_base_str = "Structure: {0}"
        resource_base_str = "ResourceType: {0:.1f} {1} per second"
        is_in_territory_base_str = "This area is {0} in your Territory"

        if self.tile.get_structure():
            structure_label = tkinter.Label(self.overview_frame)
            structure_label["text"] = structure_base_str.format(self.tile.get_structure().name)
            structure_label.pack(side=tkinter.TOP, pady=distance)

            resource_label = tkinter.Label(self.overview_frame)
            resource_label["text"] = resource_base_str.format(self.tile.get_structure().resources_per_loop,
                                                              self.tile.get_structure().resources_type)
            resource_label.pack(side=tkinter.TOP, pady=distance)

        else:
            structure_label = tkinter.Label(self.overview_frame)
            structure_label["text"] = structure_base_str.format("No building")
            structure_label.pack(side=tkinter.TOP, pady=distance)

            resource_label = tkinter.Label(self.overview_frame)
            resource_label["text"] = resource_base_str.format(0.0, "resources")
            resource_label.pack(side=tkinter.TOP, pady=distance)

        if self.tile.is_in_territory:
            territory_label = tkinter.Label(self.overview_frame)
            territory_label["text"] = is_in_territory_base_str.format("")
            territory_label.pack(side=tkinter.TOP, pady=distance)
        else:
            territory_label = tkinter.Label(self.overview_frame)
            territory_label["text"] = is_in_territory_base_str.format("not")
            territory_label.pack(side=tkinter.TOP, pady=distance)

        if self.tile.construction is not None:
            self.construction_label = tkinter.Label(self.overview_frame)
            self.construction_label["text"] = self.tile.construction.__str__()
            self.construction_label.pack(side=tkinter.TOP, pady=distance)

        construction_button = tkinter.Button(self.overview_frame)
        construction_button["text"] = "Construction"
        construction_button["command"] = self.create_construction_frame
        construction_button.pack(side=tkinter.BOTTOM, pady=distance)

    def create_construction_frame(self) -> None:
        """
            Lay's out all the components for the construction view.
        """
        self.overview_frame.destroy()

        self.construction_frame = tkinter.Frame(self.top_level)
        # self.construction_frame["bg"] = "green"
        self.construction_frame.pack(fill=tkinter.BOTH, ipady=10, pady=5, expand=True)

        construction_options = tkinter.Listbox(self.construction_frame, height=5)

        counter = 0
        for option in self.get_construction_options():  # type: Structures.Structure
            construction_options.insert(counter, option.name)
            counter += 1

        construction_options.pack(side=tkinter.TOP, pady=20)

        build_button = tkinter.Button(self.construction_frame)
        build_button["text"] = "Build"
        build_button["command"] = lambda listbox=construction_options: self.build(listbox)
        build_button.pack(side=tkinter.TOP)

        construction_button = tkinter.Button(self.construction_frame)
        construction_button["text"] = "Back"
        construction_button["command"] = self.back_to_main_frame
        construction_button.pack(side=tkinter.BOTTOM)

    def back_to_main_frame(self) -> None:
        """
            destroys the construction frame and opens the Tile overview
        """
        self.construction_frame.destroy()
        self.create_overview_frame()

    def get_construction_options(self) -> List[Structures.Structure]:
        """
            checks what Structures can be build on this Tile
        """
        all_structures: List[Structures.Structure] = get_all_structures()

        construction_options: List[Structures.Structure] = []
        for structure in all_structures:
            print(structure)
            if structure.can_build(self.tile):
                construction_options.append(structure)

        return construction_options

    def build(self, listbox: tkinter.Listbox) -> None:
        """
            Builds the structure which is selected
            :param listbox: the listbox from which to get the structure to build
        """
        if listbox.curselection().__len__() > 0:
            # TODO LOG logger.debug("Building " + listbox.get(listbox.curselection()[0]))

            self.tile.construction = GameMechanics.Construction(self.game, self.tile.rel_pos_tuple,
                                                                listbox.get(listbox.curselection()[0]))
            self.level.constructions.append(self.tile.construction)
            self.back_to_main_frame()


class InGameMenu:
    """
        The in-game Menu screen.
    """

    def __init__(self, game):
        self.game = game
        self.is_active = True
        self.game.pause = True

        self.root = tkinter.Tk()
        self.root.title("Menu")
        self.root.geometry("400x400+100+100")
        self.root.iconbitmap(get_system_path_from_relative_path("textures/gloria_pause_icon.ico"))
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.make_widgets()

    def make_widgets(self) -> None:
        """
            The layout for the in-game menu
        """
        distance = 10
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.pack()

        close_game_button = GuiFactoryPack.button("Close Game", self.close_game, master=self.main_frame)
        close_game_button.pack(side=tkinter.BOTTOM, pady=distance)

        main_menu_button = GuiFactoryPack.button("Main Menu", self.open_main_menu, master=self.main_frame)
        main_menu_button.pack(side=tkinter.BOTTOM, pady=distance)

        options_button = GuiFactoryPack.button("Options", self.options, master=self.main_frame)
        options_button.pack(side=tkinter.BOTTOM, pady=distance)

        save_game_button = GuiFactoryPack.button("Save Game", self.save_level, master=self.main_frame)
        save_game_button.pack(side=tkinter.BOTTOM, pady=distance)

        resume_game_button = GuiFactoryPack.button("Resume game", self.close, master=self.main_frame)
        resume_game_button.pack(side=tkinter.BOTTOM, pady=distance)

    def save_level(self) -> None:
        """
            opens the save level menu
        """
        self.main_frame.destroy()
        self.save_menu = SaveMenu(self.root, self.game)
        back_button = tkinter.Button(master=self.save_menu, text="Back", command=self.back_to_main_frame)
        back_button.pack(side=tkinter.BOTTOM)

    def close_game(self) -> None:
        """
            closes the game
        """
        self.close()
        self.game.close()

    def options(self) -> None:
        """
            opens the options menu
        """
        self.main_frame.destroy()
        self.options = OptionFrame(self.root, game=self.game)
        self.options.pack()
        back_button = GuiFactoryPack.button("Back", self.back_to_main_frame, master=self.options)
        back_button.pack(side=tkinter.BOTTOM)
        # TODO LOG logger.info("Opened Options from the ingame-Menue ")

    def close(self) -> None:
        """
            closes the in-game menu
        """
        self.is_active = False
        self.game.pause = False
        self.root.destroy()
        # TODO LOG logger.info("Close ingame menue")

    def open_main_menu(self) -> None:
        """
            closes the game and this menu and opens the main menu
        """
        self.close()
        self.game.close()

        MainMenu(root=tkinter.Tk())

    def update(self) -> None:
        """
            updates this screen
        """
        self.root.update()

    def back_to_main_frame(self) -> None:
        """
            closes every screen and opens the  in-game menu.
            and loads the settingss for the game in case something changed.
        """
        for ele in self.root.winfo_children():
            ele.destroy()

        self.make_widgets()
        self.game.load_settings()


class SaveMenu(tkinter.Frame):
    """
        The save menu as an own window

        Attributes
        ----------
            forbidden_characters an List which includes all characters which are forbidden in the filename.

    """
    forbidden_characters: List[str] = ['/', '\\', '<', '>', ':', '"', '|', '?', '*', ' ', '.']
    game = None
    is_active: bool
    input_textfield: Textfield

    def __init__(self, root: tkinter.Tk, game) -> None:
        self.game = game
        self.is_active = True

        super().__init__(root)
        self.pack(fill=tkinter.BOTH, expand=True)

        self.make_widgets()

    def make_widgets(self) -> None:
        """
            lays out all the components for the save window
        """
        save_label: tkinter.Label = GuiFactoryPack.label("Name of your Save:", master=self)
        save_label.pack(side=tkinter.TOP, pady=(0, 30))

        self.input_textfield = Textfield(self, side=tkinter.TOP, pad_y=10)

        save_button: tkinter.Button = GuiFactoryPack.button("Save", self.save, self)
        save_button.pack(side=tkinter.TOP, pady=0)

    def save(self) -> None:
        """
            saves the level in the state it is as this is executed
        """
        input_is_valid: bool = True
        self.input_textfield.entry["bg"] = ColorHex.white

        user_input: str = self.input_textfield.get_user_input

        for symbol in self.forbidden_characters:
            if symbol in user_input:
                forbidden_symbols_label = GuiFactoryPack.label(
                    '"/", "\\", "<", ">", ":", """, "|", "?", "*", " ", "." \n are not allowed', master=self)
                forbidden_symbols_label.height = 2
                x = 200 - (forbidden_symbols_label["text"].__len__() / 2)
                forbidden_symbols_label.place(x=x / 2, y=20)

                self.input_textfield.mark_false_input(user_input)
                input_is_valid = False

        if input_is_valid:
            GameMechanics.LevelWriter(user_input, self.game.level)
            saved_label = GuiFactoryPack.label("Saved", master=self)
            saved_label.height = 2
            saved_label.place(x=180, y=40)

    def close(self) -> None:
        """
            close this window
        """
        self.is_active = False
        self.destroy()


class MainMenu:
    """
        the main menu of the game and all its funktions
    """

    root: tkinter.Tk
    y_pos: int = 20

    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("400x400")
        self.root.protocol("WM_DELETE_WINDOW", self.close_main_menu)
        self.root.iconbitmap(get_system_path_from_relative_path("textures/gloria_castle_icon.ico"))
        self.root.attributes("-topmost", True)

        self.main_menu_components()
        # TODO LOG logger.info("Started Main Menue")

    def options(self):
        """
            opens the options screen
        """
        # TODO LOG logger.info("Opened Options from Main Menu")
        self.main_frame.destroy()
        self.option_frame = OptionFrame(self.root)
        create_button(self.option_frame.pack(), "Back", self.back_to_myself, 200, 300)
        self.option_frame.pack()
        # TODO LOG logger.info("Opened Options")

    def back_to_myself(self):
        """
            back to the root menu
        """
        for ele in self.root.winfo_children():
            ele.destroy()

        self.main_menu_components()

    def main_menu_components(self):
        """
            creates the main menu components
        """
        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.grid()

        new_game_button = tkinter.Button(master=self.main_frame, text="New game", command=self.new_game)
        new_game_button.grid(row=0, column=0)

        load_game_button = tkinter.Button(master=self.main_frame, text="Load game", command=self.load_game)
        load_game_button.grid(row=1, column=1)

        options_button = tkinter.Button(master=self.main_frame, text="Options", command=self.options)
        options_button.grid(row=2, column=2)

        close_button = tkinter.Button(master=self.main_frame, text="Close", command=self.close_main_menu)
        close_button.grid(row=3, column=3)

    def load_game(self):
        """
            opens the load game menu
        """
        # TODO LOG logger.info("Load Game")
        self.main_frame.destroy()

        save_folder = get_system_path_from_relative_path("saves")
        os.chdir(save_folder)

        self.load_game_sub_frame = tkinter.Frame(self.root).pack()

        for root, dirs, files in os.walk(save_folder):
            for file in files:
                path = os.path.join(root, file).__str__()
                self.make_game_saves_widget(path, file)

        create_button(self.load_game_sub_frame, "Back", self.back_to_myself, 200, 300)

    def new_game(self):
        """
            opens the new game screen
        """
        # TODO LOG logger.info("New Game")
        self.main_frame.destroy()
        self.new_game_sub_frame = tkinter.Frame(self.root).pack()

        level_1 = "maps/level_1.map"
        level_2 = "maps/level_2.map"

        map_1_button = tkinter.Button(master=self.new_game_sub_frame, text="Map 1",
                                      command=lambda: self.start_game(level_1))
        map_1_button.place(x=100, y=10)

        map_2_button = tkinter.Button(master=self.new_game_sub_frame, text="Map 2",
                                      command=lambda: self.start_game(level_2))
        map_2_button.place(x=100, y=40)

        create_button(self.new_game_sub_frame, "Back", self.back_to_myself, 200, 300)

    def close_main_menu(self):
        """
            closes the main menu
        """
        self.root.destroy()

    def start(self):
        """
            the tk screens
        """
        self.root.mainloop()

    def start_game(self, map_to_load: str):
        """
            startes the game from a file
        :param map_to_load: the path to the level file
        """
        self.root.destroy()
        # TODO LOG logger.info("Start Game")
        map_path = map_to_load
        # TODO LOG logger.info("The map_path to load is " + map_path)

        level = GameMechanics.LevelParser(map_path).get_level()

        # TODO LOG logger.debug("The loaded Level is " + level.__str__())

        new_game = GameMechanics.Game(level)
        # new_game.level = level
        new_game.execute()

    def make_game_saves_widget(self, save_path: str, file: str):
        """
            makes the wigets for the saved games screen
        :param save_path: the path were the sve files are
        :param file: the file name
        """
        b = tkinter.Button(master=self.load_game_sub_frame, text=file[:-5],
                           command=lambda p=save_path: self.start_game(p))
        b.place(x=100, y=self.y_pos)
        self.y_pos += 30


class OptionFrame(tkinter.Frame):
    """
        the options screen as an own class
    """

    def __init__(self, master, game=None):
        self.game = game
        super().__init__(master)
        self.pack(fill=tkinter.BOTH, expand=True)
        create_label(self.pack(), "Volume: ", 50, 50, bg_color=ColorHex.white)
        self.scale_music_vol = tkinter.Scale(self.pack(), length=300, tickinterval=10, from_=0, to=100,
                                             orient=tkinter.HORIZONTAL)
        self.scale_music_vol.set((float(cfg.get_value(cfg.sound_section, cfg.music_volume_option)) * 100))
        self.scale_music_vol.place(x=50, y=70)

        create_label(self.pack(), "Sound effects: ", 50, 150, bg_color=ColorHex.white)
        self.scale_effects_vol = tkinter.Scale(self.pack(), length=300, tickinterval=10, from_=0, to=100,
                                               orient=tkinter.HORIZONTAL)
        self.scale_effects_vol.set((float(cfg.get_value(cfg.sound_section, cfg.sfx_volume_option)) * 100))
        self.scale_effects_vol.place(x=50, y=170)

        create_button(self.pack(), "Save options", self.save_options, 100, 300)

    def save_options(self):
        """
            saves all options
        """
        cfg.set_value(cfg.sound_section, cfg.music_volume_option, str(self.scale_music_vol.get() / 100))
        cfg.set_value(cfg.sound_section, cfg.sfx_volume_option, str(self.scale_effects_vol.get() / 100))

        if self.game is not None:
            self.game.load_settings()


def create_label(screen, text: str, xPos: int, yPos: int, justify="left", bg_color=ColorHex.white, height=1,
                 borderwith=0,
                 relief=None) -> tkinter.Label:
    """

    bg_color:type = ColorHex

    reliefs:     
        FLAT
        RAISED
        SUNKEN
        GROOVE
        RIDGE
    """

    label = tkinter.Label(screen, text=text, justify=justify)
    label["bg"] = bg_color
    label["height"] = height
    label["borderwidth"] = borderwith
    label["relief"] = relief
    label.place(x=xPos, y=yPos)
    return label


def create_button(screen, text: str, command: str, xPos: int, yPos: int, bg_color=None, bd=5) -> tkinter.Button:
    """
    creates a tkinter button

    :param screen:
    :param text:
    :param command:
    :param xPos:
    :param yPos:
    :param bg_color:
    :param bd:
    :return: a tkinter button
    """
    button = tkinter.Button(screen, text=text, command=command)
    button["bg"] = bg_color
    button["bd"] = bd
    button.place(x=xPos, y=yPos)
    return button


class MyImage:
    """
        for the tile screen
    """

    def __init__(self, screen, image_path: str):
        self.img = tkinter.PhotoImage(file=image_path, master=screen)
        self.screen = screen

    def create_image(self, side, height, width, fill=None):
        """
        Creates label with a image as its content
        :param side: where to pack
        :param height: wanted height
        :param width: wanted height
        :param fill: how to fill
        :return: a label with a image as its content
        """
        scale_w = round(width / self.img.width())
        scale_h = round(height / self.img.height())
        self.img = self.img.zoom(scale_w, scale_h)

        label = tkinter.Label(self.screen, image=self.img)
        label.image = self.img  # keep a reference!
        label.pack(side=side, fill=fill)
        return label


class GuiFactoryPack:
    """
        A factory for easy creating tkinter Gui components
    """

    @staticmethod
    def button(text: str, command, master=None):
        """
        creates a tk.Button
        :param text: the text of the button
        :param command: what happens if the button is pressed
        :param master: the root
        :return: a tk.Button
        """
        button = tkinter.Button(master)
        button["text"] = text
        button["command"] = command
        return button

    @staticmethod
    def label(text: str, master=None):
        """
        creates a a tk.Label
        :param text: of the label
        :param master: the root
        :return: a tk.Label
        """
        label = tkinter.Label(master)
        label["text"] = text
        return label
