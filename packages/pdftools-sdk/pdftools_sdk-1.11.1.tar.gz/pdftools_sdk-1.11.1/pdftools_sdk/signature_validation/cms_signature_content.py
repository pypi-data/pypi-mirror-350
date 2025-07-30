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
import pdftools_sdk.signature_validation.signature_content

if TYPE_CHECKING:
    from pdftools_sdk.sys.date import _Date
    from pdftools_sdk.signature_validation.time_source import TimeSource
    from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm
    from pdftools_sdk.signature_validation.time_stamp_content import TimeStampContent
    from pdftools_sdk.signature_validation.certificate import Certificate
    from pdftools_sdk.signature_validation.certificate_chain import CertificateChain

else:
    _Date = "pdftools_sdk.sys.date._Date"
    TimeSource = "pdftools_sdk.signature_validation.time_source.TimeSource"
    HashAlgorithm = "pdftools_sdk.crypto.hash_algorithm.HashAlgorithm"
    TimeStampContent = "pdftools_sdk.signature_validation.time_stamp_content.TimeStampContent"
    Certificate = "pdftools_sdk.signature_validation.certificate.Certificate"
    CertificateChain = "pdftools_sdk.signature_validation.certificate_chain.CertificateChain"


class CmsSignatureContent(pdftools_sdk.signature_validation.signature_content.SignatureContent):
    """
    The data and validation result of the cryptographic signature


    """
    @property
    def validation_time(self) -> datetime:
        """
        The time at which the signature has been validated



        Returns:
            datetime

        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTime.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTime.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTime(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val._to_datetime()


    @property
    def validation_time_source(self) -> TimeSource:
        """
        The source for the validation time



        Returns:
            pdftools_sdk.signature_validation.time_source.TimeSource

        """
        from pdftools_sdk.signature_validation.time_source import TimeSource

        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTimeSource.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTimeSource.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetValidationTimeSource(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return TimeSource(ret_val)



    @property
    def hash_algorithm(self) -> HashAlgorithm:
        """
        The hash algorithm used to calculate the signature's message digest



        Returns:
            pdftools_sdk.crypto.hash_algorithm.HashAlgorithm

        """
        from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm

        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetHashAlgorithm.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetHashAlgorithm.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetHashAlgorithm(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return HashAlgorithm(ret_val)



    @property
    def time_stamp(self) -> Optional[TimeStampContent]:
        """
        The data and validation result of the embedded time-stamp



        Returns:
            Optional[pdftools_sdk.signature_validation.time_stamp_content.TimeStampContent]

        """
        from pdftools_sdk.signature_validation.time_stamp_content import TimeStampContent

        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetTimeStamp.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetTimeStamp.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetTimeStamp(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return TimeStampContent._create_dynamic_type(ret_val)


    @property
    def signing_certificate(self) -> Optional[Certificate]:
        """
        The signing certificate



        Returns:
            Optional[pdftools_sdk.signature_validation.certificate.Certificate]

        """
        from pdftools_sdk.signature_validation.certificate import Certificate

        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetSigningCertificate.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetSigningCertificate.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetSigningCertificate(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Certificate._create_dynamic_type(ret_val)


    @property
    def certificate_chain(self) -> Optional[CertificateChain]:
        """
        The certificate chain of the signing certificate



        Returns:
            Optional[pdftools_sdk.signature_validation.certificate_chain.CertificateChain]

        """
        from pdftools_sdk.signature_validation.certificate_chain import CertificateChain

        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetCertificateChain.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetCertificateChain.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_CmsSignatureContent_GetCertificateChain(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return CertificateChain._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return CmsSignatureContent._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = CmsSignatureContent.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
