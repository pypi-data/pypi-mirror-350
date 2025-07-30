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
    from pdftools_sdk.signature_validation.indication import Indication
    from pdftools_sdk.signature_validation.sub_indication import SubIndication

else:
    Indication = "pdftools_sdk.signature_validation.indication.Indication"
    SubIndication = "pdftools_sdk.signature_validation.sub_indication.SubIndication"


class ConstraintResult(_NativeObject):
    """
    The result of a constraint validation.


    """
    @property
    def message(self) -> str:
        """
        The validation message



        Returns:
            str

        """
        _lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSignatureValidation_ConstraintResult_GetMessageW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def indication(self) -> Indication:
        """
        The main indication



        Returns:
            pdftools_sdk.signature_validation.indication.Indication

        """
        from pdftools_sdk.signature_validation.indication import Indication

        _lib.PdfToolsSignatureValidation_ConstraintResult_GetIndication.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_ConstraintResult_GetIndication.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidation_ConstraintResult_GetIndication(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Indication(ret_val)



    @property
    def sub_indication(self) -> SubIndication:
        """
        The sub indication



        Returns:
            pdftools_sdk.signature_validation.sub_indication.SubIndication

        """
        from pdftools_sdk.signature_validation.sub_indication import SubIndication

        _lib.PdfToolsSignatureValidation_ConstraintResult_GetSubIndication.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_ConstraintResult_GetSubIndication.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidation_ConstraintResult_GetSubIndication(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return SubIndication(ret_val)




    @staticmethod
    def _create_dynamic_type(handle):
        return ConstraintResult._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ConstraintResult.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
