from ctypes import *
from enum import IntEnum

class CompressionAlgorithmSelection(IntEnum):
    """
    The strategy for recompressing images

    The strategy expresses the broad goal when recompressing images.



    Attributes:
        PRESERVE_QUALITY (int):
            The image quality is preserved as far as possible.

        BALANCED (int):
            A compromise between
            :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY` 
            and
            :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.SPEED` .

        SPEED (int):
            Favor fast compression time over image quality.


    """
    PRESERVE_QUALITY = 1
    BALANCED = 2
    SPEED = 3

