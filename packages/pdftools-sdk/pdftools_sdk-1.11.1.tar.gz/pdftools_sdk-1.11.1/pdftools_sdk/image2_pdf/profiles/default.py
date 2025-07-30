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
import pdftools_sdk.image2_pdf.profiles.profile

if TYPE_CHECKING:
    from pdftools_sdk.pdf.conformance import Conformance

else:
    Conformance = "pdftools_sdk.pdf.conformance.Conformance"


class Default(pdftools_sdk.image2_pdf.profiles.profile.Profile):
    """
    The default profile for image to PDF conversion

    This profile is suitable for the conversion of input images to PDF.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsImage2PdfProfiles_Default_New.argtypes = []
        _lib.PdfToolsImage2PdfProfiles_Default_New.restype = c_void_p
        ret_val = _lib.PdfToolsImage2PdfProfiles_Default_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def conformance(self) -> Conformance:
        """
        The PDF conformance of the output document

         
        All PDF conformances are supported.
        For PDF/A the :class:`pdftools_sdk.image2_pdf.profiles.archive.Archive`  profile must be used.
         
        Default value: "PDF 1.7"



        Returns:
            pdftools_sdk.pdf.conformance.Conformance

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsImage2PdfProfiles_Default_GetConformance.argtypes = [c_void_p]
        _lib.PdfToolsImage2PdfProfiles_Default_GetConformance.restype = c_int
        ret_val = _lib.PdfToolsImage2PdfProfiles_Default_GetConformance(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Conformance(ret_val)



    @conformance.setter
    def conformance(self, val: Conformance) -> None:
        """
        The PDF conformance of the output document

         
        All PDF conformances are supported.
        For PDF/A the :class:`pdftools_sdk.image2_pdf.profiles.archive.Archive`  profile must be used.
         
        Default value: "PDF 1.7"



        Args:
            val (pdftools_sdk.pdf.conformance.Conformance):
                property value

        Raises:
            ValueError:
                The conformance is PDF/A but must be PDF for this profile.
                Use the profile :class:`pdftools_sdk.image2_pdf.profiles.archive.Archive`  to create PDF/A documents.


        """
        from pdftools_sdk.pdf.conformance import Conformance

        if not isinstance(val, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsImage2PdfProfiles_Default_SetConformance.argtypes = [c_void_p, c_int]
        _lib.PdfToolsImage2PdfProfiles_Default_SetConformance.restype = c_bool
        if not _lib.PdfToolsImage2PdfProfiles_Default_SetConformance(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Default._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Default.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
