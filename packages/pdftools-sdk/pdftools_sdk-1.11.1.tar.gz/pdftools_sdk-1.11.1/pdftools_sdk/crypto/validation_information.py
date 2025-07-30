from ctypes import *
from enum import IntEnum

class ValidationInformation(IntEnum):
    """
    Whether to embed validation information to enable the long-term validation (LTV) of the signature

     
    Embed revocation information such as online certificate status response (OCSP - RFC2560) and certificate revocation lists (CRL - RFC3280).
    Revocation information of a certificate is provided by a validation service at the time of signing and acts as proof that the certificate
    was valid at the time of signing.
    This is useful because even when the certificate expires or is revoked at a later time, the signature in the signed document remains valid.
     
    Embedding revocation information is optional but suggested when applying advanced or qualified electronic signatures.
    This feature is not always available.
    It has to be supported by the signing certificate and the cryptographic provider.
    Also, it is not supported by document time-stamp signatures.
    For these cases, a subsequent invocation of :meth:`pdftools_sdk.sign.signer.Signer.process`  with
    :attr:`pdftools_sdk.sign.output_options.OutputOptions.add_validation_information` 
    is required.
     
    Revocation information is embedded for the signing certificate and all certificates of its trust chain.
    This implies that both OCSP responses and CRLs can be present in the same message.
    The disadvantages of embedding revocation information are the increase of the file size (normally by around 20KB),
    and that it requires a web request to a validation service, which delays the process of signing.
    Embedding revocation information requires an online connection to the CA that issues them.
    The firewall must be configured accordingly.
    If a web proxy is used (see :attr:`pdftools_sdk.sdk.Sdk.proxy` ), make sure the following MIME types are supported:
     
    - `application/ocsp-request`
    - `application/ocsp-response`
     



    Attributes:
        NONE (int):
        EMBED_IN_SIGNATURE (int):
            This is only possible for Legacy PAdES Basic signatures (signature format :attr:`pdftools_sdk.crypto.signature_format.SignatureFormat.ADBEPKCS7DETACHED` ).

        EMBED_IN_DOCUMENT (int):
             
            Embedding validation information into the document security store (DSS) is recommended,
            because it creates smaller files and is supported for all signature formats.
             
            The document security store has been standardized in 2009 by the standard for PAdES-LTV Profiles (ETSI TS 102 778-4).
            Therefore, some legacy signature validation software may not support this.
            For these cases, it is necessary to use `EmbedInSignature`.


    """
    NONE = 0
    EMBED_IN_SIGNATURE = 1
    EMBED_IN_DOCUMENT = 2

