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

class DocumentCopyOptions(_NativeObject):
    """
    The document-level copy options applied when copying a document.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_New.argtypes = []
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def copy_metadata(self) -> bool:
        """
         
        Copy document information dictionary and XMP metadata.
         
        Default is `False`.



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyMetadata.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyMetadata.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyMetadata(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_metadata.setter
    def copy_metadata(self, val: bool) -> None:
        """
         
        Copy document information dictionary and XMP metadata.
         
        Default is `False`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyMetadata.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyMetadata.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyMetadata(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def copy_output_intent(self) -> bool:
        """
         
        Copy the PDF/A output intent.
         
        Default is `False`.



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyOutputIntent.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyOutputIntent.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyOutputIntent(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_output_intent.setter
    def copy_output_intent(self, val: bool) -> None:
        """
         
        Copy the PDF/A output intent.
         
        Default is `False`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyOutputIntent.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyOutputIntent.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyOutputIntent(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def copy_viewer_settings(self) -> bool:
        """
         
        Copy viewer properties, which include: Page Layout, Page Mode, Open Actions, Piece Info, and Collection properties.
         
        Default is `False`.



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyViewerSettings.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyViewerSettings.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyViewerSettings(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_viewer_settings.setter
    def copy_viewer_settings(self, val: bool) -> None:
        """
         
        Copy viewer properties, which include: Page Layout, Page Mode, Open Actions, Piece Info, and Collection properties.
         
        Default is `False`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyViewerSettings.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyViewerSettings.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyViewerSettings(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def copy_embedded_files(self) -> bool:
        """
         
        If set to `True`: All embedded files are copied. If set to `False`: Only embedded files associated with pages
        within the given page range are copied. (PDF/A-3 only, :attr:`pdftools_sdk.document_assembly.page_copy_options.PageCopyOptions.copy_associated_files`  must be set.)
         
        Default is `False`.



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyEmbeddedFiles.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyEmbeddedFiles.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_GetCopyEmbeddedFiles(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_embedded_files.setter
    def copy_embedded_files(self, val: bool) -> None:
        """
         
        If set to `True`: All embedded files are copied. If set to `False`: Only embedded files associated with pages
        within the given page range are copied. (PDF/A-3 only, :attr:`pdftools_sdk.document_assembly.page_copy_options.PageCopyOptions.copy_associated_files`  must be set.)
         
        Default is `False`.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyEmbeddedFiles.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyEmbeddedFiles.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_DocumentCopyOptions_SetCopyEmbeddedFiles(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return DocumentCopyOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = DocumentCopyOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
