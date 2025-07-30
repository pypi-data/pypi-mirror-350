from ctypes import *
from enum import IntEnum

class ErrorCategory(IntEnum):
    """
    The validation error category



    Attributes:
        FORMAT (int):
            The file format (header, trailer, objects, xref, streams) is corrupted.

        PDF (int):
            The document doesn't conform to the PDF reference or PDF/A Specification (missing required entries, wrong value types, etc.).

        ENCRYPTION (int):
            The file is encrypted.

        COLOR (int):
            The document contains device-specific color spaces.

        RENDERING (int):
            The document contains illegal rendering hints (unknown intents, interpolation, transfer and halftone functions).

        ALTERNATE (int):
            The document contains alternate information (images).

        POST_SCRIPT (int):
            The document contains embedded PostScript code.

        EXTERNAL (int):
            The document contains references to external content (reference XObjects, OPI).

        FONT (int):
            The document contains fonts without embedded font programs or encoding information (CMAPs)

        UNICODE (int):
            The document contains fonts without appropriate character to Unicode mapping information (ToUnicode maps)

        TRANSPARENCY (int):
            The document contains transparency.

        UNSUPPORTED_ANNOTATION (int):
            The document contains unknown annotation types.

        MULTIMEDIA (int):
            The document contains multimedia annotations (sound, movies).

        PRINT (int):
            The document contains hidden, invisible, non-viewable or non-printable annotations.

        APPEARANCE (int):
            The document contains annotations or form fields with ambiguous or without appropriate appearances. 

        ACTION (int):
            The document contains actions types other than for navigation (launch, JavaScript, ResetForm, etc.)

        METADATA (int):
            The document's meta data is either missing or inconsistent or corrupt.

        STRUCTURE (int):
            The document doesn't provide appropriate logical structure information.

        OPTIONAL_CONTENT (int):
            The document contains optional content (layers).

        EMBEDDED_FILE (int):
            The document contains embedded files.

        SIGNATURE (int):
            The document contains signatures.

        CUSTOM (int):
            Violations of custom corporate directives.


    """
    FORMAT = 0x00000001
    PDF = 0x00000002
    ENCRYPTION = 0x00000004
    COLOR = 0x00000008
    RENDERING = 0x00000010
    ALTERNATE = 0x00000020
    POST_SCRIPT = 0x00000040
    EXTERNAL = 0x00000080
    FONT = 0x00000100
    UNICODE = 0x00000200
    TRANSPARENCY = 0x00000400
    UNSUPPORTED_ANNOTATION = 0x00000800
    MULTIMEDIA = 0x00001000
    PRINT = 0x00002000
    APPEARANCE = 0x00004000
    ACTION = 0x00008000
    METADATA = 0x00010000
    STRUCTURE = 0x00020000
    OPTIONAL_CONTENT = 0x00040000
    EMBEDDED_FILE = 0x00080000
    SIGNATURE = 0x00100000
    CUSTOM = 0x40000000

