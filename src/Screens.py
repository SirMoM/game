import glob
import os

from src import Tiles, Structures, main_game
import tkinter
from src.Utilities import ColorHex


class TileScreen(tkinter.Frame):

    def __init__(self, level, tile: Tiles.Tile):
        self.root = tkinter.Tk()

        self.tile = tile
        self.level = level
        self.is_active = True

        self.root.title(tile.name)
        self.root.geometry("300x400")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        super().__init__(self.root)

        self.pack()

        self.close_button = create_button(self.root, "X", self.close, 145, 375, bg_color=ColorHex.red)
        self.create_things()

    def create_things(self):
        self.tile_img = Image(self.root, self.tile.img_path)
        self.tile_img.create_image(50, 0, 200, 200)

        if self.tile.get_structure():
            structure_str = "Structure: " + self.tile.get_structure().name
            resource_str = "Resources: " + str(
                self.tile.get_structure().resources_per_loop) + " " + self.tile.get_structure().resources_type + " per second"
            create_label(self.root, structure_str, 10, 100)
            create_label(self.root, resource_str, 10, 200)

        create_button(self.root, "Construction Lumber Jack", self.construction_lj, 10, 300)
        create_button(self.root, "Construction Mine", self.construction_mine, 10, 335)

    def close(self):
        self.is_active = False
        self.root.destroy()

    def construction_lj(self):
        tempStructure = Structures.LumberJack()

        previous_structure = self.tile.get_structure()
        if previous_structure is not None and previous_structure in self.level.structures:
            self.level.structures.remove(previous_structure)

        self.tile.set_structure(tempStructure)
        self.level.structures.append(tempStructure)
        self.create_things()

    def construction_mine(self):
        tempStructure = Structures.IronMine()

        previous_structure = self.tile.get_structure()
        if previous_structure is not None and previous_structure in self.level.structures:
            self.level.structures.remove(previous_structure)

        self.tile.set_structure(tempStructure)
        self.level.structures.append(tempStructure)
        self.create_things()


class InGameMenu(tkinter.Frame):
    def __init__(self, game) -> tkinter.Frame:
        self.game = game
        self.is_active = True

        self.root = tkinter.Tk()
        self.root.title("Menu")
        self.root.geometry("300x400+100+100")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        super().__init__(self.root)
        self.pack()

        self.make_widgets()

    def make_widgets(self):
        create_button(self.root, "Resume game", self.close, 100, 100)
        create_button(self.root, "Options", self.options, 100, 150)
        create_button(self.root, "Save Game", self.save_level, 100, 200)
        create_button(self.root, "Main Menu", self.open_main_menu, 100, 250)
        create_button(self.root, "Close game", self.close_game, 100, 300)


    def save_level(self):
        temp_save_menu = SaveMenu(self.game)
        self.game.windows.append(temp_save_menu)
        self.close()

    def close_game(self):
        self.game.close_game()

    def options(self):
        self.close()
        # TODO open the Options Screen

    def close(self):
        self.is_active = False
        self.root.destroy()

    def open_main_menu(self):
        self.close()
        self.game.close_game()

        MainMenu(root=tkinter.Tk())

class SaveMenu(tkinter.Frame):
    forbidden_characters = ['/', '\\', '<', '>', ':', '"', '|', '?', '*', ' ', '.']

    def __init__(self, game) -> tkinter.Frame:
        self.game = game
        self.is_active = True
        self.input_textfield: Textfield = None

        self.root = tkinter.Tk()
        self.root.title("Menu")
        self.root.geometry("250x120")
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        super().__init__(self.root)
        self.pack()

        self.make_widgets()

    def make_widgets(self):
        create_label(self.root, "Name of your Save:", 0, 0)
        self.input_textfield = Textfield(self.root, xPos=0, yPos=60)
        create_button(self.root, "Save", self.save, 0, 80)

    def save(self):
        input_is_valid = True
        self.input_textfield.entry["bg"] = ColorHex.white
        user_input = self.input_textfield.get_user_input()
        for symbol in self.forbidden_characters:
            if symbol in user_input:
                create_label(self.root, '"/", "\\", "<", ">", ":", """, "|", "?", "*", " ", "." \n are not allowed', 0,
                             25, height=2)
                self.input_textfield.mark_false_input(user_input)
                input_is_valid = False

        if input_is_valid:
            main_game.LevelWriter(user_input, self.game.level)
            create_label(self.root, 'Saved', 0, 25, height=2)
            self.close()

    def close(self):
        self.is_active = False
        self.root.destroy()


class MainMenu:
    def __init__(self, root: tkinter.Tk):
        self.root = root
        self.root.title("Main Menu")
        self.root.geometry("400x400")
        self.root.protocol("WM_DELETE_WINDOW", self.close_main_menu)

        self.main_frame = tkinter.Frame(self.root)
        self.main_frame.grid()

        new_game_button = tkinter.Button(master=self.main_frame, text="New game", command=self.launch_new_game)
        new_game_button.grid(row=0, column=0)

        load_game_button = tkinter.Button(master=self.main_frame, text="Load game", command=self.load_game)
        load_game_button.grid(row=1, column=1)

        options_button = tkinter.Button(master=self.main_frame, text="Options", command=self.options)
        options_button.grid(row=2, column=2)

        close_button = tkinter.Button(master=self.main_frame, text="Close", command=self.close_main_menu)
        close_button.grid(row=3, column=3)

    def options(self):
        print("Options")
        self.main_frame.destroy()

    def load_game(self):
        print("Load Game")
        self.main_frame.destroy()

        parent_dir = os.path.dirname(os.getcwd())
        save_folder = os.path.join(parent_dir, "saves")
        os.chdir(save_folder)
        file_paths = []

        self.load_game_sub_frame = tkinter.Frame(self.root).pack()

        y_pos = 100
        for root, dirs, files in os.walk(save_folder):
            for file in files:
                self.increment_button_pos()
                path = os.path.join(root, file).__str__()
                print(path)
                b = tkinter.Button(master=self.load_game_sub_frame, text=file[:-5],
                                   command=lambda p=path: self.start_game(p))
                b.place(x=100, y=y_pos)
                file_paths.append(os.path.join(root, file))
            y_pos += 30

    def launch_new_game(self):
        print("New game")
        self.main_frame.destroy()
        self.new_game_sub_frame = tkinter.Frame(self.root).pack()
        # self.new_game_sub_frame.grid()
        level_1 = "maps/level_1.map"
        level_2 = "maps/level_2.map"

        map_1_button = tkinter.Button(master=self.new_game_sub_frame, text="Map 1",
                                      command=lambda: self.start_game(level_1))
        map_1_button.place(x=100, y=10)

        map_2_button = tkinter.Button(master=self.new_game_sub_frame, text="Map 2",
                                      command=lambda: self.start_game(level_2))
        map_2_button.place(x=100, y=40)

    def close_main_menu(self):
        self.root.destroy()

    def start(self):
        self.root.mainloop()

    def start_game(self, map_to_load: str):
        self.root.destroy()
        map = map_to_load
        print(map)
        level = main_game.LevelParser(map).get_level()
        new_game = main_game.Game()
        new_game.level = level
        new_game.execute()


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


def create_button(screen, text: str, command: str, xPos: int, yPos: int, bg_color=None) -> tkinter.Button:
    button = tkinter.Button(screen, text=text, command=command)
    button["bg"] = bg_color
    button["bd"] = 5
    button.place(x=xPos, y=yPos)
    return button


class Image:
    def __init__(self, screen, image_path: str):
        self.img = tkinter.PhotoImage(file=image_path, name="TEST", master=screen)
        self.screen = screen

    def create_image(self, xPos, yPos, height, width):
        scale_w = round(width / self.img.width())
        scale_h = round(height / self.img.height())
        self.img = self.img.zoom(scale_w, scale_h)

        label = tkinter.Label(self.screen, image=self.img)
        label.image = self.img  # keep a reference!
        label.place(x=xPos, y=yPos)
        return label


class Textfield:
    def __init__(self, screen, xPos, yPos):
        self.entry = tkinter.Entry(screen)
        self.entry.place(x=xPos, y=yPos)

    def get_user_input(self):
        return self.entry.get()

    def mark_false_input(self, text):
        self.entry["bg"] = ColorHex.red
        self.entry.delete(0, len(self.entry.get()))
        self.entry.insert(0, text)
