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
from abc import ABC

import pdftools_sdk.internal
import pdftools_sdk.pdf.signed_signature_field

class Signature(pdftools_sdk.pdf.signed_signature_field.SignedSignatureField, ABC):
    """
    A base class for certain signature types


    """
    @property
    def location(self) -> Optional[str]:
        """
        The location of signing

        The CPU host name or physical location of the signing.



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the object has already been closed


        """
        _lib.PdfToolsPdf_Signature_GetLocationW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Signature_GetLocationW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Signature_GetLocationW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Signature_GetLocationW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def reason(self) -> Optional[str]:
        """
        The reason for signing



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the object has already been closed


        """
        _lib.PdfToolsPdf_Signature_GetReasonW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Signature_GetReasonW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Signature_GetReasonW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Signature_GetReasonW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def contact_info(self) -> Optional[str]:
        """
        The contact information of the signer

        Information provided by the signer to enable a recipient to contact
        the signer to verify the signature.
        For example, a phone number.



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the object has already been closed


        """
        _lib.PdfToolsPdf_Signature_GetContactInfoW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Signature_GetContactInfoW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Signature_GetContactInfoW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Signature_GetContactInfoW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf_Signature_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Signature_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf_Signature_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Signature._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.pdf.document_signature import DocumentSignature 
            return DocumentSignature._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.pdf.certification_signature import CertificationSignature 
            return CertificationSignature._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Signature.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
