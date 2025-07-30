from __future__ import annotations
import io
from typing import List, Iterator, Tuple, Optional, Any, TYPE_CHECKING, Callable
from ctypes import *
from datetime import datetime
from numbers import Number
from pdftools_sdk.internal import _lib
from pdftools_sdk.internal.utils import _string_to_utf16, _utf16_to_string
from pdftools_sdk.internal.streams import _StreamDescriptor, _NativeStream
from pdftools_sdk.internal.native_base import _NativeBase
from pdftools_sdk.internal.native_object import _NativeObject

import pdftools_sdk.internal
import pdftools_sdk.pdf.output_options

if TYPE_CHECKING:
    from pdftools_sdk.sign.signature_removal import SignatureRemoval
    from pdftools_sdk.sign.add_validation_information import AddValidationInformation

else:
    SignatureRemoval = "pdftools_sdk.sign.signature_removal.SignatureRemoval"
    AddValidationInformation = "pdftools_sdk.sign.add_validation_information.AddValidationInformation"


class OutputOptions(pdftools_sdk.pdf.output_options.OutputOptions):
    """
    Additional document level options

     
    These options are available for all signature operations of the :class:`pdftools_sdk.sign.signer.Signer` .
    They can also be used without a signature operation with the method :meth:`pdftools_sdk.sign.signer.Signer.process` .
     
    Notes on document encryption when processing files with the :class:`pdftools_sdk.sign.signer.Signer` :
     
    - PDF/A conformance is removed from input files.
      In this case, a :func:`pdftools_sdk.sign.signer.WarningFunc`  with an :attr:`pdftools_sdk.sign.warning_category.WarningCategory.PDFAREMOVED`  is generated.
    - Signed documents cannot be encrypted or decrypted.
      In this case, a :func:`pdftools_sdk.sign.signer.WarningFunc`  with an :attr:`pdftools_sdk.sign.warning_category.WarningCategory.SIGNEDDOCENCRYPTIONUNCHANGED`  is generated.
     


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsSign_OutputOptions_New.argtypes = []
        _lib.PdfToolsSign_OutputOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsSign_OutputOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def remove_signatures(self) -> SignatureRemoval:
        """
        Whether to remove any signatures

         
        By default, all signatures of the input document are preserved.
        Optionally, some or all of them can be removed.
         
        Default is :attr:`pdftools_sdk.sign.signature_removal.SignatureRemoval.NONE` 



        Returns:
            pdftools_sdk.sign.signature_removal.SignatureRemoval

        """
        from pdftools_sdk.sign.signature_removal import SignatureRemoval

        _lib.PdfToolsSign_OutputOptions_GetRemoveSignatures.argtypes = [c_void_p]
        _lib.PdfToolsSign_OutputOptions_GetRemoveSignatures.restype = c_int
        ret_val = _lib.PdfToolsSign_OutputOptions_GetRemoveSignatures(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return SignatureRemoval(ret_val)



    @remove_signatures.setter
    def remove_signatures(self, val: SignatureRemoval) -> None:
        """
        Whether to remove any signatures

         
        By default, all signatures of the input document are preserved.
        Optionally, some or all of them can be removed.
         
        Default is :attr:`pdftools_sdk.sign.signature_removal.SignatureRemoval.NONE` 



        Args:
            val (pdftools_sdk.sign.signature_removal.SignatureRemoval):
                property value

        """
        from pdftools_sdk.sign.signature_removal import SignatureRemoval

        if not isinstance(val, SignatureRemoval):
            raise TypeError(f"Expected type {SignatureRemoval.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSign_OutputOptions_SetRemoveSignatures.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSign_OutputOptions_SetRemoveSignatures.restype = c_bool
        if not _lib.PdfToolsSign_OutputOptions_SetRemoveSignatures(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def add_validation_information(self) -> AddValidationInformation:
        """
        Add validation information to existing signatures of input document

         
        Add signature validation information to the document security store (DSS).
        This information includes:
         
        - All certificates of the signing certificate’s trust chain, unless they are already embedded into the signature.
        - Revocation data (OCSP or CRL) for all certificates that support revocation information.
         
        This method can be used to create signatures with long-term validation material or to enlarge the longevity of existing signatures.
        For more details on validation information, see also :class:`pdftools_sdk.crypto.validation_information.ValidationInformation` .
         
        Validation information for embedded time-stamp tokens is added as well.
         
        If adding validation information fails, an :func:`pdftools_sdk.sign.signer.WarningFunc`  with an
        :attr:`pdftools_sdk.sign.warning_category.WarningCategory.ADDVALIDATIONINFORMATIONFAILED`  is generated.
         
        All types of cryptographic providers support this method.
        However, this method fails when using a provider whose certificate store is missing a required certificate.
         
        *Note:*
        This property has no effect on any new signatures or time-stamp that may also be added.
        The validation information of signatures and time-stamps is controlled by the respective property in the signature or time-stamp configuration object.
         
        *Note:*
        This method does not validate the signatures, but only downloads the information required.
         
        *Note:*
        Adding validation information for expired certificates is not possible.
        Therefore, it is crucial to enlarge the longevity of signatures before they expire.
         
        *Note:*
        Adding validation information to document certification (MDP) signatures is not possible,
        because it would break the signature.
        Validation information must be added to certification signatures when creating them.
         
        Default is :attr:`pdftools_sdk.sign.add_validation_information.AddValidationInformation.NONE` 



        Returns:
            pdftools_sdk.sign.add_validation_information.AddValidationInformation

        """
        from pdftools_sdk.sign.add_validation_information import AddValidationInformation

        _lib.PdfToolsSign_OutputOptions_GetAddValidationInformation.argtypes = [c_void_p]
        _lib.PdfToolsSign_OutputOptions_GetAddValidationInformation.restype = c_int
        ret_val = _lib.PdfToolsSign_OutputOptions_GetAddValidationInformation(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return AddValidationInformation(ret_val)



    @add_validation_information.setter
    def add_validation_information(self, val: AddValidationInformation) -> None:
        """
        Add validation information to existing signatures of input document

         
        Add signature validation information to the document security store (DSS).
        This information includes:
         
        - All certificates of the signing certificate’s trust chain, unless they are already embedded into the signature.
        - Revocation data (OCSP or CRL) for all certificates that support revocation information.
         
        This method can be used to create signatures with long-term validation material or to enlarge the longevity of existing signatures.
        For more details on validation information, see also :class:`pdftools_sdk.crypto.validation_information.ValidationInformation` .
         
        Validation information for embedded time-stamp tokens is added as well.
         
        If adding validation information fails, an :func:`pdftools_sdk.sign.signer.WarningFunc`  with an
        :attr:`pdftools_sdk.sign.warning_category.WarningCategory.ADDVALIDATIONINFORMATIONFAILED`  is generated.
         
        All types of cryptographic providers support this method.
        However, this method fails when using a provider whose certificate store is missing a required certificate.
         
        *Note:*
        This property has no effect on any new signatures or time-stamp that may also be added.
        The validation information of signatures and time-stamps is controlled by the respective property in the signature or time-stamp configuration object.
         
        *Note:*
        This method does not validate the signatures, but only downloads the information required.
         
        *Note:*
        Adding validation information for expired certificates is not possible.
        Therefore, it is crucial to enlarge the longevity of signatures before they expire.
         
        *Note:*
        Adding validation information to document certification (MDP) signatures is not possible,
        because it would break the signature.
        Validation information must be added to certification signatures when creating them.
         
        Default is :attr:`pdftools_sdk.sign.add_validation_information.AddValidationInformation.NONE` 



        Args:
            val (pdftools_sdk.sign.add_validation_information.AddValidationInformation):
                property value

        """
        from pdftools_sdk.sign.add_validation_information import AddValidationInformation

        if not isinstance(val, AddValidationInformation):
            raise TypeError(f"Expected type {AddValidationInformation.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSign_OutputOptions_SetAddValidationInformation.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSign_OutputOptions_SetAddValidationInformation.restype = c_bool
        if not _lib.PdfToolsSign_OutputOptions_SetAddValidationInformation(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return OutputOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = OutputOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
