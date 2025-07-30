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

if TYPE_CHECKING:
    from pdftools_sdk.optimization.compression_algorithm_selection import CompressionAlgorithmSelection

else:
    CompressionAlgorithmSelection = "pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection"


class ImageRecompressionOptions(_NativeObject):
    """
    The parameters for image recompression


    """
    @property
    def algorithm_selection(self) -> CompressionAlgorithmSelection:
        """
        The strategy for image recompression

         
        For each image to be recompressed, a specific choice of compression
        algorithms are tried. The selection of algorithms depends on this strategy, the
        type of the optimizer profile (e.g. :class:`pdftools_sdk.optimization.profiles.web.Web` ),
        the color space of the image, and :attr:`pdftools_sdk.optimization.image_recompression_options.ImageRecompressionOptions.compression_quality` .
        The image is recompressed using the algorithm resulting in the
        smallest output file.
         
        Refer to :class:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection`  for
        more information on strategies.
         
        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY`
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY`
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`
         



        Returns:
            pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection

        """
        from pdftools_sdk.optimization.compression_algorithm_selection import CompressionAlgorithmSelection

        _lib.PdfToolsOptimization_ImageRecompressionOptions_GetAlgorithmSelection.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_ImageRecompressionOptions_GetAlgorithmSelection.restype = c_int
        ret_val = _lib.PdfToolsOptimization_ImageRecompressionOptions_GetAlgorithmSelection(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return CompressionAlgorithmSelection(ret_val)



    @algorithm_selection.setter
    def algorithm_selection(self, val: CompressionAlgorithmSelection) -> None:
        """
        The strategy for image recompression

         
        For each image to be recompressed, a specific choice of compression
        algorithms are tried. The selection of algorithms depends on this strategy, the
        type of the optimizer profile (e.g. :class:`pdftools_sdk.optimization.profiles.web.Web` ),
        the color space of the image, and :attr:`pdftools_sdk.optimization.image_recompression_options.ImageRecompressionOptions.compression_quality` .
        The image is recompressed using the algorithm resulting in the
        smallest output file.
         
        Refer to :class:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection`  for
        more information on strategies.
         
        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY`
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.PRESERVEQUALITY`
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: :attr:`pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection.BALANCED`
         



        Args:
            val (pdftools_sdk.optimization.compression_algorithm_selection.CompressionAlgorithmSelection):
                property value

        """
        from pdftools_sdk.optimization.compression_algorithm_selection import CompressionAlgorithmSelection

        if not isinstance(val, CompressionAlgorithmSelection):
            raise TypeError(f"Expected type {CompressionAlgorithmSelection.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_ImageRecompressionOptions_SetAlgorithmSelection.argtypes = [c_void_p, c_int]
        _lib.PdfToolsOptimization_ImageRecompressionOptions_SetAlgorithmSelection.restype = c_bool
        if not _lib.PdfToolsOptimization_ImageRecompressionOptions_SetAlgorithmSelection(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def compression_quality(self) -> float:
        """
        The compression quality for lossy image compression algorithms

         
        This property specifies the compression quality for the JPEG and JPEG2000 image compression algorithms.
        Valid values are between 0 (lowest quality) and 1 (highest quality).
         
        Although the JBIG2 algorithm for bi-tonal images also allows lossy compression, it is not influenced by this property.
        The JBIG2 compression quality is fixed at 1 (lossless).
         
        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: 0.8
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: 0.9
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: 0.9
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: 0.75
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: 0.75
         



        Returns:
            float

        """
        _lib.PdfToolsOptimization_ImageRecompressionOptions_GetCompressionQuality.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_ImageRecompressionOptions_GetCompressionQuality.restype = c_double
        ret_val = _lib.PdfToolsOptimization_ImageRecompressionOptions_GetCompressionQuality(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @compression_quality.setter
    def compression_quality(self, val: float) -> None:
        """
        The compression quality for lossy image compression algorithms

         
        This property specifies the compression quality for the JPEG and JPEG2000 image compression algorithms.
        Valid values are between 0 (lowest quality) and 1 (highest quality).
         
        Although the JBIG2 algorithm for bi-tonal images also allows lossy compression, it is not influenced by this property.
        The JBIG2 compression quality is fixed at 1 (lossless).
         
        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: 0.8
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: 0.9
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: 0.9
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: 0.75
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: 0.75
         



        Args:
            val (float):
                property value

        Raises:
            ValueError:
                If the given value is outside of the range 0 - 1


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_ImageRecompressionOptions_SetCompressionQuality.argtypes = [c_void_p, c_double]
        _lib.PdfToolsOptimization_ImageRecompressionOptions_SetCompressionQuality.restype = c_bool
        if not _lib.PdfToolsOptimization_ImageRecompressionOptions_SetCompressionQuality(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def reduce_color_complexity(self) -> bool:
        """
        Enable color complexity reduction.

        When enabled, the software analyzes images that utilize device color spaces (DeviceRGB, DeviceCMYK, or DeviceGray) as well as indexed images with a device color space as their base. If applicable, the images are converted according to the following criteria:
         
        - Images in DeviceRGB or DeviceCMYK color space where all pixels are gray will be converted to grayscale using the DeviceGray color space.
        - Images containing only black and white pixels will be converted to bitonal images.
        - Images where all pixels are of the same color will be downsampled to a single pixel.
         
        Additionally, image masks and soft masks are optimized in the following ways:
         
        - Soft masks consisting only of black and white pixels will be converted into a standard mask.
        - Any (soft) mask that is completely opaque will be removed.
         
        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: `False`
         



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_ImageRecompressionOptions_GetReduceColorComplexity.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_ImageRecompressionOptions_GetReduceColorComplexity.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_ImageRecompressionOptions_GetReduceColorComplexity(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @reduce_color_complexity.setter
    def reduce_color_complexity(self, val: bool) -> None:
        """
        Enable color complexity reduction.

        When enabled, the software analyzes images that utilize device color spaces (DeviceRGB, DeviceCMYK, or DeviceGray) as well as indexed images with a device color space as their base. If applicable, the images are converted according to the following criteria:
         
        - Images in DeviceRGB or DeviceCMYK color space where all pixels are gray will be converted to grayscale using the DeviceGray color space.
        - Images containing only black and white pixels will be converted to bitonal images.
        - Images where all pixels are of the same color will be downsampled to a single pixel.
         
        Additionally, image masks and soft masks are optimized in the following ways:
         
        - Soft masks consisting only of black and white pixels will be converted into a standard mask.
        - Any (soft) mask that is completely opaque will be removed.
         
        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: `False`
         



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_ImageRecompressionOptions_SetReduceColorComplexity.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_ImageRecompressionOptions_SetReduceColorComplexity.restype = c_bool
        if not _lib.PdfToolsOptimization_ImageRecompressionOptions_SetReduceColorComplexity(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ImageRecompressionOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ImageRecompressionOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
