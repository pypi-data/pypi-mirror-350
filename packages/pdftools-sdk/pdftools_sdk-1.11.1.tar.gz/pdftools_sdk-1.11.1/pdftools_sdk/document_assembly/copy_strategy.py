from ctypes import *
from enum import IntEnum

class CopyStrategy(IntEnum):
    """

    Attributes:
        COPY (int):
            The elements are copied as-is to the output document.

        FLATTEN (int):
            The visual appearance of elements is preserved, but they are not interactive anymore.

        REMOVE (int):
            The elements are removed completely.


    """
    COPY = 1
    FLATTEN = 2
    REMOVE = 3

