from ctypes import *
from enum import IntEnum

class WarningCategory(IntEnum):
    """
    The warning category

    The category of the warning of :func:`pdftools_sdk.sign.signer.WarningFunc` .



    Attributes:
        PDF_A_REMOVED (int):
            PDF/A conformance of input file removed due to file encryption (i.e. :attr:`pdftools_sdk.pdf.output_options.OutputOptions.encryption`  is not `None`).
            Removal of PDF/A conformance is necessary, because encryption is not allowed by the PDF/A standard.

        SIGNED_DOC_ENCRYPTION_UNCHANGED (int):
             
            When processing signed documents, their encryption parameters (user password, owner password, permissions) cannot be changed.
            Therefore, the property :attr:`pdftools_sdk.pdf.output_options.OutputOptions.encryption`  has no effect.
             
            This warning is generated so that the following situations can be detected:
             
            - If :attr:`pdftools_sdk.pdf.output_options.OutputOptions.encryption`  is `None` and the input document is encrypted.
              The output document is also encrypted.
            - If :attr:`pdftools_sdk.pdf.output_options.OutputOptions.encryption`  not `None` and the input document is encrypted using different encryption parameters.
              The output document is also encrypted, preserving the encryption parameters of the input document.
            - If :attr:`pdftools_sdk.pdf.output_options.OutputOptions.encryption`  not `None` and the input document is not encrypted.
              The output document is not encrypted.
             
             
            Encryption parameters of signed documents can be changed by removing all existing signatures using the property :attr:`pdftools_sdk.sign.output_options.OutputOptions.remove_signatures` .
            In this case, this warning is not generated.

        ADD_VALIDATION_INFORMATION_FAILED (int):
             
            Error adding validation information to existing signatures of input document as requested by
            :attr:`pdftools_sdk.sign.output_options.OutputOptions.add_validation_information` .
            The warning's `context` contains a description of the affected signature.
             
            Potential causes of this warning are:
             
            - *Missing issuer certificate:*
              All certificates of the trust chain are required to add validation information.
              Preferably, the certificates should be present in the cryptographic provider's certificate store.
              Alternatively, if supported by the certificate,
              the issuer certificate is downloaded from the certificate authority's server and
              stored in the user's `Certificates` directory (see :class:`pdftools_sdk.crypto.providers.built_in.provider.Provider` ).
            - *Network problem:*
              The network must allow OCSP and CRL responses to be downloaded from the certificate authority's server.
              Make sure your proxy configuration (see :attr:`pdftools_sdk.sdk.Sdk.proxy` ) is correct.
             


    """
    PDF_A_REMOVED = 1
    SIGNED_DOC_ENCRYPTION_UNCHANGED = 2
    ADD_VALIDATION_INFORMATION_FAILED = 3

