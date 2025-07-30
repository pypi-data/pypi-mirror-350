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
import pdftools_sdk.pdf2_image.image_options

if TYPE_CHECKING:
    from pdftools_sdk.pdf2_image.fax_vertical_resolution import FaxVerticalResolution
    from pdftools_sdk.pdf2_image.tiff_bitonal_compression_type import TiffBitonalCompressionType

else:
    FaxVerticalResolution = "pdftools_sdk.pdf2_image.fax_vertical_resolution.FaxVerticalResolution"
    TiffBitonalCompressionType = "pdftools_sdk.pdf2_image.tiff_bitonal_compression_type.TiffBitonalCompressionType"


class FaxImageOptions(pdftools_sdk.pdf2_image.image_options.ImageOptions):
    """
    The settings for TIFF Fax output images

    Create a black-and-white (bitonal) TIFF Fax output image.
    For the output file name, it is recommended to use the file extension ".tif".


    """
    @property
    def vertical_resolution(self) -> FaxVerticalResolution:
        """
        The vertical image resolution

         
        This property allows a choice of which vertical
        resolution to use.
        For details, see :class:`pdftools_sdk.pdf2_image.fax_vertical_resolution.FaxVerticalResolution` .
         
        Note that the horizontal resolution is fixed at 204 DPI by the
        Fax standard.
         
        Default is :attr:`pdftools_sdk.pdf2_image.fax_vertical_resolution.FaxVerticalResolution.STANDARD` 



        Returns:
            pdftools_sdk.pdf2_image.fax_vertical_resolution.FaxVerticalResolution

        """
        from pdftools_sdk.pdf2_image.fax_vertical_resolution import FaxVerticalResolution

        _lib.PdfToolsPdf2Image_FaxImageOptions_GetVerticalResolution.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_FaxImageOptions_GetVerticalResolution.restype = c_int
        ret_val = _lib.PdfToolsPdf2Image_FaxImageOptions_GetVerticalResolution(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return FaxVerticalResolution(ret_val)



    @vertical_resolution.setter
    def vertical_resolution(self, val: FaxVerticalResolution) -> None:
        """
        The vertical image resolution

         
        This property allows a choice of which vertical
        resolution to use.
        For details, see :class:`pdftools_sdk.pdf2_image.fax_vertical_resolution.FaxVerticalResolution` .
         
        Note that the horizontal resolution is fixed at 204 DPI by the
        Fax standard.
         
        Default is :attr:`pdftools_sdk.pdf2_image.fax_vertical_resolution.FaxVerticalResolution.STANDARD` 



        Args:
            val (pdftools_sdk.pdf2_image.fax_vertical_resolution.FaxVerticalResolution):
                property value

        """
        from pdftools_sdk.pdf2_image.fax_vertical_resolution import FaxVerticalResolution

        if not isinstance(val, FaxVerticalResolution):
            raise TypeError(f"Expected type {FaxVerticalResolution.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_FaxImageOptions_SetVerticalResolution.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf2Image_FaxImageOptions_SetVerticalResolution.restype = c_bool
        if not _lib.PdfToolsPdf2Image_FaxImageOptions_SetVerticalResolution(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def compression(self) -> TiffBitonalCompressionType:
        """
        The Fax compression algorithm

         
        This property allows a choice of which compression
        type to use.
        For details, see :class:`pdftools_sdk.pdf2_image.tiff_bitonal_compression_type.TiffBitonalCompressionType` .
         
        Default is :attr:`pdftools_sdk.pdf2_image.tiff_bitonal_compression_type.TiffBitonalCompressionType.G3` 



        Returns:
            pdftools_sdk.pdf2_image.tiff_bitonal_compression_type.TiffBitonalCompressionType

        """
        from pdftools_sdk.pdf2_image.tiff_bitonal_compression_type import TiffBitonalCompressionType

        _lib.PdfToolsPdf2Image_FaxImageOptions_GetCompression.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_FaxImageOptions_GetCompression.restype = c_int
        ret_val = _lib.PdfToolsPdf2Image_FaxImageOptions_GetCompression(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return TiffBitonalCompressionType(ret_val)



    @compression.setter
    def compression(self, val: TiffBitonalCompressionType) -> None:
        """
        The Fax compression algorithm

         
        This property allows a choice of which compression
        type to use.
        For details, see :class:`pdftools_sdk.pdf2_image.tiff_bitonal_compression_type.TiffBitonalCompressionType` .
         
        Default is :attr:`pdftools_sdk.pdf2_image.tiff_bitonal_compression_type.TiffBitonalCompressionType.G3` 



        Args:
            val (pdftools_sdk.pdf2_image.tiff_bitonal_compression_type.TiffBitonalCompressionType):
                property value

        """
        from pdftools_sdk.pdf2_image.tiff_bitonal_compression_type import TiffBitonalCompressionType

        if not isinstance(val, TiffBitonalCompressionType):
            raise TypeError(f"Expected type {TiffBitonalCompressionType.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_FaxImageOptions_SetCompression.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf2Image_FaxImageOptions_SetCompression.restype = c_bool
        if not _lib.PdfToolsPdf2Image_FaxImageOptions_SetCompression(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return FaxImageOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = FaxImageOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
