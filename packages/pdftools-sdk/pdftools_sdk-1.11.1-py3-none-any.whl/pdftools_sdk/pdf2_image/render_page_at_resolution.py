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
    from pdftools_sdk.geometry.units.resolution import Resolution

else:
    Resolution = "pdftools_sdk.geometry.units.resolution.Resolution"


class RenderPageAtResolution(pdftools_sdk.pdf2_image.image_section_mapping.ImageSectionMapping):
    """
    The image section mapping to render entire pages at a specific resolution

     
    The entire PDF page is rendered into an image of the same size and the specified resolution.
     
    For example, this mapping is suitable to create images of entire PDF pages.


    """
    def __init__(self, resolution: Resolution):
        """

        Args:
            resolution (pdftools_sdk.geometry.units.resolution.Resolution): 
                The resolution of the output image.



        Raises:
            ValueError:
                The resolution is smaller than 0.0 or greater than 10000.0.


        """
        from pdftools_sdk.geometry.units.resolution import Resolution

        if not isinstance(resolution, Resolution):
            raise TypeError(f"Expected type {Resolution.__name__}, but got {type(resolution).__name__}.")

        _lib.PdfToolsPdf2Image_RenderPageAtResolution_New.argtypes = [POINTER(Resolution)]
        _lib.PdfToolsPdf2Image_RenderPageAtResolution_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_RenderPageAtResolution_New(resolution)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def resolution(self) -> Resolution:
        """
        The resolution of the output image

        Valid values are 0.0, 10000.0 or in between.



        Returns:
            pdftools_sdk.geometry.units.resolution.Resolution

        """
        from pdftools_sdk.geometry.units.resolution import Resolution

        _lib.PdfToolsPdf2Image_RenderPageAtResolution_GetResolution.argtypes = [c_void_p, POINTER(Resolution)]
        _lib.PdfToolsPdf2Image_RenderPageAtResolution_GetResolution.restype = c_bool
        ret_val = Resolution()
        if not _lib.PdfToolsPdf2Image_RenderPageAtResolution_GetResolution(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @resolution.setter
    def resolution(self, val: Resolution) -> None:
        """
        The resolution of the output image

        Valid values are 0.0, 10000.0 or in between.



        Args:
            val (pdftools_sdk.geometry.units.resolution.Resolution):
                property value

        """
        from pdftools_sdk.geometry.units.resolution import Resolution

        if not isinstance(val, Resolution):
            raise TypeError(f"Expected type {Resolution.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_RenderPageAtResolution_SetResolution.argtypes = [c_void_p, POINTER(Resolution)]
        _lib.PdfToolsPdf2Image_RenderPageAtResolution_SetResolution.restype = c_bool
        if not _lib.PdfToolsPdf2Image_RenderPageAtResolution_SetResolution(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return RenderPageAtResolution._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = RenderPageAtResolution.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
