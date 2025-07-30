from ctypes import *
from enum import IntEnum

class AddValidationInformation(IntEnum):
    """

    Attributes:
        NONE (int):
            Do not add validation information to any existing signatures of input document.

        LATEST (int):
            Add validation information to latest existing signature of input document.

        ALL (int):
            Add validation information to all existing signatures of input document.


    """
    NONE = 1
    LATEST = 2
    ALL = 3

