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

if TYPE_CHECKING:
    from pdftools_sdk.pdf2_image.content_options import ContentOptions

else:
    ContentOptions = "pdftools_sdk.pdf2_image.content_options.ContentOptions"


class Profile(_NativeObject, ABC):
    """
    The base class for PDF to image conversion profiles

    The profile defines how the PDF pages are rendered and what type of output image is used.
    A profile implements the converter settings suitable for a practical
    use case, e.g. create images for sending over Facsimile, for
    viewing, or for archiving.


    """
    @property
    def content_options(self) -> ContentOptions:
        """
        The parameters how to render PDF content elements



        Returns:
            pdftools_sdk.pdf2_image.content_options.ContentOptions

        """
        from pdftools_sdk.pdf2_image.content_options import ContentOptions

        _lib.PdfToolsPdf2ImageProfiles_Profile_GetContentOptions.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Profile_GetContentOptions.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Profile_GetContentOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ContentOptions._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf2ImageProfiles_Profile_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Profile_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf2ImageProfiles_Profile_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Profile._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.pdf2_image.profiles.fax import Fax 
            return Fax._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.pdf2_image.profiles.archive import Archive 
            return Archive._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.pdf2_image.profiles.viewing import Viewing 
            return Viewing._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Profile.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
