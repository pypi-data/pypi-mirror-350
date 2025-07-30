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
    from pdftools_sdk.pdf2_image.background_type import BackgroundType
    from pdftools_sdk.pdf2_image.color_space import ColorSpace

else:
    BackgroundType = "pdftools_sdk.pdf2_image.background_type.BackgroundType"
    ColorSpace = "pdftools_sdk.pdf2_image.color_space.ColorSpace"


class TiffLzwImageOptions(pdftools_sdk.pdf2_image.image_options.ImageOptions):
    """
    The settings for TIFF output images using the LZW compression algorithm

     
    LZW (Lempel-Ziv-Welch) is a lossless compression algorithm for images. Please
    consult the copyright laws of your country prior to using this
    compression algorithm.
     
    For the output file name, it is recommended to use the file extension ".tif".


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_New.argtypes = []
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_TiffLzwImageOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def background(self) -> BackgroundType:
        """
        Combine a background with the image

         
        This property allows a choice of which background
        to combine with the image.
         
        Default is :attr:`pdftools_sdk.pdf2_image.background_type.BackgroundType.WHITE` 



        Returns:
            pdftools_sdk.pdf2_image.background_type.BackgroundType

        """
        from pdftools_sdk.pdf2_image.background_type import BackgroundType

        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetBackground.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetBackground.restype = c_int
        ret_val = _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetBackground(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return BackgroundType(ret_val)



    @background.setter
    def background(self, val: BackgroundType) -> None:
        """
        Combine a background with the image

         
        This property allows a choice of which background
        to combine with the image.
         
        Default is :attr:`pdftools_sdk.pdf2_image.background_type.BackgroundType.WHITE` 



        Args:
            val (pdftools_sdk.pdf2_image.background_type.BackgroundType):
                property value

        """
        from pdftools_sdk.pdf2_image.background_type import BackgroundType

        if not isinstance(val, BackgroundType):
            raise TypeError(f"Expected type {BackgroundType.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetBackground.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetBackground.restype = c_bool
        if not _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetBackground(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def color_space(self) -> Optional[ColorSpace]:
        """
        The color space of the output image

         
        Get or set the color space. If null, the blending color space of the page is used.
         
        Default is :attr:`pdftools_sdk.pdf2_image.color_space.ColorSpace.RGB` 



        Returns:
            Optional[pdftools_sdk.pdf2_image.color_space.ColorSpace]

        """
        from pdftools_sdk.pdf2_image.color_space import ColorSpace

        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetColorSpace.restype = c_bool
        ret_val = c_int()
        if not _lib.PdfToolsPdf2Image_TiffLzwImageOptions_GetColorSpace(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ColorSpace(ret_val.value)



    @color_space.setter
    def color_space(self, val: Optional[ColorSpace]) -> None:
        """
        The color space of the output image

         
        Get or set the color space. If null, the blending color space of the page is used.
         
        Default is :attr:`pdftools_sdk.pdf2_image.color_space.ColorSpace.RGB` 



        Args:
            val (Optional[pdftools_sdk.pdf2_image.color_space.ColorSpace]):
                property value

        """
        from pdftools_sdk.pdf2_image.color_space import ColorSpace

        if val is not None and not isinstance(val, ColorSpace):
            raise TypeError(f"Expected type {ColorSpace.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetColorSpace.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetColorSpace.restype = c_bool
        if not _lib.PdfToolsPdf2Image_TiffLzwImageOptions_SetColorSpace(self._handle, byref(c_int(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return TiffLzwImageOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TiffLzwImageOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
