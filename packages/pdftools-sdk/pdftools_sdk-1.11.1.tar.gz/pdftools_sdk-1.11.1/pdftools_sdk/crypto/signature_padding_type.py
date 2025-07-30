from ctypes import *
from enum import IntEnum

class SignaturePaddingType(IntEnum):
    """
    Padding scheme of the cryptographic signature algorithm

    The signature algorithm is defined by the signing certificate's key type.
    For example, RSA or ECDSA.
    For some keys, e.g. RSA keys, there are different padding algorithms.
    Some cryptographic providers let you set this padding algorithm.
    However, this only has an effect on signatures created by the cryptographic provider itself.
    All signed data acquired from external sources may use other signing algorithms;
    more specifically, the issuer certificates of the trust chain, the time-stamp’s signature, 
    or those used for the revocation information (CRL, OCSP).
    It is recommended to verify that the algorithms of all signatures provide a similar level of security.



    Attributes:
        DEFAULT (int):
            The default padding scheme.
            Used for the :attr:`pdftools_sdk.crypto.signature_algorithm.SignatureAlgorithm.ECDSA`  signature algorithm.

        RSA_RSA (int):
            Padding scheme for RSA keys that corresponds to the :attr:`pdftools_sdk.crypto.signature_algorithm.SignatureAlgorithm.RSARSA`  signature algorithm.

        RSA_SSA_PSS (int):
            Padding scheme for RSA keys that corresponds to the :attr:`pdftools_sdk.crypto.signature_algorithm.SignatureAlgorithm.RSASSAPSS`  signature algorithm.


    """
    DEFAULT = 0
    RSA_RSA = 1
    RSA_SSA_PSS = 2

