from ctypes import *
from enum import IntEnum

class AFRelationship(IntEnum):
    """
    The AFRelationship determines the relation of the embedded file to the PDF.



    Attributes:
        SOURCE (int):
            The file specification is the original source material for the associated content.

        DATA (int):
            The file specification represents information used to derive a visual presentation – such as for a table or a graph.

        ALTERNATIVE (int):
            The file specification is an alternative representation of content, for example audio

        SUPPLEMENT (int):
            The file specification represents a supplemental representation of the original source or data that may be more easily consumable.

        UNSPECIFIED (int):
            The relationship is not known or cannot be described using one of the other values.


    """
    SOURCE = 1
    DATA = 2
    ALTERNATIVE = 3
    SUPPLEMENT = 4
    UNSPECIFIED = 5

