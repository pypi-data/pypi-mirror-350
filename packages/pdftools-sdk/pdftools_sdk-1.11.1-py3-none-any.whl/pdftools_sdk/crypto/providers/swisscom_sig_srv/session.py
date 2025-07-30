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
    from pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration import SignatureConfiguration
    from pdftools_sdk.crypto.providers.swisscom_sig_srv.step_up import StepUp
    from pdftools_sdk.crypto.providers.swisscom_sig_srv.timestamp_configuration import TimestampConfiguration
    from pdftools_sdk.http_client_handler import HttpClientHandler

else:
    SignatureConfiguration = "pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration.SignatureConfiguration"
    StepUp = "pdftools_sdk.crypto.providers.swisscom_sig_srv.step_up.StepUp"
    TimestampConfiguration = "pdftools_sdk.crypto.providers.swisscom_sig_srv.timestamp_configuration.TimestampConfiguration"
    HttpClientHandler = "pdftools_sdk.http_client_handler.HttpClientHandler"


class Session(pdftools_sdk.crypto.providers.provider.Provider):
    """
    The Swisscom Signing Service

     
     
    When signing with this provider, these errors can occur:
     
    - :class:`pdftools_sdk.permission_error.PermissionError` : The server did not accept the SSL client certificate or the Claimed Identity string.
    - :class:`pdftools_sdk.permission_error.PermissionError` : The requested requested distinguished name of the on-demand certificate is not allowed (:meth:`pdftools_sdk.crypto.providers.swisscom_sig_srv.session.Session.create_signature_for_on_demand_identity` ).
    - :class:`pdftools_sdk.retry_error.RetryError` : The signing request could not be processed on time by the service.
      The service may be overloaded.
    - :class:`ValueError` : The key identity of the Claimed Identity string is invalid or not allowed.
    - :class:`pdftools_sdk.http_error.HttpError` : If a network error occurs or the service is not operational.
     
     
    When signing with step-up authorization, these errors can also occur.
     
    - :class:`pdftools_sdk.permission_error.PermissionError` : The user canceled the authorization request or failed to enter correct authentication data (password, OTP).
     


    """
    def __init__(self, url: str, http_client_handler: HttpClientHandler):
        """

        Args:
            url (str): 
                 
                The service endpoint base URL.
                 
                Example: `https://ais.swisscom.com`

            httpClientHandler (pdftools_sdk.http_client_handler.HttpClientHandler): 
                The SSL configuration with the client certificate and trust store.
                Use :meth:`pdftools_sdk.http_client_handler.HttpClientHandler.set_client_certificate`  to set your SSL client certificate "clientcert.p12"
                of your Swisscom Signing Service account.



        Raises:
            pdftools_sdk.http_error.HttpError:
                If a network error occurs.

            pdftools_sdk.permission_error.PermissionError:
                If the SSL client certificate is rejected.


        """
        from pdftools_sdk.http_client_handler import HttpClientHandler

        if not isinstance(url, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(url).__name__}.")
        if not isinstance(http_client_handler, HttpClientHandler):
            raise TypeError(f"Expected type {HttpClientHandler.__name__}, but got {type(http_client_handler).__name__}.")

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_NewW.argtypes = [c_wchar_p, c_void_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_NewW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_NewW(_string_to_utf16(url), http_client_handler._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def create_signature_for_static_identity(self, identity: str, name: str) -> SignatureConfiguration:
        """
        Create a signature configuration for a static certificate.



        Args:
            identity (str): 
                 
                The Claimed Identity string as provided by Swisscom: `‹customer name›:‹key identity›`
                 
                Example: `"ais-90days-trial:static-saphir4-ch"`

            name (str): 
                 
                Name of the signer.
                This parameter is not used for certificate selection, but for the signature appearance and signature description in the PDF only.
                 
                Example: `"Signing Service TEST account"`



        Returns:
            pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration.SignatureConfiguration: 


        """
        from pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration import SignatureConfiguration

        if not isinstance(identity, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(identity).__name__}.")
        if not isinstance(name, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(name).__name__}.")

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForStaticIdentityW.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForStaticIdentityW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForStaticIdentityW(self._handle, _string_to_utf16(identity), _string_to_utf16(name))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_signature_for_on_demand_identity(self, identity: str, distinguished_name: str, step_up: Optional[StepUp]) -> SignatureConfiguration:
        """
        Create a signature configuration for an on-demand certificate



        Args:
            identity (str): 
                 
                The Claimed Identity string as provided by Swisscom: `‹customer name›:‹key identity›`
                 
                Example: `"ais-90days-trial:OnDemand-Advanced4"`

            distinguishedName (str): 
                 
                The requested distinguished name of the on-demand certificate.
                 
                Example: `"cn=Hans Muster,o=ACME,c=CH"`

            stepUp (Optional[pdftools_sdk.crypto.providers.swisscom_sig_srv.step_up.StepUp]): 
                Options for step-up authorization using Mobile ID.



        Returns:
            pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration.SignatureConfiguration: 


        """
        from pdftools_sdk.crypto.providers.swisscom_sig_srv.step_up import StepUp
        from pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration import SignatureConfiguration

        if not isinstance(identity, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(identity).__name__}.")
        if not isinstance(distinguished_name, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(distinguished_name).__name__}.")
        if step_up is not None and not isinstance(step_up, StepUp):
            raise TypeError(f"Expected type {StepUp.__name__} or None, but got {type(step_up).__name__}.")

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForOnDemandIdentityW.argtypes = [c_void_p, c_wchar_p, c_wchar_p, c_void_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForOnDemandIdentityW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateSignatureForOnDemandIdentityW(self._handle, _string_to_utf16(identity), _string_to_utf16(distinguished_name), step_up._handle if step_up is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_timestamp(self, identity: str) -> TimestampConfiguration:
        """
        Create a time-stamp configuration



        Args:
            identity (str): 
                 
                The Claimed Identity string as provided by Swisscom: `‹customer name›`
                 
                Example: `"ais-90days-trial"`



        Returns:
            pdftools_sdk.crypto.providers.swisscom_sig_srv.timestamp_configuration.TimestampConfiguration: 


        """
        from pdftools_sdk.crypto.providers.swisscom_sig_srv.timestamp_configuration import TimestampConfiguration

        if not isinstance(identity, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(identity).__name__}.")

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateTimestampW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateTimestampW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_Session_CreateTimestampW(self._handle, _string_to_utf16(identity))
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
