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
    from pdftools_sdk.sign.appearance import Appearance

else:
    Appearance = "pdftools_sdk.sign.appearance.Appearance"


class SignatureFieldOptions(_NativeObject):
    """
    Options for adding unsigned signature fields

    These options control the creation of unsigned signature fields in :meth:`pdftools_sdk.sign.signer.Signer.add_signature_field` .


    """
    def __init__(self, bounding_box: Appearance):
        """

        Args:
            boundingBox (pdftools_sdk.sign.appearance.Appearance): 
                The bounding box of the signature field



        Raises:
            ValueError:
                If the `boundingBox` argument is `None` or not a valid bounding box


        """
        from pdftools_sdk.sign.appearance import Appearance

        if not isinstance(bounding_box, Appearance):
            raise TypeError(f"Expected type {Appearance.__name__}, but got {type(bounding_box).__name__}.")

        _lib.PdfToolsSign_SignatureFieldOptions_New.argtypes = [c_void_p]
        _lib.PdfToolsSign_SignatureFieldOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsSign_SignatureFieldOptions_New(bounding_box._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def bounding_box(self) -> Appearance:
        """
        The bounding box of the signature field

         
        The bounding box is the area where the visual appearance of the signature is inserted, when the signature field is signed.
         
        Use :meth:`pdftools_sdk.sign.appearance.Appearance.create_field_bounding_box`  to create the bounding box object.



        Returns:
            pdftools_sdk.sign.appearance.Appearance

        """
        from pdftools_sdk.sign.appearance import Appearance

        _lib.PdfToolsSign_SignatureFieldOptions_GetBoundingBox.argtypes = [c_void_p]
        _lib.PdfToolsSign_SignatureFieldOptions_GetBoundingBox.restype = c_void_p
        ret_val = _lib.PdfToolsSign_SignatureFieldOptions_GetBoundingBox(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Appearance._create_dynamic_type(ret_val)


    @property
    def field_name(self) -> Optional[str]:
        """
        The name of the new signature field

         
        If `None`, a new signature field is created using a unique field name.
         
        Default is `None`



        Returns:
            Optional[str]

        """
        _lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_SignatureFieldOptions_GetFieldNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @field_name.setter
    def field_name(self, val: Optional[str]) -> None:
        """
        The name of the new signature field

         
        If `None`, a new signature field is created using a unique field name.
         
        Default is `None`



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_SignatureFieldOptions_SetFieldNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsSign_SignatureFieldOptions_SetFieldNameW.restype = c_bool
        if not _lib.PdfToolsSign_SignatureFieldOptions_SetFieldNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return SignatureFieldOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignatureFieldOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
