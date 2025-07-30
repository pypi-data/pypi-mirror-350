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


class ConversionOptions(_NativeObject):
    """
    The PDF/A conversion options

    The options for the conversion of documents using the converter's method :meth:`pdftools_sdk.pdf_a.conversion.converter.Converter.convert` 


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdfAConversion_ConversionOptions_New.argtypes = []
        _lib.PdfToolsPdfAConversion_ConversionOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAConversion_ConversionOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def conformance(self) -> Optional[Conformance]:
        """
        The minimal target conformance

         
        If a conformance is set, it is used as the minimal target conformance.
        The PDF/A version of the conformance must match the PDF/A version of the analysisOptions of :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.analyze` .
        If the conformance level cannot be achieved, the conversion will abort with the error :class:`pdftools_sdk.conformance_error.ConformanceError` .
        If a higher conformance level can be achieved, it is used automatically.
         
        If `None` is used, the optimal conformance determined in the analysis
        (i.e. :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.recommended_conformance` ) is used.
        It is highly recommended to use `None`.
         
        Default value: `None`



        Returns:
            Optional[pdftools_sdk.pdf.conformance.Conformance]

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsPdfAConversion_ConversionOptions_GetConformance.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdfAConversion_ConversionOptions_GetConformance.restype = c_bool
        ret_val = c_int()
        if not _lib.PdfToolsPdfAConversion_ConversionOptions_GetConformance(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return Conformance(ret_val.value)



    @conformance.setter
    def conformance(self, val: Optional[Conformance]) -> None:
        """
        The minimal target conformance

         
        If a conformance is set, it is used as the minimal target conformance.
        The PDF/A version of the conformance must match the PDF/A version of the analysisOptions of :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.analyze` .
        If the conformance level cannot be achieved, the conversion will abort with the error :class:`pdftools_sdk.conformance_error.ConformanceError` .
        If a higher conformance level can be achieved, it is used automatically.
         
        If `None` is used, the optimal conformance determined in the analysis
        (i.e. :attr:`pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult.recommended_conformance` ) is used.
        It is highly recommended to use `None`.
         
        Default value: `None`



        Args:
            val (Optional[pdftools_sdk.pdf.conformance.Conformance]):
                property value

        """
        from pdftools_sdk.pdf.conformance import Conformance

        if val is not None and not isinstance(val, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdfAConversion_ConversionOptions_SetConformance.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdfAConversion_ConversionOptions_SetConformance.restype = c_bool
        if not _lib.PdfToolsPdfAConversion_ConversionOptions_SetConformance(self._handle, byref(c_int(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def copy_metadata(self) -> bool:
        """
        Whether to copy metadata

        Copy document information dictionary and XMP metadata.
        Default: `True`.



        Returns:
            bool

        """
        _lib.PdfToolsPdfAConversion_ConversionOptions_GetCopyMetadata.argtypes = [c_void_p]
        _lib.PdfToolsPdfAConversion_ConversionOptions_GetCopyMetadata.restype = c_bool
        ret_val = _lib.PdfToolsPdfAConversion_ConversionOptions_GetCopyMetadata(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_metadata.setter
    def copy_metadata(self, val: bool) -> None:
        """
        Whether to copy metadata

        Copy document information dictionary and XMP metadata.
        Default: `True`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdfAConversion_ConversionOptions_SetCopyMetadata.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsPdfAConversion_ConversionOptions_SetCopyMetadata.restype = c_bool
        if not _lib.PdfToolsPdfAConversion_ConversionOptions_SetCopyMetadata(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def image_quality(self) -> float:
        """
        Image quality of recompressed images

         
        The image quality for images that use a prohibited lossy compression type and must be recompressed.
        Supported values are `0.01` to `1.0`.
        A higher value means better visual quality at the cost of a larger file size.
        Recommended values range from `0.7` to `0.9`.
         
        Example:
        JPX (JPEG2000) is not allowed in PDF/A-1. If a PDF contains a JPX compressed image, its compression type must be altered. 
        Thus the image is converted to an image with JPEG compression using the image quality defined by this property.
        Default value: `0.8`



        Returns:
            float

        """
        _lib.PdfToolsPdfAConversion_ConversionOptions_GetImageQuality.argtypes = [c_void_p]
        _lib.PdfToolsPdfAConversion_ConversionOptions_GetImageQuality.restype = c_double
        ret_val = _lib.PdfToolsPdfAConversion_ConversionOptions_GetImageQuality(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @image_quality.setter
    def image_quality(self, val: float) -> None:
        """
        Image quality of recompressed images

         
        The image quality for images that use a prohibited lossy compression type and must be recompressed.
        Supported values are `0.01` to `1.0`.
        A higher value means better visual quality at the cost of a larger file size.
        Recommended values range from `0.7` to `0.9`.
         
        Example:
        JPX (JPEG2000) is not allowed in PDF/A-1. If a PDF contains a JPX compressed image, its compression type must be altered. 
        Thus the image is converted to an image with JPEG compression using the image quality defined by this property.
        Default value: `0.8`



        Args:
            val (float):
                property value

        Raises:
            ValueError:
                The given value is smaller than `0.1` or greater than `1`.


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdfAConversion_ConversionOptions_SetImageQuality.argtypes = [c_void_p, c_double]
        _lib.PdfToolsPdfAConversion_ConversionOptions_SetImageQuality.restype = c_bool
        if not _lib.PdfToolsPdfAConversion_ConversionOptions_SetImageQuality(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ConversionOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ConversionOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
