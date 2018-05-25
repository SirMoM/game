from src import Tiles, Structures
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
        self.tile_img.create_image(50, 0, 200, 200, 32)

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


def create_label(screen, text: str, xPos: int, yPos: int, bg_color=ColorHex.white, height=1, borderwith=1,
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

    label = tkinter.Label(screen, text=text)
    label["bg"] = bg_color
    label["height"] = height
    label["width"] = len(label["text"])
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

    def create_image(self, xPos, yPos, height, width, img_size):
        scale_w = round(width / self.img.width())
        scale_h = round(height / self.img.height())
        self.img = self.img.zoom(scale_w, scale_h)

        label = tkinter.Label(self.screen, image=self.img)
        # label.image = self.img  # keep a reference!
        label.place(x=xPos, y=yPos)
        return label
