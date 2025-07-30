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
    from pdftools_sdk.image.document import Document as ImageDocument
    from pdftools_sdk.image2_pdf.profiles.profile import Profile
    from pdftools_sdk.pdf.output_options import OutputOptions
    from pdftools_sdk.pdf.document import Document as PdfDocument
    from pdftools_sdk.image.document_list import DocumentList

else:
    ImageDocument = "pdftools_sdk.image.document.Document"
    Profile = "pdftools_sdk.image2_pdf.profiles.profile.Profile"
    OutputOptions = "pdftools_sdk.pdf.output_options.OutputOptions"
    PdfDocument = "pdftools_sdk.pdf.document.Document"
    DocumentList = "pdftools_sdk.image.document_list.DocumentList"


class Converter(_NativeObject):
    """
    The class to convert one or more images to a PDF document


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsImage2Pdf_Converter_New.argtypes = []
        _lib.PdfToolsImage2Pdf_Converter_New.restype = c_void_p
        ret_val = _lib.PdfToolsImage2Pdf_Converter_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def convert(self, image: ImageDocument, out_stream: io.IOBase, profile: Profile, out_options: Optional[OutputOptions] = None) -> PdfDocument:
        """
        Convert an image to a PDF document



        Args:
            image (pdftools_sdk.image.document.Document): 
                The input image document containing one or more pages.

            outStream (io.IOBase): 
                The stream to which the PDF is written.

            profile (pdftools_sdk.image2_pdf.profiles.profile.Profile): 
                 
                The profile defines the properties of the output document and
                how the images are placed onto the pages.
                 
                For details, see :class:`pdftools_sdk.image2_pdf.profiles.profile.Profile` .

            outOptions (Optional[pdftools_sdk.pdf.output_options.OutputOptions]): 
                The PDF output options, e.g. to encrypt the output document.



        Returns:
            pdftools_sdk.pdf.document.Document: 
                 
                The resulting output PDF which can be used as a new input
                for further processing.
                 
                Note that, this object must be disposed before the output stream
                object (method argument `outStream`).



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license is invalid.

            OSError:
                Writing to the output PDF failed.

            pdftools_sdk.corrupt_error.CorruptError:
                The input image document is corrupt and cannot be read.

            pdftools_sdk.generic_error.GenericError:
                An unexpected failure occurred.

            pdftools_sdk.processing_error.ProcessingError:
                The conversion failed.

            ValueError:
                The `profile` specifies invalid options.

            ValueError:
                The `outOptions` specifies document encryption and the `profile` PDF/A conformance, which is not allowed.


        """
        from pdftools_sdk.image.document import Document as ImageDocument
        from pdftools_sdk.image2_pdf.profiles.profile import Profile
        from pdftools_sdk.pdf.output_options import OutputOptions
        from pdftools_sdk.pdf.document import Document as PdfDocument

        if not isinstance(image, ImageDocument):
            raise TypeError(f"Expected type {ImageDocument.__name__}, but got {type(image).__name__}.")
        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if not isinstance(profile, Profile):
            raise TypeError(f"Expected type {Profile.__name__}, but got {type(profile).__name__}.")
        if out_options is not None and not isinstance(out_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(out_options).__name__}.")

        _lib.PdfToolsImage2Pdf_Converter_Convert.argtypes = [c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, c_void_p]
        _lib.PdfToolsImage2Pdf_Converter_Convert.restype = c_void_p
        ret_val = _lib.PdfToolsImage2Pdf_Converter_Convert(self._handle, image._handle, _StreamDescriptor(out_stream), profile._handle, out_options._handle if out_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PdfDocument._create_dynamic_type(ret_val)


    def convert_multiple(self, images: DocumentList, out_stream: io.IOBase, profile: Profile, out_options: Optional[OutputOptions] = None) -> PdfDocument:
        """
        Convert a list of images to a PDF document



        Args:
            images (pdftools_sdk.image.document_list.DocumentList): 
                The input image document list, each image containing one or more pages.

            outStream (io.IOBase): 
                The stream to which the PDF is written.

            profile (pdftools_sdk.image2_pdf.profiles.profile.Profile): 
                 
                The profile defines the properties of the output document and
                how the images are placed onto the pages.
                 
                For details, see :class:`pdftools_sdk.image2_pdf.profiles.profile.Profile` .

            outOptions (Optional[pdftools_sdk.pdf.output_options.OutputOptions]): 
                The PDF output options, e.g. to encrypt the output document.



        Returns:
            pdftools_sdk.pdf.document.Document: 
                 
                The resulting output PDF which can be used as a new input
                for further processing.
                 
                Note that, this object must be disposed before the output stream
                object (method argument `outStream`).



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license is invalid.

            OSError:
                Writing to the output PDF failed.

            pdftools_sdk.corrupt_error.CorruptError:
                An input image document is corrupt and cannot be read.

            pdftools_sdk.generic_error.GenericError:
                An unexpected failure occurred.

            pdftools_sdk.processing_error.ProcessingError:
                The conversion failed.

            ValueError:
                The `profile` specifies invalid options.

            ValueError:
                The `outOptions` specifies document encryption and the `profile` PDF/A conformance, which is not allowed.


        """
        from pdftools_sdk.image.document_list import DocumentList
        from pdftools_sdk.image2_pdf.profiles.profile import Profile
        from pdftools_sdk.pdf.output_options import OutputOptions
        from pdftools_sdk.pdf.document import Document as PdfDocument

        if not isinstance(images, DocumentList):
            raise TypeError(f"Expected type {DocumentList.__name__}, but got {type(images).__name__}.")
        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if not isinstance(profile, Profile):
            raise TypeError(f"Expected type {Profile.__name__}, but got {type(profile).__name__}.")
        if out_options is not None and not isinstance(out_options, OutputOptions):
            raise TypeError(f"Expected type {OutputOptions.__name__} or None, but got {type(out_options).__name__}.")

        _lib.PdfToolsImage2Pdf_Converter_ConvertMultiple.argtypes = [c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, c_void_p]
        _lib.PdfToolsImage2Pdf_Converter_ConvertMultiple.restype = c_void_p
        ret_val = _lib.PdfToolsImage2Pdf_Converter_ConvertMultiple(self._handle, images._handle, _StreamDescriptor(out_stream), profile._handle, out_options._handle if out_options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PdfDocument._create_dynamic_type(ret_val)



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
