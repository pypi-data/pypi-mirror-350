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
    from pdftools_sdk.signature_validation.data_source import DataSource
    from pdftools_sdk.signature_validation.profiles.revocation_check_policy import RevocationCheckPolicy

else:
    DataSource = "pdftools_sdk.signature_validation.data_source.DataSource"
    RevocationCheckPolicy = "pdftools_sdk.signature_validation.profiles.revocation_check_policy.RevocationCheckPolicy"


class TrustConstraints(_NativeObject):
    """
    Certificate trust constraints


    """
    @property
    def trust_sources(self) -> DataSource:
        """
        Allowed sources for trusted certificates

        Note that the trust sources are implicitly added to the profile's :attr:`pdftools_sdk.signature_validation.profiles.validation_options.ValidationOptions.certificate_sources` .



        Returns:
            pdftools_sdk.signature_validation.data_source.DataSource

        """
        from pdftools_sdk.signature_validation.data_source import DataSource

        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetTrustSources.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetTrustSources.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetTrustSources(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return DataSource(ret_val)



    @trust_sources.setter
    def trust_sources(self, val: DataSource) -> None:
        """
        Allowed sources for trusted certificates

        Note that the trust sources are implicitly added to the profile's :attr:`pdftools_sdk.signature_validation.profiles.validation_options.ValidationOptions.certificate_sources` .



        Args:
            val (pdftools_sdk.signature_validation.data_source.DataSource):
                property value

        """
        from pdftools_sdk.signature_validation.data_source import DataSource

        if not isinstance(val, DataSource):
            raise TypeError(f"Expected type {DataSource.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetTrustSources.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetTrustSources.restype = c_bool
        if not _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetTrustSources(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def revocation_check_policy(self) -> RevocationCheckPolicy:
        """
        Whether to check certificate revocation



        Returns:
            pdftools_sdk.signature_validation.profiles.revocation_check_policy.RevocationCheckPolicy

        """
        from pdftools_sdk.signature_validation.profiles.revocation_check_policy import RevocationCheckPolicy

        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetRevocationCheckPolicy.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetRevocationCheckPolicy.restype = c_int
        ret_val = _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_GetRevocationCheckPolicy(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return RevocationCheckPolicy(ret_val)



    @revocation_check_policy.setter
    def revocation_check_policy(self, val: RevocationCheckPolicy) -> None:
        """
        Whether to check certificate revocation



        Args:
            val (pdftools_sdk.signature_validation.profiles.revocation_check_policy.RevocationCheckPolicy):
                property value

        """
        from pdftools_sdk.signature_validation.profiles.revocation_check_policy import RevocationCheckPolicy

        if not isinstance(val, RevocationCheckPolicy):
            raise TypeError(f"Expected type {RevocationCheckPolicy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetRevocationCheckPolicy.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetRevocationCheckPolicy.restype = c_bool
        if not _lib.PdfToolsSignatureValidationProfiles_TrustConstraints_SetRevocationCheckPolicy(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return TrustConstraints._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TrustConstraints.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
