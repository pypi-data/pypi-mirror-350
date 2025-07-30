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
import pdftools_sdk.pdf2_image.image_section_mapping

if TYPE_CHECKING:
    from pdftools_sdk.geometry.integer.size import Size

else:
    Size = "pdftools_sdk.geometry.integer.size.Size"


class RenderPageToMaxImageSize(pdftools_sdk.pdf2_image.image_section_mapping.ImageSectionMapping):
    """
    The image section mapping to render entire pages using a specific image pixel size

     
    Render a PDF page and scale it, thereby preserving the aspect
    ratio, to fit best on the target image size. The image size is
    specified in number of pixels.
     
    For example, this mapping is suitable to create thumbnail images.


    """
    def __init__(self, size: Size):
        """

        Args:
            size (pdftools_sdk.geometry.integer.size.Size): 
                The maximum size of the image in pixels.



        Raises:
            ValueError:
                The dimensions of `size` are smaller than 1.


        """
        from pdftools_sdk.geometry.integer.size import Size

        if not isinstance(size, Size):
            raise TypeError(f"Expected type {Size.__name__}, but got {type(size).__name__}.")

        _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_New.argtypes = [POINTER(Size)]
        _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_New(size)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def size(self) -> Size:
        """
        The maximum size of the image in pixels

         
        Set or get the image size.
         
        The dimensions of `size` must be 1 or greater.



        Returns:
            pdftools_sdk.geometry.integer.size.Size

        """
        from pdftools_sdk.geometry.integer.size import Size

        _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_GetSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_GetSize.restype = c_bool
        ret_val = Size()
        if not _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_GetSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @size.setter
    def size(self, val: Size) -> None:
        """
        The maximum size of the image in pixels

         
        Set or get the image size.
         
        The dimensions of `size` must be 1 or greater.



        Args:
            val (pdftools_sdk.geometry.integer.size.Size):
                property value

        Raises:
            ValueError:
                The dimensions of `size` are smaller than 1.


        """
        from pdftools_sdk.geometry.integer.size import Size

        if not isinstance(val, Size):
            raise TypeError(f"Expected type {Size.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_SetSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_SetSize.restype = c_bool
        if not _lib.PdfToolsPdf2Image_RenderPageToMaxImageSize_SetSize(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return RenderPageToMaxImageSize._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = RenderPageToMaxImageSize.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
