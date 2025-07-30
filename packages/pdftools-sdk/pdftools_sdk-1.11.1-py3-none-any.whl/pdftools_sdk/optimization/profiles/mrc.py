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

class Mrc(pdftools_sdk.optimization.profiles.profile.Profile):
    """
    The optimization profile suitable for documents with Mixed Raster Content

    Reduce the file size for documents containing large images, e.g. scanned pages, while maintaining the readability of text. 
    This is accomplished by separating the images into a foreground, background and a mask layer. 
    The foreground and background layers are heavily down-sampled and compressed. 
    The textual information is stored in the mask with a lossless compression type. 
    Additionally, redundant objects are removed, resources are optimized and embedded fonts are merged.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsOptimizationProfiles_Mrc_New.argtypes = []
        _lib.PdfToolsOptimizationProfiles_Mrc_New.restype = c_void_p
        ret_val = _lib.PdfToolsOptimizationProfiles_Mrc_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def layer_compression_quality(self) -> float:
        """
        The image quality for MRC foreground and background layers

         
        This is a value between `0` (lowest quality) and `1` (highest quality).
         
        Default:
         
        - :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY`  algorithm: `1`.
        - :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`  algorithm: `0.25`.
        - :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.SPEED`  algorithm: `0.25`.
         



        Returns:
            float

        """
        _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerCompressionQuality.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerCompressionQuality.restype = c_double
        ret_val = _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerCompressionQuality(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @layer_compression_quality.setter
    def layer_compression_quality(self, val: float) -> None:
        """
        The image quality for MRC foreground and background layers

         
        This is a value between `0` (lowest quality) and `1` (highest quality).
         
        Default:
         
        - :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY`  algorithm: `1`.
        - :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`  algorithm: `0.25`.
        - :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.SPEED`  algorithm: `0.25`.
         



        Args:
            val (float):
                property value

        Raises:
            ValueError:
                The given value is smaller than `0` or greater than `1`.


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerCompressionQuality.argtypes = [c_void_p, c_double]
        _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerCompressionQuality.restype = c_bool
        if not _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerCompressionQuality(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def layer_resolution_d_p_i(self) -> Optional[float]:
        """
        The target resolution in DPI (dots per inch) for downsampling MRC foreground and background layers

         
        Valid values are 1, or 10000, or in between.
        Set to `None` to deactivate downsampling of images.
         
        Default is `70`.



        Returns:
            Optional[float]

        """
        _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerResolutionDPI.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsOptimizationProfiles_Mrc_GetLayerResolutionDPI(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @layer_resolution_d_p_i.setter
    def layer_resolution_d_p_i(self, val: Optional[float]) -> None:
        """
        The target resolution in DPI (dots per inch) for downsampling MRC foreground and background layers

         
        Valid values are 1, or 10000, or in between.
        Set to `None` to deactivate downsampling of images.
         
        Default is `70`.



        Args:
            val (Optional[float]):
                property value

        Raises:
            ValueError:
                The given value is smaller than 1 or greater than 10000.


        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerResolutionDPI.restype = c_bool
        if not _lib.PdfToolsOptimizationProfiles_Mrc_SetLayerResolutionDPI(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def recognize_pictures(self) -> bool:
        """
        The option to recognize photographic regions when doing MRC.

         
        Regardless of this property’s setting, monochrome (grayscale) images are always treated as entire photographic regions (cut­out pictures)
        by the MRC algorithm.
         
        Default is `False`.



        Returns:
            bool

        """
        _lib.PdfToolsOptimizationProfiles_Mrc_GetRecognizePictures.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_Mrc_GetRecognizePictures.restype = c_bool
        ret_val = _lib.PdfToolsOptimizationProfiles_Mrc_GetRecognizePictures(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @recognize_pictures.setter
    def recognize_pictures(self, val: bool) -> None:
        """
        The option to recognize photographic regions when doing MRC.

         
        Regardless of this property’s setting, monochrome (grayscale) images are always treated as entire photographic regions (cut­out pictures)
        by the MRC algorithm.
         
        Default is `False`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimizationProfiles_Mrc_SetRecognizePictures.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimizationProfiles_Mrc_SetRecognizePictures.restype = c_bool
        if not _lib.PdfToolsOptimizationProfiles_Mrc_SetRecognizePictures(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Mrc._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Mrc.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
