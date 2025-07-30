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

ConsentRequiredFunc = Callable[[str], None]
"""
Event containing the URL for step-up authentication using password and SMS challenge (OTP).
Password and SMS challenge are used as a fallback mechanism for the Mobile ID authentication.
For example, if the Mobile ID of the user is not activated.
The user must be redirected to this URL for consent of will.



Args:
    url (str): 
        The consent URL where the user must be redirected to acknowledge the declaration of will.


"""

class StepUp(_NativeObject):
    """
    The options for step-up authorization using Mobile ID


    """
    # Event definition
    _ConsentRequiredFunc = CFUNCTYPE(None, c_void_p, c_wchar_p)
    def _wrap_consent_required_func(self, py_callback: ConsentRequiredFunc) -> StepUp._ConsentRequiredFunc:

        def _c_callback(event_context, url):
            # Call the Python callback
            py_callback(_utf16_to_string(url))

        # Wrap the callback in CFUNCTYPE so it becomes a valid C function pointer
        return StepUp._ConsentRequiredFunc(_c_callback)


    def __init__(self, msisdn: str, message: str, language: str):
        """

        Args:
            msisdn (str): 
                The mobile phone number

            message (str): 
                The message to be displayed on the mobile phone

            language (str): 
                The language of the message



        """
        if not isinstance(msisdn, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(msisdn).__name__}.")
        if not isinstance(message, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(message).__name__}.")
        if not isinstance(language, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(language).__name__}.")

        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_NewW.argtypes = [c_wchar_p, c_wchar_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_NewW.restype = c_void_p
        ret_val = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_NewW(_string_to_utf16(msisdn), _string_to_utf16(message), _string_to_utf16(language))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)
        self._consent_required_callback_map = {}


    @property
    def m_s_i_s_d_n(self) -> str:
        """
        The mobile phone number

        Example: `"+41798765432"`



        Returns:
            str

        """
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMSISDNW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @m_s_i_s_d_n.setter
    def m_s_i_s_d_n(self, val: str) -> None:
        """
        The mobile phone number

        Example: `"+41798765432"`



        Args:
            val (str):
                property value

        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMSISDNW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMSISDNW.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMSISDNW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def message(self) -> str:
        """
        The message to be displayed on the mobile phone

        Example: `"Do you authorize your signature on Contract.pdf?"`



        Returns:
            str

        """
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetMessageW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @message.setter
    def message(self, val: str) -> None:
        """
        The message to be displayed on the mobile phone

        Example: `"Do you authorize your signature on Contract.pdf?"`



        Args:
            val (str):
                property value

        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMessageW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMessageW.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetMessageW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def language(self) -> str:
        """
        The language of the message

        Example: `"DE"`



        Returns:
            str

        """
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW.restype = c_size_t
        ret_val_size = _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_GetLanguageW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @language.setter
    def language(self, val: str) -> None:
        """
        The language of the message

        Example: `"DE"`



        Args:
            val (str):
                property value

        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetLanguageW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetLanguageW.restype = c_bool
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_SetLanguageW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    def add_consent_required_handler(self, handler: ConsentRequiredFunc) -> None:
        """
        Add handler for the :func:`ConsentRequiredFunc` event.

        Args:
            handler: Event handler. If a handler is added that is already registered, it is ignored.
        """
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_AddConsentRequiredHandlerW.argtypes = [c_void_p, c_void_p, self._ConsentRequiredFunc]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_AddConsentRequiredHandlerW.restype = c_bool

        # Wrap the handler with the C callback
        _c_callback = self._wrap_consent_required_func(handler)

        # Now pass the callback function as a proper C function type instance
        if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_AddConsentRequiredHandlerW(self._handle, None, _c_callback):
            _NativeBase._throw_last_error()

        # Add to the class-level callback map (increase count if already added)
        if handler in self._consent_required_callback_map:
            self._consent_required_callback_map[handler]['count'] += 1
        else:
            self._consent_required_callback_map[handler] = {'callback': _c_callback, 'count': 1}

    def remove_consent_required_handler(self, handler: ConsentRequiredFunc) -> None:
        """
        Remove registered handler of the :func:`ConsentRequiredFunc` event.

        Args:
            handler: Event handler that shall be removed. If a handler is not registered, it is ignored.
        """
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_RemoveConsentRequiredHandlerW.argtypes = [c_void_p, c_void_p, self._ConsentRequiredFunc]
        _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_RemoveConsentRequiredHandlerW.restype = c_bool

        # Check if the handler exists in the class-level map
        if handler in self._consent_required_callback_map:
            from pdftools_sdk.not_found_error import NotFoundError
            _c_callback = self._consent_required_callback_map[handler]['callback']
            try:
                if not _lib.PdfToolsCryptoProvidersSwisscomSigSrv_StepUp_RemoveConsentRequiredHandlerW(self._handle, None, _c_callback):
                    _NativeBase._throw_last_error()
            except pdftools_sdk.NotFoundError as e:
                del self._consent_required_callback_map[handler]

            # Decrease the count or remove the callback entirely
            if self._consent_required_callback_map[handler]['count'] > 1:
                self._consent_required_callback_map[handler]['count'] -= 1
            else:
                del self._consent_required_callback_map[handler]


    @staticmethod
    def _create_dynamic_type(handle):
        return StepUp._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = StepUp.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
        self._consent_required_callback_map = {}
