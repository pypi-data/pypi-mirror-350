from ctypes import *
from enum import IntEnum

class RevocationCheckPolicy(IntEnum):
    """
    The revocation check policy



    Attributes:
        REQUIRED (int):
             
            - Certificate must have revocation information (OCSP or CRL)
            - Revocation information is acquired from revocation sources
            - Revocation information is validated
             

        SUPPORTED (int):
            Same as `Required` for certificates that have revocation information and `NoCheck` otherwise.

        OPTIONAL (int):
            Same as `Supported` if revocation information is available in the `RevocationInformationSources` and `NoCheck` otherwise.

        NO_CHECK (int):

    """
    REQUIRED = 1
    SUPPORTED = 2
    OPTIONAL = 3
    NO_CHECK = 4

