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

class Provider(_NativeObject, ABC):
    """
    Base class for cryptographic providers

     
    The cryptographic provider manages certificates, their private keys and implements cryptographic algorithms.
     
    This SDK supports various different cryptographic providers.
    The following list shows the signing certificate type that can be used for each provider.
     
     
    - *Soft Certificate*:
      Soft certificates are typically PKCS#12 files that have the extension `.pfx` or `.p12` and contain
      the signing certificate as well as the private key and trust chain (issuer certificates).
      Soft certificates can be used with the :class:`pdftools_sdk.crypto.providers.built_in.provider.Provider` , where they can be loaded using
      :meth:`pdftools_sdk.crypto.providers.built_in.provider.Provider.create_signature_from_certificate` .
    - *Hardware Security Module (HSM)*:
      HSMs always offer very good PKCS#11 support, so the :class:`pdftools_sdk.crypto.providers.pkcs11.session.Session`  is suitable.
      For more information and installation instructions, consult the separate document "TechNotePKCS11.pdf".
    - *USB Token or Smart Card*:
      These devices typically offer a PKCS#11 interface, so the recommended provider is the :class:`pdftools_sdk.crypto.providers.pkcs11.session.Session` .
      Note that in any case, signing documents is only possible in an interactive user session.
      So these devices cannot be used in a service or web application environment.
    - *Swisscom Signing Service*:
      The :class:`pdftools_sdk.crypto.providers.swisscom_sig_srv.session.Session`  supports both static and on-demand signing certificates.
    - *GlobalSign Digital Signing Service*:
      The :class:`pdftools_sdk.crypto.providers.global_sign_dss.session.Session`  supports all features of the service.
     


    """
    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PdfToolsCryptoProviders_Provider_Close.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProviders_Provider_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PdfToolsCryptoProviders_Provider_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsCryptoProviders_Provider_GetType.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProviders_Provider_GetType.restype = c_int

        obj_type = _lib.PdfToolsCryptoProviders_Provider_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Provider._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.crypto.providers.global_sign_dss.session import Session 
            return Session._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.crypto.providers.swisscom_sig_srv.session import Session 
            return Session._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.crypto.providers.pkcs11.session import Session 
            return Session._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.crypto.providers.built_in.provider import Provider 
            return Provider._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Provider.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
