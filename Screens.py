import tkinter
from Utilities import ColorHex


class TileScreen(tkinter.Frame):

    def __init__(self, tile):
        self.root = tkinter.Tk()
        print("New TileScreen")
        self.root.title(tile.name)
        self.root.geometry("300x400")
        super().__init__(self.root)
        self.pack()
        self.close_button = create_button(self.root, "X", self.close, 275, 0, bg_color=ColorHex.red)
        self.is_active = True

    def close(self):
        self.is_active = False
        self.root.destroy()


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
