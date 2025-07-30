from ctypes import *
from enum import IntEnum

class InvoiceType(IntEnum):
    """

    Attributes:
        ZUGFERD (int):
            ZUGFeRD (version and profile are determined automatically).

        FACTUR_X (int):
            Factur-X (version and profile are determined automatically).


    """
    ZUGFERD = 1
    FACTUR_X = 2

