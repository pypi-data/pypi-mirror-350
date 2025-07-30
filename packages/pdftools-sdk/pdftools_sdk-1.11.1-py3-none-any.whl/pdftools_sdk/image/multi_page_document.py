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
    from pdftools_sdk.image.page_list import PageList

else:
    PageList = "pdftools_sdk.image.page_list.PageList"


class MultiPageDocument(pdftools_sdk.image.document.Document):
    """
    The image document of an image format that supports multi-page images

    This class is used for TIFF images, which can contain one or more pages.


    """
    @property
    def pages(self) -> PageList:
        """
        The pages of the image



        Returns:
            pdftools_sdk.image.page_list.PageList

        """
        from pdftools_sdk.image.page_list import PageList

        _lib.PdfToolsImage_MultiPageDocument_GetPages.argtypes = [c_void_p]
        _lib.PdfToolsImage_MultiPageDocument_GetPages.restype = c_void_p
        ret_val = _lib.PdfToolsImage_MultiPageDocument_GetPages(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PageList._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return MultiPageDocument._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = MultiPageDocument.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
