from ctypes import *
from enum import IntEnum

class SignatureSelector(IntEnum):
    """
    Select the signatures



    Attributes:
        LATEST (int):
        ALL (int):

    """
    LATEST = 1
    ALL = 2

