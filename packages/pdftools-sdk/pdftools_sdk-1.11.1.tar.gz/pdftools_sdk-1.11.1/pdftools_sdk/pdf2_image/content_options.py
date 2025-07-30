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
    from pdftools_sdk.pdf2_image.annotation_options import AnnotationOptions

else:
    AnnotationOptions = "pdftools_sdk.pdf2_image.annotation_options.AnnotationOptions"


class ContentOptions(_NativeObject):
    """
    The parameters how to render PDF content elements


    """
    @property
    def annotations(self) -> AnnotationOptions:
        """
        The render strategy for annotations

         
        Defines whether to render annotation popups.
        For details, see :class:`pdftools_sdk.pdf2_image.annotation_options.AnnotationOptions` .
         
        Default is :attr:`pdftools_sdk.pdf2_image.annotation_options.AnnotationOptions.SHOWANNOTATIONS` 



        Returns:
            pdftools_sdk.pdf2_image.annotation_options.AnnotationOptions

        """
        from pdftools_sdk.pdf2_image.annotation_options import AnnotationOptions

        _lib.PdfToolsPdf2Image_ContentOptions_GetAnnotations.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_ContentOptions_GetAnnotations.restype = c_int
        ret_val = _lib.PdfToolsPdf2Image_ContentOptions_GetAnnotations(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return AnnotationOptions(ret_val)



    @annotations.setter
    def annotations(self, val: AnnotationOptions) -> None:
        """
        The render strategy for annotations

         
        Defines whether to render annotation popups.
        For details, see :class:`pdftools_sdk.pdf2_image.annotation_options.AnnotationOptions` .
         
        Default is :attr:`pdftools_sdk.pdf2_image.annotation_options.AnnotationOptions.SHOWANNOTATIONS` 



        Args:
            val (pdftools_sdk.pdf2_image.annotation_options.AnnotationOptions):
                property value

        """
        from pdftools_sdk.pdf2_image.annotation_options import AnnotationOptions

        if not isinstance(val, AnnotationOptions):
            raise TypeError(f"Expected type {AnnotationOptions.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_ContentOptions_SetAnnotations.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf2Image_ContentOptions_SetAnnotations.restype = c_bool
        if not _lib.PdfToolsPdf2Image_ContentOptions_SetAnnotations(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def render_text(self) -> bool:
        """
         
        Defines whether to render text. When set to `False`, text rendering is skipped entirely.
        Text embedded in images and text created by drawing lines or paths are still rendered.
        Skipping text rendering can speed up the rendering process, especially for documents with many text elements.
         
        Default is `True`.



        Returns:
            bool

        """
        _lib.PdfToolsPdf2Image_ContentOptions_GetRenderText.argtypes = [c_void_p]
        _lib.PdfToolsPdf2Image_ContentOptions_GetRenderText.restype = c_bool
        ret_val = _lib.PdfToolsPdf2Image_ContentOptions_GetRenderText(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @render_text.setter
    def render_text(self, val: bool) -> None:
        """
         
        Defines whether to render text. When set to `False`, text rendering is skipped entirely.
        Text embedded in images and text created by drawing lines or paths are still rendered.
        Skipping text rendering can speed up the rendering process, especially for documents with many text elements.
         
        Default is `True`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsPdf2Image_ContentOptions_SetRenderText.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsPdf2Image_ContentOptions_SetRenderText.restype = c_bool
        if not _lib.PdfToolsPdf2Image_ContentOptions_SetRenderText(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ContentOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ContentOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
