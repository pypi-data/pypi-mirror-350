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

class MinimalFileSize(pdftools_sdk.optimization.profiles.profile.Profile):
    """
    The optimization profile producing a minimal file size

     
    This profile optimizes the output PDF for minimal file size.
    This is achieved by using a varied palette of image compression
    algorithms, appropriate resolution setting and higher
    compression rates at the price of slightly lower image quality.
     
    The output file size is further reduced by converting Embedded
    Type1 (PostScript) fonts to Type1C (Compact Font Format) and
    removing metadata and output intents 
    (see :attr:`pdftools_sdk.optimization.profiles.profile.Profile.removal_options` ).
    Also Spider (web capture) information is removed.
     
    Images above 182 DPI are down-sampled and recompressed to 130 DPI.
    This leads to smaller output files. The property
    :attr:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize.resolution_d_p_i`  has influence on both values.
     
    When an image is recompressed, the
    :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED` 
    strategy is used; this can be overridden through the
    property :attr:`pdftools_sdk.optimization.profiles.profile.Profile.image_recompression_options` .
     
    With this profile, the output PDF version is updated to PDF 1.7 or higher and
    PDF/A conformance removed.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_New.argtypes = []
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_New.restype = c_void_p
        ret_val = _lib.PdfToolsOptimizationProfiles_MinimalFileSize_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def resolution_d_p_i(self) -> Optional[float]:
        """
        The target resolution of images in DPI

         
        The target resolution in DPI (dots per inch) for color and grayscale images.
         
        Images with a resolution above :attr:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize.threshold_d_p_i`  are down-sampled.
         
        Valid values are in the range 1.0 to 10000.
         
        If `None`, then resolution setting is disabled.
         
        Default is `130`.



        Returns:
            Optional[float]

        """
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetResolutionDPI.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetResolutionDPI(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @resolution_d_p_i.setter
    def resolution_d_p_i(self, val: Optional[float]) -> None:
        """
        The target resolution of images in DPI

         
        The target resolution in DPI (dots per inch) for color and grayscale images.
         
        Images with a resolution above :attr:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize.threshold_d_p_i`  are down-sampled.
         
        Valid values are in the range 1.0 to 10000.
         
        If `None`, then resolution setting is disabled.
         
        Default is `130`.



        Args:
            val (Optional[float]):
                property value

        Raises:
            ValueError:
                The given value is outside of range 1.0 to 10000.0.


        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetResolutionDPI.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetResolutionDPI.restype = c_bool
        if not _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetResolutionDPI(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def threshold_d_p_i(self) -> float:
        """
        The threshold resolution of images in DPI.

         
        The threshold resolution in DPI (dots per inch) to selectively activate downsampling for color and grayscale images.
         
        Valid values are in the range 1.0 to 10000.
        To deactivate down-sampling of images set :attr:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize.resolution_d_p_i`  to `None`.
         
        Default is `1.4` times :attr:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize.resolution_d_p_i` .



        Returns:
            float

        """
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetThresholdDPI.argtypes = [c_void_p]
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetThresholdDPI.restype = c_double
        ret_val = _lib.PdfToolsOptimizationProfiles_MinimalFileSize_GetThresholdDPI(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @threshold_d_p_i.setter
    def threshold_d_p_i(self, val: float) -> None:
        """
        The threshold resolution of images in DPI.

         
        The threshold resolution in DPI (dots per inch) to selectively activate downsampling for color and grayscale images.
         
        Valid values are in the range 1.0 to 10000.
        To deactivate down-sampling of images set :attr:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize.resolution_d_p_i`  to `None`.
         
        Default is `1.4` times :attr:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize.resolution_d_p_i` .



        Args:
            val (float):
                property value

        Raises:
            ValueError:
                The given value is outside of range 1.0 to 10000.0.


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetThresholdDPI.argtypes = [c_void_p, c_double]
        _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetThresholdDPI.restype = c_bool
        if not _lib.PdfToolsOptimizationProfiles_MinimalFileSize_SetThresholdDPI(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return MinimalFileSize._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = MinimalFileSize.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
