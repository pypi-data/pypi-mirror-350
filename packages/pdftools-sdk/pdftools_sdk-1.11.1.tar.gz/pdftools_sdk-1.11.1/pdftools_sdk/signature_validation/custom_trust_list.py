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

class CustomTrustList(_NativeObject):
    """
    The custom collection of trusted certificates

    This class defines a custom collection of trusted certificates.
    They define the certificates used for :attr:`pdftools_sdk.signature_validation.data_source.DataSource.CUSTOMTRUSTLIST`  and can be set in the validation profile with :attr:`pdftools_sdk.signature_validation.profiles.profile.Profile.custom_trust_list` .


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsSignatureValidation_CustomTrustList_New.argtypes = []
        _lib.PdfToolsSignatureValidation_CustomTrustList_New.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_CustomTrustList_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def add_certificates(self, certificate: io.IOBase) -> None:
        """
        Add one or more certificates

        Add certificates to the trust list.



        Args:
            certificate (io.IOBase): 
                The sequence of certificates in either PEM (.pem, ASCII text) or DER (.cer, binary) form




        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                If the certificate is corrupt and cannot be read


        """
        if not isinstance(certificate, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(certificate).__name__}.")

        _lib.PdfToolsSignatureValidation_CustomTrustList_AddCertificates.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsSignatureValidation_CustomTrustList_AddCertificates.restype = c_bool
        if not _lib.PdfToolsSignatureValidation_CustomTrustList_AddCertificates(self._handle, _StreamDescriptor(certificate)):
            _NativeBase._throw_last_error(False)


    def add_archive(self, stream: io.IOBase, password: Optional[str] = None) -> None:
        """
        Add certificates from a PFX (PKCS#12) archive

        Add certificates to the trust list.



        Args:
            stream (io.IOBase): 
                The certificates in PKCS#12 format (.p12, .pfx)

            password (Optional[str]): 
                The password required to decrypt the archive.




        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                The PFX (PKCS#12) archive is corrupt and cannot be read.

            pdftools_sdk.password_error.PasswordError:
                The password is invalid.


        """
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PdfToolsSignatureValidation_CustomTrustList_AddArchiveW.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_wchar_p]
        _lib.PdfToolsSignatureValidation_CustomTrustList_AddArchiveW.restype = c_bool
        if not _lib.PdfToolsSignatureValidation_CustomTrustList_AddArchiveW(self._handle, _StreamDescriptor(stream), _string_to_utf16(password)):
            _NativeBase._throw_last_error(False)



    @staticmethod
    def _create_dynamic_type(handle):
        return CustomTrustList._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = CustomTrustList.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
