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

class CustomTextVariableMap(_NativeObject, dict):
    """
    A map that maps custom text variable names to its value.


    """
    def __len__(self) -> int:
        _lib.PdfToolsSign_CustomTextVariableMap_GetCount.argtypes = [c_void_p]
        _lib.PdfToolsSign_CustomTextVariableMap_GetCount.restype = c_int
        ret_val = _lib.PdfToolsSign_CustomTextVariableMap_GetCount(self._handle)
        if ret_val < 0:
            _NativeBase._throw_last_error(False)
        return ret_val

    def __delitem__(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")

        it = self._get(key)  # Find iterator using the key
        if it == -1:
            raise KeyError(f"Key {key} not found!")

        _lib.PdfToolsSign_CustomTextVariableMap_Remove.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSign_CustomTextVariableMap_Remove.restype = c_bool
        if not _lib.PdfToolsSign_CustomTextVariableMap_Remove(self._handle, it):
            _NativeBase._throw_last_error(False)

    def clear(self) -> None:
        _lib.PdfToolsSign_CustomTextVariableMap_Clear.argtypes = [c_void_p]
        _lib.PdfToolsSign_CustomTextVariableMap_Clear.restype = c_bool
        if not _lib.PdfToolsSign_CustomTextVariableMap_Clear(self._handle):
            _NativeBase._throw_last_error(False)

    def _get(self, key: str) -> int:
        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")

        _lib.PdfToolsSign_CustomTextVariableMap_GetW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsSign_CustomTextVariableMap_GetW.restype = c_int
        ret_val = _lib.PdfToolsSign_CustomTextVariableMap_GetW(self._handle, _string_to_utf16(key))
        if ret_val == -1 and _NativeBase._last_error_code() != 5:
            _NativeBase._throw_last_error()
        return ret_val

    def _get_key(self, it: int) -> str:
        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PdfToolsSign_CustomTextVariableMap_GetKeyW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_CustomTextVariableMap_GetKeyW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_CustomTextVariableMap_GetKeyW(self._handle, it, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_CustomTextVariableMap_GetKeyW(self._handle, it, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)

    def pop(self, key, default=None):
        raise NotImplementedError("Pop method is not supported in CustomTextVariableMap.")

    def popitem(self):
        raise NotImplementedError("Popitem method is not supported in CustomTextVariableMap.")

    def update(self, *args, **kwargs):
        raise NotImplementedError("Update method is not supported in CustomTextVariableMap.")

    def setdefault(self, key, default=None):
        raise NotImplementedError("Setdefault method is not supported in CustomTextVariableMap.")
    def __missing__(self, key):
        raise NotImplementedError("Missing is not supported in CustomTextVariableMap.")

    def __getitem__(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")

        it = self._get(key)
        if it == -1:
            raise KeyError(f"Key {key} not found!")
        return self._get_value(it)

    def __setitem__(self, key: str, value: str) -> None:

        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")
        if not isinstance(value, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(value).__name__}.")

        _lib.PdfToolsSign_CustomTextVariableMap_SetW.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
        _lib.PdfToolsSign_CustomTextVariableMap_SetW.restype = c_bool
        if not _lib.PdfToolsSign_CustomTextVariableMap_SetW(self._handle, _string_to_utf16(key), _string_to_utf16(value)):
            _NativeBase._throw_last_error(False)


    def _get_value(self, it: int) -> str:

        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PdfToolsSign_CustomTextVariableMap_GetValueW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_CustomTextVariableMap_GetValueW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_CustomTextVariableMap_GetValueW(self._handle, it, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_CustomTextVariableMap_GetValueW(self._handle, it, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    # Iterable implementation
    def __iter__(self) -> Iterator[str]:
        return CustomTextVariableMap._CustomTextVariableMapKeyIterator(self)

    def keys(self) -> Iterator[str]:
        return iter(self)

    def _get_begin(self) -> int:
        _lib.PdfToolsSign_CustomTextVariableMap_GetBegin.argtypes = [c_void_p]
        _lib.PdfToolsSign_CustomTextVariableMap_GetBegin.restype = c_int
        ret_val = _lib.PdfToolsSign_CustomTextVariableMap_GetBegin(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def _get_end(self) -> int:
        _lib.PdfToolsSign_CustomTextVariableMap_GetEnd.argtypes = [c_void_p]
        _lib.PdfToolsSign_CustomTextVariableMap_GetEnd.restype = c_int
        ret_val = _lib.PdfToolsSign_CustomTextVariableMap_GetEnd(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def _get_next(self, it: int) -> int:
        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PdfToolsSign_CustomTextVariableMap_GetNext.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSign_CustomTextVariableMap_GetNext.restype = c_int
        ret_val = _lib.PdfToolsSign_CustomTextVariableMap_GetNext(self._handle, it)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def items(self) -> Iterator[Tuple[str, str]]:
        return CustomTextVariableMap._CustomTextVariableMapKeyValueIterator(self)

    def values(self) -> Iterator[str]:
        return CustomTextVariableMap._CustomTextVariableMapValueIterator(self)


    class _CustomTextVariableMapKeyIterator:
        def __init__(self, map_instance: CustomTextVariableMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> CustomTextVariableMap._CustomTextVariableMapKeyIterator:
            return self

        def __next__(self) -> str:
            if self._current == self._end:
                raise StopIteration
            if self._current == -1:
                self._current = self._map_instance._get_begin()
            else:
                self._current = self._map_instance._get_next(self._current)
            if self._current == self._end:
                raise StopIteration
            return self._map_instance._get_key(self._current)

    class _CustomTextVariableMapValueIterator:
        def __init__(self, map_instance: CustomTextVariableMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> CustomTextVariableMap._CustomTextVariableMapValueIterator:
            return self

        def __next__(self):
            if self._current == self._end:
                raise StopIteration
            if self._current == -1:
                self._current = self._map_instance._get_begin()
            else:
                self._current = self._map_instance._get_next(self._current)
            if self._current == self._end:
                raise StopIteration
            return self._map_instance._get_value(self._current)

    class _CustomTextVariableMapKeyValueIterator:
        def __init__(self, map_instance: CustomTextVariableMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> CustomTextVariableMap._CustomTextVariableMapKeyValueIterator:
            return self

        def __next__(self):
            if self._current == self._end:
                raise StopIteration
            if self._current == -1:
                self._current = self._map_instance._get_begin()
            else:
                self._current = self._map_instance._get_next(self._current)
            if self._current == self._end:
                raise StopIteration
            return self._map_instance._get_key(self._current), self._map_instance._get_value(self._current)

    @staticmethod
    def _create_dynamic_type(handle):
        return CustomTextVariableMap._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = CustomTextVariableMap.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
