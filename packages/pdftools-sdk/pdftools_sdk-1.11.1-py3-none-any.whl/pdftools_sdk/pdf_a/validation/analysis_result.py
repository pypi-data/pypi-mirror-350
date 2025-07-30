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


class AnalysisResult(_NativeObject):
    """
    The PDF/A analysis result

     
    Result of the validator's method :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.analyze`  which is required for the conversion to PDF/A with :meth:`pdftools_sdk.pdf_a.conversion.converter.Converter.convert` .
     
    Note that :class:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult`  objects remain valid as long as their :class:`pdftools_sdk.pdf.document.Document`  has not been closed and the analysis result has not been used in :meth:`pdftools_sdk.pdf_a.conversion.converter.Converter.convert` .


    """
    @property
    def conformance(self) -> Conformance:
        """
        The conformance used for analysis

         
        The PDF/A level might differ from the :attr:`pdftools_sdk.pdf_a.validation.analysis_options.AnalysisOptions.conformance` .
        If the claimed PDF/A level of the input document is higher than  :attr:`pdftools_sdk.pdf_a.validation.analysis_options.AnalysisOptions.conformance` , the higher level is used for :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.conformance` .
         
        For example, if  :attr:`pdftools_sdk.pdf_a.validation.analysis_options.AnalysisOptions.conformance`  is PDF/A-2b, but the document's claimed conformance is PDF/A-2u, the analysis checks if the document actually conforms to its claimed conformance PDF/A-2u.
        Because otherwise a conversion is required.



        Returns:
            pdftools_sdk.pdf.conformance.Conformance

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsPdfAValidation_AnalysisResult_GetConformance.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisResult_GetConformance.restype = c_int
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisResult_GetConformance(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Conformance(ret_val)



    @property
    def recommended_conformance(self) -> Conformance:
        """
        The recommended conversion conformance

        The optimal PDF/A conformance for the conversion (i.e. the :attr:`pdftools_sdk.pdf_a.conversion.conversion_options.ConversionOptions.conformance` ).
        The recommended conformance level might be higher than the analysis conformance, if the document actually contains all data required for the higher level.
        It might also be lower, if the document is missing some required data.



        Returns:
            pdftools_sdk.pdf.conformance.Conformance

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsPdfAValidation_AnalysisResult_GetRecommendedConformance.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisResult_GetRecommendedConformance.restype = c_int
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisResult_GetRecommendedConformance(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Conformance(ret_val)



    @property
    def is_conversion_recommended(self) -> bool:
        """
        Whether the document should be converted to PDF/A

         
        A conversion is generally recommended in the following cases:
         
        - If :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.is_conforming`  is `False`, i.e. if the document does not conform to the :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.conformance` .
        - If the document is conforming, but other issues are found for which a conversion is highly recommended.
          For example, if certain corner cases of the specification are detected.
         
         
        Note that in certain processes it might also be beneficial to convert a document if its conformance does not match the :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.recommended_conformance` .
        This will actually upgrade the PDF/A level of the input document.



        Returns:
            bool

        """
        _lib.PdfToolsPdfAValidation_AnalysisResult_IsConversionRecommended.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisResult_IsConversionRecommended.restype = c_bool
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisResult_IsConversionRecommended(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def is_conforming(self) -> bool:
        """
        Whether the document is conforming

        Whether the document conforms to the :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.conformance` .
        Note that even if this property returns `True` a conversion might still be recommended as indicated by :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.is_conversion_recommended` .



        Returns:
            bool

        """
        _lib.PdfToolsPdfAValidation_AnalysisResult_IsConforming.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisResult_IsConforming.restype = c_bool
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisResult_IsConforming(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def is_signed(self) -> bool:
        """
        Whether the document is digitally signed



        Returns:
            bool

        """
        _lib.PdfToolsPdfAValidation_AnalysisResult_IsSigned.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisResult_IsSigned.restype = c_bool
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisResult_IsSigned(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def has_embedded_files(self) -> bool:
        """
        Whether the document contains embedded files



        Returns:
            bool

        """
        _lib.PdfToolsPdfAValidation_AnalysisResult_GetHasEmbeddedFiles.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisResult_GetHasEmbeddedFiles.restype = c_bool
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisResult_GetHasEmbeddedFiles(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def font_count(self) -> int:
        """
        The number of fonts used in the document



        Returns:
            int

        """
        _lib.PdfToolsPdfAValidation_AnalysisResult_GetFontCount.argtypes = [c_void_p]
        _lib.PdfToolsPdfAValidation_AnalysisResult_GetFontCount.restype = c_int
        ret_val = _lib.PdfToolsPdfAValidation_AnalysisResult_GetFontCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        return AnalysisResult._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = AnalysisResult.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
