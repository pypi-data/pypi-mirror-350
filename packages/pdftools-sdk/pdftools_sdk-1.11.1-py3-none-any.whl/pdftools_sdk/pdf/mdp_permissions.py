from ctypes import *
from enum import IntEnum

class MdpPermissions(IntEnum):
    """

    Attributes:
        NO_CHANGES (int):
            No changes to the document shall be permitted;
            any change to the document invalidates the signature.

        FORM_FILLING (int):
            Permitted changes are filling in forms, instantiating page templates, and signing;
            other changes invalidate the signature.

        ANNOTATE (int):
            Permitted changes are the same as for :attr:`pdftools_sdk.pdf.mdp_permissions.MdpPermissions.FORMFILLING` ,
            as well as annotation creation, deletion, and modification;
            other changes invalidate the signature.


    """
    NO_CHANGES = 1
    FORM_FILLING = 2
    ANNOTATE = 3

