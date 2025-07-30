from ctypes import *
from enum import IntEnum

class BackgroundType(IntEnum):
    """
    The background type to use when rendering into an image



    Attributes:
        WHITE (int):
            The input PDF content will be rendered on a white background.

        TRANSPARENT (int):
            The input PDF content will be rendered into an image with an
            alpha channel and no background.


    """
    WHITE = 1
    TRANSPARENT = 2

