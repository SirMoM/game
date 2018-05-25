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
        if previous_structure is not None:
            self.level.structures.remove(previous_structure)

        self.tile.set_structure(tempStructure)
        self.level.structures.append(tempStructure)
        self.create_things()

    def construction_mine(self):
        tempStructure = Structures.IronMine()

        previous_structure = self.tile.get_structure()
        if previous_structure is not None:
            self.level.structures.remove(previous_structure)

        self.tile.set_structure(tempStructure)
        self.level.structures.append(tempStructure)
        self.create_things()


class InGameMenu(tkinter.Frame):
    def __init__(self, game: main_game.Game) -> tkinter.Frame:
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
        create_button(self.root, "Close game", self.close_game, 100, 250)

    def save_level(self):
        temp_save_Menu = SaveMenu(self.game)
        self.game.windows.append(temp_save_Menu)
        self.close()

    def close_game(self):
        self.game.running = False

    def options(self):
        self.close()
        # TODO open the Options Screen

    def close(self):
        self.is_active = False
        self.root.destroy()


class SaveMenu(tkinter.Frame):
    forbidden_characters = ['/', '\\', '<', '>', ':', '"', '|', '?', '*', ' ', '.']

    def __init__(self, game: main_game.Game) -> tkinter.Frame:
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
            main_game.LevelWriter(user_input)

    def close(self):
        self.is_active = False
        self.root.destroy()


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
