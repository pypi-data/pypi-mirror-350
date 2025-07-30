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

class Certificate(_NativeObject):
    """
    A X.509 certificate


    """
    @property
    def name(self) -> Optional[str]:
        """
        The name (subject) of the certificate

        The common name (CN) of the person or authority who owns the certificate.



        Returns:
            Optional[str]

        """
        _lib.PdfToolsCryptoProviders_Certificate_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProviders_Certificate_GetNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProviders_Certificate_GetNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProviders_Certificate_GetNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def subject(self) -> str:
        """
        The subject of the certificate

        The distinguished name (DN) of the person or authority who owns the certificate.
        Formatted according to RFC 4514.



        Returns:
            str

        """
        _lib.PdfToolsCryptoProviders_Certificate_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProviders_Certificate_GetSubjectW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProviders_Certificate_GetSubjectW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProviders_Certificate_GetSubjectW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def issuer(self) -> Optional[str]:
        """
        The name of the certificate's issuer (CA)

        The common name (CN) of the certificate authority (CA) who issued the certificate.



        Returns:
            Optional[str]

        """
        _lib.PdfToolsCryptoProviders_Certificate_GetIssuerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProviders_Certificate_GetIssuerW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProviders_Certificate_GetIssuerW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProviders_Certificate_GetIssuerW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def fingerprint(self) -> Optional[str]:
        """
        The certificate's fingerprint

        The hex string representation of the certificate’s SHA-1 digest.



        Returns:
            Optional[str]

        """
        _lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProviders_Certificate_GetFingerprintW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def has_private_key(self) -> bool:
        """
        Whether the cryptographic provider has a private key for the certificate.

        Note that whether the private key is found and whether it can actually be used for signing may depend on the provider's login state.



        Returns:
            bool

        """
        _lib.PdfToolsCryptoProviders_Certificate_GetHasPrivateKey.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProviders_Certificate_GetHasPrivateKey.restype = c_bool
        ret_val = _lib.PdfToolsCryptoProviders_Certificate_GetHasPrivateKey(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




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
