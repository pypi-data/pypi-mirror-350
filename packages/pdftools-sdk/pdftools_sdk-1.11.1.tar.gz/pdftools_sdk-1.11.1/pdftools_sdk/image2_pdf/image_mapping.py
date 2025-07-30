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

class ImageMapping(_NativeObject, ABC):
    """
    The base class for image mappings

    The image mapping specifies how an input image is transformed and placed
    onto the output PDF page.


    """
    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsImage2Pdf_ImageMapping_GetType.argtypes = [c_void_p]
        _lib.PdfToolsImage2Pdf_ImageMapping_GetType.restype = c_int

        obj_type = _lib.PdfToolsImage2Pdf_ImageMapping_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return ImageMapping._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.image2_pdf.auto import Auto 
            return Auto._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.image2_pdf.shrink_to_page import ShrinkToPage 
            return ShrinkToPage._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.image2_pdf.shrink_to_fit import ShrinkToFit 
            return ShrinkToFit._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.image2_pdf.shrink_to_portrait import ShrinkToPortrait 
            return ShrinkToPortrait._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ImageMapping.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
