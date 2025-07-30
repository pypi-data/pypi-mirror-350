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
import pdftools_sdk.pdf2_image.profiles.profile

if TYPE_CHECKING:
    from pdftools_sdk.pdf2_image.fax_image_options import FaxImageOptions
    from pdftools_sdk.pdf2_image.render_page_as_fax import RenderPageAsFax

else:
    FaxImageOptions = "pdftools_sdk.pdf2_image.fax_image_options.FaxImageOptions"
    RenderPageAsFax = "pdftools_sdk.pdf2_image.render_page_as_fax.RenderPageAsFax"


class Fax(pdftools_sdk.pdf2_image.profiles.profile.Profile):
    """
    The profile to convert PDF documents to TIFF Fax images

     
    This profile is suitable for converting PDFs into
    TIFF-F conforming rasterized images for Facsimile transmission.
     
    The output format is a multi-page TIFF file containing all
    rasterized PDF pages.
     
    By default,
     
    - the output images are Group 3 - compressed
    - scaled to a width of 1728 pixels, a horizontal
      resolution of 204 DPI, and a vertical resolution
      of 98 DPI
    - all colors and gray scale tones are converted
      to bitonal by using dithering
     
     
    The compression type and the vertical resolution can be set
    through :attr:`pdftools_sdk.pdf2_image.profiles.fax.Fax.image_options` .


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf2ImageProfiles_Fax_New.argtypes = []
        _lib.PdfToolsPdf2ImageProfiles_Fax_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Fax_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def image_options(self) -> FaxImageOptions:
        """
        The settings for the output image



        Returns:
            pdftools_sdk.pdf2_image.fax_image_options.FaxImageOptions

        """
        from pdftools_sdk.pdf2_image.fax_image_options import FaxImageOptions

        _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageOptions.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageOptions.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FaxImageOptions._create_dynamic_type(ret_val)


    @property
    def image_section_mapping(self) -> RenderPageAsFax:
        """
        The image section mapping

        This property specifies how a PDF page is placed onto the target image.



        Returns:
            pdftools_sdk.pdf2_image.render_page_as_fax.RenderPageAsFax

        """
        from pdftools_sdk.pdf2_image.render_page_as_fax import RenderPageAsFax

        _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageSectionMapping.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageSectionMapping.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Fax_GetImageSectionMapping(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return RenderPageAsFax._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Fax._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Fax.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
