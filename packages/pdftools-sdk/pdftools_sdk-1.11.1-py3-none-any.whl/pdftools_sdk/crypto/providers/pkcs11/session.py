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
    from pdftools_sdk.crypto.providers.certificate import Certificate
    from pdftools_sdk.crypto.providers.pkcs11.signature_configuration import SignatureConfiguration
    from pdftools_sdk.crypto.providers.pkcs11.timestamp_configuration import TimestampConfiguration
    from pdftools_sdk.crypto.providers.certificate_list import CertificateList

else:
    Certificate = "pdftools_sdk.crypto.providers.certificate.Certificate"
    SignatureConfiguration = "pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration"
    TimestampConfiguration = "pdftools_sdk.crypto.providers.pkcs11.timestamp_configuration.TimestampConfiguration"
    CertificateList = "pdftools_sdk.crypto.providers.certificate_list.CertificateList"


class Session(pdftools_sdk.crypto.providers.provider.Provider):
    """
    A session to a cryptographic device (HSM, USB token, etc.) to perform cryptographic operations

     
    The session can be used to create signature configuration to sign documents.
     
    To acquire a session, the following steps must be performed:
     
    - Load the PKCS#11 driver module using :meth:`pdftools_sdk.crypto.providers.pkcs11.module.Module.load` .
    - Get the appropriate cryptographic device from the module's :attr:`pdftools_sdk.crypto.providers.pkcs11.module.Module.devices` .
      If it can be assumed that there is only a single device available, the :meth:`pdftools_sdk.crypto.providers.pkcs11.device_list.DeviceList.get_single`  can be used.
    - Create a session to the device using :meth:`pdftools_sdk.crypto.providers.pkcs11.device.Device.create_session` .
     


    """
    def login(self, password: Optional[str]) -> None:
        """
        Log in user into the cryptographic device

         
        Login is typically required to enable cryptographic operations.
        Furthermore, some of the device's objects such as certificates or private keys might only be visible when logged in.
         
        Note that many devices are locked after a number of failed login attempts.
        Therefore, it is crucial to not retry this method using the same `password` after a failed attempt.



        Args:
            password (Optional[str]): 
                The user's password




        Raises:
            pdftools_sdk.password_error.PasswordError:
                If the `password` is not correct

            pdftools_sdk.permission_error.PermissionError:
                If the `password` has been locked or is expired

            OperationError:
                If the user has already logged in


        """
        if password is not None and not isinstance(password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(password).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_Session_LoginW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_LoginW.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_Session_LoginW(self._handle, _string_to_utf16(password)):
            _NativeBase._throw_last_error(False)


    def create_signature(self, certificate: Certificate) -> SignatureConfiguration:
        """
        Create a signature configuration based on signing certificate



        Args:
            certificate (pdftools_sdk.crypto.providers.certificate.Certificate): 
                The signing certificate from :attr:`pdftools_sdk.crypto.providers.pkcs11.session.Session.certificates` 



        Returns:
            pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration: 


        Raises:
            ValueError:
                If the `certificate` is not a valid signing certificate.

            ValueError:
                If the `certificate` has expired.


        """
        from pdftools_sdk.crypto.providers.certificate import Certificate
        from pdftools_sdk.crypto.providers.pkcs11.signature_configuration import SignatureConfiguration

        if not isinstance(certificate, Certificate):
            raise TypeError(f"Expected type {Certificate.__name__}, but got {type(certificate).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignature.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignature.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignature(self._handle, certificate._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_signature_from_name(self, name: str) -> SignatureConfiguration:
        """
        Create a signature configuration based on certificate name



        Args:
            name (str): 
                The name of the signing certificate (:attr:`pdftools_sdk.crypto.providers.certificate.Certificate.name` )



        Returns:
            pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration: 


        Raises:
            pdftools_sdk.not_found_error.NotFoundError:
                If the certificate cannot be found in :attr:`pdftools_sdk.crypto.providers.pkcs11.session.Session.certificates` 

            ValueError:
                If the certificate is not a valid signing certificate


        """
        from pdftools_sdk.crypto.providers.pkcs11.signature_configuration import SignatureConfiguration

        if not isinstance(name, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(name).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromNameW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromNameW(self._handle, _string_to_utf16(name))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_signature_from_key_id(self, id: List[int], certificate: io.IOBase) -> SignatureConfiguration:
        """
        Create a signature configuration based on the private key's ID and an external certificate

         
        Create a signature configuration where only the private key is contained in the PKCS#11 device and
        the signing certificate is provided externally.
        This is intended for PKCS#11 devices that can only store private keys, e.g. the Google Cloud Key Management (KMS).
         
        The private key object is identified using its ID,
        i.e. the `CKA_ID` object attribute in the PKCS#11 store.
         
        The certificates of the trust chain should be added using :meth:`pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration.add_certificate` .



        Args:
            id (List[int]): 
                The ID of the private key object in the PKCS#11 store

            certificate (io.IOBase): 
                The signing certificate in either PEM (.pem, ASCII text) or DER (.cer, binary) form



        Returns:
            pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration: 


        Raises:
            pdftools_sdk.not_found_error.NotFoundError:
                If the private key cannot be found in the PKCS#11 store

            ValueError:
                If the certificate is not a valid signing certificate

            ValueError:
                If the key specification matches more than one key


        """
        from pdftools_sdk.crypto.providers.pkcs11.signature_configuration import SignatureConfiguration

        if not isinstance(id, list):
            raise TypeError(f"Expected type {list.__name__}, but got {type(id).__name__}.")
        if not all(isinstance(c, int) for c in id):
            raise TypeError(f"All elements in {id} must be {int}")
        if not isinstance(certificate, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(certificate).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyId.argtypes = [c_void_p, POINTER(c_ubyte), c_size_t, POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyId.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyId(self._handle, (c_ubyte * len(id))(*id), len(id), _StreamDescriptor(certificate))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_signature_from_key_label(self, label: str, certificate: io.IOBase) -> SignatureConfiguration:
        """
        Create a signature configuration based on the private key's label (name) and an external certificate

         
        Create a signature configuration where only the private key is contained in the PKCS#11 device and
        the signing certificate is provided externally.
        This is intended for PKCS#11 devices that can only store private keys, e.g. the Google Cloud Key Management (KMS).
         
        The private key object is identified using its label,
        i.e. the `CKA_LABEL` object attribute in the PKCS#11 store.
         
        The certificates of the trust chain should be added using :meth:`pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration.add_certificate` .



        Args:
            label (str): 
                The label of the private key object in the PKCS#11 store

            certificate (io.IOBase): 
                The signing certificate in either PEM (.pem, ASCII text) or DER (.cer, binary) form



        Returns:
            pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration: 


        Raises:
            pdftools_sdk.not_found_error.NotFoundError:
                If the private key cannot be found in the PKCS#11 store

            ValueError:
                If the certificate is not a valid signing certificate

            ValueError:
                If the key specification matches more than one key


        """
        from pdftools_sdk.crypto.providers.pkcs11.signature_configuration import SignatureConfiguration

        if not isinstance(label, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(label).__name__}.")
        if not isinstance(certificate, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(certificate).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyLabelW.argtypes = [c_void_p, c_wchar_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyLabelW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateSignatureFromKeyLabelW(self._handle, _string_to_utf16(label), _StreamDescriptor(certificate))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureConfiguration._create_dynamic_type(ret_val)


    def create_timestamp(self) -> TimestampConfiguration:
        """
        Create a time-stamp configuration

        Note that to create time-stamps, the :attr:`pdftools_sdk.crypto.providers.pkcs11.session.Session.timestamp_url`  must be set.




        Returns:
            pdftools_sdk.crypto.providers.pkcs11.timestamp_configuration.TimestampConfiguration: 


        """
        from pdftools_sdk.crypto.providers.pkcs11.timestamp_configuration import TimestampConfiguration

        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateTimestamp.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateTimestamp.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Session_CreateTimestamp(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return TimestampConfiguration._create_dynamic_type(ret_val)



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
        _lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProvidersPkcs11_Session_GetTimestampUrlW(self._handle, ret_val, c_size_t(ret_val_size))
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
        _lib.PdfToolsCryptoProvidersPkcs11_Session_SetTimestampUrlW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_SetTimestampUrlW.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_Session_SetTimestampUrlW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def certificates(self) -> CertificateList:
        """
        The cerfificates of the device

        The certificates available in this device.
        Note that some certificates or their private keys (see :attr:`pdftools_sdk.crypto.providers.certificate.Certificate.has_private_key` ) might only be visible
        after :meth:`pdftools_sdk.crypto.providers.pkcs11.session.Session.login` .



        Returns:
            pdftools_sdk.crypto.providers.certificate_list.CertificateList

        """
        from pdftools_sdk.crypto.providers.certificate_list import CertificateList

        _lib.PdfToolsCryptoProvidersPkcs11_Session_GetCertificates.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_Session_GetCertificates.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_Session_GetCertificates(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return CertificateList._create_dynamic_type(ret_val)



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
