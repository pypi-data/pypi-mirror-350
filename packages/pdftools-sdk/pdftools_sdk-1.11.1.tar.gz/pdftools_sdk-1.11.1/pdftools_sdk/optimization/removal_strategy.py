from ctypes import *
from enum import IntEnum

class RemovalStrategy(IntEnum):
    """
    The removal strategy for PDF objects



    Attributes:
        FLATTEN (int):
            The object is removed, but its visual appearance is drawn as
            non-editable graphic onto the output page.

        REMOVE (int):
            The object is removed together with its visual appearance.


    """
    FLATTEN = 2
    REMOVE = 3

