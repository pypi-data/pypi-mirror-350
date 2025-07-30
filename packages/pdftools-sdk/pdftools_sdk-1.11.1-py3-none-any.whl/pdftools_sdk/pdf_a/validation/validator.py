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
    from pdftools_sdk.pdf_a.validation.validation_options import ValidationOptions
    from pdftools_sdk.pdf_a.validation.validation_result import ValidationResult
    from pdftools_sdk.pdf_a.validation.analysis_options import AnalysisOptions
    from pdftools_sdk.pdf_a.validation.analysis_result import AnalysisResult
    from pdftools_sdk.pdf_a.validation.error_category import ErrorCategory

else:
    Document = "pdftools_sdk.pdf.document.Document"
    ValidationOptions = "pdftools_sdk.pdf_a.validation.validation_options.ValidationOptions"
    ValidationResult = "pdftools_sdk.pdf_a.validation.validation_result.ValidationResult"
    AnalysisOptions = "pdftools_sdk.pdf_a.validation.analysis_options.AnalysisOptions"
    AnalysisResult = "pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult"
    ErrorCategory = "pdftools_sdk.pdf_a.validation.error_category.ErrorCategory"


if not TYPE_CHECKING:
    ErrorCategory = "ErrorCategory"

ErrorFunc = Callable[[Optional[str], str, ErrorCategory, str, int, int], None]
"""
Report a validation issue found in :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.analyze`  or :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.validate` .



Args:
    dataPart (Optional[str]): 
         
        The data part is `None` for the main file and a data part specification for embedded files.
         
        Examples:
         
        - `embedded-file:file.pdf`: For a file `file.pdf` that is embedded in the main file.
        - `embedded-file:file1.pdf/embedded-file:file2.pdf`: For a file `file2.pdf` that is embedded in an embedded file `file1.pdf`.
         

    message (str): 
        The validation message

    category (pdftools_sdk.pdf_a.validation.error_category.ErrorCategory): 
        The category of the validation error

    context (str): 
        A description of the context where the error occurred

    pageNo (int): 
        The page number this error is associated to or `0`

    objectNo (int): 
        The number of the PDF object this error is associated to


"""

class Validator(_NativeObject):
    """
    The class to validate the standard conformance of documents


    """
    # Event definition
    _ErrorFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_wchar_p, c_int, c_wchar_p, c_int, c_int)
    def _wrap_error_func(self, py_callback: ErrorFunc) -> Validator._ErrorFunc:

        def _c_callback(event_context, data_part, message, category, context, page_no, object_no):
            from pdftools_sdk.pdf_a.validation.error_category import ErrorCategory

            # Call the Python callback
            py_callback(_utf16_to_string(data_part), _utf16_to_string(message), ErrorCategory(category), _utf16_to_string(context), page_no, object_no)

        # Wrap the callback in CFUNCTYPE so it becomes a valid C function pointer
        return Validator._ErrorFunc(_c_callback)


    def __init__(self):
        """


        """
        _lib.PdfToolsPdfAValidation_Validator_New.argtypes = []
        _lib.PdfToolsPdfAValidation_Validator_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAValidation_Validator_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)
        self._error_callback_map = {}


    def validate(self, document: Document, options: Optional[ValidationOptions] = None) -> ValidationResult:
        """
        Validate the standards conformance of a PDF document.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The document to check the quality of

            options (Optional[pdftools_sdk.pdf_a.validation.validation_options.ValidationOptions]): 
                The options or `None` for default validation options



        Returns:
            pdftools_sdk.pdf_a.validation.validation_result.ValidationResult: 
                The result of the validation



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            pdftools_sdk.processing_error.ProcessingError:
                The processing has failed.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.pdf_a.validation.validation_options import ValidationOptions
        from pdftools_sdk.pdf_a.validation.validation_result import ValidationResult

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if options is not None and not isinstance(options, ValidationOptions):
            raise TypeError(f"Expected type {ValidationOptions.__name__} or None, but got {type(options).__name__}.")

        _lib.PdfToolsPdfAValidation_Validator_Validate.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PdfToolsPdfAValidation_Validator_Validate.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAValidation_Validator_Validate(self._handle, document._handle, options._handle if options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ValidationResult._create_dynamic_type(ret_val)


    def analyze(self, document: Document, options: Optional[AnalysisOptions] = None) -> AnalysisResult:
        """
        Analyze a PDF document in preparation for its conversion to PDF/A.

        This method validates the document's standards conformance like :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.validate` .
        In addition to that, certain additional checks can be performed.
        However, the main difference is that the analysis result can be used in :meth:`pdftools_sdk.pdf_a.conversion.converter.Converter.convert`  to convert the PDF document to PDF/A.



        Args:
            document (pdftools_sdk.pdf.document.Document): 
                The document to analyze

            options (Optional[pdftools_sdk.pdf_a.validation.analysis_options.AnalysisOptions]): 
                The options or `None` for default analysis options



        Returns:
            pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult: 
                The result of the analysis



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            ValueError:
                The conformance of the `options` argument is not PDF/A.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.pdf_a.validation.analysis_options import AnalysisOptions
        from pdftools_sdk.pdf_a.validation.analysis_result import AnalysisResult

        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if options is not None and not isinstance(options, AnalysisOptions):
            raise TypeError(f"Expected type {AnalysisOptions.__name__} or None, but got {type(options).__name__}.")

        _lib.PdfToolsPdfAValidation_Validator_Analyze.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PdfToolsPdfAValidation_Validator_Analyze.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAValidation_Validator_Analyze(self._handle, document._handle, options._handle if options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return AnalysisResult._create_dynamic_type(ret_val)



    def add_error_handler(self, handler: ErrorFunc) -> None:
        """
        Add handler for the :func:`ErrorFunc` event.

        Args:
            handler: Event handler. If a handler is added that is already registered, it is ignored.
        """
        _lib.PdfToolsPdfAValidation_Validator_AddErrorHandlerW.argtypes = [c_void_p, c_void_p, self._ErrorFunc]
        _lib.PdfToolsPdfAValidation_Validator_AddErrorHandlerW.restype = c_bool

        # Wrap the handler with the C callback
        _c_callback = self._wrap_error_func(handler)

        # Now pass the callback function as a proper C function type instance
        if not _lib.PdfToolsPdfAValidation_Validator_AddErrorHandlerW(self._handle, None, _c_callback):
            _NativeBase._throw_last_error()

        # Add to the class-level callback map (increase count if already added)
        if handler in self._error_callback_map:
            self._error_callback_map[handler]['count'] += 1
        else:
            self._error_callback_map[handler] = {'callback': _c_callback, 'count': 1}

    def remove_error_handler(self, handler: ErrorFunc) -> None:
        """
        Remove registered handler of the :func:`ErrorFunc` event.

        Args:
            handler: Event handler that shall be removed. If a handler is not registered, it is ignored.
        """
        _lib.PdfToolsPdfAValidation_Validator_RemoveErrorHandlerW.argtypes = [c_void_p, c_void_p, self._ErrorFunc]
        _lib.PdfToolsPdfAValidation_Validator_RemoveErrorHandlerW.restype = c_bool

        # Check if the handler exists in the class-level map
        if handler in self._error_callback_map:
            from pdftools_sdk.not_found_error import NotFoundError
            _c_callback = self._error_callback_map[handler]['callback']
            try:
                if not _lib.PdfToolsPdfAValidation_Validator_RemoveErrorHandlerW(self._handle, None, _c_callback):
                    _NativeBase._throw_last_error()
            except pdftools_sdk.NotFoundError as e:
                del self._error_callback_map[handler]

            # Decrease the count or remove the callback entirely
            if self._error_callback_map[handler]['count'] > 1:
                self._error_callback_map[handler]['count'] -= 1
            else:
                del self._error_callback_map[handler]


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
        self._error_callback_map = {}
