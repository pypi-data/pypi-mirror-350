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
    from pdftools_sdk.image2_pdf.image_mapping import ImageMapping

else:
    ImageMapping = "pdftools_sdk.image2_pdf.image_mapping.ImageMapping"


class ImageOptions(_NativeObject):
    """
    The conversion options related to the images


    """
    @property
    def mapping(self) -> ImageMapping:
        """
        The image mapping

         
        The image mapping specifies how an input image is transformed and placed
        onto the output PDF page.
         
        Default is :class:`pdftools_sdk.image2_pdf.shrink_to_fit.ShrinkToFit` 



        Returns:
            pdftools_sdk.image2_pdf.image_mapping.ImageMapping

        """
        from pdftools_sdk.image2_pdf.image_mapping import ImageMapping

        _lib.PdfToolsImage2Pdf_ImageOptions_GetMapping.argtypes = [c_void_p]
        _lib.PdfToolsImage2Pdf_ImageOptions_GetMapping.restype = c_void_p
        ret_val = _lib.PdfToolsImage2Pdf_ImageOptions_GetMapping(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageMapping._create_dynamic_type(ret_val)


    @mapping.setter
    def mapping(self, val: ImageMapping) -> None:
        """
        The image mapping

         
        The image mapping specifies how an input image is transformed and placed
        onto the output PDF page.
         
        Default is :class:`pdftools_sdk.image2_pdf.shrink_to_fit.ShrinkToFit` 



        Args:
            val (pdftools_sdk.image2_pdf.image_mapping.ImageMapping):
                property value

        """
        from pdftools_sdk.image2_pdf.image_mapping import ImageMapping

        if not isinstance(val, ImageMapping):
            raise TypeError(f"Expected type {ImageMapping.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsImage2Pdf_ImageOptions_SetMapping.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsImage2Pdf_ImageOptions_SetMapping.restype = c_bool
        if not _lib.PdfToolsImage2Pdf_ImageOptions_SetMapping(self._handle, val._handle):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ImageOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ImageOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
