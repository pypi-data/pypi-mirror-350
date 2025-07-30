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
    from pdftools_sdk.pdf.document import Document as PdfDocument
    from pdftools_sdk.pdf2_image.profiles.profile import Profile
    from pdftools_sdk.image.multi_page_document import MultiPageDocument
    from pdftools_sdk.image.document import Document as ImageDocument

else:
    PdfDocument = "pdftools_sdk.pdf.document.Document"
    Profile = "pdftools_sdk.pdf2_image.profiles.profile.Profile"
    MultiPageDocument = "pdftools_sdk.image.multi_page_document.MultiPageDocument"
    ImageDocument = "pdftools_sdk.image.document.Document"


class Converter(_NativeObject):
    """
    The class to convert a PDF document to a rasterized image


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf2Image_Converter_New.argtypes = []
        _lib.PdfToolsPdf2Image_Converter_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_Converter_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def convert_document(self, in_doc: PdfDocument, out_stream: io.IOBase, profile: Profile) -> MultiPageDocument:
        """
        Convert all pages of a PDF document to a rasterized image



        Args:
            inDoc (pdftools_sdk.pdf.document.Document): 
                The input PDF document

            outStream (io.IOBase): 
                The stream to which the rasterized image is written.

            profile (pdftools_sdk.pdf2_image.profiles.profile.Profile): 
                 
                The profile defines how the PDF pages are rendered and what type of output image is used.
                Note that the profile's image options must support multi-page images (TIFF).
                For other profiles, the method :meth:`pdftools_sdk.pdf2_image.converter.Converter.convert_page`  should be used.
                 
                For details, see :class:`pdftools_sdk.pdf2_image.profiles.profile.Profile` .



        Returns:
            pdftools_sdk.image.multi_page_document.MultiPageDocument: 
                 
                The output image document.
                The object can be used as input for further processing.
                 
                Note that, this object must be disposed before the output stream
                object (method argument `outStream`).



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license is invalid.

            OSError:
                Writing to the output image failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF is a PDF collection (Portfolio) that has no cover pages.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            pdftools_sdk.generic_error.GenericError:
                An unexpected failure occurred.

            ValueError:
                The `profile` does not support multi-page output.

            pdftools_sdk.processing_error.ProcessingError:
                The processing has failed.

            StateError:
                Internal error has occured.


        """
        from pdftools_sdk.pdf.document import Document as PdfDocument
        from pdftools_sdk.pdf2_image.profiles.profile import Profile
        from pdftools_sdk.image.multi_page_document import MultiPageDocument

        if not isinstance(in_doc, PdfDocument):
            raise TypeError(f"Expected type {PdfDocument.__name__}, but got {type(in_doc).__name__}.")
        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if not isinstance(profile, Profile):
            raise TypeError(f"Expected type {Profile.__name__}, but got {type(profile).__name__}.")

        _lib.PdfToolsPdf2Image_Converter_ConvertDocument.argtypes = [c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p]
        _lib.PdfToolsPdf2Image_Converter_ConvertDocument.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_Converter_ConvertDocument(self._handle, in_doc._handle, _StreamDescriptor(out_stream), profile._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return MultiPageDocument._create_dynamic_type(ret_val)


    def convert_page(self, in_doc: PdfDocument, out_stream: io.IOBase, profile: Profile, page_number: int) -> ImageDocument:
        """
        Convert a single page of a PDF document to a rasterized image



        Args:
            inDoc (pdftools_sdk.pdf.document.Document): 
                The input PDF document

            outStream (io.IOBase): 
                The stream to which the rasterized image is written.

            profile (pdftools_sdk.pdf2_image.profiles.profile.Profile): 
                 
                The profile defines how the PDF page is rendered and what type of output image is used.
                 
                For details, see :class:`pdftools_sdk.pdf2_image.profiles.profile.Profile` .

            pageNumber (int): 
                The PDF page number to be converted.
                The number must be in the range of `1` (first page) to :attr:`pdftools_sdk.pdf.document.Document.page_count`  (last page).



        Returns:
            pdftools_sdk.image.document.Document: 
                 
                The image object allowing to open and read the
                output image and treat it as a new input for further processing.
                 
                Note that, this object must be disposed before the output stream
                object (method argument `outStream`).



        Raises:
            pdftools_sdk.license_error.LicenseError:
                The license is invalid.

            ValueError:
                The `pageNumber` is not in the allowed range.

            OSError:
                Writing to the output image failed.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF is a collection that has no cover pages.

            pdftools_sdk.unsupported_feature_error.UnsupportedFeatureError:
                The input PDF contains unrendered XFA form fields.
                See :attr:`pdftools_sdk.pdf.document.Document.xfa`  for more information on how to detect and handle XFA documents.

            pdftools_sdk.generic_error.GenericError:
                An unexpected failure occurred.

            pdftools_sdk.processing_error.ProcessingError:
                The processing has failed.


        """
        from pdftools_sdk.pdf.document import Document as PdfDocument
        from pdftools_sdk.pdf2_image.profiles.profile import Profile
        from pdftools_sdk.image.document import Document as ImageDocument

        if not isinstance(in_doc, PdfDocument):
            raise TypeError(f"Expected type {PdfDocument.__name__}, but got {type(in_doc).__name__}.")
        if not isinstance(out_stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(out_stream).__name__}.")
        if not isinstance(profile, Profile):
            raise TypeError(f"Expected type {Profile.__name__}, but got {type(profile).__name__}.")
        if not isinstance(page_number, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(page_number).__name__}.")

        _lib.PdfToolsPdf2Image_Converter_ConvertPage.argtypes = [c_void_p, c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor), c_void_p, c_int]
        _lib.PdfToolsPdf2Image_Converter_ConvertPage.restype = c_void_p
        ret_val = _lib.PdfToolsPdf2Image_Converter_ConvertPage(self._handle, in_doc._handle, _StreamDescriptor(out_stream), profile._handle, page_number)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ImageDocument._create_dynamic_type(ret_val)



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
