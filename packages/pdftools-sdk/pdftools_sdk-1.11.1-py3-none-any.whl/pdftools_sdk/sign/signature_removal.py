from ctypes import *
from enum import IntEnum

class SignatureRemoval(IntEnum):
    """

    Attributes:
        NONE (int):
            Do not remove any signatures.

        SIGNED (int):
             
            Remove all signed signatures, but no unsigned signature fields.
            This lets you change the encryption parameters of signed input documents, e.g. to encrypt or decrypt them (see :attr:`pdftools_sdk.sign.warning_category.WarningCategory.SIGNEDDOCENCRYPTIONUNCHANGED` ).
             
            While the cryptographic parts of the signatures are removed, their visual appearances are preserved.

        ALL (int):
            Remove all signed (see :attr:`pdftools_sdk.sign.signature_removal.SignatureRemoval.SIGNED` ) and unsigned signature fields.


    """
    NONE = 1
    SIGNED = 2
    ALL = 3

