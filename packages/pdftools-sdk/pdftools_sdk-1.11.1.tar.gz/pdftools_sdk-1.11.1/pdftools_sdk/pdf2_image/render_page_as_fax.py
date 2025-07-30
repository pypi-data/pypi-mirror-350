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

class RenderPageAsFax(pdftools_sdk.pdf2_image.image_section_mapping.ImageSectionMapping):
    """
    The image section mapping suitable for Fax output images

     
    Render a PDF page without scaling onto the image, top-aligned
    and horizontally centered.
     
    Note that, the image has a fixed width of 1728 pixels / 8.5 inches.
     
    A page larger than the target image is scaled down to fit in.


    """
    @staticmethod
    def _create_dynamic_type(handle):
        return RenderPageAsFax._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = RenderPageAsFax.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
