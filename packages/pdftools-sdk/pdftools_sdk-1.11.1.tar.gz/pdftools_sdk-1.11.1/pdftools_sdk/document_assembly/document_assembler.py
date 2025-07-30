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
    from pdftools_sdk.document_assembly.document_copy_options import DocumentCopyOptions
    from pdftools_sdk.document_assembly.page_copy_options import PageCopyOptions
    from pdftools_sdk.pdf.output_options import OutputOptions
    from pdftools_sdk.pdf.conformance import Conformance

else:
    Document = "pdftools_sdk.pdf.document.Document"
    DocumentCopyOptions = "pdftools_sdk.document_assembly.document_copy_options.DocumentCopyOptions"
    PageCopyOptions = "pdftools_sdk.document_assembly.page_copy_options.PageCopyOptions"
    OutputOptions = "pdftools_sdk.pdf.output_options.OutputOptions"
    Conformance = "pdftools_sdk.pdf.conformance.Conformance"


class DocumentAssembler(_NativeObject):
    """
    The class for splitting or merging PDF documents


    """
    def __init__(self, out_stream: io.IOBase, out_options: Optional[OutputOptions], conformance: Optional[Conformance]):
        """

        Args:
            outStream (io.IOBase): 
                The stream to which the output PDF is written

            outOptions (Optional[pdftools_sdk.pdf.output_options.OutputOptions]): 
                The PDF output options, e.g. to encrypt the output document.

            conformance (Optional[pdftools_sdk.pdf.conformance.Conformance]): 
                 
                The required conformance level of the PDF document.
                Adding pages or content from incompatible documents or using
                incompatible features will lead to a conformance error.
                 
                When using `None`, the conformance is determined automatically,
                based on the conformance of the input documents used in the :meth:`pdftools_sdk.document_assembly.document_assembler.DocumentAssembler.append`  method
                and the requirements of the used features.



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            ValueError:
                An invalid encryption was specified in `outOptions`.

            OSError:
                Unable to write to the stream.

            pdftools_sdk.generic_error.GenericError:
                A generic error occurred.


        """
        from pdftools_sdk.pdf.output_options import OutputOptions
        from pdftools_sdk.pdf.conformance import Conformance

        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if out_options is not None and not isinstance(out_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(out_options).__name__}.")
        if conformance is not None and not isinstance(conformance, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__} or None, but got {type(conformance).__name__}.")

        _lib.PdfToolsDocumentAssembly_DocumentAssembler_New.argtypes = [POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, POINTER(c_int)]
        _lib.PdfToolsDocumentAssembly_DocumentAssembler_New.restype = c_void_p
        ret_val = _lib.PdfToolsDocumentAssembly_DocumentAssembler_New(_StreamDescriptor(out_stream), out_options._handle if out_options is not None else None, byref(c_int(conformance)) if conformance is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def append(self, in_doc: Document, first_page: Optional[int] = None, last_page: Optional[int] = None, document_copy_options: Optional[DocumentCopyOptions] = None, page_copy_options: Optional[PageCopyOptions] = None) -> None:
        """
        This method copies document properties and a range of pages from `inDoc`.



        Args:
            inDoc (pdftools_sdk.pdf.document.Document): 
            firstPage (Optional[int]): 
                 
                Optional parameter denoting the index of the first page to be copied. This index is one-based.
                If set, the number must be in the range of `1` (first page) to :attr:`pdftools_sdk.pdf.document.Document.page_count`  (last page).
                 
                If not set, `1` is used.

            lastPage (Optional[int]): 
                 
                Optional parameter denoting the index of the last page to be copied. This index is one-based.
                If set, the number must be in the range of `1` (first page) to :attr:`pdftools_sdk.pdf.document.Document.page_count`  (last page).
                 
                If not set, :attr:`pdftools_sdk.pdf.document.Document.page_count`  is used.

            documentCopyOptions (Optional[pdftools_sdk.document_assembly.document_copy_options.DocumentCopyOptions]): 
            pageCopyOptions (Optional[pdftools_sdk.document_assembly.page_copy_options.PageCopyOptions]): 



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            ValueError:
                The `firstPage` or `lastPage` are not in the allowed range.

            ValueError:
                If the method has already been called with any of the following properties set to `True`:
                 
                - :attr:`pdftools_sdk.document_assembly.document_copy_options.DocumentCopyOptions.copy_metadata`
                - :attr:`pdftools_sdk.document_assembly.document_copy_options.DocumentCopyOptions.copy_viewer_settings`
                - :attr:`pdftools_sdk.document_assembly.document_copy_options.DocumentCopyOptions.copy_output_intent`
                 

            pdftools_sdk.conformance_error.ConformanceError:
                The conformance level of the input document is not compatible
                with the conformance level of the output document.

            pdftools_sdk.conformance_error.ConformanceError:
                The explicitly requested conformance level is PDF/A Level A
                (:attr:`pdftools_sdk.pdf.conformance.Conformance.PDFA1A` , :attr:`pdftools_sdk.pdf.conformance.Conformance.PDFA2A` ,
                or :attr:`pdftools_sdk.pdf.conformance.Conformance.PDFA3A` )
                and the copy option :attr:`pdftools_sdk.document_assembly.page_copy_options.PageCopyOptions.copy_logical_structure`  is set to `False`.

            StateError:
                If :meth:`pdftools_sdk.document_assembly.document_assembler.DocumentAssembler.assemble`  has already been called.

            pdftools_sdk.processing_error.ProcessingError:
                The processing has failed.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.document_assembly.document_copy_options import DocumentCopyOptions
        from pdftools_sdk.document_assembly.page_copy_options import PageCopyOptions

        if not isinstance(in_doc, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(in_doc).__name__}.")
        if first_page is not None and not isinstance(first_page, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(first_page).__name__}.")
        if last_page is not None and not isinstance(last_page, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(last_page).__name__}.")
        if document_copy_options is not None and not isinstance(document_copy_options, DocumentCopyOptions):
            raise TypeError(f"Expected type {DocumentCopyOptions.__name__} or None, but got {type(document_copy_options).__name__}.")
        if page_copy_options is not None and not isinstance(page_copy_options, PageCopyOptions):
            raise TypeError(f"Expected type {PageCopyOptions.__name__} or None, but got {type(page_copy_options).__name__}.")

        _lib.PdfToolsDocumentAssembly_DocumentAssembler_Append.argtypes = [c_void_p, c_void_p, POINTER(c_int), POINTER(c_int), c_void_p, c_void_p]
        _lib.PdfToolsDocumentAssembly_DocumentAssembler_Append.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_DocumentAssembler_Append(self._handle, in_doc._handle, byref(c_int(first_page)) if first_page is not None else None, byref(c_int(last_page)) if last_page is not None else None, document_copy_options._handle if document_copy_options is not None else None, page_copy_options._handle if page_copy_options is not None else None):
            _NativeBase._throw_last_error(False)


    def assemble(self) -> Document:
        """
        Assemble the input documents

        The input documents appended with :meth:`pdftools_sdk.document_assembly.document_assembler.DocumentAssembler.append`  are assembled into the output PDF.




        Returns:
            pdftools_sdk.pdf.document.Document: 
                The assembled PDF, which can be used as a new input for further processing.



        Raises:
            StateError:
                If :meth:`pdftools_sdk.document_assembly.document_assembler.DocumentAssembler.assemble`  has already been called.


        """
        from pdftools_sdk.pdf.document import Document

        _lib.PdfToolsDocumentAssembly_DocumentAssembler_Assemble.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_DocumentAssembler_Assemble.restype = c_void_p
        ret_val = _lib.PdfToolsDocumentAssembly_DocumentAssembler_Assemble(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)



    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PdfToolsDocumentAssembly_DocumentAssembler_Close.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_DocumentAssembler_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PdfToolsDocumentAssembly_DocumentAssembler_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        return DocumentAssembler._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = DocumentAssembler.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
