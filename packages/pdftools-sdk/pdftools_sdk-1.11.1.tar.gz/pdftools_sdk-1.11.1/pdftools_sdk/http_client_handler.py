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

class HttpClientHandler(_NativeObject):
    """
    The handler and options for communication to remote server

     
    This class can be used to configure HTTP and HTTPS communication.
     
    Also see :attr:`pdftools_sdk.sdk.Sdk.proxy`  for the product wide proxy configuration.
     
    For HTTPS (SSL/TLS) communication, the server certificate's trustworthiness is verified using the system's default trust store (CA certificate store).
    If the server certificate's trustworthiness cannot be determined, the connection to the server is aborted.
     
    The default trust store is:
     
    - *Windows:*
      The Windows certificate store for "Trusted Root Certification Authorities" is used.
      You can manually install the root certificate of a private CA on a computer by using the `CertMgr` tool.
      The certificate store is only available if the user profile has been loaded.
    - *Linux:*
      The certificates available in `CAfile` and `CApath` are trusted:
      - `CAfile`:
      The file can contain a concatenated sequence of CA certificates in PEM format.
      The SDK searches for the file at the following locations:
      - The file of your local OpenSSL installation (if `libssl.so` is found), or
      - the environment variable `SSL_CERT_FILE`, or
      - the default location `/etc/ssl/cert.pem`.
      - `CApath`:
      A directory containing CA certificates in PEM format.
      The files are looked up by the CA subject name hash value, e.g. `9d66eef0.0`.
      The SDK searches for the directory at the following locations:
      - The directory of your local OpenSSL installation (if `libssl.so` is found), or
      - the environment variable `SSL_CERT_DIR`, or
      - the default location `/etc/ssl/certs/`.
    - *macOS:*
      The trusted certificates from the macOS keychain are used.
      You can manually install the root certificate of a private CA by dragging the certificate file onto the Keychain Access app.
     
     
    You can add more certificates to the trust store using :meth:`pdftools_sdk.http_client_handler.HttpClientHandler.add_trusted_certificate` .
     
    Instances of this class can be used in multiple threads concurrently, as long as they are not modified concurrently.


    """
    def __init__(self):
        """
        The default values of newly created objects are not copied from the default handler :attr:`pdftools_sdk.sdk.Sdk.http_client_handler` ,
        but are as described in this documentation.




        """
        _lib.PdfTools_HttpClientHandler_New.argtypes = []
        _lib.PdfTools_HttpClientHandler_New.restype = c_void_p
        ret_val = _lib.PdfTools_HttpClientHandler_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def set_client_certificate(self, archive: io.IOBase, password: Optional[str]) -> None:
        """
        Set the SSL/TLS client certificate as PFX (PKCS#12) archive

        The file must contain the certificate itself, all certificates of the trust chain, and the private key.



        Args:
            archive (io.IOBase): 
                The SSL client certificate in PKCS#12 format (.p12, .pfx)

            password (Optional[str]): 
                The password required to decrypt the private key of the archive




        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                The PFX (PKCS#12) archive is corrupt and cannot be read.

            pdftools_sdk.password_error.PasswordError:
                The password is invalid.

            ValueError:
                The PFX (PKCS#12) archive is incomplete.


        """
        if not isinstance(archive, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(archive).__name__}.")
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PdfTools_HttpClientHandler_SetClientCertificateW.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_wchar_p]
        _lib.PdfTools_HttpClientHandler_SetClientCertificateW.restype = c_bool
        if not _lib.PdfTools_HttpClientHandler_SetClientCertificateW(self._handle, _StreamDescriptor(archive), _string_to_utf16(password)):
            _NativeBase._throw_last_error(False)


    def set_client_certificate_and_key(self, cert: io.IOBase, key: io.IOBase, password: Optional[str]) -> None:
        """
        Set the SSL/TLS client certificate and private key

        The file must contain the certificate and its private key.
        It is also recommended to include all certificates of the trust chain.



        Args:
            cert (io.IOBase): 
                The certificate may be in either PEM (.pem, ASCII text) or DER (.cer, binary) form.

            key (io.IOBase): 
                The encrypted private key of the certificate must be in PEM (ASCII text) form (.pem).

            password (Optional[str]): 
                The password required to decrypt the private key.




        Raises:
            pdftools_sdk.password_error.PasswordError:
                The password is invalid.

            pdftools_sdk.corrupt_error.CorruptError:
                The certificate or key cannot be read.


        """
        if not isinstance(cert, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(cert).__name__}.")
        if not isinstance(key, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(key).__name__}.")
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PdfTools_HttpClientHandler_SetClientCertificateAndKeyW.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_wchar_p]
        _lib.PdfTools_HttpClientHandler_SetClientCertificateAndKeyW.restype = c_bool
        if not _lib.PdfTools_HttpClientHandler_SetClientCertificateAndKeyW(self._handle, _StreamDescriptor(cert), _StreamDescriptor(key), _string_to_utf16(password)):
            _NativeBase._throw_last_error(False)


    def add_trusted_certificate(self, cert: io.IOBase) -> None:
        """
        Add a certificate to the trust store

        Add a certificate to the trust store of this `HttpClientHandler` instance.
        The certificates in the trust store are used to verify the certificate of the SSL/TLS server (see :class:`pdftools_sdk.http_client_handler.HttpClientHandler` ).
        You should add trusted certification authorities (Root CA) certificates to the trust store.
        However, you can also add server certificates (e.g. self-signed certificates) and intermediate CA certificates.



        Args:
            cert (io.IOBase): 
                The certificate may be in either PEM (.pem, ASCII text) or DER (.cer, binary) form.




        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                The certificate cannot be read.


        """
        if not isinstance(cert, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(cert).__name__}.")

        _lib.PdfTools_HttpClientHandler_AddTrustedCertificate.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfTools_HttpClientHandler_AddTrustedCertificate.restype = c_bool
        if not _lib.PdfTools_HttpClientHandler_AddTrustedCertificate(self._handle, _StreamDescriptor(cert)):
            _NativeBase._throw_last_error(False)



    @property
    def ssl_verify_server_certificate(self) -> bool:
        """
        Verify the server certificate for SSL/TLS

         
        If `True` the server certificate's trustworthiness is verified.
        If the verification process fails, the handshake is immediately terminated and the connection is aborted.
        The verification requires a trust store; otherwise, verification always fails.
         
        Default is `True`



        Returns:
            bool

        """
        _lib.PdfTools_HttpClientHandler_GetSslVerifyServerCertificate.argtypes = [c_void_p]
        _lib.PdfTools_HttpClientHandler_GetSslVerifyServerCertificate.restype = c_bool
        ret_val = _lib.PdfTools_HttpClientHandler_GetSslVerifyServerCertificate(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @ssl_verify_server_certificate.setter
    def ssl_verify_server_certificate(self, val: bool) -> None:
        """
        Verify the server certificate for SSL/TLS

         
        If `True` the server certificate's trustworthiness is verified.
        If the verification process fails, the handshake is immediately terminated and the connection is aborted.
        The verification requires a trust store; otherwise, verification always fails.
         
        Default is `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfTools_HttpClientHandler_SetSslVerifyServerCertificate.argtypes = [c_void_p, c_bool]
        _lib.PdfTools_HttpClientHandler_SetSslVerifyServerCertificate.restype = c_bool
        if not _lib.PdfTools_HttpClientHandler_SetSslVerifyServerCertificate(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return HttpClientHandler._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = HttpClientHandler.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
