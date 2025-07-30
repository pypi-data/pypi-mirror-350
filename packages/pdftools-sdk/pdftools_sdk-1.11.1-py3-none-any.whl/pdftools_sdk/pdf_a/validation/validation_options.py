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


class ValidationOptions(_NativeObject):
    """
    The PDF validation options

    Options to check the quality and standard conformance of documents using the validator's method :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.validate` .


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdfAValidation_ValidationOptions_New.argtypes = []
        _lib.PdfToolsPdfAValidation_ValidationOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAValidation_ValidationOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def conformance(self) -> Optional[Conformance]:
        """
        The conformance to be validated

         
        The required conformance or `None` to validate the document's claimed conformance, i.e. :attr:`pdftools_sdk.pdf.document.Document.conformance` .
         
        The PDF validation verifies if the input document conforms to all standards associated with this conformance.
         
        Note that it is generally only meaningful to validate the claimed conformance of a document.
         
        Default value: `None`, i.e. validate the document's claimed conformance.



        Returns:
            Optional[pdftools_sdk.pdf.conformance.Conformance]

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsPdfAValidation_ValidationOptions_GetConformance.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdfAValidation_ValidationOptions_GetConformance.restype = c_bool
        ret_val = c_int()
        if not _lib.PdfToolsPdfAValidation_ValidationOptions_GetConformance(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return Conformance(ret_val.value)



    @conformance.setter
    def conformance(self, val: Optional[Conformance]) -> None:
        """
        The conformance to be validated

         
        The required conformance or `None` to validate the document's claimed conformance, i.e. :attr:`pdftools_sdk.pdf.document.Document.conformance` .
         
        The PDF validation verifies if the input document conforms to all standards associated with this conformance.
         
        Note that it is generally only meaningful to validate the claimed conformance of a document.
         
        Default value: `None`, i.e. validate the document's claimed conformance.



        Args:
            val (Optional[pdftools_sdk.pdf.conformance.Conformance]):
                property value

        """
        from pdftools_sdk.pdf.conformance import Conformance

        if val is not None and not isinstance(val, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdfAValidation_ValidationOptions_SetConformance.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdfAValidation_ValidationOptions_SetConformance.restype = c_bool
        if not _lib.PdfToolsPdfAValidation_ValidationOptions_SetConformance(self._handle, byref(c_int(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ValidationOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ValidationOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
