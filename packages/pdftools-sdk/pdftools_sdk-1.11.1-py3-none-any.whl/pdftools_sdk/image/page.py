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

if TYPE_CHECKING:
    from pdftools_sdk.geometry.integer.size import Size
    from pdftools_sdk.geometry.units.resolution import Resolution

else:
    Size = "pdftools_sdk.geometry.integer.size.Size"
    Resolution = "pdftools_sdk.geometry.units.resolution.Resolution"


class Page(_NativeObject):
    """
    The page of an image document


    """
    @property
    def size(self) -> Size:
        """
        The size of the page in number of pixels



        Returns:
            pdftools_sdk.geometry.integer.size.Size

        Raises:
            pdftools_sdk.generic_error.GenericError:
                A generic error occurred.


        """
        from pdftools_sdk.geometry.integer.size import Size

        _lib.PdfToolsImage_Page_GetSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PdfToolsImage_Page_GetSize.restype = c_bool
        ret_val = Size()
        if not _lib.PdfToolsImage_Page_GetSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def resolution(self) -> Optional[Resolution]:
        """
        The resolution of the page

        The resolution can be `None` if the image does not specify a resolution.



        Returns:
            Optional[pdftools_sdk.geometry.units.resolution.Resolution]

        Raises:
            pdftools_sdk.generic_error.GenericError:
                A generic error occurred.


        """
        from pdftools_sdk.geometry.units.resolution import Resolution

        _lib.PdfToolsImage_Page_GetResolution.argtypes = [c_void_p, POINTER(Resolution)]
        _lib.PdfToolsImage_Page_GetResolution.restype = c_bool
        ret_val = Resolution()
        if not _lib.PdfToolsImage_Page_GetResolution(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val



    @staticmethod
    def _create_dynamic_type(handle):
        return Page._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Page.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
