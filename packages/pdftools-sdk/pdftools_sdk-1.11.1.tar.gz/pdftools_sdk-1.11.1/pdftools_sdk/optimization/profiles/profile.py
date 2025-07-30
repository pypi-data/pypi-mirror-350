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
    from pdftools_sdk.optimization.image_recompression_options import ImageRecompressionOptions
    from pdftools_sdk.optimization.font_options import FontOptions
    from pdftools_sdk.optimization.removal_options import RemovalOptions

else:
    ImageRecompressionOptions = "pdftools_sdk.optimization.image_recompression_options.ImageRecompressionOptions"
    FontOptions = "pdftools_sdk.optimization.font_options.FontOptions"
    RemovalOptions = "pdftools_sdk.optimization.removal_options.RemovalOptions"


class Profile(_NativeObject, ABC):
    """
    The base class for PDF optimization profiles

    The profile defines the optimization parameters suitable for a particular
    use case, e.g. archiving, or publication on the web.


    """
    @property
    def image_recompression_options(self) -> ImageRecompressionOptions:
        """
        The image recompression options



        Returns:
            pdftools_sdk.optimization.image_recompression_options.ImageRecompressionOptions

        """
        from pdftools_sdk.optimization.image_recompression_options import ImageRecompressionOptions

        _lib.PdfToolsOptimizationProfiles_Profile_GetImageRecompressionOptions.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_Profile_GetImageRecompressionOptions.restype = c_void_p
        ret_val = _lib.PdfToolsOptimizationProfiles_Profile_GetImageRecompressionOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageRecompressionOptions._create_dynamic_type(ret_val)


    @property
    def font_options(self) -> FontOptions:
        """
        The font optimization options



        Returns:
            pdftools_sdk.optimization.font_options.FontOptions

        """
        from pdftools_sdk.optimization.font_options import FontOptions

        _lib.PdfToolsOptimizationProfiles_Profile_GetFontOptions.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_Profile_GetFontOptions.restype = c_void_p
        ret_val = _lib.PdfToolsOptimizationProfiles_Profile_GetFontOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FontOptions._create_dynamic_type(ret_val)


    @property
    def removal_options(self) -> RemovalOptions:
        """
        The parameters defining the optional data to remove or flatten



        Returns:
            pdftools_sdk.optimization.removal_options.RemovalOptions

        """
        from pdftools_sdk.optimization.removal_options import RemovalOptions

        _lib.PdfToolsOptimizationProfiles_Profile_GetRemovalOptions.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_Profile_GetRemovalOptions.restype = c_void_p
        ret_val = _lib.PdfToolsOptimizationProfiles_Profile_GetRemovalOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return RemovalOptions._create_dynamic_type(ret_val)


    @property
    def copy_metadata(self) -> bool:
        """
        Whether to copy metadata

        Copy document information dictionary and XMP metadata.
        Default: `True`.



        Returns:
            bool

        """
        _lib.PdfToolsOptimizationProfiles_Profile_GetCopyMetadata.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_Profile_GetCopyMetadata.restype = c_bool
        ret_val = _lib.PdfToolsOptimizationProfiles_Profile_GetCopyMetadata(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_metadata.setter
    def copy_metadata(self, val: bool) -> None:
        """
        Whether to copy metadata

        Copy document information dictionary and XMP metadata.
        Default: `True`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimizationProfiles_Profile_SetCopyMetadata.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimizationProfiles_Profile_SetCopyMetadata.restype = c_bool
        if not _lib.PdfToolsOptimizationProfiles_Profile_SetCopyMetadata(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsOptimizationProfiles_Profile_GetType.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_Profile_GetType.restype = c_int

        obj_type = _lib.PdfToolsOptimizationProfiles_Profile_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Profile._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.optimization.profiles.web import Web 
            return Web._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.optimization.profiles.print import Print 
            return Print._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.optimization.profiles.archive import Archive 
            return Archive._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.optimization.profiles.minimal_file_size import MinimalFileSize 
            return MinimalFileSize._from_handle(handle)
        elif obj_type == 5:
            from pdftools_sdk.optimization.profiles.mrc import Mrc 
            return Mrc._from_handle(handle)
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
