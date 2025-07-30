from ctypes import *
from enum import IntEnum

class TextExtractionFormat(IntEnum):
    """

    Attributes:
        DOCUMENT_ORDER (int):
            Text is extracted in the order how it is embedded in the PDF.

        MONOSPACE (int):
            The extracted monospaced text mimics the layout of the page by use of whitespaces.


    """
    DOCUMENT_ORDER = 1
    MONOSPACE = 2

