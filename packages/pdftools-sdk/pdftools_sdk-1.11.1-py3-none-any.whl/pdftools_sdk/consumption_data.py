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

class ConsumptionData(_NativeObject):
    """
    This class contains page-based license usage data.


    """
    @property
    def remaining_pages(self) -> int:
        """
        Denotes the number of pages left to consume before entering the over-consumption state.
        When this value reaches zero, the SDK can still be used as long as :attr:`pdftools_sdk.consumption_data.ConsumptionData.overconsumption`  is positive.



        Returns:
            int

        """
        _lib.PdfTools_ConsumptionData_GetRemainingPages.argtypes = [c_void_p]
        _lib.PdfTools_ConsumptionData_GetRemainingPages.restype = c_int
        ret_val = _lib.PdfTools_ConsumptionData_GetRemainingPages(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def overconsumption(self) -> int:
        """
        Denotes the number of pages left to consume in the over-consumption state.
        The over-consumption state begins after all :attr:`pdftools_sdk.consumption_data.ConsumptionData.remaining_pages`  are consumed.
        When this value reaches zero, a license error is thrown for every attempt to use the SDK.



        Returns:
            int

        """
        _lib.PdfTools_ConsumptionData_GetOverconsumption.argtypes = [c_void_p]
        _lib.PdfTools_ConsumptionData_GetOverconsumption.restype = c_int
        ret_val = _lib.PdfTools_ConsumptionData_GetOverconsumption(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        return ConsumptionData._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ConsumptionData.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
