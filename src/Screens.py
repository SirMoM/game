import inspect
import os
import sys
import tkinter

from src import Tiles, Game, Structures
from src import config as cfg
from src.Utilities import ColorHex


class TileScreen:

    def __init__(self, level, tile: Tiles.Tile):

        self.level = level
        self.tile = tile
        self.is_active = True

        self.top_level = tkinter.Tk()
        self.top_level.title(tile.name)
        self.top_level.geometry("450x450")
        self.top_level.protocol("WM_DELETE_WINDOW", self.close)

        self.tile_img = MyImage(self.top_level, self.tile.img_path)
        self.tile_img.create_image(tkinter.TOP, 200, 200)

        self.create_overview_frame()

    def close(self):
        self.is_active = False
        self.top_level.destroy()

    def update(self):
        self.top_level.update()

    def create_overview_frame(self):
        abstand = 10

        self.overview_frame = tkinter.Frame(self.top_level)
        # self.overview_frame["bg"] = "red"
        self.overview_frame.pack(fill=tkinter.BOTH, ipady=10, pady=5, expand=True)

        structure_base_str = "Structure: {0}"
        resource_base_str = "Resources: {0:.1f} {1} per second"
        is_in_territory_base_str = "This area is {0} in your Territory"

        if self.tile.structure:
            structure_label = tkinter.Label(self.overview_frame)
            structure_label["text"] = structure_base_str.format(self.tile.structure.name)
            structure_label.pack(side=tkinter.TOP, pady=abstand)

            resource_label = tkinter.Label(self.overview_frame)
            resource_label["text"] = resource_base_str.format(self.tile.structure.resources_per_loop,
                                                              self.tile.structure.resources_type)
            resource_label.pack(side=tkinter.TOP, pady=abstand)

        else:
            structure_label = tkinter.Label(self.overview_frame)
            structure_label["text"] = structure_base_str.format("No building")
            structure_label.pack(side=tkinter.TOP, pady=abstand)

            resource_label = tkinter.Label(self.overview_frame)
            resource_label["text"] = resource_base_str.format(0.0, "resources")
            resource_label.pack(side=tkinter.TOP, pady=abstand)

        if self.tile.is_in_territory:
            territory_label = tkinter.Label(self.overview_frame)
            territory_label["text"] = is_in_territory_base_str.format(self.tile.name, "")
            territory_label.pack(side=tkinter.TOP, pady=abstand)
        else:
            territory_label = tkinter.Label(self.overview_frame)
            territory_label["text"] = is_in_territory_base_str.format("not")
            territory_label.pack(side=tkinter.TOP, pady=abstand)

        construction_button = tkinter.Button(self.overview_frame)
        construction_button["text"] = "Construction"
        construction_button["command"] = self.create_construction_frame
        construction_button.pack(side=tkinter.BOTTOM, pady=abstand)

    def create_construction_frame(self):
        self.overview_frame.destroy()

        self.construction_frame = tkinter.Frame(self.top_level)
        # self.construction_frame["bg"] = "green"
        self.construction_frame.pack(fill=tkinter.BOTH, ipady=10, pady=5, expand=True)

        construction_options = tkinter.Listbox(self.construction_frame, height=5)

        counter = 0
        for option in self.get_construction_options(self.tile):
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

    def back_to_main_frame(self):
        self.construction_frame.destroy()
        self.create_overview_frame()

    def get_construction_options(self, tile):
        all_structures = get_all_structures()
        construction_options = []
        for structure in all_structures:
            if structure.can_build(tile):
                construction_options.append(structure)

        return construction_options

    def build(self, listbox):
        print(listbox.curselection())
        print("Building", listbox.get(listbox.curselection()[0]))


class InGameMenu:
    def __init__(self, game: Game.Game):
        self.game = game
        self.is_active = True
        self.game.pause = True

        self.root = tkinter.Tk()
        self.root.title("Menu")
        self.root.geometry("400x400+100+100")
        self.root.iconbitmap(os.path.join(os.path.dirname(os.getcwd()), "textures/gloria_pause_icon.ico"))
        self.root.protocol("WM_DELETE_WINDOW", self.close)

        self.make_widgets()

    def make_widgets(self):
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


    def save_level(self):
        self.main_frame.destroy()
        self.save_menu = SaveMenu(self.root, self.game)
        back_button = tkinter.Button(master=self.save_menu, text="Back", command=self.back_to_main_frame)
        back_button.pack(side=tkinter.BOTTOM)

    def close_game(self):
        self.close()
        self.game.close()

    def options(self):
        self.main_frame.destroy()
        self.options = OptionFrame(self.root, game=self.game)
        self.options.pack()
        back_button = GuiFactoryPack.button("Back", self.back_to_main_frame, master=self.options)
        back_button.pack(side=tkinter.BOTTOM)

    def close(self):
        self.is_active = False
        self.game.pause = False
        self.root.destroy()

    def open_main_menu(self):
        self.close()
        self.game.close()

        MainMenu(root=tkinter.Tk())

    def update(self):
        self.root.update()

    def back_to_main_frame(self):
        for ele in self.root.winfo_children():
            ele.destroy()

        self.make_widgets()
        self.game.load_settings()


class SaveMenu(tkinter.Frame):
    forbidden_characters = ['/', '\\', '<', '>', ':', '"', '|', '?', '*', ' ', '.']

    def __init__(self, root, game) -> tkinter.Frame:
        self.game = game
        self.is_active = True
        self.input_textfield: Textfield = None

        super().__init__(root)
        self.pack(fill=tkinter.BOTH, expand=True)

        self.make_widgets()

    def make_widgets(self):
        save_label = GuiFactoryPack.label("Name of your Save:", master=self)
        save_label.pack(side=tkinter.TOP, pady=(0, 30))

        self.input_textfield = Textfield(self, side=tkinter.TOP, pad_y=10)

        save_button = GuiFactoryPack.button("Save", self.save, self)
        save_button.pack(side=tkinter.TOP, pady=0)
        print()

    def save(self):
        input_is_valid = True
        self.input_textfield.entry["bg"] = ColorHex.white

        user_input = self.input_textfield.get_user_input()

        for symbol in self.forbidden_characters:
            if symbol in user_input:
                forbidden_symbols_label = GuiFactoryPack.label(
                    '"/", "\\", "<", ">", ":", """, "|", "?", "*", " ", "." \n are not allowed', master=self)
                forbidden_symbols_label.height = 2
                x = 200 - (forbidden_symbols_label["text"].__len__() / 2)
                print(x)
                forbidden_symbols_label.place(x=x / 2, y=20)

                self.input_textfield.mark_false_input(user_input)
                input_is_valid = False

        if input_is_valid:
            Game.LevelWriter(user_input, self.game.level)
            saved_label = GuiFactoryPack.label("Saved", master=self)
            saved_label.height = 2
            saved_label.place(x=180, y=40)

    def close(self):
        self.is_active = False
        self.destroy()


class MainMenu:
    def __init__(self, root: tkinter.Tk):
        self.y_pos = 20
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("400x400")
        self.root.protocol("WM_DELETE_WINDOW", self.close_main_menu)
        self.root.iconbitmap(os.path.join(os.path.dirname(os.getcwd()), "textures/gloria_castle_icon.ico"))
        self.root.attributes("-topmost", True)

        self.main_menu_components()

    def options(self):
        print("Options")
        self.main_frame.destroy()
        self.option_frame = OptionFrame(self.root)
        create_button(self.option_frame.pack(), "Back", self.back_to_myself, 200, 300)
        self.option_frame.pack()

    def back_to_myself(self):
        for ele in self.root.winfo_children():
            ele.destroy()

        self.main_menu_components()

    def main_menu_components(self):
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
        print("Load Game")
        self.main_frame.destroy()

        parent_dir = os.path.dirname(os.getcwd())
        save_folder = os.path.join(parent_dir, "saves")
        os.chdir(save_folder)

        self.load_game_sub_frame = tkinter.Frame(self.root).pack()

        for root, dirs, files in os.walk(save_folder):
            for file in files:
                path = os.path.join(root, file).__str__()
                print(path)
                self.make_game_saves_widget(path, file)

        create_button(self.load_game_sub_frame, "Back", self.back_to_myself, 200, 300)

    def new_game(self):
        print("New game")
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
        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def start_game(self, map_to_load: str):
        self.root.destroy()
        map = map_to_load
        print(map)
        level = Game.LevelParser(map).get_level()
        new_game = Game.Game()
        new_game.level = level
        new_game.execute()

    def make_game_saves_widget(self, save_path, file):
        b = tkinter.Button(master=self.load_game_sub_frame, text=file[:-5],
                           command=lambda p=save_path: self.start_game(p))
        b.place(x=100, y=self.y_pos)
        self.y_pos += 30


class OptionFrame(tkinter.Frame):
    def __init__(self, master, game=None):
        self.game = game
        super().__init__(master)
        self.pack(fill=tkinter.BOTH, expand=True)
        create_label(self.pack(), "Volume: ", 50, 100, bg_color=ColorHex.white)
        self.scale = tkinter.Scale(self.pack(), length=300, tickinterval=10, from_=0, to=100, orient=tkinter.HORIZONTAL)
        self.scale.set((float(cfg.get_value(cfg.sound_section, cfg.music_volume_option)) * 100))
        self.scale.place(x=50, y=120)

        create_button(self.pack(), "Save options", self.save_options, 100, 300)

    def save_options(self):
        cfg.set_value(cfg.sound_section, cfg.music_volume_option, str(self.scale.get() / 100))
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
    button = tkinter.Button(screen, text=text, command=command)
    button["bg"] = bg_color
    button["bd"] = bd
    button.place(x=xPos, y=yPos)
    return button


class MyImage:
    def __init__(self, screen, image_path: str):
        self.img = tkinter.PhotoImage(file=image_path, master=screen)
        self.screen = screen

    def create_image(self, side, height, width, fill=None):
        scale_w = round(width / self.img.width())
        scale_h = round(height / self.img.height())
        self.img = self.img.zoom(scale_w, scale_h)

        label = tkinter.Label(self.screen, image=self.img)
        label.image = self.img  # keep a reference!
        label.pack(side=side, fill=fill)
        return label


class Textfield:
    def __init__(self, screen, side=None, pad_y=None, pad_x=None):
        self.entry = tkinter.Entry(screen)
        self.entry.pack(side=side, pady=pad_y, padx=pad_x)

    def get_user_input(self):
        return self.entry.get()

    def mark_false_input(self, text):
        self.entry["bg"] = ColorHex.red
        self.entry.delete(0, len(self.entry.get()))
        self.entry.insert(0, text)


def get_all_structures():
    structures = []
    for name, obj in inspect.getmembers(sys.modules[Structures.__name__]):
        if inspect.isclass(obj):
            structures.append(obj)

    return structures


class GuiFactoryPack:

    @staticmethod
    def button(text: str, command, master=None):
        button = tkinter.Button(master)
        button["text"] = text
        button["command"] = command
        return button

    @staticmethod
    def label(text: str, master=None):
        label = tkinter.Label(master)
        label["text"] = text
        return label
