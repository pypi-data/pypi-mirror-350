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

if TYPE_CHECKING:
    from pdftools_sdk.pdf.signed_signature_field import SignedSignatureField
    from pdftools_sdk.signature_validation.signature_content import SignatureContent

else:
    SignedSignatureField = "pdftools_sdk.pdf.signed_signature_field.SignedSignatureField"
    SignatureContent = "pdftools_sdk.signature_validation.signature_content.SignatureContent"


class ValidationResult(_NativeObject):
    """
    The result of a signature validation


    """
    @property
    def signature_field(self) -> SignedSignatureField:
        """
        The signature field



        Returns:
            pdftools_sdk.pdf.signed_signature_field.SignedSignatureField

        """
        from pdftools_sdk.pdf.signed_signature_field import SignedSignatureField

        _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureField.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureField.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureField(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignedSignatureField._create_dynamic_type(ret_val)


    @property
    def signature_content(self) -> SignatureContent:
        """
        The data and validation result of the cryptographic signature



        Returns:
            pdftools_sdk.signature_validation.signature_content.SignatureContent

        """
        from pdftools_sdk.signature_validation.signature_content import SignatureContent

        _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureContent.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureContent.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_ValidationResult_GetSignatureContent(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureContent._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return ValidationResult._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ValidationResult.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
