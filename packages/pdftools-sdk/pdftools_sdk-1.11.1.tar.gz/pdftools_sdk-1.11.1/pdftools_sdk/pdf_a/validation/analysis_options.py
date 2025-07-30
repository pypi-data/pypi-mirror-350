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


class AnalysisOptions(_NativeObject):
    """
    The PDF/A analysis options

    Options for the analysis of documents using the validator's method :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.analyze`  in preparation for the document's conversion to PDF/A.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdfAValidation_AnalysisOptions_New.argtypes = []
        _lib.PdfToolsPdfAValidation_AnalysisOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def conformance(self) -> Conformance:
        """
        The PDF/A conformance to validate

         
        It is recommended to use:
         
        - The input document's claimed conformance :attr:`pdftools_sdk.pdf.document.Document.conformance` , if it is an acceptable conversion conformance.
          No conversion is needed, if the analysis result's property :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.is_conversion_recommended`  is `False`.
        - PDF/A-2b for the conversion to PDF/A-2. This is the recommended value for all other input documents.
        - PDF/A-3b for the conversion to PDF/A-3
        - PDF/A-1b for the conversion to PDF/A-1
         
         
        Default is "PDF/A-2b"



        Returns:
            pdftools_sdk.pdf.conformance.Conformance

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsPdfAValidation_AnalysisOptions_GetConformance.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisOptions_GetConformance.restype = c_int
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisOptions_GetConformance(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Conformance(ret_val)



    @conformance.setter
    def conformance(self, val: Conformance) -> None:
        """
        The PDF/A conformance to validate

         
        It is recommended to use:
         
        - The input document's claimed conformance :attr:`pdftools_sdk.pdf.document.Document.conformance` , if it is an acceptable conversion conformance.
          No conversion is needed, if the analysis result's property :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.is_conversion_recommended`  is `False`.
        - PDF/A-2b for the conversion to PDF/A-2. This is the recommended value for all other input documents.
        - PDF/A-3b for the conversion to PDF/A-3
        - PDF/A-1b for the conversion to PDF/A-1
         
         
        Default is "PDF/A-2b"



        Args:
            val (pdftools_sdk.pdf.conformance.Conformance):
                property value

        """
        from pdftools_sdk.pdf.conformance import Conformance

        if not isinstance(val, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdfAValidation_AnalysisOptions_SetConformance.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdfAValidation_AnalysisOptions_SetConformance.restype = c_bool
        if not _lib.PdfToolsPdfAValidation_AnalysisOptions_SetConformance(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def strict_mode(self) -> bool:
        """
        Whether to enable additional, strict validation checks

         
        Whether to check for potential issues that are corner cases of the PDF/A ISO Standard in which a conversion is strongly advised.
        Also see the documentation of :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.is_conversion_recommended` .
         
        Default is `True`



        Returns:
            bool

        """
        _lib.PdfToolsPdfAValidation_AnalysisOptions_GetStrictMode.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisOptions_GetStrictMode.restype = c_bool
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisOptions_GetStrictMode(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @strict_mode.setter
    def strict_mode(self, val: bool) -> None:
        """
        Whether to enable additional, strict validation checks

         
        Whether to check for potential issues that are corner cases of the PDF/A ISO Standard in which a conversion is strongly advised.
        Also see the documentation of :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.is_conversion_recommended` .
         
        Default is `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdfAValidation_AnalysisOptions_SetStrictMode.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsPdfAValidation_AnalysisOptions_SetStrictMode.restype = c_bool
        if not _lib.PdfToolsPdfAValidation_AnalysisOptions_SetStrictMode(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return AnalysisOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = AnalysisOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
