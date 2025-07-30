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
import pdftools_sdk.image2_pdf.image_mapping

if TYPE_CHECKING:
    from pdftools_sdk.geometry.units.size import Size
    from pdftools_sdk.geometry.units.margin import Margin

else:
    Size = "pdftools_sdk.geometry.units.size.Size"
    Margin = "pdftools_sdk.geometry.units.margin.Margin"


class Auto(pdftools_sdk.image2_pdf.image_mapping.ImageMapping):
    """
    The image mapping that automatically determines a suitable conversion

     
    Images with a meaningful resolution, e.g. scans or graphics,
    are converted to PDF pages fitting the image. The
    image size is preserved if it is smaller than :attr:`pdftools_sdk.image2_pdf.auto.Auto.max_page_size` .
    Otherwise, it is scaled down.
    For all images except scans, a margin :attr:`pdftools_sdk.image2_pdf.auto.Auto.default_page_margin`  is used.
     
    Images with no meaningful resolution, e.g. photos are scaled, to fit onto
    :attr:`pdftools_sdk.image2_pdf.auto.Auto.max_page_size` .


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsImage2Pdf_Auto_New.argtypes = []
        _lib.PdfToolsImage2Pdf_Auto_New.restype = c_void_p
        ret_val = _lib.PdfToolsImage2Pdf_Auto_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def max_page_size(self) -> Size:
        """
        The maximum page size

         
        Each image is scaled individually such that neither the
        width nor the height exceeds the maximum page size.
        For landscape images the maximum page size is assumed
        to be landscape, and equivalently for portrait images.
         
        Default value: "A4" (210mm 297mm)



        Returns:
            pdftools_sdk.geometry.units.size.Size

        """
        from pdftools_sdk.geometry.units.size import Size

        _lib.PdfToolsImage2Pdf_Auto_GetMaxPageSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PdfToolsImage2Pdf_Auto_GetMaxPageSize.restype = c_bool
        ret_val = Size()
        if not _lib.PdfToolsImage2Pdf_Auto_GetMaxPageSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @max_page_size.setter
    def max_page_size(self, val: Size) -> None:
        """
        The maximum page size

         
        Each image is scaled individually such that neither the
        width nor the height exceeds the maximum page size.
        For landscape images the maximum page size is assumed
        to be landscape, and equivalently for portrait images.
         
        Default value: "A4" (210mm 297mm)



        Args:
            val (pdftools_sdk.geometry.units.size.Size):
                property value

        Raises:
            ValueError:
                The argument is smaller than "3pt 3pt" or larger than "14400pt 14400pt".


        """
        from pdftools_sdk.geometry.units.size import Size

        if not isinstance(val, Size):
            raise TypeError(f"Expected type {Size.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsImage2Pdf_Auto_SetMaxPageSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PdfToolsImage2Pdf_Auto_SetMaxPageSize.restype = c_bool
        if not _lib.PdfToolsImage2Pdf_Auto_SetMaxPageSize(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def default_page_margin(self) -> Margin:
        """
        The default page margin

        Default value: 20mm (0.79in)



        Returns:
            pdftools_sdk.geometry.units.margin.Margin

        """
        from pdftools_sdk.geometry.units.margin import Margin

        _lib.PdfToolsImage2Pdf_Auto_GetDefaultPageMargin.argtypes = [c_void_p, POINTER(Margin)]
        _lib.PdfToolsImage2Pdf_Auto_GetDefaultPageMargin.restype = c_bool
        ret_val = Margin()
        if not _lib.PdfToolsImage2Pdf_Auto_GetDefaultPageMargin(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @default_page_margin.setter
    def default_page_margin(self, val: Margin) -> None:
        """
        The default page margin

        Default value: 20mm (0.79in)



        Args:
            val (pdftools_sdk.geometry.units.margin.Margin):
                property value

        Raises:
            ValueError:
                The argument has negative margin values.


        """
        from pdftools_sdk.geometry.units.margin import Margin

        if not isinstance(val, Margin):
            raise TypeError(f"Expected type {Margin.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsImage2Pdf_Auto_SetDefaultPageMargin.argtypes = [c_void_p, POINTER(Margin)]
        _lib.PdfToolsImage2Pdf_Auto_SetDefaultPageMargin.restype = c_bool
        if not _lib.PdfToolsImage2Pdf_Auto_SetDefaultPageMargin(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Auto._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Auto.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
