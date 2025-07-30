from ctypes import *
from enum import IntEnum

class FaxVerticalResolution(IntEnum):
    """
    The vertical resolution of Fax images

    The two resolutions available in Fax images.



    Attributes:
        STANDARD (int):
        HIGH (int):

    """
    STANDARD = 1
    HIGH = 2

