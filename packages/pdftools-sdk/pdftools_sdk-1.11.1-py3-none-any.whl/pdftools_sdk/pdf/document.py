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
    from pdftools_sdk.pdf.conformance import Conformance
    from pdftools_sdk.pdf.permission import Permission
    from pdftools_sdk.pdf.signature_field_list import SignatureFieldList
    from pdftools_sdk.pdf.xfa_type import XfaType
    from pdftools_sdk.pdf.metadata import Metadata

else:
    Conformance = "pdftools_sdk.pdf.conformance.Conformance"
    Permission = "pdftools_sdk.pdf.permission.Permission"
    SignatureFieldList = "pdftools_sdk.pdf.signature_field_list.SignatureFieldList"
    XfaType = "pdftools_sdk.pdf.xfa_type.XfaType"
    Metadata = "pdftools_sdk.pdf.metadata.Metadata"


class Document(_NativeObject):
    """
    The PDF document

    PDF documents are either opened using :meth:`pdftools_sdk.pdf.document.Document.open`  or the result of an operation, e.g. of PDF optimization (see :meth:`pdftools_sdk.optimization.optimizer.Optimizer.optimize_document` ).


    """
    @staticmethod
    def open(stream: io.IOBase, password: Optional[str] = None) -> Document:
        """
        Open a PDF document.

        Documents opened with this method are read-only and cannot be modified.



        Args:
            stream (io.IOBase): 
                The stream from which the PDF is read.

            password (Optional[str]): 
                The password to open the PDF document.
                If `None` or empty, no password is used.



        Returns:
            pdftools_sdk.pdf.document.Document: 
                The newly created document instance



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            pdftools_sdk.password_error.PasswordError:
                The document is encrypted and the `password` is invalid.

            pdftools_sdk.corrupt_error.CorruptError:
                The document is corrupt or not a PDF.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The document is an unencrypted wrapper document.

            pdftools_sdk.generic_error.GenericError:
                A generic error occurred.


        """
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PdfToolsPdf_Document_OpenW.argtypes = [POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_wchar_p]
        _lib.PdfToolsPdf_Document_OpenW.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_Document_OpenW(_StreamDescriptor(stream), _string_to_utf16(password))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)



    @property
    def conformance(self) -> Optional[Conformance]:
        """
        The claimed conformance of the document

         
        This method only returns the claimed conformance level,
        the document is not validated.
         
        This property can return `None` if the document's conformance is unknown.



        Returns:
            Optional[pdftools_sdk.pdf.conformance.Conformance]

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsPdf_Document_GetConformance.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdf_Document_GetConformance.restype = c_bool
        ret_val = c_int()
        if not _lib.PdfToolsPdf_Document_GetConformance(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return Conformance(ret_val.value)



    @property
    def page_count(self) -> int:
        """
        The number of pages in the document

        If the document is a collection (also known as PDF Portfolio), then this property is `0`.



        Returns:
            int

        """
        _lib.PdfToolsPdf_Document_GetPageCount.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_GetPageCount.restype = c_int
        ret_val = _lib.PdfToolsPdf_Document_GetPageCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def permissions(self) -> Optional[Permission]:
        """
        The access permissions applicable for this document

         
        This property is `None`, if the document is not encrypted.
         
        Note that these permissions might be different from the "Document Restrictions Summary" displayed in Adobe Acrobat.
        This is because Acrobat's restrictions are also affected by other factors.
        For example, "Document Assembly" is generally only allowed in Acrobat Pro and not the Acrobat Reader.



        Returns:
            Optional[pdftools_sdk.pdf.permission.Permission]

        """
        from pdftools_sdk.pdf.permission import Permission

        _lib.PdfToolsPdf_Document_GetPermissions.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsPdf_Document_GetPermissions.restype = c_bool
        ret_val = c_int()
        if not _lib.PdfToolsPdf_Document_GetPermissions(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return Permission(ret_val.value)



    @property
    def is_linearized(self) -> bool:
        """
        Whether the document is linearized



        Returns:
            bool

        """
        _lib.PdfToolsPdf_Document_IsLinearized.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_IsLinearized.restype = c_bool
        ret_val = _lib.PdfToolsPdf_Document_IsLinearized(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def is_signed(self) -> bool:
        """

        Returns:
            bool

        """
        _lib.PdfToolsPdf_Document_IsSigned.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_IsSigned.restype = c_bool
        ret_val = _lib.PdfToolsPdf_Document_IsSigned(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def signature_fields(self) -> SignatureFieldList:
        """

        Returns:
            pdftools_sdk.pdf.signature_field_list.SignatureFieldList

        """
        from pdftools_sdk.pdf.signature_field_list import SignatureFieldList

        _lib.PdfToolsPdf_Document_GetSignatureFields.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_GetSignatureFields.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_Document_GetSignatureFields(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureFieldList._create_dynamic_type(ret_val)


    @property
    def xfa(self) -> XfaType:
        """
        Whether the document is an XML Forms Architecture (XFA) or a PDF document

        While XFA documents may seem like regular PDF documents they are not and cannot be processed by many components (error :class:`pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError` ).
        An XFA form is included as a resource in a mere shell PDF.
        The PDF pages' content is generated dynamically from the XFA data, which is a complex, non-standardized process.
        For this reason, XFA is forbidden by the ISO Standards ISO 19'005-2 (PDF/A-2) and ISO 32'000-2 (PDF 2.0) and newer.
        It is recommended to convert XFA documents to PDF using an Adobe product, e.g. by using the "Print to PDF" function of Adobe Acrobat Reader.



        Returns:
            pdftools_sdk.pdf.xfa_type.XfaType

        """
        from pdftools_sdk.pdf.xfa_type import XfaType

        _lib.PdfToolsPdf_Document_GetXfa.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_GetXfa.restype = c_int
        ret_val = _lib.PdfToolsPdf_Document_GetXfa(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return XfaType(ret_val)



    @property
    def metadata(self) -> Metadata:
        """
        The metadata of the document.



        Returns:
            pdftools_sdk.pdf.metadata.Metadata

        """
        from pdftools_sdk.pdf.metadata import Metadata

        _lib.PdfToolsPdf_Document_GetMetadata.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_GetMetadata.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_Document_GetMetadata(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Metadata._create_dynamic_type(ret_val)



    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PdfToolsPdf_Document_Close.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PdfToolsPdf_Document_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf_Document_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Document_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf_Document_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Document._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.sign.prepared_document import PreparedDocument 
            return PreparedDocument._from_handle(handle)
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
