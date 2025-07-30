from ctypes import *
from enum import IntEnum

class SignatureAlgorithm(IntEnum):
    """
    Cryptographic signature algorithm



    Attributes:
        RSA_RSA (int):
            This is the RSA with PKCS#1 v1.5 algorithm which is widely supported by cryptographic providers.

        RSA_SSA_PSS (int):
            This algorithm is generally recommended because it is considered a more secure alternative to `RSA_RSA`.
            However, it is not supported by all cryptographic providers.

        ECDSA (int):
            This algorithm is generally recommended for new applications.
            However, it is not supported by all cryptographic providers.


    """
    RSA_RSA = 1
    RSA_SSA_PSS = 2
    ECDSA = 3

