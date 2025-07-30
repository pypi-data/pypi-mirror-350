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
    from pdftools_sdk.pdf2_image.image_section_mapping import ImageSectionMapping

else:
    ImageOptions = "pdftools_sdk.pdf2_image.image_options.ImageOptions"
    ImageSectionMapping = "pdftools_sdk.pdf2_image.image_section_mapping.ImageSectionMapping"


class Viewing(pdftools_sdk.pdf2_image.profiles.profile.Profile):
    """
    The profile to convert PDF documents to JPEG or PNG images for viewing

     
    This profile is suitable for converting PDFs to
    rasterized images for using in web and desktop viewing
    applications or as thumbnails.
     
    By default, :attr:`pdftools_sdk.pdf2_image.profiles.viewing.Viewing.image_options`  is set to
    :class:`pdftools_sdk.pdf2_image.png_image_options.PngImageOptions`  which uses the output format
    PNG and lossless compression.
    If set to :class:`pdftools_sdk.pdf2_image.jpeg_image_options.JpegImageOptions` , the output format
    is JPEG.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf2ImageProfiles_Viewing_New.argtypes = []
        _lib.PdfToolsPdf2ImageProfiles_Viewing_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Viewing_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def image_options(self) -> ImageOptions:
        """
        The settings for the output image

         
        Supported types are:
         
        - :class:`pdftools_sdk.pdf2_image.png_image_options.PngImageOptions`  to create PNG images
        - :class:`pdftools_sdk.pdf2_image.jpeg_image_options.JpegImageOptions`  to create JPEG images
         
         
        Default is :class:`pdftools_sdk.pdf2_image.png_image_options.PngImageOptions` 



        Returns:
            pdftools_sdk.pdf2_image.image_options.ImageOptions

        """
        from pdftools_sdk.pdf2_image.image_options import ImageOptions

        _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageOptions.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageOptions.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageOptions._create_dynamic_type(ret_val)


    @image_options.setter
    def image_options(self, val: ImageOptions) -> None:
        """
        The settings for the output image

         
        Supported types are:
         
        - :class:`pdftools_sdk.pdf2_image.png_image_options.PngImageOptions`  to create PNG images
        - :class:`pdftools_sdk.pdf2_image.jpeg_image_options.JpegImageOptions`  to create JPEG images
         
         
        Default is :class:`pdftools_sdk.pdf2_image.png_image_options.PngImageOptions` 



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
        _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageOptions.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageOptions.restype = c_bool
        if not _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageOptions(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def image_section_mapping(self) -> ImageSectionMapping:
        """
        The image section mapping

         
        This property specifies how a PDF page is placed onto the target image.
         
        Supported types are:
         
        - :class:`pdftools_sdk.pdf2_image.render_page_at_resolution.RenderPageAtResolution`  to define the resolution of the output images.
        - :class:`pdftools_sdk.pdf2_image.render_page_to_max_image_size.RenderPageToMaxImageSize`  to define the maximum image size of the output images.
         
         
        Default is :class:`pdftools_sdk.pdf2_image.render_page_at_resolution.RenderPageAtResolution`  with 150 DPI.



        Returns:
            pdftools_sdk.pdf2_image.image_section_mapping.ImageSectionMapping

        """
        from pdftools_sdk.pdf2_image.image_section_mapping import ImageSectionMapping

        _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageSectionMapping.argtypes = [c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageSectionMapping.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2ImageProfiles_Viewing_GetImageSectionMapping(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageSectionMapping._create_dynamic_type(ret_val)


    @image_section_mapping.setter
    def image_section_mapping(self, val: ImageSectionMapping) -> None:
        """
        The image section mapping

         
        This property specifies how a PDF page is placed onto the target image.
         
        Supported types are:
         
        - :class:`pdftools_sdk.pdf2_image.render_page_at_resolution.RenderPageAtResolution`  to define the resolution of the output images.
        - :class:`pdftools_sdk.pdf2_image.render_page_to_max_image_size.RenderPageToMaxImageSize`  to define the maximum image size of the output images.
         
         
        Default is :class:`pdftools_sdk.pdf2_image.render_page_at_resolution.RenderPageAtResolution`  with 150 DPI.



        Args:
            val (pdftools_sdk.pdf2_image.image_section_mapping.ImageSectionMapping):
                property value

        Raises:
            ValueError:
                The given object has the wrong type.


        """
        from pdftools_sdk.pdf2_image.image_section_mapping import ImageSectionMapping

        if not isinstance(val, ImageSectionMapping):
            raise TypeError(f"Expected type {ImageSectionMapping.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageSectionMapping.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageSectionMapping.restype = c_bool
        if not _lib.PdfToolsPdf2ImageProfiles_Viewing_SetImageSectionMapping(self._handle, val._handle):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Viewing._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Viewing.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
