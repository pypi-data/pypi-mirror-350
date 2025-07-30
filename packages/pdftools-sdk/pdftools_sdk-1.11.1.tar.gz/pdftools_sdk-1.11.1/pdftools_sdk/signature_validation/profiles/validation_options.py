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
    from pdftools_sdk.signature_validation.time_source import TimeSource
    from pdftools_sdk.signature_validation.data_source import DataSource

else:
    TimeSource = "pdftools_sdk.signature_validation.time_source.TimeSource"
    DataSource = "pdftools_sdk.signature_validation.data_source.DataSource"


class ValidationOptions(_NativeObject):
    """
    Signature validation options


    """
    @property
    def time_source(self) -> TimeSource:
        """
        Allowed validation time sources



        Returns:
            pdftools_sdk.signature_validation.time_source.TimeSource

        """
        from pdftools_sdk.signature_validation.time_source import TimeSource

        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetTimeSource.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetTimeSource.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetTimeSource(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return TimeSource(ret_val)



    @time_source.setter
    def time_source(self, val: TimeSource) -> None:
        """
        Allowed validation time sources



        Args:
            val (pdftools_sdk.signature_validation.time_source.TimeSource):
                property value

        """
        from pdftools_sdk.signature_validation.time_source import TimeSource

        if not isinstance(val, TimeSource):
            raise TypeError(f"Expected type {TimeSource.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetTimeSource.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetTimeSource.restype = c_bool
        if not _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetTimeSource(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def certificate_sources(self) -> DataSource:
        """
        Allowed sources to get certificates, e.g. intermediate issuer certificates



        Returns:
            pdftools_sdk.signature_validation.data_source.DataSource

        """
        from pdftools_sdk.signature_validation.data_source import DataSource

        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetCertificateSources.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetCertificateSources.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetCertificateSources(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return DataSource(ret_val)



    @certificate_sources.setter
    def certificate_sources(self, val: DataSource) -> None:
        """
        Allowed sources to get certificates, e.g. intermediate issuer certificates



        Args:
            val (pdftools_sdk.signature_validation.data_source.DataSource):
                property value

        """
        from pdftools_sdk.signature_validation.data_source import DataSource

        if not isinstance(val, DataSource):
            raise TypeError(f"Expected type {DataSource.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetCertificateSources.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetCertificateSources.restype = c_bool
        if not _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetCertificateSources(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def revocation_information_sources(self) -> DataSource:
        """
        Allowed sources to get revocation information (OCSP, CRL)



        Returns:
            pdftools_sdk.signature_validation.data_source.DataSource

        """
        from pdftools_sdk.signature_validation.data_source import DataSource

        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetRevocationInformationSources.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetRevocationInformationSources.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_GetRevocationInformationSources(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return DataSource(ret_val)



    @revocation_information_sources.setter
    def revocation_information_sources(self, val: DataSource) -> None:
        """
        Allowed sources to get revocation information (OCSP, CRL)



        Args:
            val (pdftools_sdk.signature_validation.data_source.DataSource):
                property value

        """
        from pdftools_sdk.signature_validation.data_source import DataSource

        if not isinstance(val, DataSource):
            raise TypeError(f"Expected type {DataSource.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetRevocationInformationSources.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetRevocationInformationSources.restype = c_bool
        if not _lib.PdfToolsSignatureValidationProfiles_ValidationOptions_SetRevocationInformationSources(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ValidationOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ValidationOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
