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

if TYPE_CHECKING:
    from pdftools_sdk.sys.date import _Date
    from pdftools_sdk.consumption_data import ConsumptionData

else:
    _Date = "pdftools_sdk.sys.date._Date"
    ConsumptionData = "pdftools_sdk.consumption_data.ConsumptionData"


class LicenseInfo(_NativeObject):
    """
    This class contains license information.


    """
    @property
    def is_valid(self) -> bool:
        """
        Denotes whether the license is valid.



        Returns:
            bool

        """
        _lib.PdfTools_LicenseInfo_IsValid.argtypes = [c_void_p]
        _lib.PdfTools_LicenseInfo_IsValid.restype = c_bool
        ret_val = _lib.PdfTools_LicenseInfo_IsValid(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def expiration_date(self) -> Optional[datetime]:
        """
        The license expiration date.



        Returns:
            Optional[datetime]

        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfTools_LicenseInfo_GetExpirationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfTools_LicenseInfo_GetExpirationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfTools_LicenseInfo_GetExpirationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @property
    def consumption_data(self) -> Optional[ConsumptionData]:
        """
        This property exists only for page-based licenses. It is `None` for all other licenses.



        Returns:
            Optional[pdftools_sdk.consumption_data.ConsumptionData]

        """
        from pdftools_sdk.consumption_data import ConsumptionData

        _lib.PdfTools_LicenseInfo_GetConsumptionData.argtypes = [c_void_p]
        _lib.PdfTools_LicenseInfo_GetConsumptionData.restype = c_void_p
        ret_val = _lib.PdfTools_LicenseInfo_GetConsumptionData(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return ConsumptionData._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return LicenseInfo._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = LicenseInfo.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
