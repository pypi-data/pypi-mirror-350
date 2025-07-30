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

class StringList(_NativeObject, list):
    """
    """
    def __init__(self):
        """


        """
        _lib.PdfTools_StringList_New.argtypes = []
        _lib.PdfTools_StringList_New.restype = c_void_p
        ret_val = _lib.PdfTools_StringList_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def __len__(self) -> int:
        _lib.PdfTools_StringList_GetCount.argtypes = [c_void_p]
        _lib.PdfTools_StringList_GetCount.restype = c_int
        ret_val = _lib.PdfTools_StringList_GetCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in StringList.")

    def __delitem__(self, index: int) -> None:
        if index < 0:  # Handle negative indexing
            index += len(self)
        self.remove(index)

    def remove(self, index: int) -> None:
        raise NotImplementedError("Removing elements is not supported in StringList.")

    def extend(self, items: StringList) -> None:
        if not isinstance(items, StringList):
            raise TypeError(f"Expected type {StringList.__name__}, but got {type(items).__name__}.")
        for item in items:
            self.append(item)

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError("Insert method is not supported in StringList.")

    def pop(self, index: int = -1) -> Any:
        raise NotImplementedError("Pop method is not supported in StringList.")

    def copy(self) -> StringList:
        raise NotImplementedError("Copy method is not supported in StringList.")

    def sort(self, key=None, reverse=False) -> None:
        raise NotImplementedError("Sort method is not supported in StringList.")

    def reverse(self) -> None:
        raise NotImplementedError("Reverse method is not supported in StringList.")

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        if isinstance(index, slice):
            raise NotImplementedError("Slicing is not implemented.")
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PdfTools_StringList_GetW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
        _lib.PdfTools_StringList_GetW.restype = c_size_t
        ret_val_size = _lib.PdfTools_StringList_GetW(self._handle, index, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfTools_StringList_GetW(self._handle, index, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)

    def __setitem__(self, index: int, value: Any) -> None:
        raise NotImplementedError("Setting elements is not supported in StringList.")

    def append(self, value: str) -> None:
        if not isinstance(value, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(value).__name__}.")

        _lib.PdfTools_StringList_AddW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfTools_StringList_AddW.restype = c_bool
        ret_val = _lib.PdfTools_StringList_AddW(self._handle, _string_to_utf16(value))
        if not ret_val:
            _NativeBase._throw_last_error(False)


    def index(self, value: str, start: int = 0, stop: Optional[int] = None) -> int:
        if not isinstance(value, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(value).__name__}.")
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
        return StringList._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = StringList.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
