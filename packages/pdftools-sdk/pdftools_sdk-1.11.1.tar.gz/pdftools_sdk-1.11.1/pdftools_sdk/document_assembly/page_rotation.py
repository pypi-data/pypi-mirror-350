from ctypes import *
from enum import IntEnum

class PageRotation(IntEnum):
    """

    Attributes:
        NO_ROTATION (int):
            No rotation is applied.

        CLOCKWISE90 (int):
            Rotation for 90 degrees clockwise.

        CLOCKWISE180 (int):
            Rotation for 180 degrees clockwise.

        CLOCKWISE270 (int):
            Rotation for 270 degrees clockwise.


    """
    NO_ROTATION = 0
    CLOCKWISE90 = 1
    CLOCKWISE180 = 2
    CLOCKWISE270 = 3

