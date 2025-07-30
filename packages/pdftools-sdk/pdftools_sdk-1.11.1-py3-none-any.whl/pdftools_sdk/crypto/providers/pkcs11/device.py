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
    from pdftools_sdk.crypto.providers.pkcs11.session import Session

else:
    Session = "pdftools_sdk.crypto.providers.pkcs11.session.Session"


class Device(_NativeObject):
    """
    The cryptographic device (HSM, USB token, etc.)


    """
    def create_session(self, password: Optional[str]) -> Session:
        """
        Create a session



        Args:
            password (Optional[str]): 
                If this parameter is not `None`, the session is created and :meth:`pdftools_sdk.crypto.providers.pkcs11.session.Session.login`  executed.



        Returns:
            pdftools_sdk.crypto.providers.pkcs11.session.Session: 


        """
        from pdftools_sdk.crypto.providers.pkcs11.session import Session

        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_Device_CreateSessionW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Device_CreateSessionW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Device_CreateSessionW(self._handle, _string_to_utf16(password))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Session._create_dynamic_type(ret_val)



    @property
    def description(self) -> Optional[str]:
        """
        Description of the device



        Returns:
            Optional[str]

        """
        _lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProvidersPkcs11_Device_GetDescriptionW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def manufacturer_i_d(self) -> Optional[str]:
        """
        ID of the device's manufacturer



        Returns:
            Optional[str]

        """
        _lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProvidersPkcs11_Device_GetManufacturerIDW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)



    @staticmethod
    def _create_dynamic_type(handle):
        return Device._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Device.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
