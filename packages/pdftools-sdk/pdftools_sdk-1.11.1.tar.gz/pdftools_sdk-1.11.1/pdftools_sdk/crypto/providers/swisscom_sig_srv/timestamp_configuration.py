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
import pdftools_sdk.sign.timestamp_configuration

if TYPE_CHECKING:
    from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm

else:
    HashAlgorithm = "pdftools_sdk.crypto.hash_algorithm.HashAlgorithm"


class TimestampConfiguration(pdftools_sdk.sign.timestamp_configuration.TimestampConfiguration):
    """
    The time-stamp configuration


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

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_GetHashAlgorithm.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_GetHashAlgorithm.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_GetHashAlgorithm(self._handle)
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
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_SetHashAlgorithm.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_SetHashAlgorithm.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_TimestampConfiguration_SetHashAlgorithm(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return TimestampConfiguration._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TimestampConfiguration.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
