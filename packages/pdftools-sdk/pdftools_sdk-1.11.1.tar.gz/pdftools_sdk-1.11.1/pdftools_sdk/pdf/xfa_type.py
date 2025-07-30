from ctypes import *
from enum import IntEnum

class XfaType(IntEnum):
    """
    The XFA type of a PDF document

    See :attr:`pdftools_sdk.pdf.document.Document.xfa`  to get the XFA type of a PDF document.



    Attributes:
        NO_XFA (int):
            The document is not an XFA document but a regular PDF document.

        XFA_NEEDS_RENDERING (int):
            The document is an XFA document.
            The document cannot be processed by many components, so it is recommended to convert it to a PDF document beforehand.

        XFA_RENDERED (int):
            The document is a "rendered" XFA document where the PDF pages' content has been generated from the XFA form.
            Such documents can be processed as regular PDF documents.
            However, there is no guarantee that the generated pages accurately reflect the XFA document.


    """
    NO_XFA = 0
    XFA_NEEDS_RENDERING = 1
    XFA_RENDERED = 2

