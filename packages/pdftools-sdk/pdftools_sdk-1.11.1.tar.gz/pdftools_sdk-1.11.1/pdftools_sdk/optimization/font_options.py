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

class FontOptions(_NativeObject):
    """
    The parameters for font optimization


    """
    @property
    def merge(self) -> bool:
        """
        Whether to merge fonts and font programs

         
        A PDF document can have the same font, or a subset of it,
        embedded multiple times.
        This commonly occurs, when multiple PDFs are merged into
        one large PDF.
        Such fonts can be merged into one font.
         
        Merging fonts and font programs can greatly reduce the file size.
        However, it is computationally complex and can increase file processing time
        and memory usage substantially.
         
        Default is `True`.



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_FontOptions_GetMerge.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_FontOptions_GetMerge.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_FontOptions_GetMerge(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @merge.setter
    def merge(self, val: bool) -> None:
        """
        Whether to merge fonts and font programs

         
        A PDF document can have the same font, or a subset of it,
        embedded multiple times.
        This commonly occurs, when multiple PDFs are merged into
        one large PDF.
        Such fonts can be merged into one font.
         
        Merging fonts and font programs can greatly reduce the file size.
        However, it is computationally complex and can increase file processing time
        and memory usage substantially.
         
        Default is `True`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_FontOptions_SetMerge.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_FontOptions_SetMerge.restype = c_bool
        if not _lib.PdfToolsOptimization_FontOptions_SetMerge(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_standard_fonts(self) -> bool:
        """
        Whether to remove standard fonts

         
        Enable or disable un-embedding of the font programs of all embedded
        standard fonts, such as Arial, Courier, CourierNew, Helvetica, Symbol,
        Times, TimesNewRoman and ZapfDingbats.
        This decreases the file size.
         
        The fonts are replaced with one of the 14 PDF Standard Fonts, all of
        which have no associated font program.
        A PDF viewer must be able to display these 14 PDF Standard Fonts correctly.
        Therefore, enabling this property usually does not visually alter the PDF
        when it is displayed.
         
        Un-embedding the font works based on the font's Unicode information,
        i.e. the un-embedded font's characters are mapped to those of the
        original font with the same Unicode.
        Therefore, only fonts with Unicode information are un-embedded.
         
        If a font's Unicode information is incorrect, un-embedding may lead
        to visual differences.
        The correctness of a Unicode information can be verified by extracting
        text that uses the font.
         
        If the extracted text is meaningful, the font's Unicode information is
        correct, and un-embedding of the font does not cause visual differences.
         
        Default is `False` (disabled) except in the profile :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize` .



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_FontOptions_GetRemoveStandardFonts.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_FontOptions_GetRemoveStandardFonts.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_FontOptions_GetRemoveStandardFonts(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_standard_fonts.setter
    def remove_standard_fonts(self, val: bool) -> None:
        """
        Whether to remove standard fonts

         
        Enable or disable un-embedding of the font programs of all embedded
        standard fonts, such as Arial, Courier, CourierNew, Helvetica, Symbol,
        Times, TimesNewRoman and ZapfDingbats.
        This decreases the file size.
         
        The fonts are replaced with one of the 14 PDF Standard Fonts, all of
        which have no associated font program.
        A PDF viewer must be able to display these 14 PDF Standard Fonts correctly.
        Therefore, enabling this property usually does not visually alter the PDF
        when it is displayed.
         
        Un-embedding the font works based on the font's Unicode information,
        i.e. the un-embedded font's characters are mapped to those of the
        original font with the same Unicode.
        Therefore, only fonts with Unicode information are un-embedded.
         
        If a font's Unicode information is incorrect, un-embedding may lead
        to visual differences.
        The correctness of a Unicode information can be verified by extracting
        text that uses the font.
         
        If the extracted text is meaningful, the font's Unicode information is
        correct, and un-embedding of the font does not cause visual differences.
         
        Default is `False` (disabled) except in the profile :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize` .



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_FontOptions_SetRemoveStandardFonts.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_FontOptions_SetRemoveStandardFonts.restype = c_bool
        if not _lib.PdfToolsOptimization_FontOptions_SetRemoveStandardFonts(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return FontOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = FontOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
