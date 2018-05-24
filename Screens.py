import Structures
import Tiles
import tkinter
from Utilities import ColorHex


class TileScreen(tkinter.Frame):

    def __init__(self, level, tile: Tiles.Tile):
        self.tile = tile
        self.level = level
        self.is_active = True
        self.root = tkinter.Tk()
        print("New TileScreen")
        self.root.title(tile.name)
        self.root.geometry("300x400")
        super().__init__(self.root)
        self.pack()
        self.close_button = create_button(self.root, "X", self.close, 275, 0, bg_color=ColorHex.red)

        self.create_things()

    def create_things(self):
        if self.tile.get_structure():
            structure_str = "Structure: " + self.tile.get_structure().name
            resource_str = "Resources: " + str(
                self.tile.get_structure().resources_per_loop) + " " + self.tile.get_structure().resources_type + " per second"
            create_label(self.root, structure_str, 10, 100)
            create_label(self.root, resource_str, 10, 200)
        else:
            create_button(self.root, "Construction", self.construction, 10, 300)

    def close(self):
        self.is_active = False
        self.root.destroy()

    def construction(self):
        tempStructure = Structures.LumberJack()
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


def create_button(screen, text: str, command: str, xPos: int, yPos: int, bg_color=None):
    button = tkinter.Button(screen, text=text, command=command)
    button["bg"] = bg_color
    button["bd"] = 5
    button.place(x=xPos, y=yPos)
    return button
