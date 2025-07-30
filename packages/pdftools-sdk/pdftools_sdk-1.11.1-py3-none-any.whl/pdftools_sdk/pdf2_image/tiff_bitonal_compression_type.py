from ctypes import *
from enum import IntEnum

class TiffBitonalCompressionType(IntEnum):
    """
    The compression type for bitonal (Fax) TIFF images



    Attributes:
        G3 (int):
            CCITT Group 3 is the predecessor to CCITT Group 4, it is a simpler
            algorithm that normally results in a lower compression ratio.

        G4 (int):
            CCITT Group 4 is the standard compression for bitonal TIFF images
            (i.e. facsimile).


    """
    G3 = 1
    G4 = 2

