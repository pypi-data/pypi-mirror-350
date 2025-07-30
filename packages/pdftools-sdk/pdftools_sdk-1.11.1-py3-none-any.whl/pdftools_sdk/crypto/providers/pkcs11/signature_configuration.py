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
import pdftools_sdk.sign.signature_configuration

if TYPE_CHECKING:
    from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm
    from pdftools_sdk.crypto.signature_padding_type import SignaturePaddingType
    from pdftools_sdk.crypto.signature_format import SignatureFormat
    from pdftools_sdk.crypto.validation_information import ValidationInformation

else:
    HashAlgorithm = "pdftools_sdk.crypto.hash_algorithm.HashAlgorithm"
    SignaturePaddingType = "pdftools_sdk.crypto.signature_padding_type.SignaturePaddingType"
    SignatureFormat = "pdftools_sdk.crypto.signature_format.SignatureFormat"
    ValidationInformation = "pdftools_sdk.crypto.validation_information.ValidationInformation"


class SignatureConfiguration(pdftools_sdk.sign.signature_configuration.SignatureConfiguration):
    """
    The signature configuration


    """
    def add_certificate(self, certificate: io.IOBase) -> None:
        """
        Add a certificate

        Add a certificate to the signature configuration.
        Adding certificates of the trust chain is often required, if they are missing in the PKCS#11 device's store and
        validation information is added (see :attr:`pdftools_sdk.crypto.providers.pkcs11.signature_configuration.SignatureConfiguration.validation_information` ).
        For example, if this object has been created using :meth:`pdftools_sdk.crypto.providers.pkcs11.session.Session.create_signature_from_key_id` .



        Args:
            certificate (io.IOBase): 
                The certificate in either PEM (.pem, ASCII text) or DER (.cer, binary) form




        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                If the certificate is corrupt and cannot be read


        """
        if not isinstance(certificate, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(certificate).__name__}.")

        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_AddCertificate.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_AddCertificate.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_AddCertificate(self._handle, _StreamDescriptor(certificate)):
            _NativeBase._throw_last_error(False)



    @property
    def hash_algorithm(self) -> HashAlgorithm:
        """
        The message digest algorithm

         
        The algorithm used to hash the document and from which the cryptographic signature is created.
         
        Default is :attr:`pdftools_sdk.crypto.hash_algorithm.HashAlgorithm.SHA256` 



        Returns:
            pdftools_sdk.crypto.hash_algorithm.HashAlgorithm

        """
        from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm

        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetHashAlgorithm.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetHashAlgorithm(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return HashAlgorithm(ret_val)



    @hash_algorithm.setter
    def hash_algorithm(self, val: HashAlgorithm) -> None:
        """
        The message digest algorithm

         
        The algorithm used to hash the document and from which the cryptographic signature is created.
         
        Default is :attr:`pdftools_sdk.crypto.hash_algorithm.HashAlgorithm.SHA256` 



        Args:
            val (pdftools_sdk.crypto.hash_algorithm.HashAlgorithm):
                property value

        Raises:
            ValueError:
                If the value is invalid or not supported.


        """
        from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm

        if not isinstance(val, HashAlgorithm):
            raise TypeError(f"Expected type {HashAlgorithm.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetHashAlgorithm.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetHashAlgorithm(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def signature_padding_type(self) -> SignaturePaddingType:
        """
        The padding type of the cryptographic signature

        Default is :attr:`pdftools_sdk.crypto.signature_padding_type.SignaturePaddingType.RSASSAPSS`  for RSA and :attr:`pdftools_sdk.crypto.signature_padding_type.SignaturePaddingType.DEFAULT`  for ECDSA certificates



        Returns:
            pdftools_sdk.crypto.signature_padding_type.SignaturePaddingType

        """
        from pdftools_sdk.crypto.signature_padding_type import SignaturePaddingType

        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignaturePaddingType.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignaturePaddingType.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignaturePaddingType(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return SignaturePaddingType(ret_val)



    @signature_padding_type.setter
    def signature_padding_type(self, val: SignaturePaddingType) -> None:
        """
        The padding type of the cryptographic signature

        Default is :attr:`pdftools_sdk.crypto.signature_padding_type.SignaturePaddingType.RSASSAPSS`  for RSA and :attr:`pdftools_sdk.crypto.signature_padding_type.SignaturePaddingType.DEFAULT`  for ECDSA certificates



        Args:
            val (pdftools_sdk.crypto.signature_padding_type.SignaturePaddingType):
                property value

        Raises:
            ValueError:
                If the value is invalid or not supported.


        """
        from pdftools_sdk.crypto.signature_padding_type import SignaturePaddingType

        if not isinstance(val, SignaturePaddingType):
            raise TypeError(f"Expected type {SignaturePaddingType.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignaturePaddingType.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignaturePaddingType.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignaturePaddingType(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def signature_format(self) -> SignatureFormat:
        """
        The format (encoding) of the cryptographic signature

        Default is :attr:`pdftools_sdk.crypto.signature_format.SignatureFormat.ETSICADESDETACHED` 



        Returns:
            pdftools_sdk.crypto.signature_format.SignatureFormat

        """
        from pdftools_sdk.crypto.signature_format import SignatureFormat

        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignatureFormat.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignatureFormat.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetSignatureFormat(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return SignatureFormat(ret_val)



    @signature_format.setter
    def signature_format(self, val: SignatureFormat) -> None:
        """
        The format (encoding) of the cryptographic signature

        Default is :attr:`pdftools_sdk.crypto.signature_format.SignatureFormat.ETSICADESDETACHED` 



        Args:
            val (pdftools_sdk.crypto.signature_format.SignatureFormat):
                property value

        """
        from pdftools_sdk.crypto.signature_format import SignatureFormat

        if not isinstance(val, SignatureFormat):
            raise TypeError(f"Expected type {SignatureFormat.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignatureFormat.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignatureFormat.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetSignatureFormat(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def add_timestamp(self) -> bool:
        """
        Whether to add a trusted time-stamp to the signature

         
        If `True`, the :attr:`pdftools_sdk.crypto.providers.pkcs11.session.Session.timestamp_url`  must be set.
         
        Default is `False`



        Returns:
            bool

        """
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetAddTimestamp.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetAddTimestamp.restype = c_bool
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetAddTimestamp(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @add_timestamp.setter
    def add_timestamp(self, val: bool) -> None:
        """
        Whether to add a trusted time-stamp to the signature

         
        If `True`, the :attr:`pdftools_sdk.crypto.providers.pkcs11.session.Session.timestamp_url`  must be set.
         
        Default is `False`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetAddTimestamp.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetAddTimestamp.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetAddTimestamp(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def validation_information(self) -> ValidationInformation:
        """
        Whether to add validation information (LTV)

         
        For signing certificates that do not offer validation (revocation) information (OCSP or CRL),
        this property is ignored.
         
        If downloading validation information fails, an error :class:`pdftools_sdk.not_found_error.NotFoundError`  or :class:`pdftools_sdk.http_error.HttpError`  is generated.
        See :attr:`pdftools_sdk.sign.warning_category.WarningCategory.ADDVALIDATIONINFORMATIONFAILED`  for a description of possible error causes
        and solutions.
         
        Default is :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.EMBEDINDOCUMENT`  if the signing certificate offers validation information and :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.NONE`  otherwise



        Returns:
            pdftools_sdk.crypto.validation_information.ValidationInformation

        """
        from pdftools_sdk.crypto.validation_information import ValidationInformation

        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetValidationInformation.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetValidationInformation.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_GetValidationInformation(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ValidationInformation(ret_val)



    @validation_information.setter
    def validation_information(self, val: ValidationInformation) -> None:
        """
        Whether to add validation information (LTV)

         
        For signing certificates that do not offer validation (revocation) information (OCSP or CRL),
        this property is ignored.
         
        If downloading validation information fails, an error :class:`pdftools_sdk.not_found_error.NotFoundError`  or :class:`pdftools_sdk.http_error.HttpError`  is generated.
        See :attr:`pdftools_sdk.sign.warning_category.WarningCategory.ADDVALIDATIONINFORMATIONFAILED`  for a description of possible error causes
        and solutions.
         
        Default is :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.EMBEDINDOCUMENT`  if the signing certificate offers validation information and :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.NONE`  otherwise



        Args:
            val (pdftools_sdk.crypto.validation_information.ValidationInformation):
                property value

        """
        from pdftools_sdk.crypto.validation_information import ValidationInformation

        if not isinstance(val, ValidationInformation):
            raise TypeError(f"Expected type {ValidationInformation.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetValidationInformation.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetValidationInformation.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersPkcs11_SignatureConfiguration_SetValidationInformation(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return SignatureConfiguration._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignatureConfiguration.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
