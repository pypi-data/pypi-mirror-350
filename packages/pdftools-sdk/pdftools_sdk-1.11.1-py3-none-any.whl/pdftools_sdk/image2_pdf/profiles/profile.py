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
    from pdftools_sdk.image2_pdf.image_options import ImageOptions

else:
    ImageOptions = "pdftools_sdk.image2_pdf.image_options.ImageOptions"


class Profile(_NativeObject, ABC):
    """
    The base class for image to PDF conversion profiles

    A profile implements the conversion settings suitable for a practical
    use case.


    """
    @property
    def image_options(self) -> ImageOptions:
        """
        The image conversion options



        Returns:
            pdftools_sdk.image2_pdf.image_options.ImageOptions

        """
        from pdftools_sdk.image2_pdf.image_options import ImageOptions

        _lib.PdfToolsImage2PdfProfiles_Profile_GetImageOptions.argtypes = [c_void_p]
        _lib.PdfToolsImage2PdfProfiles_Profile_GetImageOptions.restype = c_void_p
        ret_val = _lib.PdfToolsImage2PdfProfiles_Profile_GetImageOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageOptions._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsImage2PdfProfiles_Profile_GetType.argtypes = [c_void_p]
        _lib.PdfToolsImage2PdfProfiles_Profile_GetType.restype = c_int

        obj_type = _lib.PdfToolsImage2PdfProfiles_Profile_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Profile._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.image2_pdf.profiles.default import Default 
            return Default._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.image2_pdf.profiles.archive import Archive 
            return Archive._from_handle(handle)
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
