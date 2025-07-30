from ctypes import *
from enum import IntEnum

class NameConflictResolution(IntEnum):
    """

    Attributes:
        MERGE (int):
            Elements with the same name are considered the same and are merged if possible.

        RENAME (int):
            Elements with the same name are considered different and the later occurrence is renamed.


    """
    MERGE = 1
    RENAME = 2

