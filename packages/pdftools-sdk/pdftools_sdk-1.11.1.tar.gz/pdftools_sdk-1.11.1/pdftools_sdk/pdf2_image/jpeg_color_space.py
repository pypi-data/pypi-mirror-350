from ctypes import *
from enum import IntEnum

class JpegColorSpace(IntEnum):
    """
    The color space used in JPEG images



    Attributes:
        RGB (int):
        GRAY (int):
        CMYK (int):

    """
    RGB = 1
    GRAY = 2
    CMYK = 3

