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
    from pdftools_sdk.sign.appearance import Appearance

else:
    Appearance = "pdftools_sdk.sign.appearance.Appearance"


class SignatureConfiguration(_NativeObject):
    """
    Configuration for signature creation

     
    This configuration controls the signature creation in :meth:`pdftools_sdk.sign.signer.Signer.sign`  and :meth:`pdftools_sdk.sign.signer.Signer.certify` .
     
    Use a :class:`pdftools_sdk.crypto.providers.provider.Provider`  to create a signature configuration.
     
    Note that this object can be re-used to sign multiple documents for mass-signing applications.


    """
    @property
    def field_name(self) -> Optional[str]:
        """
        The name of the existing signature field

         
        The :attr:`pdftools_sdk.pdf.signature_field.SignatureField.field_name`  of an existing, unsigned signature field to sign.
        Note that when an existing signature field is signed, the appearance's position is defined by the existing field.
        Therefore, make sure the :attr:`pdftools_sdk.sign.signature_configuration.SignatureConfiguration.appearance`  fits into the :attr:`pdftools_sdk.pdf.signature_field.SignatureField.bounding_box` .
         
        If `None` a new signature field is created using a unique field name.
         
        Default is `None`



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        _lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_SignatureConfiguration_GetFieldNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @field_name.setter
    def field_name(self, val: Optional[str]) -> None:
        """
        The name of the existing signature field

         
        The :attr:`pdftools_sdk.pdf.signature_field.SignatureField.field_name`  of an existing, unsigned signature field to sign.
        Note that when an existing signature field is signed, the appearance's position is defined by the existing field.
        Therefore, make sure the :attr:`pdftools_sdk.sign.signature_configuration.SignatureConfiguration.appearance`  fits into the :attr:`pdftools_sdk.pdf.signature_field.SignatureField.bounding_box` .
         
        If `None` a new signature field is created using a unique field name.
         
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
        _lib.PdfToolsSign_SignatureConfiguration_SetFieldNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsSign_SignatureConfiguration_SetFieldNameW.restype = c_bool
        if not _lib.PdfToolsSign_SignatureConfiguration_SetFieldNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def appearance(self) -> Optional[Appearance]:
        """
        The visual appearance of the signature

         
        The visual appearance or `None` to create a signature without a visual appearance.
         
        Default is `None`



        Returns:
            Optional[pdftools_sdk.sign.appearance.Appearance]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        from pdftools_sdk.sign.appearance import Appearance

        _lib.PdfToolsSign_SignatureConfiguration_GetAppearance.argtypes = [c_void_p]
        _lib.PdfToolsSign_SignatureConfiguration_GetAppearance.restype = c_void_p
        ret_val = _lib.PdfToolsSign_SignatureConfiguration_GetAppearance(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Appearance._create_dynamic_type(ret_val)


    @appearance.setter
    def appearance(self, val: Optional[Appearance]) -> None:
        """
        The visual appearance of the signature

         
        The visual appearance or `None` to create a signature without a visual appearance.
         
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
        _lib.PdfToolsSign_SignatureConfiguration_SetAppearance.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsSign_SignatureConfiguration_SetAppearance.restype = c_bool
        if not _lib.PdfToolsSign_SignatureConfiguration_SetAppearance(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def name(self) -> Optional[str]:
        """
        The name of the signing certificate



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        _lib.PdfToolsSign_SignatureConfiguration_GetNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_SignatureConfiguration_GetNameW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_SignatureConfiguration_GetNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_SignatureConfiguration_GetNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def location(self) -> Optional[str]:
        """
        The location of signing

        The CPU host name or physical location of the signing.



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        _lib.PdfToolsSign_SignatureConfiguration_GetLocationW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_SignatureConfiguration_GetLocationW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_SignatureConfiguration_GetLocationW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_SignatureConfiguration_GetLocationW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @location.setter
    def location(self, val: Optional[str]) -> None:
        """
        The location of signing

        The CPU host name or physical location of the signing.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_SignatureConfiguration_SetLocationW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsSign_SignatureConfiguration_SetLocationW.restype = c_bool
        if not _lib.PdfToolsSign_SignatureConfiguration_SetLocationW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def reason(self) -> Optional[str]:
        """
        The reason for signing



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        _lib.PdfToolsSign_SignatureConfiguration_GetReasonW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_SignatureConfiguration_GetReasonW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_SignatureConfiguration_GetReasonW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_SignatureConfiguration_GetReasonW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @reason.setter
    def reason(self, val: Optional[str]) -> None:
        """
        The reason for signing



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_SignatureConfiguration_SetReasonW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsSign_SignatureConfiguration_SetReasonW.restype = c_bool
        if not _lib.PdfToolsSign_SignatureConfiguration_SetReasonW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def contact_info(self) -> Optional[str]:
        """
        The contact information of the signer

        Information provided by the signer to enable a recipient to contact
        the signer to verify the signature.
        For example, a phone number.



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        _lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW.restype = c_size_t
        ret_val_size = _lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsSign_SignatureConfiguration_GetContactInfoW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @contact_info.setter
    def contact_info(self, val: Optional[str]) -> None:
        """
        The contact information of the signer

        Information provided by the signer to enable a recipient to contact
        the signer to verify the signature.
        For example, a phone number.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the creating provider has already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_SignatureConfiguration_SetContactInfoW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsSign_SignatureConfiguration_SetContactInfoW.restype = c_bool
        if not _lib.PdfToolsSign_SignatureConfiguration_SetContactInfoW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PdfToolsSign_SignatureConfiguration_GetType.argtypes = [c_void_p]
        _lib.PdfToolsSign_SignatureConfiguration_GetType.restype = c_int

        obj_type = _lib.PdfToolsSign_SignatureConfiguration_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return SignatureConfiguration._from_handle(handle)
        elif obj_type == 1:
            from pdftools_sdk.crypto.providers.global_sign_dss.signature_configuration import SignatureConfiguration 
            return SignatureConfiguration._from_handle(handle)
        elif obj_type == 2:
            from pdftools_sdk.crypto.providers.swisscom_sig_srv.signature_configuration import SignatureConfiguration 
            return SignatureConfiguration._from_handle(handle)
        elif obj_type == 3:
            from pdftools_sdk.crypto.providers.pkcs11.signature_configuration import SignatureConfiguration 
            return SignatureConfiguration._from_handle(handle)
        elif obj_type == 4:
            from pdftools_sdk.crypto.providers.built_in.signature_configuration import SignatureConfiguration 
            return SignatureConfiguration._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = SignatureConfiguration.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
