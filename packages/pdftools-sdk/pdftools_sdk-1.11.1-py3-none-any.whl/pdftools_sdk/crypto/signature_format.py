from ctypes import *
from enum import IntEnum

class SignatureFormat(IntEnum):
    """

    Attributes:
        ADBE_PKCS7_DETACHED (int):
            Legacy PAdES Basic signature specified by ETSI TS 102 778, Part 2.
            This type can be used for document signatures and certification (MDP) signatures.

        ETSI_CADES_DETACHED (int):
            PAdES signature as specified by European Standard ETSI EN 319 142.
            This type can be used for document signatures and certification (MDP) signatures.


    """
    ADBE_PKCS7_DETACHED = 1
    ETSI_CADES_DETACHED = 2

