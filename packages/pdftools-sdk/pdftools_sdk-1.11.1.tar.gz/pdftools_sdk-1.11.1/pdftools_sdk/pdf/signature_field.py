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

if TYPE_CHECKING:
    from pdftools_sdk.geometry.units.rectangle import Rectangle

else:
    Rectangle = "pdftools_sdk.geometry.units.rectangle.Rectangle"


class SignatureField(_NativeObject, ABC):
    """
    A digital signature field


    """
    @property
    def field_name(self) -> Optional[str]:
        """
        The name of the signature field

        The field name uniquely identifies the signature field within the document.



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the object has already been closed


        """
        _lib.PdfToolsPdf_SignatureField_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_SignatureField_GetFieldNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_SignatureField_GetFieldNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_SignatureField_GetFieldNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def page_number(self) -> int:
        """
        The number of the page where this signature is located

        Whether the signature field has a visual appearance on that page is indicated by the :attr:`pdftools_sdk.pdf.signature_field.SignatureField.bounding_box` .



        Returns:
            int

        Raises:
            StateError:
                If the object has already been closed.

            pdftools_sdk.not_found_error.NotFoundError:
                If the field is not properly linked to a page.


        """
        _lib.PdfToolsPdf_SignatureField_GetPageNumber.argtypes = [c_void_p]
        _lib.PdfToolsPdf_SignatureField_GetPageNumber.restype = c_int
        ret_val = _lib.PdfToolsPdf_SignatureField_GetPageNumber(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def bounding_box(self) -> Optional[Rectangle]:
        """
        The location on the page

        The location of the signature field on the page.
        Or `None` if the signature field has no visual appearance.



        Returns:
            Optional[pdftools_sdk.geometry.units.rectangle.Rectangle]

        Raises:
            StateError:
                If the object has already been closed


        """
        from pdftools_sdk.geometry.units.rectangle import Rectangle

        _lib.PdfToolsPdf_SignatureField_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PdfToolsPdf_SignatureField_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PdfToolsPdf_SignatureField_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf_SignatureField_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf_SignatureField_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf_SignatureField_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return SignatureField._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.pdf.unsigned_signature_field import UnsignedSignatureField 
            return UnsignedSignatureField._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.pdf.signed_signature_field import SignedSignatureField 
            return SignedSignatureField._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.pdf.signature import Signature 
            return Signature._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.pdf.document_signature import DocumentSignature 
            return DocumentSignature._from_handle(handle)
        elif obj_type == 5:
            from pdftools_sdk.pdf.certification_signature import CertificationSignature 
            return CertificationSignature._from_handle(handle)
        elif obj_type == 6:
            from pdftools_sdk.pdf.document_timestamp import DocumentTimestamp 
            return DocumentTimestamp._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignatureField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
