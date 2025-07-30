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
    from pdftools_sdk.sys.date import _Date
    from pdftools_sdk.signature_validation.data_source import DataSource
    from pdftools_sdk.signature_validation.constraint_result import ConstraintResult

else:
    _Date = "pdftools_sdk.sys.date._Date"
    DataSource = "pdftools_sdk.signature_validation.data_source.DataSource"
    ConstraintResult = "pdftools_sdk.signature_validation.constraint_result.ConstraintResult"


class Certificate(_NativeObject):
    """
    A X.509 certificate


    """
    @property
    def subject_name(self) -> Optional[str]:
        """
        The name (subject) of the certificate

        The common name (CN) of the person or authority that owns the certificate.



        Returns:
            Optional[str]

        """
        _lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSignatureValidation_Certificate_GetSubjectNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def subject(self) -> str:
        """
        The subject of the certificate

        The distinguished name (DN) of the person or authority that owns the certificate.
        Formatted according to RFC 4514.



        Returns:
            str

        """
        _lib.PdfToolsSignatureValidation_Certificate_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSignatureValidation_Certificate_GetSubjectW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSignatureValidation_Certificate_GetSubjectW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSignatureValidation_Certificate_GetSubjectW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def issuer_name(self) -> Optional[str]:
        """
        The name of the certificate's issuer (CA)

        The common name (CN) of the certificate authority (CA) that issued the certificate.



        Returns:
            Optional[str]

        """
        _lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSignatureValidation_Certificate_GetIssuerNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def not_after(self) -> datetime:
        """
        The date after which the certificate is no longer valid.



        Returns:
            datetime

        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsSignatureValidation_Certificate_GetNotAfter.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsSignatureValidation_Certificate_GetNotAfter.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsSignatureValidation_Certificate_GetNotAfter(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val._to_datetime()


    @property
    def not_before(self) -> datetime:
        """
        The date on which the certificate becomes valid.



        Returns:
            datetime

        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsSignatureValidation_Certificate_GetNotBefore.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsSignatureValidation_Certificate_GetNotBefore.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsSignatureValidation_Certificate_GetNotBefore(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val._to_datetime()


    @property
    def fingerprint(self) -> str:
        """
        The certificate's fingerprint

        The hex string representation of the certificate’s SHA-1 digest.



        Returns:
            str

        """
        _lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSignatureValidation_Certificate_GetFingerprintW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def raw_data(self) -> List[int]:
        """
        The raw data of the certificate as a byte array



        Returns:
            List[int]

        """
        _lib.PdfToolsSignatureValidation_Certificate_GetRawData.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t]
        _lib.PdfToolsSignatureValidation_Certificate_GetRawData.restype = c_size_t
        ret_val_size = _lib.PdfToolsSignatureValidation_Certificate_GetRawData(self._handle, None, 0)
        if ret_val_size == -1:
            _NativeBase._throw_last_error(False)
        ret_val = (c_ubyte * ret_val_size)()
        _lib.PdfToolsSignatureValidation_Certificate_GetRawData(self._handle, ret_val, c_size_t(ret_val_size))
        return list(ret_val)


    @property
    def source(self) -> DataSource:
        """
        Source of the certificate



        Returns:
            pdftools_sdk.signature_validation.data_source.DataSource

        """
        from pdftools_sdk.signature_validation.data_source import DataSource

        _lib.PdfToolsSignatureValidation_Certificate_GetSource.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_Certificate_GetSource.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidation_Certificate_GetSource(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return DataSource(ret_val)



    @property
    def validity(self) -> ConstraintResult:
        """
        Whether the certificate is valid according to the validation profile used



        Returns:
            pdftools_sdk.signature_validation.constraint_result.ConstraintResult

        """
        from pdftools_sdk.signature_validation.constraint_result import ConstraintResult

        _lib.PdfToolsSignatureValidation_Certificate_GetValidity.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_Certificate_GetValidity.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_Certificate_GetValidity(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ConstraintResult._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Certificate._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Certificate.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
