from ctypes import *
from enum import IntEnum

class ColorSpace(IntEnum):
    """
    The color space used in various image formats



    Attributes:
        RGB (int):
        GRAY (int):
        CMYK (int):

    """
    RGB = 1
    GRAY = 2
    CMYK = 3

