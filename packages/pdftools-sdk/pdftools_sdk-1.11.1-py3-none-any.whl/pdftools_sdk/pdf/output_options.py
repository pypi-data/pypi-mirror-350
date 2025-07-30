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
    from pdftools_sdk.pdf.encryption import Encryption
    from pdftools_sdk.pdf.metadata_settings import MetadataSettings

else:
    Encryption = "pdftools_sdk.pdf.encryption.Encryption"
    MetadataSettings = "pdftools_sdk.pdf.metadata_settings.MetadataSettings"


class OutputOptions(_NativeObject):
    """
    The parameters for document-level features of output PDFs

    Output options are used in many operations that create PDF documents.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf_OutputOptions_New.argtypes = []
        _lib.PdfToolsPdf_OutputOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_OutputOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def encryption(self) -> Optional[Encryption]:
        """
        The parameters to encrypt output PDFs

         
        If `None`, no encryption is used.
         
        Encryption is not allowed by the PDF/A ISO standards.
        For that reason, it is recommended to use `None` when processing PDF/A documents.
        Otherwise, most operations will remove PDF/A conformance from the output document.
        More details can be found in the documentation of the operation.
         
        Default is `None`, no encryption is used.



        Returns:
            Optional[pdftools_sdk.pdf.encryption.Encryption]

        """
        from pdftools_sdk.pdf.encryption import Encryption

        _lib.PdfToolsPdf_OutputOptions_GetEncryption.argtypes = [c_void_p]
        _lib.PdfToolsPdf_OutputOptions_GetEncryption.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_OutputOptions_GetEncryption(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Encryption._create_dynamic_type(ret_val)


    @encryption.setter
    def encryption(self, val: Optional[Encryption]) -> None:
        """
        The parameters to encrypt output PDFs

         
        If `None`, no encryption is used.
         
        Encryption is not allowed by the PDF/A ISO standards.
        For that reason, it is recommended to use `None` when processing PDF/A documents.
        Otherwise, most operations will remove PDF/A conformance from the output document.
        More details can be found in the documentation of the operation.
         
        Default is `None`, no encryption is used.



        Args:
            val (Optional[pdftools_sdk.pdf.encryption.Encryption]):
                property value

        """
        from pdftools_sdk.pdf.encryption import Encryption

        if val is not None and not isinstance(val, Encryption):
            raise TypeError(f"Expected type {Encryption.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_OutputOptions_SetEncryption.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsPdf_OutputOptions_SetEncryption.restype = c_bool
        if not _lib.PdfToolsPdf_OutputOptions_SetEncryption(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def metadata_settings(self) -> Optional[MetadataSettings]:
        """
        Default is `None`, metadata are copied to the output document.



        Returns:
            Optional[pdftools_sdk.pdf.metadata_settings.MetadataSettings]

        """
        from pdftools_sdk.pdf.metadata_settings import MetadataSettings

        _lib.PdfToolsPdf_OutputOptions_GetMetadataSettings.argtypes = [c_void_p]
        _lib.PdfToolsPdf_OutputOptions_GetMetadataSettings.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_OutputOptions_GetMetadataSettings(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return MetadataSettings._create_dynamic_type(ret_val)


    @metadata_settings.setter
    def metadata_settings(self, val: Optional[MetadataSettings]) -> None:
        """
        Default is `None`, metadata are copied to the output document.



        Args:
            val (Optional[pdftools_sdk.pdf.metadata_settings.MetadataSettings]):
                property value

        """
        from pdftools_sdk.pdf.metadata_settings import MetadataSettings

        if val is not None and not isinstance(val, MetadataSettings):
            raise TypeError(f"Expected type {MetadataSettings.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_OutputOptions_SetMetadataSettings.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsPdf_OutputOptions_SetMetadataSettings.restype = c_bool
        if not _lib.PdfToolsPdf_OutputOptions_SetMetadataSettings(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf_OutputOptions_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf_OutputOptions_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf_OutputOptions_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return OutputOptions._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.sign.output_options import OutputOptions 
            return OutputOptions._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = OutputOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
