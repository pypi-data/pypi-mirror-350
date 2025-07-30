from ctypes import *
from enum import IntEnum

class HashAlgorithm(IntEnum):
    """

    Attributes:
        MD5 (int):
            This algorithm is considered broken and therefore strongly discouraged by the cryptographic community.

        RIPE_MD160 (int):
        SHA1 (int):
            This algorithm is considered broken and therefore strongly discouraged by the cryptographic community.

        SHA256 (int):
        SHA384 (int):
        SHA512 (int):
        SHA3_256 (int):
            `SHA3-256` is a new hashing algorithm and may not be supported by some applications.

        SHA3_384 (int):
            `SHA3-384` is a new hashing algorithm and may not be supported by some applications.

        SHA3_512 (int):
            `SHA3-512` is a new hashing algorithm and may not be supported by some applications.


    """
    MD5 = 1
    RIPE_MD160 = 2
    SHA1 = 3
    SHA256 = 4
    SHA384 = 5
    SHA512 = 6
    SHA3_256 = 7
    SHA3_384 = 8
    SHA3_512 = 9

