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
import pdftools_sdk.pdf.signature_field

if TYPE_CHECKING:
    from pdftools_sdk.pdf.signature_field import SignatureField

else:
    SignatureField = "pdftools_sdk.pdf.signature_field.SignatureField"


class SignatureFieldList(_NativeObject, list):
    """
    """
    def __len__(self) -> int:
        _lib.PdfToolsPdf_SignatureFieldList_GetCount.argtypes = [c_void_p]
        _lib.PdfToolsPdf_SignatureFieldList_GetCount.restype = c_int
        ret_val = _lib.PdfToolsPdf_SignatureFieldList_GetCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in SignatureFieldList.")

    def __delitem__(self, index: int) -> None:
        if index < 0:  # Handle negative indexing
            index += len(self)
        self.remove(index)

    def remove(self, index: int) -> None:
        raise NotImplementedError("Removing elements is not supported in SignatureFieldList.")

    def extend(self, items: SignatureFieldList) -> None:
        if not isinstance(items, SignatureFieldList):
            raise TypeError(f"Expected type {SignatureFieldList.__name__}, but got {type(items).__name__}.")
        raise NotImplementedError("Extend method is not supported in SignatureFieldList.")

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError("Insert method is not supported in SignatureFieldList.")

    def pop(self, index: int = -1) -> Any:
        raise NotImplementedError("Pop method is not supported in SignatureFieldList.")

    def copy(self) -> SignatureFieldList:
        raise NotImplementedError("Copy method is not supported in SignatureFieldList.")

    def sort(self, key=None, reverse=False) -> None:
        raise NotImplementedError("Sort method is not supported in SignatureFieldList.")

    def reverse(self) -> None:
        raise NotImplementedError("Reverse method is not supported in SignatureFieldList.")

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        from pdftools_sdk.pdf.signature_field import SignatureField

        if isinstance(index, slice):
            raise NotImplementedError("Slicing is not implemented.")
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PdfToolsPdf_SignatureFieldList_Get.argtypes = [c_void_p, c_int]
        _lib.PdfToolsPdf_SignatureFieldList_Get.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_SignatureFieldList_Get(self._handle, index)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return SignatureField._create_dynamic_type(ret_val)

    def __setitem__(self, index: int, value: Any) -> None:
        raise NotImplementedError("Setting elements is not supported in SignatureFieldList.")

    def append(self, value: SignatureField) -> None:
        raise NotImplementedError("Append method is not supported in SignatureFieldList.")

    def index(self, value: SignatureField, start: int = 0, stop: Optional[int] = None) -> int:
        from pdftools_sdk.pdf.signature_field import SignatureField

        if not isinstance(value, SignatureField):
            raise TypeError(f"Expected type {SignatureField.__name__}, but got {type(value).__name__}.")
        if not isinstance(start, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(start).__name__}.")
        if stop is not None and not isinstance(stop, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(stop).__name__}.")

        length = len(self)
        if start < 0:
            start += length
        if stop is None:
            stop = length
        elif stop < 0:
            stop += length

        for i in range(max(start, 0), min(stop, length)):
            if self[i] == value:
                return i

        raise ValueError(f"{value} is not in the list.")


    def __iter__(self):
        self._iter_index = 0  # Initialize the index for iteration
        return self

    def __next__(self):
        if self._iter_index < len(self):  # Check if there are more items to iterate over
            item = self.__getitem__(self._iter_index)  # Get the item at the current index
            self._iter_index += 1  # Move to the next index
            return item
        else:
            raise StopIteration  # Signal that iteration is complete

    @staticmethod
    def _create_dynamic_type(handle):
        return SignatureFieldList._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignatureFieldList.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
