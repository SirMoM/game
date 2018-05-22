import tkinter


class Screen(tkinter.Frame):
    def __init__(self):
        self.root = tkinter.Tk()  # Create a background window
        super().__init__(self.root)
        self.pack()
        self.create_widgets()
        self.root.mainloop(1)

    def create_widgets(self):
        self.hi_there = tkinter.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tkinter.Button(self, text="QUIT", fg="red", command=self.root.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")


class TileScreen(tkinter.Frame):
    root = tkinter.Tk()

    def __init__(self, tile):
        self.root.title(tile.name)
        self.root.geometry("300x400")
        super().__init__(self.root)
        self.pack()
        self.hi_there = tkinter.Button(self)
        self.hi_there.place(x=100, y=100)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack()
        self.root.mainloop()
        print("New TileScreen")

    def say_hi(self):
        print("hi there, everyone!")


class ColorHex:
    def __init__(self):
        print("This is a Utility Class DO NOT create a Object")

    black = "#000000"
    white = "#FFFFFF"
    red = "#FF0000"
    Lime = "#00FF00"
    blue = "#0000FF"
    purple = "#800080"
    grey = "#bbbbbb"


def create_label(screen, text, xPos, yPos, bg_color=ColorHex.white, height=1, borderwith=1, relief=None):
    # "raised"
    lb = tkinter.Label(screen, text=text)
    lb["bg"] = bg_color
    lb["height"] = height
    lb["width"] = len(lb["text"])
    lb["borderwidth"] = borderwith
    lb["relief"] = relief
    lb.place(x=xPos, y=yPos)
    return lb


def create_button(screen, text, command, xPos, yPos, bg_color=None):
    button = tkinter.Button(screen, text=text, command=command)
    button["bg"] = bg_color
    button["bd"] = 5
    button.place(x=xPos, y=yPos)
    return button
