"""
This module is just a little helper.

Import
------
    ClassVar
        used for type hinting
    Tuple
        used for type hinting
"""
from typing import ClassVar, Tuple


class ColorHex:
    """
        Some Colors in Hexadecimal as Strings

        Attributes
        ----------
            black: str
                the color black as an hex-string
            white: str
                the color white as an hex-string
            red: str
                the color red as an hex-string
            lime: str
                the color lime as an hex-string
            blue: str
                the color blue as an hex-string
            purple: str
                the color purple as an hex-string
            grey: str
                the color grey as an hex-string
    """

    def __init__(self):
        print("This is a Utility Class DO NOT create a Object")

    black: ClassVar[str] = "#000000"
    white: ClassVar[str] = "#FFFFFF"
    red: ClassVar[str] = "#FF0000"
    lime: ClassVar[str] = "#00FF00"
    blue: ClassVar[str] = "#0000FF"
    purple: ClassVar[str] = "#800080"
    grey: ClassVar[str] = "#bbbbbb"


class ColorRGB:
    """
        Some Colors in RGB as tuples

        Attributes
        ----------
            black: tuple
                the color black as an RGB-tuple
            white: tuple
                the color white as an RGB-tuple
            red: tuple
                the color red as an RGB-tuple
            lime: tuple
                the color lime as an RGB-tuple
            blue: tuple
                the color blue as an RGB-tuple
            purple: tuple
                the color purple as an RGB-tuple
            grey: tuple
                the color grey as an RGB-tuple
    """

    def __init__(self):
        print("This is a Utility Class DO NOT create a Object")

    black: ClassVar[Tuple[int, int, int]] = (0, 0, 0)
    white: ClassVar[Tuple[int, int, int]] = (255, 255, 255)
    red: ClassVar[Tuple[int, int, int]] = (255, 0, 0)
    green: ClassVar[Tuple[int, int, int]] = (0, 255, 0)
    blue: ClassVar[Tuple[int, int, int]] = (0, 0, 255)
    purple: ClassVar[Tuple[int, int, int]] = (150, 43, 186)
    grey: ClassVar[Tuple[int, int, int]] = (150, 150, 150)
