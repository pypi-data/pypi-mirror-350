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
    from pdftools_sdk.pdf.conformance import Conformance

else:
    Conformance = "pdftools_sdk.pdf.conformance.Conformance"


class ValidationResult(_NativeObject):
    """
    The PDF validation result

    Result of the validator's method :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.validate` .


    """
    @property
    def conformance(self) -> Conformance:
        """
        The validated conformance



        Returns:
            pdftools_sdk.pdf.conformance.Conformance

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsPdfAValidation_ValidationResult_GetConformance.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_ValidationResult_GetConformance.restype = c_int
        ret_val = _lib.PdfToolsPdfAValidation_ValidationResult_GetConformance(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Conformance(ret_val)



    @property
    def is_conforming(self) -> bool:
        """
        Whether the document is conforming

        Whether the document conforms to all standards referenced to the :attr:`pdftools_sdk.pdf_a.validation.validation_result.ValidationResult.conformance` .
        Any issues found are reported as :func:`pdftools_sdk.pdf_a.validation.validator.ErrorFunc` .



        Returns:
            bool

        """
        _lib.PdfToolsPdfAValidation_ValidationResult_IsConforming.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_ValidationResult_IsConforming.restype = c_bool
        ret_val = _lib.PdfToolsPdfAValidation_ValidationResult_IsConforming(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




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
