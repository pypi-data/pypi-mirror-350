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
    from pdftools_sdk.extraction.text_extraction_format import TextExtractionFormat

else:
    TextExtractionFormat = "pdftools_sdk.extraction.text_extraction_format.TextExtractionFormat"


class TextOptions(_NativeObject):
    """
    Options for text extraction

    This class specifies the details of text extraction.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsExtraction_TextOptions_New.argtypes = []
        _lib.PdfToolsExtraction_TextOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsExtraction_TextOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def extraction_format(self) -> TextExtractionFormat:
        """
        Format of the extracted text.

         
        Specifies the format of the extracted text.
         
        Default value: :attr:`pdftools_sdk.extraction.text_extraction_format.TextExtractionFormat.DOCUMENTORDER` 



        Returns:
            pdftools_sdk.extraction.text_extraction_format.TextExtractionFormat

        """
        from pdftools_sdk.extraction.text_extraction_format import TextExtractionFormat

        _lib.PdfToolsExtraction_TextOptions_GetExtractionFormat.argtypes = [c_void_p]
        _lib.PdfToolsExtraction_TextOptions_GetExtractionFormat.restype = c_int
        ret_val = _lib.PdfToolsExtraction_TextOptions_GetExtractionFormat(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return TextExtractionFormat(ret_val)



    @extraction_format.setter
    def extraction_format(self, val: TextExtractionFormat) -> None:
        """
        Format of the extracted text.

         
        Specifies the format of the extracted text.
         
        Default value: :attr:`pdftools_sdk.extraction.text_extraction_format.TextExtractionFormat.DOCUMENTORDER` 



        Args:
            val (pdftools_sdk.extraction.text_extraction_format.TextExtractionFormat):
                property value

        """
        from pdftools_sdk.extraction.text_extraction_format import TextExtractionFormat

        if not isinstance(val, TextExtractionFormat):
            raise TypeError(f"Expected type {TextExtractionFormat.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsExtraction_TextOptions_SetExtractionFormat.argtypes = [c_void_p, c_int]
        _lib.PdfToolsExtraction_TextOptions_SetExtractionFormat.restype = c_bool
        if not _lib.PdfToolsExtraction_TextOptions_SetExtractionFormat(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def advance_width(self) -> Optional[float]:
        """
         
        The horizontal space in a PDF that corresponds to a character in monospaced text output.
         
        If `None`, the horizontal space is 7.2pt.
         
        Default value: `None`



        Returns:
            Optional[float]

        """
        _lib.PdfToolsExtraction_TextOptions_GetAdvanceWidth.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsExtraction_TextOptions_GetAdvanceWidth.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsExtraction_TextOptions_GetAdvanceWidth(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @advance_width.setter
    def advance_width(self, val: Optional[float]) -> None:
        """
         
        The horizontal space in a PDF that corresponds to a character in monospaced text output.
         
        If `None`, the horizontal space is 7.2pt.
         
        Default value: `None`



        Args:
            val (Optional[float]):
                property value

        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsExtraction_TextOptions_SetAdvanceWidth.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsExtraction_TextOptions_SetAdvanceWidth.restype = c_bool
        if not _lib.PdfToolsExtraction_TextOptions_SetAdvanceWidth(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def line_height(self) -> Optional[float]:
        """
         
        The vertical space in a PDF that triggers a new line in monospaced text output.
         
        If `None`, no extra blank lines are added in the text output.
         
        Default value: `None`



        Returns:
            Optional[float]

        """
        _lib.PdfToolsExtraction_TextOptions_GetLineHeight.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsExtraction_TextOptions_GetLineHeight.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsExtraction_TextOptions_GetLineHeight(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @line_height.setter
    def line_height(self, val: Optional[float]) -> None:
        """
         
        The vertical space in a PDF that triggers a new line in monospaced text output.
         
        If `None`, no extra blank lines are added in the text output.
         
        Default value: `None`



        Args:
            val (Optional[float]):
                property value

        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsExtraction_TextOptions_SetLineHeight.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsExtraction_TextOptions_SetLineHeight.restype = c_bool
        if not _lib.PdfToolsExtraction_TextOptions_SetLineHeight(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def word_separation_factor(self) -> float:
        """
         
        This parameter defines a factor multiplied by the width of the space character to determine word boundaries.
        If the distance between two characters exceeds this calculated value, it is recognized as a word separation.
         
        Default value: 0.3



        Returns:
            float

        """
        _lib.PdfToolsExtraction_TextOptions_GetWordSeparationFactor.argtypes = [c_void_p]
        _lib.PdfToolsExtraction_TextOptions_GetWordSeparationFactor.restype = c_double
        ret_val = _lib.PdfToolsExtraction_TextOptions_GetWordSeparationFactor(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @word_separation_factor.setter
    def word_separation_factor(self, val: float) -> None:
        """
         
        This parameter defines a factor multiplied by the width of the space character to determine word boundaries.
        If the distance between two characters exceeds this calculated value, it is recognized as a word separation.
         
        Default value: 0.3



        Args:
            val (float):
                property value

        Raises:
            ValueError:
                The word separation factor is invalid.


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsExtraction_TextOptions_SetWordSeparationFactor.argtypes = [c_void_p, c_double]
        _lib.PdfToolsExtraction_TextOptions_SetWordSeparationFactor.restype = c_bool
        if not _lib.PdfToolsExtraction_TextOptions_SetWordSeparationFactor(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return TextOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TextOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
