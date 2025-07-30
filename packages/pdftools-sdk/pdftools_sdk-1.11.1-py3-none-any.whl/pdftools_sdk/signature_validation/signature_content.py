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
    from pdftools_sdk.signature_validation.constraint_result import ConstraintResult

else:
    ConstraintResult = "pdftools_sdk.signature_validation.constraint_result.ConstraintResult"


class SignatureContent(_NativeObject, ABC):
    """
    The data and validation result of the cryptographic signature


    """
    @property
    def validity(self) -> ConstraintResult:
        """
        Whether the cryptographic signature is valid according to the validation profile used



        Returns:
            pdftools_sdk.signature_validation.constraint_result.ConstraintResult

        """
        from pdftools_sdk.signature_validation.constraint_result import ConstraintResult

        _lib.PdfToolsSignatureValidation_SignatureContent_GetValidity.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_SignatureContent_GetValidity.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_SignatureContent_GetValidity(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ConstraintResult._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsSignatureValidation_SignatureContent_GetType.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_SignatureContent_GetType.restype = c_int

        obj_type = _lib.PdfToolsSignatureValidation_SignatureContent_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return SignatureContent._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.signature_validation.unsupported_signature_content import UnsupportedSignatureContent 
            return UnsupportedSignatureContent._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.signature_validation.cms_signature_content import CmsSignatureContent 
            return CmsSignatureContent._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.signature_validation.time_stamp_content import TimeStampContent 
            return TimeStampContent._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignatureContent.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
