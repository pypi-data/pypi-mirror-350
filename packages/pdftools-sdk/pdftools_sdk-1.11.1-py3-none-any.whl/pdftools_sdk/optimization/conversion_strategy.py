from ctypes import *
from enum import IntEnum

class ConversionStrategy(IntEnum):
    """
    The conversion strategy for PDF objects



    Attributes:
        COPY (int):
            The object is copied onto the output page.

        FLATTEN (int):
            The object is removed, but its visual appearance is drawn as
            non-editable graphic onto the output page.


    """
    COPY = 1
    FLATTEN = 2

