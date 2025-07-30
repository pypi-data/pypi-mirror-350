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

if TYPE_CHECKING:
    from pdftools_sdk.signature_validation.profiles.validation_options import ValidationOptions
    from pdftools_sdk.signature_validation.profiles.trust_constraints import TrustConstraints
    from pdftools_sdk.signature_validation.custom_trust_list import CustomTrustList

else:
    ValidationOptions = "pdftools_sdk.signature_validation.profiles.validation_options.ValidationOptions"
    TrustConstraints = "pdftools_sdk.signature_validation.profiles.trust_constraints.TrustConstraints"
    CustomTrustList = "pdftools_sdk.signature_validation.custom_trust_list.CustomTrustList"


class Profile(_NativeObject, ABC):
    """
    The base class for signature validation profiles

    The profile defines the validation constraints.


    """
    @property
    def validation_options(self) -> ValidationOptions:
        """
        Signature validation options



        Returns:
            pdftools_sdk.signature_validation.profiles.validation_options.ValidationOptions

        """
        from pdftools_sdk.signature_validation.profiles.validation_options import ValidationOptions

        _lib.PdfToolsSignatureValidationProfiles_Profile_GetValidationOptions.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_Profile_GetValidationOptions.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidationProfiles_Profile_GetValidationOptions(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ValidationOptions._create_dynamic_type(ret_val)


    @property
    def signing_cert_trust_constraints(self) -> TrustConstraints:
        """
        Trust constraints for certificates of signatures



        Returns:
            pdftools_sdk.signature_validation.profiles.trust_constraints.TrustConstraints

        """
        from pdftools_sdk.signature_validation.profiles.trust_constraints import TrustConstraints

        _lib.PdfToolsSignatureValidationProfiles_Profile_GetSigningCertTrustConstraints.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_Profile_GetSigningCertTrustConstraints.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidationProfiles_Profile_GetSigningCertTrustConstraints(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return TrustConstraints._create_dynamic_type(ret_val)


    @property
    def time_stamp_trust_constraints(self) -> TrustConstraints:
        """
        Trust constraints for certificates of time-stamps



        Returns:
            pdftools_sdk.signature_validation.profiles.trust_constraints.TrustConstraints

        """
        from pdftools_sdk.signature_validation.profiles.trust_constraints import TrustConstraints

        _lib.PdfToolsSignatureValidationProfiles_Profile_GetTimeStampTrustConstraints.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_Profile_GetTimeStampTrustConstraints.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidationProfiles_Profile_GetTimeStampTrustConstraints(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return TrustConstraints._create_dynamic_type(ret_val)


    @property
    def custom_trust_list(self) -> Optional[CustomTrustList]:
        """
        The custom list of trusted certificates

        Default is `None` (no custom trust list)



        Returns:
            Optional[pdftools_sdk.signature_validation.custom_trust_list.CustomTrustList]

        """
        from pdftools_sdk.signature_validation.custom_trust_list import CustomTrustList

        _lib.PdfToolsSignatureValidationProfiles_Profile_GetCustomTrustList.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_Profile_GetCustomTrustList.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidationProfiles_Profile_GetCustomTrustList(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return CustomTrustList._create_dynamic_type(ret_val)


    @custom_trust_list.setter
    def custom_trust_list(self, val: Optional[CustomTrustList]) -> None:
        """
        The custom list of trusted certificates

        Default is `None` (no custom trust list)



        Args:
            val (Optional[pdftools_sdk.signature_validation.custom_trust_list.CustomTrustList]):
                property value

        """
        from pdftools_sdk.signature_validation.custom_trust_list import CustomTrustList

        if val is not None and not isinstance(val, CustomTrustList):
            raise TypeError(f"Expected type {CustomTrustList.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSignatureValidationProfiles_Profile_SetCustomTrustList.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_Profile_SetCustomTrustList.restype = c_bool
        if not _lib.PdfToolsSignatureValidationProfiles_Profile_SetCustomTrustList(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsSignatureValidationProfiles_Profile_GetType.argtypes = [c_void_p]
        _lib.PdfToolsSignatureValidationProfiles_Profile_GetType.restype = c_int

        obj_type = _lib.PdfToolsSignatureValidationProfiles_Profile_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Profile._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.signature_validation.profiles.default import Default 
            return Default._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Profile.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
