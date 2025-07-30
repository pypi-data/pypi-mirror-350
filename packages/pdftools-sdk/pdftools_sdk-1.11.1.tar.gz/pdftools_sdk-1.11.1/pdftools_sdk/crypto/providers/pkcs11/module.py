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
    from pdftools_sdk.crypto.providers.pkcs11.device_list import DeviceList

else:
    DeviceList = "pdftools_sdk.crypto.providers.pkcs11.device_list.DeviceList"


class Module(_NativeObject):
    """
    The PKCS#11 driver module

     
    The PKCS#11 driver module (middleware) manages the cryptographic devices of a particular type.
     
    *Note:* The PKCS#11 interface requires special handling of the driver modules:
     
    - In each application, the module can only be loaded once,
      so there can only be a single `Module` instance for each driver.
      Since this object is fully thread-safe, it might be used by multiple threads though.
    - The object must be closed before the application terminates.
     


    """
    @staticmethod
    def load(library: str) -> Module:
        """
        Load a PKCS#11 driver module



        Args:
            library (str): 
                 
                The name or path to the driver module (middleware).
                This can be found in the documentation of your cryptographic device.
                 
                Examples:
                 
                - For Securosys SA Primus HSM or CloudsHSM use `primusP11.dll` on Windows and `libprimusP11.so`
                  on Linux.
                - For Google Cloud HSM (Cloud KMS) use `libkmsp11.so` and :meth:`pdftools_sdk.crypto.providers.pkcs11.session.Session.create_signature_from_key_label`
                - For SafeNet Luna HSM use `cryptoki.dll` on Windows or `libCryptoki2_64.so` on Linux/UNIX.
                - The CardOS API from Atos (Siemens) uses `siecap11.dll`
                - The IBM 4758 cryptographic coprocessor uses `cryptoki.dll`
                - Devices from Aladdin Ltd. use `etpkcs11.dll`
                 



        Returns:
            pdftools_sdk.crypto.providers.pkcs11.module.Module: 


        Raises:
            pdftools_sdk.not_found_error.NotFoundError:
                The library cannot be found.

            pdftools_sdk.exists_error.ExistsError:
                The module has been loaded already by this application.

            ValueError:
                The given `library` is not a PKCS#11 driver module.


        """
        if not isinstance(library, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(library).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_Module_LoadW.argtypes = [c_wchar_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Module_LoadW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Module_LoadW(_string_to_utf16(library))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Module._create_dynamic_type(ret_val)



    @property
    def enable_full_parallelization(self) -> bool:
        """
        Enable full parallelization

         
        The PKCS#11 standard specifies that "an application can specify that it will be accessing the library concurrently from multiple
        threads, and the library must [...] ensure proper thread-safe behavior."
        However, some PKCS#11 modules (middleware) implementations are not thread-safe.
        For this reason, the SDK synchronizes all access to the module.
        If the middleware is thread-safe, full parallel usage of the cryptographic device can be enabled by setting this property to `True`
        and thereby improving the performance.
         
        Default is `False`



        Returns:
            bool

        """
        _lib.PdfToolsCryptoProvidersPkcs11_Module_GetEnableFullParallelization.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Module_GetEnableFullParallelization.restype = c_bool
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Module_GetEnableFullParallelization(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @enable_full_parallelization.setter
    def enable_full_parallelization(self, val: bool) -> None:
        """
        Enable full parallelization

         
        The PKCS#11 standard specifies that "an application can specify that it will be accessing the library concurrently from multiple
        threads, and the library must [...] ensure proper thread-safe behavior."
        However, some PKCS#11 modules (middleware) implementations are not thread-safe.
        For this reason, the SDK synchronizes all access to the module.
        If the middleware is thread-safe, full parallel usage of the cryptographic device can be enabled by setting this property to `True`
        and thereby improving the performance.
         
        Default is `False`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersPkcs11_Module_SetEnableFullParallelization.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsCryptoProvidersPkcs11_Module_SetEnableFullParallelization.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_Module_SetEnableFullParallelization(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def devices(self) -> DeviceList:
        """
        The list of devices managed by this module

        Most often there is only a single device, so the method :meth:`pdftools_sdk.crypto.providers.pkcs11.device_list.DeviceList.get_single`  can be used.



        Returns:
            pdftools_sdk.crypto.providers.pkcs11.device_list.DeviceList

        """
        from pdftools_sdk.crypto.providers.pkcs11.device_list import DeviceList

        _lib.PdfToolsCryptoProvidersPkcs11_Module_GetDevices.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Module_GetDevices.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Module_GetDevices(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return DeviceList._create_dynamic_type(ret_val)



    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PdfToolsCryptoProvidersPkcs11_Module_Close.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Module_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PdfToolsCryptoProvidersPkcs11_Module_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        return Module._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Module.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
