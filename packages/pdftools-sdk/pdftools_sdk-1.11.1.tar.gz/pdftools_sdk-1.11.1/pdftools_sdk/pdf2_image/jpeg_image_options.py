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
import pdftools_sdk.pdf2_image.image_options

if TYPE_CHECKING:
    from pdftools_sdk.pdf2_image.jpeg_color_space import JpegColorSpace

else:
    JpegColorSpace = "pdftools_sdk.pdf2_image.jpeg_color_space.JpegColorSpace"


class JpegImageOptions(pdftools_sdk.pdf2_image.image_options.ImageOptions):
    """
    The settings for JPEG output images

     
    JPEG images use a lossy compression algorithm that provides a high compression ratio.
    It is best suited for photographs and content with little or no text.
     
    For the output file name, it is recommended to use the file extension ".jpg".


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf2Image_JpegImageOptions_New.argtypes = []
        _lib.PdfToolsPdf2Image_JpegImageOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_JpegImageOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def color_space(self) -> Optional[JpegColorSpace]:
        """
        The color space of the output image

         
        Get or set the color space of the image.
        If `None`, the blending color space of the page is used.
         
        Default is :attr:`pdftools_sdk.pdf2_image.jpeg_color_space.JpegColorSpace.RGB` 



        Returns:
            Optional[pdftools_sdk.pdf2_image.jpeg_color_space.JpegColorSpace]

        """
        from pdftools_sdk.pdf2_image.jpeg_color_space import JpegColorSpace

        _lib.PdfToolsPdf2Image_JpegImageOptions_GetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdf2Image_JpegImageOptions_GetColorSpace.restype = c_bool
        ret_val = c_int()
        if not _lib.PdfToolsPdf2Image_JpegImageOptions_GetColorSpace(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return JpegColorSpace(ret_val.value)



    @color_space.setter
    def color_space(self, val: Optional[JpegColorSpace]) -> None:
        """
        The color space of the output image

         
        Get or set the color space of the image.
        If `None`, the blending color space of the page is used.
         
        Default is :attr:`pdftools_sdk.pdf2_image.jpeg_color_space.JpegColorSpace.RGB` 



        Args:
            val (Optional[pdftools_sdk.pdf2_image.jpeg_color_space.JpegColorSpace]):
                property value

        """
        from pdftools_sdk.pdf2_image.jpeg_color_space import JpegColorSpace

        if val is not None and not isinstance(val, JpegColorSpace):
            raise TypeError(f"Expected type {JpegColorSpace.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_JpegImageOptions_SetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdf2Image_JpegImageOptions_SetColorSpace.restype = c_bool
        if not _lib.PdfToolsPdf2Image_JpegImageOptions_SetColorSpace(self._handle, byref(c_int(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def jpeg_quality(self) -> int:
        """
        The JPEG quality factor

         
        Get or set the JPEG compression quality.
        Valid values are 1, or 100, or in between.
         
        Default is `85`



        Returns:
            int

        """
        _lib.PdfToolsPdf2Image_JpegImageOptions_GetJpegQuality.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_JpegImageOptions_GetJpegQuality.restype = c_int
        ret_val = _lib.PdfToolsPdf2Image_JpegImageOptions_GetJpegQuality(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @jpeg_quality.setter
    def jpeg_quality(self, val: int) -> None:
        """
        The JPEG quality factor

         
        Get or set the JPEG compression quality.
        Valid values are 1, or 100, or in between.
         
        Default is `85`



        Args:
            val (int):
                property value

        Raises:
            ValueError:
                The given value is smaller than 1 or greater than 100.


        """
        if not isinstance(val, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_JpegImageOptions_SetJpegQuality.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf2Image_JpegImageOptions_SetJpegQuality.restype = c_bool
        if not _lib.PdfToolsPdf2Image_JpegImageOptions_SetJpegQuality(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return JpegImageOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = JpegImageOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
