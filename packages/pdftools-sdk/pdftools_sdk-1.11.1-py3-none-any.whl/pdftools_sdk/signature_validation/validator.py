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
    from pdftools_sdk.pdf.document import Document
    from pdftools_sdk.signature_validation.profiles.profile import Profile
    from pdftools_sdk.signature_validation.signature_selector import SignatureSelector
    from pdftools_sdk.signature_validation.validation_results import ValidationResults
    from pdftools_sdk.signature_validation.indication import Indication
    from pdftools_sdk.signature_validation.sub_indication import SubIndication
    from pdftools_sdk.pdf.signed_signature_field import SignedSignatureField

else:
    Document = "pdftools_sdk.pdf.document.Document"
    Profile = "pdftools_sdk.signature_validation.profiles.profile.Profile"
    SignatureSelector = "pdftools_sdk.signature_validation.signature_selector.SignatureSelector"
    ValidationResults = "pdftools_sdk.signature_validation.validation_results.ValidationResults"
    Indication = "pdftools_sdk.signature_validation.indication.Indication"
    SubIndication = "pdftools_sdk.signature_validation.sub_indication.SubIndication"
    SignedSignatureField = "pdftools_sdk.pdf.signed_signature_field.SignedSignatureField"


if not TYPE_CHECKING:
    Indication = "Indication"
    SubIndication = "SubIndication"
    SignedSignatureField = "SignedSignatureField"

ConstraintFunc = Callable[[str, Indication, SubIndication, SignedSignatureField, Optional[str]], None]
"""
Report the result of a constraint validation of :meth:`pdftools_sdk.signature_validation.validator.Validator.validate` .



Args:
    message (str): 
        The validation message

    indication (pdftools_sdk.signature_validation.indication.Indication): 
        The main indication

    subIndication (pdftools_sdk.signature_validation.sub_indication.SubIndication): 
        The sub indication

    signature (pdftools_sdk.pdf.signed_signature_field.SignedSignatureField): 
        The signature field

    dataPart (Optional[str]): 
         
        The data part is `None` for constraints of the main signature and a path for constraints related to elements of the signature.
         
        Examples:
         
        - `certificate:"Some Certificate"`: When validating a certificate "Some Certificate" of the main signature.
        - `time-stamp":Some TSA Responder"/certificate:"Intermediate TSA Responder Certificate"`: When validating a certificate "Intermediate TSA Responder Certificate" of the time-stamp embedded into the main signature.
         


"""

class Validator(_NativeObject):
    """
    The class to check the validity of signatures


    """
    # Event definition
    _ConstraintFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_int, c_int, c_void_p, c_wchar_p)
    def _wrap_constraint_func(self, py_callback: ConstraintFunc) -> Validator._ConstraintFunc:

        def _c_callback(event_context, message, indication, sub_indication, signature, data_part):
            from pdftools_sdk.signature_validation.indication import Indication
            from pdftools_sdk.signature_validation.sub_indication import SubIndication
            from pdftools_sdk.pdf.signed_signature_field import SignedSignatureField

            # Call the Python callback
            py_callback(_utf16_to_string(message), Indication(indication), SubIndication(sub_indication), SignedSignatureField._create_dynamic_type(signature), _utf16_to_string(data_part))

        # Wrap the callback in CFUNCTYPE so it becomes a valid C function pointer
        return Validator._ConstraintFunc(_c_callback)


    def __init__(self):
        """


        """
        _lib.PdfToolsSignatureValidation_Validator_New.argtypes = []
        _lib.PdfToolsSignatureValidation_Validator_New.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_Validator_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)
        self._constraint_callback_map = {}


    def validate(self, document: Document, profile: Profile, selector: SignatureSelector) -> ValidationResults:
        """
        Validate the signatures of a PDF document



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The document to check the signatures of

            profile (pdftools_sdk.signature_validation.profiles.profile.Profile): 
                The validation profile

            selector (pdftools_sdk.signature_validation.signature_selector.SignatureSelector): 
                The signatures to validate



        Returns:
            pdftools_sdk.signature_validation.validation_results.ValidationResults: 
                The result of the validation



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            pdftools_sdk.processing_error.ProcessingError:
                The processing has failed.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.signature_validation.profiles.profile import Profile
        from pdftools_sdk.signature_validation.signature_selector import SignatureSelector
        from pdftools_sdk.signature_validation.validation_results import ValidationResults

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(profile, Profile):
            raise TypeError(f"Expected type {Profile.__name__}, but got {type(profile).__name__}.")
        if not isinstance(selector, SignatureSelector):
            raise TypeError(f"Expected type {SignatureSelector.__name__}, but got {type(selector).__name__}.")

        _lib.PdfToolsSignatureValidation_Validator_Validate.argtypes = [c_void_p, c_void_p, c_void_p, c_int]
        _lib.PdfToolsSignatureValidation_Validator_Validate.restype = c_void_p
        ret_val = _lib.PdfToolsSignatureValidation_Validator_Validate(self._handle, document._handle, profile._handle, c_int(selector.value))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ValidationResults._create_dynamic_type(ret_val)



    def add_constraint_handler(self, handler: ConstraintFunc) -> None:
        """
        Add handler for the :func:`ConstraintFunc` event.

        Args:
            handler: Event handler. If a handler is added that is already registered, it is ignored.
        """
        _lib.PdfToolsSignatureValidation_Validator_AddConstraintHandlerW.argtypes = [c_void_p, c_void_p, self._ConstraintFunc]
        _lib.PdfToolsSignatureValidation_Validator_AddConstraintHandlerW.restype = c_bool

        # Wrap the handler with the C callback
        _c_callback = self._wrap_constraint_func(handler)

        # Now pass the callback function as a proper C function type instance
        if not _lib.PdfToolsSignatureValidation_Validator_AddConstraintHandlerW(self._handle, None, _c_callback):
            _NativeBase._throw_last_error()

        # Add to the class-level callback map (increase count if already added)
        if handler in self._constraint_callback_map:
            self._constraint_callback_map[handler]['count'] += 1
        else:
            self._constraint_callback_map[handler] = {'callback': _c_callback, 'count': 1}

    def remove_constraint_handler(self, handler: ConstraintFunc) -> None:
        """
        Remove registered handler of the :func:`ConstraintFunc` event.

        Args:
            handler: Event handler that shall be removed. If a handler is not registered, it is ignored.
        """
        _lib.PdfToolsSignatureValidation_Validator_RemoveConstraintHandlerW.argtypes = [c_void_p, c_void_p, self._ConstraintFunc]
        _lib.PdfToolsSignatureValidation_Validator_RemoveConstraintHandlerW.restype = c_bool

        # Check if the handler exists in the class-level map
        if handler in self._constraint_callback_map:
            from pdftools_sdk.not_found_error import NotFoundError
            _c_callback = self._constraint_callback_map[handler]['callback']
            try:
                if not _lib.PdfToolsSignatureValidation_Validator_RemoveConstraintHandlerW(self._handle, None, _c_callback):
                    _NativeBase._throw_last_error()
            except pdftools_sdk.NotFoundError as e:
                del self._constraint_callback_map[handler]

            # Decrease the count or remove the callback entirely
            if self._constraint_callback_map[handler]['count'] > 1:
                self._constraint_callback_map[handler]['count'] -= 1
            else:
                del self._constraint_callback_map[handler]


    @staticmethod
    def _create_dynamic_type(handle):
        return Validator._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Validator.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
        self._constraint_callback_map = {}
