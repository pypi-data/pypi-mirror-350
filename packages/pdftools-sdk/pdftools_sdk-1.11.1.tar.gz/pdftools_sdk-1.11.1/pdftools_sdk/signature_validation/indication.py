from ctypes import *
from enum import IntEnum

class Indication(IntEnum):
    """
    Main status indication of the signature validation process

    See ETSI TS 102 853 and ETSI EN 319 102-1.



    Attributes:
        VALID (int):
        INVALID (int):
        INDETERMINATE (int):

    """
    VALID = 1
    INVALID = 2
    INDETERMINATE = 3

