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
    from pdftools_sdk.pdf2_image.image_options import ImageOptions
    from pdftools_sdk.pdf2_image.render_page_at_resolution import RenderPageAtResolution

else:
    ImageOptions = "pdftools_sdk.pdf2_image.image_options.ImageOptions"
    RenderPageAtResolution = "pdftools_sdk.pdf2_image.render_page_at_resolution.RenderPageAtResolution"


class Archive(pdftools_sdk.pdf2_image.profiles.profile.Profile):
    """
    The profile to convert PDF documents to TIFF images for archiving

     
    This profile is suitable for archiving PDF documents as rasterized images.
     
    The output format is TIFF and cannot be changed.
    Several compression types are configurable through
    :attr:`pdftools_sdk.pdf2_image.profiles.archive.Archive.image_options` .
     
    By default,
     
    - :attr:`pdftools_sdk.pdf2_image.profiles.archive.Archive.image_options`  is set to
      :class:`pdftools_sdk.pdf2_image.tiff_lzw_image_options.TiffLzwImageOptions`
    - the color space of each image corresponds to the color
      space of the PDF page
     


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf2ImageProfiles_Archive_New.argtypes = []
        _lib.PdfToolsPdf2ImageProfiles_Archive_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Archive_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def image_options(self) -> ImageOptions:
        """
        The settings for the output TIFF

         
        Defines the compression algorithm of the TIFF output image.
         
        Supported types are:
         
        - :class:`pdftools_sdk.pdf2_image.tiff_jpeg_image_options.TiffJpegImageOptions`
        - :class:`pdftools_sdk.pdf2_image.tiff_lzw_image_options.TiffLzwImageOptions`
        - :class:`pdftools_sdk.pdf2_image.tiff_flate_image_options.TiffFlateImageOptions`
         
         
        Default is :class:`pdftools_sdk.pdf2_image.tiff_lzw_image_options.TiffLzwImageOptions` 



        Returns:
            pdftools_sdk.pdf2_image.image_options.ImageOptions

        """
        from pdftools_sdk.pdf2_image.image_options import ImageOptions

        _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageOptions.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageOptions.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageOptions._create_dynamic_type(ret_val)


    @image_options.setter
    def image_options(self, val: ImageOptions) -> None:
        """
        The settings for the output TIFF

         
        Defines the compression algorithm of the TIFF output image.
         
        Supported types are:
         
        - :class:`pdftools_sdk.pdf2_image.tiff_jpeg_image_options.TiffJpegImageOptions`
        - :class:`pdftools_sdk.pdf2_image.tiff_lzw_image_options.TiffLzwImageOptions`
        - :class:`pdftools_sdk.pdf2_image.tiff_flate_image_options.TiffFlateImageOptions`
         
         
        Default is :class:`pdftools_sdk.pdf2_image.tiff_lzw_image_options.TiffLzwImageOptions` 



        Args:
            val (pdftools_sdk.pdf2_image.image_options.ImageOptions):
                property value

        Raises:
            ValueError:
                The given object has the wrong type.


        """
        from pdftools_sdk.pdf2_image.image_options import ImageOptions

        if not isinstance(val, ImageOptions):
            raise TypeError(f"Expected type {ImageOptions.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2ImageProfiles_Archive_SetImageOptions.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Archive_SetImageOptions.restype = c_bool
        if not _lib.PdfToolsPdf2ImageProfiles_Archive_SetImageOptions(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def image_section_mapping(self) -> RenderPageAtResolution:
        """
        The image section mapping

         
        This property defines the resolution of the output images.
         
        Default is 300 DPI.



        Returns:
            pdftools_sdk.pdf2_image.render_page_at_resolution.RenderPageAtResolution

        """
        from pdftools_sdk.pdf2_image.render_page_at_resolution import RenderPageAtResolution

        _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageSectionMapping.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageSectionMapping.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Archive_GetImageSectionMapping(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return RenderPageAtResolution._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Archive._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Archive.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
