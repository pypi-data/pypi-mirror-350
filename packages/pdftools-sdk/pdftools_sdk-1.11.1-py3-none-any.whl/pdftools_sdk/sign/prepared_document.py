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
import pdftools_sdk.pdf.document

if TYPE_CHECKING:
    from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm

else:
    HashAlgorithm = "pdftools_sdk.crypto.hash_algorithm.HashAlgorithm"


class PreparedDocument(pdftools_sdk.pdf.document.Document):
    """
    A document that has been prepared for signing


    """
    def get_hash(self, algorithm: HashAlgorithm) -> List[int]:
        """
        Calculate the hash value

        Calculate the hash value to create the signature from.



        Args:
            algorithm (pdftools_sdk.crypto.hash_algorithm.HashAlgorithm): 
                The hash algorithm



        Returns:
            List[int]: 


        """
        from pdftools_sdk.crypto.hash_algorithm import HashAlgorithm

        if not isinstance(algorithm, HashAlgorithm):
            raise TypeError(f"Expected type {HashAlgorithm.__name__}, but got {type(algorithm).__name__}.")

        _lib.PdfToolsSign_PreparedDocument_GetHash.argtypes = [c_void_p, c_int, POINTER(c_ubyte), c_size_t]
        _lib.PdfToolsSign_PreparedDocument_GetHash.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_PreparedDocument_GetHash(self._handle, c_int(algorithm.value), None, 0)
        if ret_val_size == -1:
            _NativeBase._throw_last_error(False)
        ret_val = (c_ubyte * ret_val_size)()
        _lib.PdfToolsSign_PreparedDocument_GetHash(self._handle, c_int(algorithm.value), ret_val, c_size_t(ret_val_size))
        return list(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return PreparedDocument._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = PreparedDocument.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
