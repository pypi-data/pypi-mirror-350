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
import pdftools_sdk.pdf.signature_field

if TYPE_CHECKING:
    from pdftools_sdk.sys.date import _Date
    from pdftools_sdk.pdf.revision import Revision

else:
    _Date = "pdftools_sdk.sys.date._Date"
    Revision = "pdftools_sdk.pdf.revision.Revision"


class SignedSignatureField(pdftools_sdk.pdf.signature_field.SignatureField, ABC):
    """
    A base class for signature fields that have been signed

    The existence of a signed signature field does not imply that the signature is valid.
    The signature is not validated at all.


    """
    @property
    def name(self) -> Optional[str]:
        """
        The name of the person or authority that signed the document

         
        This is the name of the signing certificate.
         
        *Note:* The name of the signing certificate can only be extracted for signatures conforming to the PAdES or PDF standard
        and not for proprietary/non-standard signature formats.
        For non-standard signature formats, the name as stored in the PDF is returned.



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the object has already been closed


        """
        _lib.PdfToolsPdf_SignedSignatureField_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_SignedSignatureField_GetNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_SignedSignatureField_GetNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_SignedSignatureField_GetNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def date(self) -> Optional[datetime]:
        """
        The date and time of signing

         
        This represents the date and time of signing as specified in the signature.
        For signatures that contain a time-stamp, the trusted time-stamp time is returned.
         
        *Note:* The value can only be extracted for signatures conforming to the PAdES or PDF standard
        and not for proprietary/non-standard signature formats.
        For non-standard signature formats, the date as stored in the PDF is returned.



        Returns:
            Optional[datetime]

        Raises:
            StateError:
                If the object has already been closed


        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsPdf_SignedSignatureField_GetDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsPdf_SignedSignatureField_GetDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsPdf_SignedSignatureField_GetDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @property
    def revision(self) -> Revision:
        """
        The document revision

        The revision (version) of the document that the signature signs.



        Returns:
            pdftools_sdk.pdf.revision.Revision

        Raises:
            StateError:
                If the object has already been closed

            pdftools_sdk.corrupt_error.CorruptError:
                If the signature specifies an invalid document revision


        """
        from pdftools_sdk.pdf.revision import Revision

        _lib.PdfToolsPdf_SignedSignatureField_GetRevision.argtypes = [c_void_p]
        _lib.PdfToolsPdf_SignedSignatureField_GetRevision.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_SignedSignatureField_GetRevision(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Revision._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsPdf_SignedSignatureField_GetType.argtypes = [c_void_p]
        _lib.PdfToolsPdf_SignedSignatureField_GetType.restype = c_int

        obj_type = _lib.PdfToolsPdf_SignedSignatureField_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return SignedSignatureField._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.pdf.signature import Signature 
            return Signature._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.pdf.document_signature import DocumentSignature 
            return DocumentSignature._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.pdf.certification_signature import CertificationSignature 
            return CertificationSignature._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.pdf.document_timestamp import DocumentTimestamp 
            return DocumentTimestamp._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignedSignatureField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
