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

class ImageSectionMapping(_NativeObject, ABC):
    """
    The base class for image section mappings

    An image section mapping specifies how a PDF page, or a section of
    it, is transformed (e.g. cropped or scaled) and placed
    onto the target image.


    """
    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf2Image_ImageSectionMapping_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_ImageSectionMapping_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf2Image_ImageSectionMapping_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return ImageSectionMapping._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.pdf2_image.render_page_as_fax import RenderPageAsFax 
            return RenderPageAsFax._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.pdf2_image.render_page_at_resolution import RenderPageAtResolution 
            return RenderPageAtResolution._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.pdf2_image.render_page_to_max_image_size import RenderPageToMaxImageSize 
            return RenderPageToMaxImageSize._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ImageSectionMapping.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
