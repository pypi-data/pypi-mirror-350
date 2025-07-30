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
import pdftools_sdk.signature_validation.profiles.profile

class Default(pdftools_sdk.signature_validation.profiles.profile.Profile):
    """
    The default signature validation profile

     
    This profile is suitable for general signature validation.
    It is not very strict.
     
    The default values are:
     
    - :attr:`pdftools_sdk.signature_validation.profiles.profile.Profile.validation_options` :
      - :attr:`pdftools_sdk.signature_validation.profiles.validation_options.ValidationOptions.time_source` : :attr:`pdftools_sdk.signature_validation.time_source.TimeSource.PROOFOFEXISTENCE`  + :attr:`pdftools_sdk.signature_validation.time_source.TimeSource.EXPIREDTIMESTAMP`
      - :attr:`pdftools_sdk.signature_validation.profiles.validation_options.ValidationOptions.certificate_sources` : all
      - :attr:`pdftools_sdk.signature_validation.profiles.validation_options.ValidationOptions.revocation_information_sources` : all
    - :attr:`pdftools_sdk.signature_validation.profiles.profile.Profile.signing_cert_trust_constraints` :
      - :attr:`pdftools_sdk.signature_validation.profiles.trust_constraints.TrustConstraints.trust_sources` : :attr:`pdftools_sdk.signature_validation.data_source.DataSource.AATL`  + :attr:`pdftools_sdk.signature_validation.data_source.DataSource.EUTL`  + :attr:`pdftools_sdk.signature_validation.data_source.DataSource.CUSTOMTRUSTLIST`
      - :attr:`pdftools_sdk.signature_validation.profiles.trust_constraints.TrustConstraints.revocation_check_policy` : :attr:`pdftools_sdk.signature_validation.profiles.revocation_check_policy.RevocationCheckPolicy.OPTIONAL`
    - :attr:`pdftools_sdk.signature_validation.profiles.profile.Profile.time_stamp_trust_constraints` :
      - :attr:`pdftools_sdk.signature_validation.profiles.trust_constraints.TrustConstraints.trust_sources` : :attr:`pdftools_sdk.signature_validation.data_source.DataSource.AATL`  + :attr:`pdftools_sdk.signature_validation.data_source.DataSource.EUTL`  + :attr:`pdftools_sdk.signature_validation.data_source.DataSource.CUSTOMTRUSTLIST`
      - :attr:`pdftools_sdk.signature_validation.profiles.trust_constraints.TrustConstraints.revocation_check_policy` : :attr:`pdftools_sdk.signature_validation.profiles.revocation_check_policy.RevocationCheckPolicy.OPTIONAL`
     


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsSignatureValidationProfiles_Default_New.argtypes = []
        _lib.PdfToolsSignatureValidationProfiles_Default_New.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidationProfiles_Default_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @staticmethod
    def _create_dynamic_type(handle):
        return Default._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Default.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
