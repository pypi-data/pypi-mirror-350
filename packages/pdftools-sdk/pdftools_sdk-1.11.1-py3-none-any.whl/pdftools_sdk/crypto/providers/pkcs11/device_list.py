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
import pdftools_sdk.crypto.providers.pkcs11.device

if TYPE_CHECKING:
    from pdftools_sdk.crypto.providers.pkcs11.device import Device

else:
    Device = "pdftools_sdk.crypto.providers.pkcs11.device.Device"


class DeviceList(_NativeObject, list):
    """
    The list of devices managed by a PKCS#11 module


    """
    def get_single(self) -> Device:
        """
        Get the single device




        Returns:
            pdftools_sdk.crypto.providers.pkcs11.device.Device: 


        Raises:
            pdftools_sdk.not_found_error.NotFoundError:
                No device was found.
                Make sure the device is connected and the right PKCS#11 modules has been loaded.

            OperationError:
                More than one device available.
                Choose the right one from the device list, e.g. by looking at :attr:`pdftools_sdk.crypto.providers.pkcs11.device.Device.description`  or its
                :attr:`pdftools_sdk.crypto.providers.pkcs11.session.Session.certificates` .


        """
        from pdftools_sdk.crypto.providers.pkcs11.device import Device

        _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetSingle.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetSingle.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetSingle(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Device._create_dynamic_type(ret_val)



    def __len__(self) -> int:
        _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetCount.argtypes = [c_void_p]
        _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetCount.restype = c_int
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_GetCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in DeviceList.")

    def __delitem__(self, index: int) -> None:
        if index < 0:  # Handle negative indexing
            index += len(self)
        self.remove(index)

    def remove(self, index: int) -> None:
        raise NotImplementedError("Removing elements is not supported in DeviceList.")

    def extend(self, items: DeviceList) -> None:
        if not isinstance(items, DeviceList):
            raise TypeError(f"Expected type {DeviceList.__name__}, but got {type(items).__name__}.")
        raise NotImplementedError("Extend method is not supported in DeviceList.")

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError("Insert method is not supported in DeviceList.")

    def pop(self, index: int = -1) -> Any:
        raise NotImplementedError("Pop method is not supported in DeviceList.")

    def copy(self) -> DeviceList:
        raise NotImplementedError("Copy method is not supported in DeviceList.")

    def sort(self, key=None, reverse=False) -> None:
        raise NotImplementedError("Sort method is not supported in DeviceList.")

    def reverse(self) -> None:
        raise NotImplementedError("Reverse method is not supported in DeviceList.")

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        from pdftools_sdk.crypto.providers.pkcs11.device import Device

        if isinstance(index, slice):
            raise NotImplementedError("Slicing is not implemented.")
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_Get.argtypes = [c_void_p, c_int]
        _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_Get.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersPkcs11_DeviceList_Get(self._handle, index)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Device._create_dynamic_type(ret_val)

    def __setitem__(self, index: int, value: Any) -> None:
        raise NotImplementedError("Setting elements is not supported in DeviceList.")

    def append(self, value: Device) -> None:
        raise NotImplementedError("Append method is not supported in DeviceList.")

    def index(self, value: Device, start: int = 0, stop: Optional[int] = None) -> int:
        from pdftools_sdk.crypto.providers.pkcs11.device import Device

        if not isinstance(value, Device):
            raise TypeError(f"Expected type {Device.__name__}, but got {type(value).__name__}.")
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
        return DeviceList._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = DeviceList.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
