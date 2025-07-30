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
    from pdftools_sdk.http_client_handler import HttpClientHandler
    from pdftools_sdk.license_info import LicenseInfo

else:
    HttpClientHandler = "pdftools_sdk.http_client_handler.HttpClientHandler"
    LicenseInfo = "pdftools_sdk.license_info.LicenseInfo"


class Sdk(_NativeObject):
    """
    SDK initialization and product information


    """
    @staticmethod
    def initialize(license: str, producer_suffix: Optional[str] = None) -> None:
        """
        Initialize the product and the license key.

        Before calling any of the other functions of the SDK, a license key must be set by calling this method.
        For licensing questions, contact `pdfsales@pdftools.com <mailto:pdfsales@pdftools.com>`.



        Args:
            license (str): 
                The license key.
                The format of the license key is `"<PDFSDK,V1,...>"`

            producerSuffix (Optional[str]): 
                If neither `None` nor empty, this string is appended to the producer string
                within metadata of PDF output documents (see :attr:`pdftools_sdk.sdk.Sdk.producer_full_name` ).




        Raises:
            pdftools_sdk.unknown_format_error.UnknownFormatError:
                The format (version) of the `license` argument is unknown.

            pdftools_sdk.corrupt_error.CorruptError:
                The `license` argument is not a correct license key.

            pdftools_sdk.license_error.LicenseError:
                The `license` argument can be read but the license check failed.

            pdftools_sdk.http_error.HttpError:
                A network error occurred.


        """
        if not isinstance(license, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(license).__name__}.")
        if producer_suffix is not None and not isinstance(producer_suffix, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(producer_suffix).__name__}.")

        _lib.PdfTools_Sdk_InitializeW.argtypes = [c_wchar_p, c_wchar_p]
        _lib.PdfTools_Sdk_InitializeW.restype = c_bool
        if not _lib.PdfTools_Sdk_InitializeW(_string_to_utf16(license), _string_to_utf16(producer_suffix)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def add_font_directory(directory: str) -> None:
        """
        Add custom font directory



        Args:
            directory (str): 
                The path of the directory which contains additional font files to be considered during processing.




        Raises:
            pdftools_sdk.not_found_error.NotFoundError:
                The given directory path does not exist.


        """
        if not isinstance(directory, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(directory).__name__}.")

        _lib.PdfTools_Sdk_AddFontDirectoryW.argtypes = [c_wchar_p]
        _lib.PdfTools_Sdk_AddFontDirectoryW.restype = c_bool
        if not _lib.PdfTools_Sdk_AddFontDirectoryW(_string_to_utf16(directory)):
            _NativeBase._throw_last_error(False)



    @staticmethod
    def get_version() -> str:
        """
        The version of the SDK



        Returns:
            str

        """
        _lib.PdfTools_Sdk_GetVersionW.argtypes = [POINTER(c_wchar), c_size_t]
        _lib.PdfTools_Sdk_GetVersionW.restype = c_size_t
        ret_val_size = _lib.PdfTools_Sdk_GetVersionW(None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfTools_Sdk_GetVersionW(ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @staticmethod
    def set_producer_suffix(val: Optional[str]) -> None:
        """
        The suffix for the producer

        Suffix that is appended to the producer string within metadata of PDF output documents (see :attr:`pdftools_sdk.sdk.Sdk.producer_full_name` ).



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfTools_Sdk_SetProducerSuffixW.argtypes = [c_wchar_p]
        _lib.PdfTools_Sdk_SetProducerSuffixW.restype = c_bool
        if not _lib.PdfTools_Sdk_SetProducerSuffixW(_string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @staticmethod
    def get_producer_full_name() -> str:
        """
        The producer string that is set within the metadata of PDF output documents

        The producer string depends on the license key and producer suffix set in :meth:`pdftools_sdk.sdk.Sdk.initialize` .



        Returns:
            str

        """
        _lib.PdfTools_Sdk_GetProducerFullNameW.argtypes = [POINTER(c_wchar), c_size_t]
        _lib.PdfTools_Sdk_GetProducerFullNameW.restype = c_size_t
        ret_val_size = _lib.PdfTools_Sdk_GetProducerFullNameW(None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfTools_Sdk_GetProducerFullNameW(ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @staticmethod
    def get_proxy() -> Optional[str]:
        """
        Proxy to use for all communication to remote servers

         
        The SDK can use a proxy for all HTTP and HTTPS communication.
         
        The default is `None`, i.e. no proxy is used.
        Otherwise the property’s value must be a URI with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›]`
         
        Where:
         
        - `http/https`: Protocol for connection to proxy.
        - `‹user›:‹password›` (optional): Credentials for connection to proxy (basic authorization).
        - `‹host›`: Hostname of proxy.
        - `‹port›`: Port for connection to proxy.
         
         
        Example: `"http://myproxy:8080"`
         
        For SSL/TLS connections, e.g. to a signature service, the proxy must allow the `HTTP CONNECT` request to the remote server.



        Returns:
            Optional[str]

        """
        _lib.PdfTools_Sdk_GetProxyW.argtypes = [POINTER(c_wchar), c_size_t]
        _lib.PdfTools_Sdk_GetProxyW.restype = c_size_t
        ret_val_size = _lib.PdfTools_Sdk_GetProxyW(None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfTools_Sdk_GetProxyW(ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @staticmethod
    def set_proxy(val: Optional[str]) -> None:
        """
        Proxy to use for all communication to remote servers

         
        The SDK can use a proxy for all HTTP and HTTPS communication.
         
        The default is `None`, i.e. no proxy is used.
        Otherwise the property’s value must be a URI with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›]`
         
        Where:
         
        - `http/https`: Protocol for connection to proxy.
        - `‹user›:‹password›` (optional): Credentials for connection to proxy (basic authorization).
        - `‹host›`: Hostname of proxy.
        - `‹port›`: Port for connection to proxy.
         
         
        Example: `"http://myproxy:8080"`
         
        For SSL/TLS connections, e.g. to a signature service, the proxy must allow the `HTTP CONNECT` request to the remote server.



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfTools_Sdk_SetProxyW.argtypes = [c_wchar_p]
        _lib.PdfTools_Sdk_SetProxyW.restype = c_bool
        if not _lib.PdfTools_Sdk_SetProxyW(_string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @staticmethod
    def get_http_client_handler() -> HttpClientHandler:
        """
        The default handler for communication to remote servers

        This instance is used wherever there is no dedicated HTTP client handler parameter.



        Returns:
            pdftools_sdk.http_client_handler.HttpClientHandler

        """
        from pdftools_sdk.http_client_handler import HttpClientHandler

        _lib.PdfTools_Sdk_GetHttpClientHandler.argtypes = []
        _lib.PdfTools_Sdk_GetHttpClientHandler.restype = c_void_p
        ret_val = _lib.PdfTools_Sdk_GetHttpClientHandler()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return HttpClientHandler._create_dynamic_type(ret_val)


    @staticmethod
    def get_usage_tracking() -> bool:
        """
        Property denoting whether the usage tracking is enabled or disabled

         
        The SDK is allowed to track usage when this property is set to `True`.
        The collected data includes only non-sensitive information, such as the features used,
        the document type, the number of pages, etc.
         
        The default is `True`, i.e. usage tracking is enabled.



        Returns:
            bool

        """
        _lib.PdfTools_Sdk_GetUsageTracking.argtypes = []
        _lib.PdfTools_Sdk_GetUsageTracking.restype = c_bool
        ret_val = _lib.PdfTools_Sdk_GetUsageTracking()
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @staticmethod
    def set_usage_tracking(val: bool) -> None:
        """
        Property denoting whether the usage tracking is enabled or disabled

         
        The SDK is allowed to track usage when this property is set to `True`.
        The collected data includes only non-sensitive information, such as the features used,
        the document type, the number of pages, etc.
         
        The default is `True`, i.e. usage tracking is enabled.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfTools_Sdk_SetUsageTracking.argtypes = [c_bool]
        _lib.PdfTools_Sdk_SetUsageTracking.restype = c_bool
        if not _lib.PdfTools_Sdk_SetUsageTracking(val):
            _NativeBase._throw_last_error(False)

    @staticmethod
    def get_licensing_service() -> str:
        """
        Licensing service to use for all licensing requests

         
        This property is relevant only for page-based licenses and is used to set the Licensing Gateway Service.
         
        The default is `"https://licensing.pdf-tools.com/api/v1/licenses/"` for the online Pdftools Licensing Service.
        If you plan to use the Licensing Gateway Service instead of the Pdftools Licensing Service, the property’s value must be a URI with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›]`
         
        Where:
         
        - `http/https`: Protocol for connection to the Licensing Gateway Service.
        - `‹user›:‹password›` (optional): Credentials for connection to the Licensing Gateway Service (basic authorization).
        - `‹host›`: Hostname of the Licensing Gateway Service.
        - `‹port›`: Port for connection to the Licensing Gateway Service.
         
         
        Example: `"http://localhost:9999"`



        Returns:
            str

        """
        _lib.PdfTools_Sdk_GetLicensingServiceW.argtypes = [POINTER(c_wchar), c_size_t]
        _lib.PdfTools_Sdk_GetLicensingServiceW.restype = c_size_t
        ret_val_size = _lib.PdfTools_Sdk_GetLicensingServiceW(None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfTools_Sdk_GetLicensingServiceW(ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @staticmethod
    def set_licensing_service(val: str) -> None:
        """
        Licensing service to use for all licensing requests

         
        This property is relevant only for page-based licenses and is used to set the Licensing Gateway Service.
         
        The default is `"https://licensing.pdf-tools.com/api/v1/licenses/"` for the online Pdftools Licensing Service.
        If you plan to use the Licensing Gateway Service instead of the Pdftools Licensing Service, the property’s value must be a URI with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›]`
         
        Where:
         
        - `http/https`: Protocol for connection to the Licensing Gateway Service.
        - `‹user›:‹password›` (optional): Credentials for connection to the Licensing Gateway Service (basic authorization).
        - `‹host›`: Hostname of the Licensing Gateway Service.
        - `‹port›`: Port for connection to the Licensing Gateway Service.
         
         
        Example: `"http://localhost:9999"`



        Args:
            val (str):
                property value

        Raises:
            ValueError:
                The URI is invalid.


        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.PdfTools_Sdk_SetLicensingServiceW.argtypes = [c_wchar_p]
        _lib.PdfTools_Sdk_SetLicensingServiceW.restype = c_bool
        if not _lib.PdfTools_Sdk_SetLicensingServiceW(_string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @staticmethod
    def get_license_info_snapshot() -> LicenseInfo:
        """
         
        A new snapshot is created whenever this property is accessed.
         
        Note: :meth:`pdftools_sdk.sdk.Sdk.initialize`  />*must* be called before accessing license information.
        Otherwise, the license is considered invalid.



        Returns:
            pdftools_sdk.license_info.LicenseInfo

        """
        from pdftools_sdk.license_info import LicenseInfo

        _lib.PdfTools_Sdk_GetLicenseInfoSnapshot.argtypes = []
        _lib.PdfTools_Sdk_GetLicenseInfoSnapshot.restype = c_void_p
        ret_val = _lib.PdfTools_Sdk_GetLicenseInfoSnapshot()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return LicenseInfo._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Sdk._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Sdk.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
