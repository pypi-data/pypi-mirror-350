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
    from pdftools_sdk.crypto.providers.built_in.signature_configuration import SignatureConfiguration as BuiltInSignatureConfiguration
    from pdftools_sdk.crypto.providers.built_in.timestamp_configuration import TimestampConfiguration
    from pdftools_sdk.sign.signature_configuration import SignatureConfiguration as SignSignatureConfiguration

else:
    BuiltInSignatureConfiguration = "pdftools_sdk.crypto.providers.built_in.signature_configuration.SignatureConfiguration"
    TimestampConfiguration = "pdftools_sdk.crypto.providers.built_in.timestamp_configuration.TimestampConfiguration"
    SignSignatureConfiguration = "pdftools_sdk.sign.signature_configuration.SignatureConfiguration"


class Provider(pdftools_sdk.crypto.providers.provider.Provider):
    """
    The built-in cryptographic provider

     
    The built-in cryptographic provider requires no cryptographic hardware or external service (except for the optional
    :attr:`pdftools_sdk.crypto.providers.built_in.provider.Provider.timestamp_url` ).
     
    Signing certificates with private keys can be loaded using :meth:`pdftools_sdk.crypto.providers.built_in.provider.Provider.create_signature_from_certificate` .
     
    *Certificates Directory*:
    Additional certificates, e.g. issuer certificates, can be stored in the certificates directory.
    These certificates are required when adding validation information to signatures that do not have the full trust chain embedded.
    The certificates directory may contain certificates in either PEM (.pem, ASCII text) or DER (.cer, binary) form.
     
    - Windows:
      - `%LOCALAPPDATA%\PDF Tools AG\Certificates`
      - `%ProgramData%\PDF Tools AG\Certificates`
    - Linux:
      - `~/.pdf-tools/Certificates` or `$TMP/pdf-tools/Certificates`
      - `/usr/share/pdf-tools/Certificates`
    - macOS:
      - `~/.pdf-tools/Certificates` or `$TMP/pdf-tools/Certificates`
     


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_New.argtypes = []
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_New.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersBuiltIn_Provider_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def create_signature_from_certificate(self, stream: io.IOBase, password: Optional[str]) -> BuiltInSignatureConfiguration:
        """
        Create a configuration to sign with a PFX (PKCS#12) soft certificate

        The file must contain the certificate itself, all certificates of the trust chain, and the private key.



        Args:
            stream (io.IOBase): 
                The signing certificate in PKCS#12 format (.p12, .pfx).

            password (Optional[str]): 
                The password required to decrypt the private key of the archive.



        Returns:
            pdftools_sdk.crypto.providers.built_in.signature_configuration.SignatureConfiguration: 


        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                The PFX (PKCS#12) archive is corrupt and cannot be read.

            pdftools_sdk.password_error.PasswordError:
                The password is invalid.

            ValueError:
                The certificate is not a valid signing certificate


        """
        from pdftools_sdk.crypto.providers.built_in.signature_configuration import SignatureConfiguration as BuiltInSignatureConfiguration

        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateSignatureFromCertificateW.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_wchar_p]
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateSignatureFromCertificateW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateSignatureFromCertificateW(self._handle, _StreamDescriptor(stream), _string_to_utf16(password))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return BuiltInSignatureConfiguration._create_dynamic_type(ret_val)


    def create_timestamp(self) -> TimestampConfiguration:
        """
        Create a time-stamp configuration

        Note that to create time-stamps, the :attr:`pdftools_sdk.crypto.providers.built_in.provider.Provider.timestamp_url`  must be set.




        Returns:
            pdftools_sdk.crypto.providers.built_in.timestamp_configuration.TimestampConfiguration: 


        """
        from pdftools_sdk.crypto.providers.built_in.timestamp_configuration import TimestampConfiguration

        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateTimestamp.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateTimestamp.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreateTimestamp(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return TimestampConfiguration._create_dynamic_type(ret_val)


    def create_prepared_signature(self, size: int, format: str, name: str) -> SignSignatureConfiguration:
        """
        Create a configuration to prepare a signature for an external signature handler

        This method is part of a very specialized use case requiring an external signature handler.
        The process using an external signature handler is:
         
        - :meth:`pdftools_sdk.crypto.providers.built_in.provider.Provider.create_prepared_signature` : Create the signature configuration.
        - :meth:`pdftools_sdk.sign.signer.Signer.add_prepared_signature` : Create the document with the prepared signature.
        - :meth:`pdftools_sdk.sign.prepared_document.PreparedDocument.get_hash` : Calculate the hash from the document and create the signature using an
          external signature handler.
        - :meth:`pdftools_sdk.crypto.providers.built_in.provider.Provider.read_external_signature` : Create signature configuration for the external signature.
        - :meth:`pdftools_sdk.sign.signer.Signer.sign_prepared_signature` : Insert the external signature into the document with the prepared signature.
         



        Args:
            size (int): 
                The expected size of the cryptographic signature that will be added later.
                This is the number of bytes that will be reserved in the prepared signature.

            format (str): 
                The format (SubFilter) of the cryptographic signature that is added later.
                For example, `"adbe.pkcs7.detached"` or `"ETSI.CAdES.detached"`.

            name (str): 
                The name of the signer of the cryptographic signature that will be added later.



        Returns:
            pdftools_sdk.sign.signature_configuration.SignatureConfiguration: 


        """
        from pdftools_sdk.sign.signature_configuration import SignatureConfiguration as SignSignatureConfiguration

        if not isinstance(size, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(size).__name__}.")
        if not isinstance(format, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(format).__name__}.")
        if not isinstance(name, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(name).__name__}.")

        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreatePreparedSignatureW.argtypes = [c_void_p, c_int, c_wchar_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreatePreparedSignatureW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersBuiltIn_Provider_CreatePreparedSignatureW(self._handle, size, _string_to_utf16(format), _string_to_utf16(name))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignSignatureConfiguration._create_dynamic_type(ret_val)


    def read_external_signature(self, signature: List[int]) -> SignSignatureConfiguration:
        """
        Read signature created by an external signature handler

        See :meth:`pdftools_sdk.crypto.providers.built_in.provider.Provider.create_prepared_signature`  for more information on the signing process using an external signature handler.



        Args:
            signature (List[int]): 
                This signature must not be larger than the number of bytes reserved in the prepared signature.



        Returns:
            pdftools_sdk.sign.signature_configuration.SignatureConfiguration: 


        """
        from pdftools_sdk.sign.signature_configuration import SignatureConfiguration as SignSignatureConfiguration

        if not isinstance(signature, list):
            raise TypeError(f"Expected type {list.__name__}, but got {type(signature).__name__}.")
        if not all(isinstance(c, int) for c in signature):
            raise TypeError(f"All elements in {signature} must be {int}")

        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_ReadExternalSignature.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t]
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_ReadExternalSignature.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersBuiltIn_Provider_ReadExternalSignature(self._handle, (c_ubyte * len(signature))(*signature), len(signature))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignSignatureConfiguration._create_dynamic_type(ret_val)



    @property
    def timestamp_url(self) -> Optional[str]:
        """
        The URL of the trusted time-stamp authority (TSA) from which time-stamps shall be acquired

         
        The TSA must support the time-stamp protocol as defined in RFC 3161.
         
        The property’s value must be a URL with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›][/‹resource›]`
         
        Where:
         
        - `http/https`: Protocol for connection to TSA.
        - `‹user›:‹password›` (optional): Credentials for connection to TSA (basic authorization).
        - `‹host›`: Hostname of TSA.
        - `‹port›`: Port for connection to TSA.
        - `‹resource›`: The resource.
         
         
        Applying a time-stamp requires an online connection to a time server; the firewall must be configured accordingly.
        If a web proxy is used (see :attr:`pdftools_sdk.sdk.Sdk.proxy` ), make sure the following MIME types are supported:
         
        - `application/timestamp-query`
        - `application/timestamp-reply`
         



        Returns:
            Optional[str]

        """
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_GetTimestampUrlW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @timestamp_url.setter
    def timestamp_url(self, val: Optional[str]) -> None:
        """
        The URL of the trusted time-stamp authority (TSA) from which time-stamps shall be acquired

         
        The TSA must support the time-stamp protocol as defined in RFC 3161.
         
        The property’s value must be a URL with the following elements:
         
        `http[s]://[‹user›[:‹password›]@]‹host›[:‹port›][/‹resource›]`
         
        Where:
         
        - `http/https`: Protocol for connection to TSA.
        - `‹user›:‹password›` (optional): Credentials for connection to TSA (basic authorization).
        - `‹host›`: Hostname of TSA.
        - `‹port›`: Port for connection to TSA.
        - `‹resource›`: The resource.
         
         
        Applying a time-stamp requires an online connection to a time server; the firewall must be configured accordingly.
        If a web proxy is used (see :attr:`pdftools_sdk.sdk.Sdk.proxy` ), make sure the following MIME types are supported:
         
        - `application/timestamp-query`
        - `application/timestamp-reply`
         



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_SetTimestampUrlW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersBuiltIn_Provider_SetTimestampUrlW.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersBuiltIn_Provider_SetTimestampUrlW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Provider._from_handle(handle)


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
