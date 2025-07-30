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
    from pdftools_sdk.pdf2_image.png_color_space import PngColorSpace

else:
    BackgroundType = "pdftools_sdk.pdf2_image.background_type.BackgroundType"
    PngColorSpace = "pdftools_sdk.pdf2_image.png_color_space.PngColorSpace"


class PngImageOptions(pdftools_sdk.pdf2_image.image_options.ImageOptions):
    """
    The settings for PNG output images

    For the output file name, it is recommended to use the file extension ".png".


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf2Image_PngImageOptions_New.argtypes = []
        _lib.PdfToolsPdf2Image_PngImageOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_PngImageOptions_New()
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

        _lib.PdfToolsPdf2Image_PngImageOptions_GetBackground.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_PngImageOptions_GetBackground.restype = c_int
        ret_val = _lib.PdfToolsPdf2Image_PngImageOptions_GetBackground(self._handle)
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
        _lib.PdfToolsPdf2Image_PngImageOptions_SetBackground.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf2Image_PngImageOptions_SetBackground.restype = c_bool
        if not _lib.PdfToolsPdf2Image_PngImageOptions_SetBackground(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def color_space(self) -> PngColorSpace:
        """
        The color space of the output image

         
        Get or set the color space.
         
        Default is :attr:`pdftools_sdk.pdf2_image.png_color_space.PngColorSpace.RGB` 



        Returns:
            pdftools_sdk.pdf2_image.png_color_space.PngColorSpace

        """
        from pdftools_sdk.pdf2_image.png_color_space import PngColorSpace

        _lib.PdfToolsPdf2Image_PngImageOptions_GetColorSpace.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_PngImageOptions_GetColorSpace.restype = c_int
        ret_val = _lib.PdfToolsPdf2Image_PngImageOptions_GetColorSpace(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return PngColorSpace(ret_val)



    @color_space.setter
    def color_space(self, val: PngColorSpace) -> None:
        """
        The color space of the output image

         
        Get or set the color space.
         
        Default is :attr:`pdftools_sdk.pdf2_image.png_color_space.PngColorSpace.RGB` 



        Args:
            val (pdftools_sdk.pdf2_image.png_color_space.PngColorSpace):
                property value

        """
        from pdftools_sdk.pdf2_image.png_color_space import PngColorSpace

        if not isinstance(val, PngColorSpace):
            raise TypeError(f"Expected type {PngColorSpace.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_PngImageOptions_SetColorSpace.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf2Image_PngImageOptions_SetColorSpace.restype = c_bool
        if not _lib.PdfToolsPdf2Image_PngImageOptions_SetColorSpace(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return PngImageOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = PngImageOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
