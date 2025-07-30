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
    from pdftools_sdk.extraction.text_options import TextOptions

else:
    Document = "pdftools_sdk.pdf.document.Document"
    TextOptions = "pdftools_sdk.extraction.text_options.TextOptions"


class Extractor(_NativeObject):
    """
    Allows for extracting page-wide content of a PDF.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsExtraction_Extractor_New.argtypes = []
        _lib.PdfToolsExtraction_Extractor_New.restype = c_void_p
        ret_val = _lib.PdfToolsExtraction_Extractor_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def extract_text(self, in_doc: Document, out_stream: io.IOBase, options: Optional[TextOptions] = None, first_page: Optional[int] = None, last_page: Optional[int] = None) -> None:
        """
        Extract text from a PDF document



        Args:
            inDoc (pdftools_sdk.pdf.document.Document): 
                The input PDF document.

            outStream (io.IOBase): 
                The stream to which output file the extracted text is written.

            options (Optional[pdftools_sdk.extraction.text_options.TextOptions]): 
                The option object that controls the text extraction.

            firstPage (Optional[int]): 
                 
                Optional parameter denoting the index of the first page to be copied. This index is one-based.
                If set, the number must be in the range of `1` (first page) to :attr:`pdftools_sdk.pdf.document.Document.page_count`  (last page).
                 
                If not set, `1` is used.

            lastPage (Optional[int]): 
                 
                Optional parameter denoting the index of the last page to be copied. This index is one-based.
                If set, the number must be in the range of `1` (first page) to :attr:`pdftools_sdk.pdf.document.Document.page_count`  (last page).
                 
                If not set, :attr:`pdftools_sdk.pdf.document.Document.page_count`  is used.




        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            pdftools_sdk.processing_error.ProcessingError:
                The processing has failed.

            OSError:
                Writing to the output text file has failed.

            pdftools_sdk.generic_error.GenericError:
                A generic error occurred.

            ValueError:
                The `firstPage` or `lastPage` are not in the allowed range.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.extraction.text_options import TextOptions

        if not isinstance(in_doc, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(in_doc).__name__}.")
        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if options is not None and not isinstance(options, TextOptions):
            raise TypeError(f"Expected type {TextOptions.__name__} or None, but got {type(options).__name__}.")
        if first_page is not None and not isinstance(first_page, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(first_page).__name__}.")
        if last_page is not None and not isinstance(last_page, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(last_page).__name__}.")

        _lib.PdfToolsExtraction_Extractor_ExtractText.argtypes = [c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, POINTER(c_int), POINTER(c_int)]
        _lib.PdfToolsExtraction_Extractor_ExtractText.restype = c_bool
        if not _lib.PdfToolsExtraction_Extractor_ExtractText(self._handle, in_doc._handle, _StreamDescriptor(out_stream), options._handle if options is not None else None, byref(c_int(first_page)) if first_page is not None else None, byref(c_int(last_page)) if last_page is not None else None):
            _NativeBase._throw_last_error(False)



    @staticmethod
    def _create_dynamic_type(handle):
        return Extractor._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Extractor.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
