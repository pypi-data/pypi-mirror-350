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
    from pdftools_sdk.pdf.mdp_permissions import MdpPermissions

else:
    MdpPermissions = "pdftools_sdk.pdf.mdp_permissions.MdpPermissions"


class MdpPermissionOptions(_NativeObject):
    """
    The permission options when certifying a document


    """
    def __init__(self, permissions: MdpPermissions):
        """

        Args:
            permissions (pdftools_sdk.pdf.mdp_permissions.MdpPermissions): 


        """
        from pdftools_sdk.pdf.mdp_permissions import MdpPermissions

        if not isinstance(permissions, MdpPermissions):
            raise TypeError(f"Expected type {MdpPermissions.__name__}, but got {type(permissions).__name__}.")

        _lib.PdfToolsSign_MdpPermissionOptions_New.argtypes = [c_int]
        _lib.PdfToolsSign_MdpPermissionOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsSign_MdpPermissionOptions_New(c_int(permissions.value))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def permissions(self) -> MdpPermissions:
        """
        The access permissions granted for the document



        Returns:
            pdftools_sdk.pdf.mdp_permissions.MdpPermissions

        """
        from pdftools_sdk.pdf.mdp_permissions import MdpPermissions

        _lib.PdfToolsSign_MdpPermissionOptions_GetPermissions.argtypes = [c_void_p]
        _lib.PdfToolsSign_MdpPermissionOptions_GetPermissions.restype = c_int
        ret_val = _lib.PdfToolsSign_MdpPermissionOptions_GetPermissions(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return MdpPermissions(ret_val)



    @permissions.setter
    def permissions(self, val: MdpPermissions) -> None:
        """
        The access permissions granted for the document



        Args:
            val (pdftools_sdk.pdf.mdp_permissions.MdpPermissions):
                property value

        """
        from pdftools_sdk.pdf.mdp_permissions import MdpPermissions

        if not isinstance(val, MdpPermissions):
            raise TypeError(f"Expected type {MdpPermissions.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsSign_MdpPermissionOptions_SetPermissions.argtypes = [c_void_p, c_int]
        _lib.PdfToolsSign_MdpPermissionOptions_SetPermissions.restype = c_bool
        if not _lib.PdfToolsSign_MdpPermissionOptions_SetPermissions(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return MdpPermissionOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = MdpPermissionOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
