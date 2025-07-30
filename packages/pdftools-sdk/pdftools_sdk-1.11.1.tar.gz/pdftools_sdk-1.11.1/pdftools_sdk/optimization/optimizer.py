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
    from pdftools_sdk.optimization.profiles.profile import Profile
    from pdftools_sdk.pdf.output_options import OutputOptions

else:
    Document = "pdftools_sdk.pdf.document.Document"
    Profile = "pdftools_sdk.optimization.profiles.profile.Profile"
    OutputOptions = "pdftools_sdk.pdf.output_options.OutputOptions"


class Optimizer(_NativeObject):
    """
    The class to optimize PDF documents


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsOptimization_Optimizer_New.argtypes = []
        _lib.PdfToolsOptimization_Optimizer_New.restype = c_void_p
        ret_val = _lib.PdfToolsOptimization_Optimizer_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def optimize_document(self, in_doc: Document, out_stream: io.IOBase, profile: Profile, out_options: Optional[OutputOptions] = None) -> Document:
        """
        Optimize the PDF document



        Args:
            inDoc (pdftools_sdk.pdf.document.Document): 
                The input PDF document

            outStream (io.IOBase): 
                The stream to which the output PDF is written

            profile (pdftools_sdk.optimization.profiles.profile.Profile): 
                The profile defining the optimization parameters.

            outOptions (Optional[pdftools_sdk.pdf.output_options.OutputOptions]): 
                The PDF output options, e.g. to encrypt the output document.



        Returns:
            pdftools_sdk.pdf.document.Document: 
                 
                The optimized result PDF, which can be used
                as a new input for further processing.
                 
                Note that, this object must be disposed before the output stream
                object (method argument `outStream`).



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license check has failed.

            ValueError:
                An invalid encryption was specified in `outOptions`.

            pdftools_sdk.processing_error.ProcessingError:
                The processing has failed.

            OSError:
                Writing to the output PDF has failed.

            pdftools_sdk.generic_error.GenericError:
                A generic error occurred.


        """
        from pdftools_sdk.pdf.document import Document
        from pdftools_sdk.optimization.profiles.profile import Profile
        from pdftools_sdk.pdf.output_options import OutputOptions

        if not isinstance(in_doc, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(in_doc).__name__}.")
        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if not isinstance(profile, Profile):
            raise TypeError(f"Expected type {Profile.__name__}, but got {type(profile).__name__}.")
        if out_options is not None and not isinstance(out_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(out_options).__name__}.")

        _lib.PdfToolsOptimization_Optimizer_OptimizeDocument.argtypes = [c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, c_void_p]
        _lib.PdfToolsOptimization_Optimizer_OptimizeDocument.restype = c_void_p
        ret_val = _lib.PdfToolsOptimization_Optimizer_OptimizeDocument(self._handle, in_doc._handle, _StreamDescriptor(out_stream), profile._handle, out_options._handle if out_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Document._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Optimizer._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Optimizer.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
