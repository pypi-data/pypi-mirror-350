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
import pdftools_sdk.optimization.profiles.profile

class Print(pdftools_sdk.optimization.profiles.profile.Profile):
    """
    The optimization profile suitable for printing

     
    All colors are converted to CMYK for optimal output on printing devices.
    Spider (web capture) information is removed.
    Embedded Type1 (PostScript) fonts are converted to Type1C
    (Compact Font Format) which further reduces the file size.
    The resolution of images stays untouched.
     
    When an image is recompressed, the
    :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY` 
    strategy is used; this can be overridden through the
    property :attr:`pdftools_sdk.optimization.profiles.profile.Profile.image_recompression_options` .
     
    With this profile, the output PDF version is updated to PDF 1.7 or higher and
    PDF/A conformance removed.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsOptimizationProfiles_Print_New.argtypes = []
        _lib.PdfToolsOptimizationProfiles_Print_New.restype = c_void_p
        ret_val = _lib.PdfToolsOptimizationProfiles_Print_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @staticmethod
    def _create_dynamic_type(handle):
        return Print._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Print.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
