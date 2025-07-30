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
import pdftools_sdk.image.document

if TYPE_CHECKING:
    from pdftools_sdk.image.page import Page

else:
    Page = "pdftools_sdk.image.page.Page"


class SinglePageDocument(pdftools_sdk.image.document.Document):
    """
    The image document of an image format that only supports single-page images

    This class is used for the following image formats:
     
    - JPEG
    - BMP
    - GIF
    - HEIC/HEIF
    - PNG
    - JBIG2
    - JPEG2000
     


    """
    @property
    def page(self) -> Page:
        """
        The page of the image



        Returns:
            pdftools_sdk.image.page.Page

        """
        from pdftools_sdk.image.page import Page

        _lib.PdfToolsImage_SinglePageDocument_GetPage.argtypes = [c_void_p]
        _lib.PdfToolsImage_SinglePageDocument_GetPage.restype = c_void_p
        ret_val = _lib.PdfToolsImage_SinglePageDocument_GetPage(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Page._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return SinglePageDocument._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SinglePageDocument.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
