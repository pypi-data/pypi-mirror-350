from ctypes import *
from enum import IntEnum

class RemovalStrategy(IntEnum):
    """

    Attributes:
        FLATTEN (int):
            The visual appearance of elements is preserved, but they are not interactive anymore.

        REMOVE (int):
            The elements are removed completely.


    """
    FLATTEN = 1
    REMOVE = 2

