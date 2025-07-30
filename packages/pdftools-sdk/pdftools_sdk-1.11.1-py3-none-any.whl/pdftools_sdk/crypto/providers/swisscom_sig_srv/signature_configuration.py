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
    from pdftools_sdk.crypto.signature_format import SignatureFormat

else:
    HashAlgorithm = "pdftools_sdk.crypto.hash_algorithm.HashAlgorithm"
    SignatureFormat = "pdftools_sdk.crypto.signature_format.SignatureFormat"


class SignatureConfiguration(pdftools_sdk.sign.signature_configuration.SignatureConfiguration):
    """
    The signature configuration


    """
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

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetHashAlgorithm.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetHashAlgorithm(self._handle)
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
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetHashAlgorithm.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetHashAlgorithm(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def signature_format(self) -> SignatureFormat:
        """
        The format (encoding) of the cryptographic signature

        Default is :attr:`pdftools_sdk.crypto.signature_format.SignatureFormat.ADBEPKCS7DETACHED` 



        Returns:
            pdftools_sdk.crypto.signature_format.SignatureFormat

        """
        from pdftools_sdk.crypto.signature_format import SignatureFormat

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetSignatureFormat.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetSignatureFormat.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetSignatureFormat(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return SignatureFormat(ret_val)



    @signature_format.setter
    def signature_format(self, val: SignatureFormat) -> None:
        """
        The format (encoding) of the cryptographic signature

        Default is :attr:`pdftools_sdk.crypto.signature_format.SignatureFormat.ADBEPKCS7DETACHED` 



        Args:
            val (pdftools_sdk.crypto.signature_format.SignatureFormat):
                property value

        Raises:
            ValueError:
                If the value is invalid or not supported.


        """
        from pdftools_sdk.crypto.signature_format import SignatureFormat

        if not isinstance(val, SignatureFormat):
            raise TypeError(f"Expected type {SignatureFormat.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetSignatureFormat.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetSignatureFormat.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetSignatureFormat(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def add_timestamp(self) -> bool:
        """
        Whether to add a trusted time-stamp to the signature

        Default is `False`



        Returns:
            bool

        """
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetAddTimestamp.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetAddTimestamp.restype = c_bool
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetAddTimestamp(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @add_timestamp.setter
    def add_timestamp(self, val: bool) -> None:
        """
        Whether to add a trusted time-stamp to the signature

        Default is `False`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetAddTimestamp.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetAddTimestamp.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetAddTimestamp(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def embed_validation_information(self) -> bool:
        """
        Whether to embed validation information into the signature (LTV)

         
         
        - `True`: Create an LTV signature by embedding validation information
          (see :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.EMBEDINSIGNATURE` ).
          This value is only supported, if the :attr:`pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration.SignatureConfiguration.signature_format`  is :attr:`pdftools_sdk.crypto.signature_format.SignatureFormat.ADBEPKCS7DETACHED` .
          LTV signatures for other formats can be created by adding validation information to the signed document (see :meth:`pdftools_sdk.sign.signer.Signer.process`  and :attr:`pdftools_sdk.sign.output_options.OutputOptions.add_validation_information` ).
        - `False`: Create a basic signature without validation information (see :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.NONE` ).
         
         
        Default is `True`



        Returns:
            bool

        """
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetEmbedValidationInformation.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetEmbedValidationInformation.restype = c_bool
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_GetEmbedValidationInformation(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @embed_validation_information.setter
    def embed_validation_information(self, val: bool) -> None:
        """
        Whether to embed validation information into the signature (LTV)

         
         
        - `True`: Create an LTV signature by embedding validation information
          (see :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.EMBEDINSIGNATURE` ).
          This value is only supported, if the :attr:`pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration.SignatureConfiguration.signature_format`  is :attr:`pdftools_sdk.crypto.signature_format.SignatureFormat.ADBEPKCS7DETACHED` .
          LTV signatures for other formats can be created by adding validation information to the signed document (see :meth:`pdftools_sdk.sign.signer.Signer.process`  and :attr:`pdftools_sdk.sign.output_options.OutputOptions.add_validation_information` ).
        - `False`: Create a basic signature without validation information (see :attr:`pdftools_sdk.crypto.validation_information.ValidationInformation.NONE` ).
         
         
        Default is `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetEmbedValidationInformation.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetEmbedValidationInformation.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_SignatureConfiguration_SetEmbedValidationInformation(self._handle, val):
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
