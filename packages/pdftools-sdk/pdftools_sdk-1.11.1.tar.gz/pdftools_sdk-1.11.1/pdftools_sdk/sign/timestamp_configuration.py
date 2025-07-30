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
from abc import ABC

import pdftools_sdk.internal

if TYPE_CHECKING:
    from pdftools_sdk.sign.appearance import Appearance

else:
    Appearance = "pdftools_sdk.sign.appearance.Appearance"


class TimestampConfiguration(_NativeObject, ABC):
    """
    Configuration for adding time-stamps

     
    This configuration controls the creation of time-stamps in :meth:`pdftools_sdk.sign.signer.Signer.add_timestamp` .
     
    Use a :class:`pdftools_sdk.crypto.providers.provider.Provider`  to create a time-stamp configuration.
     
    Note that this object can be re-used to add time-stamps to multiple documents for mass-signing applications.


    """
    @property
    def field_name(self) -> Optional[str]:
        """
        The name of the existing signature field

         
        The :attr:`pdftools_sdk.pdf.signature_field.SignatureField.field_name`  of an existing, unsigned signature field to time-stamp.
        Note that when an existing signature field is used, the appearance's position is defined by the existing field.
        Therefore, make sure the :attr:`pdftools_sdk.sign.timestamp_configuration.TimestampConfiguration.appearance`  fits into the :attr:`pdftools_sdk.pdf.signature_field.SignatureField.bounding_box` .
         
        If `None`, a new signature field is created using a unique field name.
         
        Default is `None`



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        _lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_TimestampConfiguration_GetFieldNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @field_name.setter
    def field_name(self, val: Optional[str]) -> None:
        """
        The name of the existing signature field

         
        The :attr:`pdftools_sdk.pdf.signature_field.SignatureField.field_name`  of an existing, unsigned signature field to time-stamp.
        Note that when an existing signature field is used, the appearance's position is defined by the existing field.
        Therefore, make sure the :attr:`pdftools_sdk.sign.timestamp_configuration.TimestampConfiguration.appearance`  fits into the :attr:`pdftools_sdk.pdf.signature_field.SignatureField.bounding_box` .
         
        If `None`, a new signature field is created using a unique field name.
         
        Default is `None`



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_TimestampConfiguration_SetFieldNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsSign_TimestampConfiguration_SetFieldNameW.restype = c_bool
        if not _lib.PdfToolsSign_TimestampConfiguration_SetFieldNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def appearance(self) -> Optional[Appearance]:
        """
        The visual appearance of the time-stamp

         
        The visual appearance or `None` to create a time-stamp without a visual appearance.
         
        For time-stamps, not all text variables are available,
        most notably the `[signature:name]`.
         
        Default is `None`



        Returns:
            Optional[pdftools_sdk.sign.appearance.Appearance]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        from pdftools_sdk.sign.appearance import Appearance

        _lib.PdfToolsSign_TimestampConfiguration_GetAppearance.argtypes = [c_void_p]
        _lib.PdfToolsSign_TimestampConfiguration_GetAppearance.restype = c_void_p
        ret_val = _lib.PdfToolsSign_TimestampConfiguration_GetAppearance(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Appearance._create_dynamic_type(ret_val)


    @appearance.setter
    def appearance(self, val: Optional[Appearance]) -> None:
        """
        The visual appearance of the time-stamp

         
        The visual appearance or `None` to create a time-stamp without a visual appearance.
         
        For time-stamps, not all text variables are available,
        most notably the `[signature:name]`.
         
        Default is `None`



        Args:
            val (Optional[pdftools_sdk.sign.appearance.Appearance]):
                property value

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        from pdftools_sdk.sign.appearance import Appearance

        if val is not None and not isinstance(val, Appearance):
            raise TypeError(f"Expected type {Appearance.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_TimestampConfiguration_SetAppearance.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsSign_TimestampConfiguration_SetAppearance.restype = c_bool
        if not _lib.PdfToolsSign_TimestampConfiguration_SetAppearance(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsSign_TimestampConfiguration_GetType.argtypes = [c_void_p]
        _lib.PdfToolsSign_TimestampConfiguration_GetType.restype = c_int

        obj_type = _lib.PdfToolsSign_TimestampConfiguration_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return TimestampConfiguration._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.crypto.providers.global_sign_dss.timestamp_configuration import TimestampConfiguration 
            return TimestampConfiguration._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.crypto.providers.swisscom_sig_srv.timestamp_configuration import TimestampConfiguration 
            return TimestampConfiguration._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.crypto.providers.pkcs11.timestamp_configuration import TimestampConfiguration 
            return TimestampConfiguration._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.crypto.providers.built_in.timestamp_configuration import TimestampConfiguration 
            return TimestampConfiguration._from_handle(handle)
        else:
            return None


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
