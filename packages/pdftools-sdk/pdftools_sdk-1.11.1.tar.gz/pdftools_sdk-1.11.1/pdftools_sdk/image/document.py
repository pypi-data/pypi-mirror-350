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

class Document(_NativeObject, ABC):
    """
    The base class for image documents

    Image documents are either opened using :meth:`pdftools_sdk.image.document.Document.open`  or the result of an operation, e.g. of PDF to image conversion using :meth:`pdftools_sdk.pdf2_image.converter.Converter.convert_page` .


    """
    @staticmethod
    def open(stream: io.IOBase) -> Document:
        """
        Open an image document

        Documents opened with this method are read-only and cannot be modified.



        Args:
            stream (io.IOBase): 
                The stream from which the image is read.



        Returns:
            pdftools_sdk.image.document.Document: 
                The newly created document instance



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            pdftools_sdk.unknown_format_error.UnknownFormatError:
                The document has a not recognized image format.

            pdftools_sdk.corrupt_error.CorruptError:
                The document is corrupt or not an image.


        """
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")

        _lib.PdfToolsImage_Document_Open.argtypes = [POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsImage_Document_Open.restype = c_void_p
        ret_val = _lib.PdfToolsImage_Document_Open(_StreamDescriptor(stream))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)



    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PdfToolsImage_Document_Close.argtypes = [c_void_p]
        _lib.PdfToolsImage_Document_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PdfToolsImage_Document_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsImage_Document_GetType.argtypes = [c_void_p]
        _lib.PdfToolsImage_Document_GetType.restype = c_int

        obj_type = _lib.PdfToolsImage_Document_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Document._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.image.single_page_document import SinglePageDocument 
            return SinglePageDocument._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.image.multi_page_document import MultiPageDocument 
            return MultiPageDocument._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Document.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
