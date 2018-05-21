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





