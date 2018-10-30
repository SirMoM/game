#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
This module is the starting point

Import
------
    tkinter
        used to create windows
    Screens
        used to create the main-menu
"""

from tkinter import Tk

from src.Screens import MainMenu

if __name__ == '__main__':
    root: Tk = Tk()
    mm: MainMenu = MainMenu(root)
    mm.start()
