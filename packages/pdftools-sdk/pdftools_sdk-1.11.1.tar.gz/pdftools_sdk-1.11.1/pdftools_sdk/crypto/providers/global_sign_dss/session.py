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
import pdftools_sdk.crypto.providers.provider

if TYPE_CHECKING:
    from pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration import SignatureConfiguration
    from pdftools_sdk.crypto.providers.global_sign_dss.timestamp_configuration import TimestampConfiguration
    from pdftools_sdk.http_client_handler import HttpClientHandler

else:
    SignatureConfiguration = "pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration.SignatureConfiguration"
    TimestampConfiguration = "pdftools_sdk.crypto.providers.global_sign_dss.timestamp_configuration.TimestampConfiguration"
    HttpClientHandler = "pdftools_sdk.http_client_handler.HttpClientHandler"


class Session(pdftools_sdk.crypto.providers.provider.Provider):
    """
    GlobalSign Digital Signing Service

     
    In this session, signatures can be created using different identities, i.e. signing certificates.
    Signing sessions and signing certificates expire after 10 minutes.
    After this time, they are renewed automatically.
     
    When signing with this provider, these errors can occur:
     
    - :class:`pdftools_sdk.permission_error.PermissionError` : If the account's quota is reached.
    - :class:`pdftools_sdk.retry_error.RetryError` : If one of the account's rate limits is exceeded.
      The service enforces rate limits for both creating new identities and signing operations.
      So, if multiple documents must be signed at once, it is advisable to re-use the signature configuration
      (and hence its signing certificates) for signing.
    - :class:`pdftools_sdk.http_error.HttpError` : If a network error occurs or the service is not operational.
     


    """
    def __init__(self, url: str, api_key: str, api_secret: str, http_client_handler: HttpClientHandler):
        """
        Establish a session to the service



        Args:
            url (str): 
                 
                The URL to the service endpoint.
                 
                Typically: `https://emea.api.dss.globalsign.com:8443`

            api_key (str): 
                Your account credentials’ key parameter for the login request.

            api_secret (str): 
                Your account credentials’ secret parameter for the login request.

            httpClientHandler (pdftools_sdk.http_client_handler.HttpClientHandler): 
                The SSL configuration with the client certificate and trust store.
                Use :meth:`pdftools_sdk.http_client_handler.HttpClientHandler.set_client_certificate_and_key`  to set your SSL client certificate "clientcert.crt"
                and private key "privateKey.key" of your GlobalSign account.



        Raises:
            pdftools_sdk.http_error.HttpError:
                If a network error occurs.

            pdftools_sdk.permission_error.PermissionError:
                If a login error occurs, e.g. because the client certificate is rejected or the credentials are incorrect.

            pdftools_sdk.retry_error.RetryError:
                If the login rate limit is exceeded.


        """
        from pdftools_sdk.http_client_handler import HttpClientHandler

        if not isinstance(url, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(url).__name__}.")
        if not isinstance(api_key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(api_key).__name__}.")
        if not isinstance(api_secret, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(api_secret).__name__}.")
        if not isinstance(http_client_handler, HttpClientHandler):
            raise TypeError(f"Expected type {HttpClientHandler.__name__}, but got {type(http_client_handler).__name__}.")

        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_NewW.argtypes = [c_wchar_p, c_wchar_p, c_wchar_p, c_void_p]
        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_NewW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_NewW(_string_to_utf16(url), _string_to_utf16(api_key), _string_to_utf16(api_secret), http_client_handler._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def create_signature_for_static_identity(self) -> SignatureConfiguration:
        """
        Create a signing certificate for an account with a static identity

        The returned signature configuration can be used for multiple signature operations.




        Returns:
            pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration.SignatureConfiguration: 


        Raises:
            pdftools_sdk.http_error.HttpError:
                If a network error occurs.

            pdftools_sdk.permission_error.PermissionError:
                If the request is not authorized by the service.

            pdftools_sdk.retry_error.RetryError:
                If the rate limit for creating new identities has been exceeded.


        """
        from pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration import SignatureConfiguration

        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForStaticIdentity.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForStaticIdentity.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForStaticIdentity(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_signature_for_dynamic_identity(self, identity: str) -> SignatureConfiguration:
        """
        Create a signing certificate for an account with a dynamic identity.



        Args:
            identity (str): 
                 
                The dynamic identity as JSON string.
                 
                Example:
                `{ "subject_dn": {"common_name": "John Doe" } }`



        Returns:
            pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration.SignatureConfiguration: 


        Raises:
            pdftools_sdk.http_error.HttpError:
                If a network error occurs.

            pdftools_sdk.permission_error.PermissionError:
                If the request is not authorized by the service.

            pdftools_sdk.retry_error.RetryError:
                If the rate limit for creating new identities has been exceeded.


        """
        from pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration import SignatureConfiguration

        if not isinstance(identity, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(identity).__name__}.")

        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForDynamicIdentityW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForDynamicIdentityW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateSignatureForDynamicIdentityW(self._handle, _string_to_utf16(identity))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_timestamp(self) -> TimestampConfiguration:
        """
        Create a time-stamp configuration




        Returns:
            pdftools_sdk.crypto.providers.global_sign_dss.timestamp_configuration.TimestampConfiguration: 


        """
        from pdftools_sdk.crypto.providers.global_sign_dss.timestamp_configuration import TimestampConfiguration

        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateTimestamp.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateTimestamp.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersGlobalSignDss_Session_CreateTimestamp(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return TimestampConfiguration._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Session._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Session.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
