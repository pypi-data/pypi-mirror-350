from ctypes import *
from enum import IntEnum

class PngColorSpace(IntEnum):
    """
    The color space used in PNG images



    Attributes:
        RGB (int):
        GRAY (int):

    """
    RGB = 1
    GRAY = 2

