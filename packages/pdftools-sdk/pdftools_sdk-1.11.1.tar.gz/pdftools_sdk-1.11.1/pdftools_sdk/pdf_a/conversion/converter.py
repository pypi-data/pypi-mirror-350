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
    from pdftools_sdk.pdf_a.conversion.invoice_type import InvoiceType
    from pdftools_sdk.pdf_a.conversion.a_f_relationship import AFRelationship
    from pdftools_sdk.sys.date import _Date
    from pdftools_sdk.pdf_a.validation.analysis_result import AnalysisResult
    from pdftools_sdk.pdf.document import Document
    from pdftools_sdk.pdf_a.conversion.conversion_options import ConversionOptions
    from pdftools_sdk.pdf.output_options import OutputOptions
    from pdftools_sdk.pdf_a.conversion.event_severity import EventSeverity
    from pdftools_sdk.pdf_a.conversion.event_category import EventCategory
    from pdftools_sdk.pdf_a.conversion.event_code import EventCode

else:
    InvoiceType = "pdftools_sdk.pdf_a.conversion.invoice_type.InvoiceType"
    AFRelationship = "pdftools_sdk.pdf_a.conversion.a_f_relationship.AFRelationship"
    _Date = "pdftools_sdk.sys.date._Date"
    AnalysisResult = "pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult"
    Document = "pdftools_sdk.pdf.document.Document"
    ConversionOptions = "pdftools_sdk.pdf_a.conversion.conversion_options.ConversionOptions"
    OutputOptions = "pdftools_sdk.pdf.output_options.OutputOptions"
    EventSeverity = "pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity"
    EventCategory = "pdftools_sdk.pdf_a.conversion.event_category.EventCategory"
    EventCode = "pdftools_sdk.pdf_a.conversion.event_code.EventCode"


if not TYPE_CHECKING:
    EventSeverity = "EventSeverity"
    EventCategory = "EventCategory"
    EventCode = "EventCode"

ConversionEventFunc = Callable[[Optional[str], str, EventSeverity, EventCategory, EventCode, str, int], None]
"""
The event for errors, warnings, and informational messages that occur during conversion

 
Report a conversion event that occurred in :meth:`pdftools_sdk.pdf_a.conversion.converter.Converter.convert` .
These events can be used to:
 
- Generate a detailed conversion report.
- Detect and handle critical conversion events.
 
 
Note that if a document cannot be converted to the requested conformance, the :meth:`pdftools_sdk.pdf_a.conversion.converter.Converter.convert`  throws an exception.
However, even if the output document meets all required standards, the conversion might have resulted in differences that might be acceptable in some processes but not in others.
Such potentially critical conversion issues are reported as conversion events.
 
We suggest checking which conversion events can be tolerated in your conversion process and which must be considered critical:
 
- *Review the suggested severity of events.*
  Each event has a default severity indicated by `severity` which is based on the event's `category`.
  Review the suggested severity of each :class:`pdftools_sdk.pdf_a.conversion.event_category.EventCategory`  and determine the :class:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity`  to be used in your process.
- *Handle events according to their severity*.
  - *Events of severity* :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.ERROR` :
  The conversion must be considered as failed.
  - *Events of severity* :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.WARNING` :
  In case of a warning, the output file is best presented to a user to decide if the result is acceptable.
  The properties `message`, `context`, and `page` in combination with the output file are helpful to make this decision.
  If a manual review is not feasible, critical warnings should be classified as an :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.ERROR` .
  An exception to this is, if all processed input documents are similar in their content, e.g. because they have been created by a single source (application).
  In this case, the conversion result can be verified using representative test files and the event severity chosen accordingly.
  - *Events of severity* :attr:`pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity.INFORMATION` :
  No further action is required.
 



Args:
    dataPart (Optional[str]): 
         
        The data part is `None` for the main file and a data part specification for embedded files.
         
        Examples:
         
        - `embedded-file:file.pdf`: For a file `file.pdf` that is embedded in the main file.
        - `embedded-file:file1.pdf/embedded-file:file2.pdf`: For a file `file2.pdf` that is embedded in an embedded file `file1.pdf`.
         

    message (str): 
        The event message

    severity (pdftools_sdk.pdf_a.conversion.event_severity.EventSeverity): 
         
        The suggested severity of the event.
         
        We suggest checking, which conversion events are tolerable in your conversion process and which must be considered critical.
        See the documentation of :func:`pdftools_sdk.pdf_a.conversion.converter.ConversionEventFunc`  for a more detailed description.

    category (pdftools_sdk.pdf_a.conversion.event_category.EventCategory): 
        The category of the event. This parameter can be used to:
         
        - Classify the severity of an event
        - Specialized handling of events
         
        See the documentation of :func:`pdftools_sdk.pdf_a.conversion.converter.ConversionEventFunc`  for a more detailed description.

    code (pdftools_sdk.pdf_a.conversion.event_code.EventCode): 
        The code identifying particular events which can be used for detection and specialized handling of specific events.
        For most applications, it suffices to handle events by `category`.

    context (str): 
        A description of the context where the event occurred

    pageNo (int): 
        The page this event is associated to or `0`


"""

class Converter(_NativeObject):
    """
    The class to convert PDF documents to PDF/A


    """
    # Event definition
    _ConversionEventFunc = CFUNCTYPE(None, c_void_p, c_wchar_p, c_wchar_p, c_int, c_int, c_int, c_wchar_p, c_int)
    def _wrap_conversion_event_func(self, py_callback: ConversionEventFunc) -> Converter._ConversionEventFunc:

        def _c_callback(event_context, data_part, message, severity, category, code, context, page_no):
            from pdftools_sdk.pdf_a.conversion.event_severity import EventSeverity
            from pdftools_sdk.pdf_a.conversion.event_category import EventCategory
            from pdftools_sdk.pdf_a.conversion.event_code import EventCode

            # Call the Python callback
            py_callback(_utf16_to_string(data_part), _utf16_to_string(message), EventSeverity(severity), EventCategory(category), EventCode(code), _utf16_to_string(context), page_no)

        # Wrap the callback in CFUNCTYPE so it becomes a valid C function pointer
        return Converter._ConversionEventFunc(_c_callback)


    def __init__(self):
        """


        """
        _lib.PdfToolsPdfAConversion_Converter_New.argtypes = []
        _lib.PdfToolsPdfAConversion_Converter_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAConversion_Converter_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)
        self._conversion_event_callback_map = {}


    def add_invoice_xml(self, invoice_type: InvoiceType, invoice: io.IOBase, af_relationship: Optional[AFRelationship] = None) -> None:
        """
        Prepares the invoice XML file (ZUGFeRD or Factur-X) for embedding.

        Note: This requires the compliance to be set to PDF/A-3.



        Args:
            invoiceType (pdftools_sdk.pdf_a.conversion.invoice_type.InvoiceType): 
                The type of invoice.

            invoice (io.IOBase): 
                The XML invoice stream.

            afRelationship (Optional[pdftools_sdk.pdf_a.conversion.a_f_relationship.AFRelationship]): 
                If no value is provided, a sensible default value is chosen based on the invoice type and version.




        Raises:
            ValueError:
                The invoice stream could not be opened for reading.


        """
        from pdftools_sdk.pdf_a.conversion.invoice_type import InvoiceType
        from pdftools_sdk.pdf_a.conversion.a_f_relationship import AFRelationship

        if not isinstance(invoice_type, InvoiceType):
            raise TypeError(f"Expected type {InvoiceType.__name__}, but got {type(invoice_type).__name__}.")
        if not isinstance(invoice, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(invoice).__name__}.")
        if af_relationship is not None and not isinstance(af_relationship, AFRelationship):
            raise TypeError(f"Expected type {AFRelationship.__name__} or None, but got {type(af_relationship).__name__}.")

        _lib.PdfToolsPdfAConversion_Converter_AddInvoiceXml.argtypes = [c_void_p, c_int, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), POINTER(c_int)]
        _lib.PdfToolsPdfAConversion_Converter_AddInvoiceXml.restype = c_bool
        if not _lib.PdfToolsPdfAConversion_Converter_AddInvoiceXml(self._handle, c_int(invoice_type.value), _StreamDescriptor(invoice), byref(c_int(af_relationship)) if af_relationship is not None else None):
            _NativeBase._throw_last_error(False)


    def add_associated_file(self, embedded_file: io.IOBase, name: str, associate: Optional[int] = None, af_relationship: Optional[AFRelationship] = None, mime_type: Optional[str] = None, description: Optional[str] = None, modification_date: Optional[datetime] = None) -> None:
        """
        Prepares the associated file for embedding.

        Add a file to the document’s embedded files.
        For PDF/A-3, the embedded file is associated with an object of the document, i.e. it is an associated file.
        The file is embedded as-is. Embedding files is not allowed for PDF/A-1 and restricted to PDF/A conforming files for PDF/A-2.



        Args:
            embeddedFile (io.IOBase): 
                The stream of the embedded file.

            name (str): 
                The name used for the embedded file.
                This name is presented to the user when viewing the list of embedded files.

            associate (Optional[int]): 
                The object to associate the embedded file with, `-1` for none, `0` for document, number greater than 0 for respective page.
                If `None`, the default value is `0` for PDF/A-3 and `-1` otherwise.

            afRelationship (Optional[pdftools_sdk.pdf_a.conversion.a_f_relationship.AFRelationship]): 
                The relationship of the embedded file to the object associate. (Ignored, if `associate` is `-1`.)
                If `None`, the default value is :attr:`pdftools_sdk.pdf_a.conversion.a_f_relationship.AFRelationship.UNSPECIFIED` .

            mimeType (Optional[str]): 
                MIME ­Type of the embedded file. Common values other than the default are `"application/pdf"`, `"application/xml"` or `"application/msword"`.
                If `None`, the default value is `"application/octet-stream"`.

            description (Optional[str]): 
                A description of the embedded file.
                This is presented to the user when viewing the list of embedded files.
                If `None`, the default value is `""`.

            modificationDate (Optional[datetime]): 
                The modify date of the file.
                If `None`, the default value is modification date of the file on the file system or current time, if not available.




        Raises:
            ValueError:
                The associated file stream could not be opened for reading.

            ValueError:
                The `associate` argument is invalid.

            OSError:
                Error reading from `embeddedFile`.


        """
        from pdftools_sdk.pdf_a.conversion.a_f_relationship import AFRelationship
        from pdftools_sdk.sys.date import _Date

        if not isinstance(embedded_file, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(embedded_file).__name__}.")
        if not isinstance(name, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(name).__name__}.")
        if associate is not None and not isinstance(associate, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(associate).__name__}.")
        if af_relationship is not None and not isinstance(af_relationship, AFRelationship):
            raise TypeError(f"Expected type {AFRelationship.__name__} or None, but got {type(af_relationship).__name__}.")
        if mime_type is not None and not isinstance(mime_type, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(mime_type).__name__}.")
        if description is not None and not isinstance(description, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(description).__name__}.")
        if modification_date is not None and not isinstance(modification_date, datetime):
            raise TypeError(f"Expected type {datetime.__name__} or None, but got {type(modification_date).__name__}.")

        _lib.PdfToolsPdfAConversion_Converter_AddAssociatedFileW.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_wchar_p, POINTER(c_int), POINTER(c_int), c_wchar_p, c_wchar_p, POINTER(_Date)]
        _lib.PdfToolsPdfAConversion_Converter_AddAssociatedFileW.restype = c_bool
        if not _lib.PdfToolsPdfAConversion_Converter_AddAssociatedFileW(self._handle, _StreamDescriptor(embedded_file), _string_to_utf16(name), byref(c_int(associate)) if associate is not None else None, byref(c_int(af_relationship)) if af_relationship is not None else None, _string_to_utf16(mime_type), _string_to_utf16(description), _Date._from_datetime(modification_date)):
            _NativeBase._throw_last_error(False)


    def convert(self, analysis: AnalysisResult, document: Document, out_stream: io.IOBase, options: Optional[ConversionOptions] = None, out_options: Optional[OutputOptions] = None) -> Document:
        """
        Convert a document to PDF/A.

        Note that it is highly recommended to use :func:`pdftools_sdk.pdf_a.conversion.converter.ConversionEventFunc`  to detect critical conversion events.



        Args:
            analysis (pdftools_sdk.pdf_a.validation.analysis_result.AnalysisResult): 
                The result of the document's analysis using :meth:`pdftools_sdk.pdf_a.validation.validator.Validator.analyze` .

            document (pdftools_sdk.pdf.document.Document): 
                The document to convert

            outStream (io.IOBase): 
                The stream where the converted document is written

            options (Optional[pdftools_sdk.pdf_a.conversion.conversion_options.ConversionOptions]): 
                The conversion options

            outOptions (Optional[pdftools_sdk.pdf.output_options.OutputOptions]): 
                The output options object



        Returns:
            pdftools_sdk.pdf.document.Document: 
                The result of the conversion



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            ValueError:
                The `outOptions` argument is invalid.

            ValueError:
                The output stream could not be opened for writing.

            StateError:
                The `document` has already been closed.

            ValueError:
                The `analysis` has already been closed, e.g. due to a previous conversion.

            ValueError:
                The PDF/A version of the analysis and the conversion options do not match.

            ValueError:
                The `analysis` is not the analysis result of `document`.

            OSError:
                Error reading from or writing to the `outStream`.

            pdftools_sdk.conformance_error.ConformanceError:
                The conformance required by `options` cannot be achieved.
                 
                - PDF/A level U: All text of the input document must be extractable.
                - PDF/A level A: In addition to the requirements of level U, the input document must be tagged.
                 

            pdftools_sdk.conformance_error.ConformanceError:
                The PDF/A version of the conformances of `analysis` and `options` differ.
                The same PDF/A version must be used for the analysis and conversion.

            ValueError:
                The `outOptions` specifies document encryption, which is not allowed in PDF/A documents.

            pdftools_sdk.generic_error.GenericError:
                The document cannot be converted to PDF/A.

            pdftools_sdk.corrupt_error.CorruptError:
                The analysis has been stopped.

            pdftools_sdk.processing_error.ProcessingError:
                Failed to add the invoice file.
                Possible reasons include an invalid XML format, or that the invoice type conflicts with the content of the XML file.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The document is not a PDF, but an XFA document.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            pdftools_sdk.not_found_error.NotFoundError:
                A required font is missing from the installed font directories.

            StateError:
                Invalid associate value for an embedded file.


        """
        from pdftools_sdk.pdf_a.validation.analysis_result import AnalysisResult
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.pdf_a.conversion.conversion_options import ConversionOptions
        from pdftools_sdk.pdf.output_options import OutputOptions

        if not isinstance(analysis, AnalysisResult):
            raise TypeError(f"Expected type {AnalysisResult.__name__}, but got {type(analysis).__name__}.")
        if not isinstance(document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(document).__name__}.")
        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if options is not None and not isinstance(options, ConversionOptions):
            raise TypeError(f"Expected type {ConversionOptions.__name__} or None, but got {type(options).__name__}.")
        if out_options is not None and not isinstance(out_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(out_options).__name__}.")

        _lib.PdfToolsPdfAConversion_Converter_Convert.argtypes = [c_void_p, c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, c_void_p]
        _lib.PdfToolsPdfAConversion_Converter_Convert.restype = c_void_p
        ret_val = _lib.PdfToolsPdfAConversion_Converter_Convert(self._handle, analysis._handle, document._handle, _StreamDescriptor(out_stream), options._handle if options is not None else None, out_options._handle if out_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)



    def add_conversion_event_handler(self, handler: ConversionEventFunc) -> None:
        """
        Add handler for the :func:`ConversionEventFunc` event.

        Args:
            handler: Event handler. If a handler is added that is already registered, it is ignored.
        """
        _lib.PdfToolsPdfAConversion_Converter_AddConversionEventHandlerW.argtypes = [c_void_p, c_void_p, self._ConversionEventFunc]
        _lib.PdfToolsPdfAConversion_Converter_AddConversionEventHandlerW.restype = c_bool

        # Wrap the handler with the C callback
        _c_callback = self._wrap_conversion_event_func(handler)

        # Now pass the callback function as a proper C function type instance
        if not _lib.PdfToolsPdfAConversion_Converter_AddConversionEventHandlerW(self._handle, None, _c_callback):
            _NativeBase._throw_last_error()

        # Add to the class-level callback map (increase count if already added)
        if handler in self._conversion_event_callback_map:
            self._conversion_event_callback_map[handler]['count'] += 1
        else:
            self._conversion_event_callback_map[handler] = {'callback': _c_callback, 'count': 1}

    def remove_conversion_event_handler(self, handler: ConversionEventFunc) -> None:
        """
        Remove registered handler of the :func:`ConversionEventFunc` event.

        Args:
            handler: Event handler that shall be removed. If a handler is not registered, it is ignored.
        """
        _lib.PdfToolsPdfAConversion_Converter_RemoveConversionEventHandlerW.argtypes = [c_void_p, c_void_p, self._ConversionEventFunc]
        _lib.PdfToolsPdfAConversion_Converter_RemoveConversionEventHandlerW.restype = c_bool

        # Check if the handler exists in the class-level map
        if handler in self._conversion_event_callback_map:
            from pdftools_sdk.not_found_error import NotFoundError
            _c_callback = self._conversion_event_callback_map[handler]['callback']
            try:
                if not _lib.PdfToolsPdfAConversion_Converter_RemoveConversionEventHandlerW(self._handle, None, _c_callback):
                    _NativeBase._throw_last_error()
            except pdftools_sdk.NotFoundError as e:
                del self._conversion_event_callback_map[handler]

            # Decrease the count or remove the callback entirely
            if self._conversion_event_callback_map[handler]['count'] > 1:
                self._conversion_event_callback_map[handler]['count'] -= 1
            else:
                del self._conversion_event_callback_map[handler]


    @staticmethod
    def _create_dynamic_type(handle):
        return Converter._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Converter.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
        self._conversion_event_callback_map = {}
