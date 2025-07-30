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
from abc import ABC

import pdftools_sdk.internal

class ImageOptions(_NativeObject, ABC):
    """
    The base class for output image options


    """
    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf2Image_ImageOptions_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_ImageOptions_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf2Image_ImageOptions_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return ImageOptions._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.pdf2_image.fax_image_options import FaxImageOptions 
            return FaxImageOptions._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.pdf2_image.tiff_jpeg_image_options import TiffJpegImageOptions 
            return TiffJpegImageOptions._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.pdf2_image.tiff_lzw_image_options import TiffLzwImageOptions 
            return TiffLzwImageOptions._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.pdf2_image.tiff_flate_image_options import TiffFlateImageOptions 
            return TiffFlateImageOptions._from_handle(handle)
        elif obj_type == 5:
            from pdftools_sdk.pdf2_image.png_image_options import PngImageOptions 
            return PngImageOptions._from_handle(handle)
        elif obj_type == 6:
            from pdftools_sdk.pdf2_image.jpeg_image_options import JpegImageOptions 
            return JpegImageOptions._from_handle(handle)
        else:
            return None


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
