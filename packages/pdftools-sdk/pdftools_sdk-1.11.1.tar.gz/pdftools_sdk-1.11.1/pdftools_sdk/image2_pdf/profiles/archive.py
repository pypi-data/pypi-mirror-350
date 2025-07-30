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
import pdftools_sdk.image2_pdf.profiles.profile

if TYPE_CHECKING:
    from pdftools_sdk.pdf.conformance import Conformance
    from pdftools_sdk.string_list import StringList

else:
    Conformance = "pdftools_sdk.pdf.conformance.Conformance"
    StringList = "pdftools_sdk.string_list.StringList"


class Archive(pdftools_sdk.image2_pdf.profiles.profile.Profile):
    """
    The profile for image to PDF/A conversion for archiving

    This profile is suitable for archiving images as PDFs.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsImage2PdfProfiles_Archive_New.argtypes = []
        _lib.PdfToolsImage2PdfProfiles_Archive_New.restype = c_void_p
        ret_val = _lib.PdfToolsImage2PdfProfiles_Archive_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def conformance(self) -> Conformance:
        """
        The PDF/A conformance of the output document

         
        The supported PDF/A conformance are:
         
        - "PDF/A-1b"
        - "PDF/A-1a"
        - "PDF/A-2b"
        - "PDF/A-2u"
        - "PDF/A-2a"
        - "PDF/A-3b"
        - "PDF/A-3u"
        - "PDF/A-3a"
         
        With level A conformances (PDF/A-1a, PDF/A-2a, PDF/A-3a),
        the properties :attr:`pdftools_sdk.image2_pdf.profiles.archive.Archive.alternate_text` 
        and :attr:`pdftools_sdk.image2_pdf.profiles.archive.Archive.language`  must be set.
         
        Default value: "PDF/A-2b"



        Returns:
            pdftools_sdk.pdf.conformance.Conformance

        """
        from pdftools_sdk.pdf.conformance import Conformance

        _lib.PdfToolsImage2PdfProfiles_Archive_GetConformance.argtypes = [c_void_p]
        _lib.PdfToolsImage2PdfProfiles_Archive_GetConformance.restype = c_int
        ret_val = _lib.PdfToolsImage2PdfProfiles_Archive_GetConformance(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Conformance(ret_val)



    @conformance.setter
    def conformance(self, val: Conformance) -> None:
        """
        The PDF/A conformance of the output document

         
        The supported PDF/A conformance are:
         
        - "PDF/A-1b"
        - "PDF/A-1a"
        - "PDF/A-2b"
        - "PDF/A-2u"
        - "PDF/A-2a"
        - "PDF/A-3b"
        - "PDF/A-3u"
        - "PDF/A-3a"
         
        With level A conformances (PDF/A-1a, PDF/A-2a, PDF/A-3a),
        the properties :attr:`pdftools_sdk.image2_pdf.profiles.archive.Archive.alternate_text` 
        and :attr:`pdftools_sdk.image2_pdf.profiles.archive.Archive.language`  must be set.
         
        Default value: "PDF/A-2b"



        Args:
            val (pdftools_sdk.pdf.conformance.Conformance):
                property value

        Raises:
            ValueError:
                The conformance is PDF but must be PDF/A for this profile.
                Use the profile :class:`pdftools_sdk.image2_pdf.profiles.default.Default`  to create PDF documents.


        """
        from pdftools_sdk.pdf.conformance import Conformance

        if not isinstance(val, Conformance):
            raise TypeError(f"Expected type {Conformance.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsImage2PdfProfiles_Archive_SetConformance.argtypes = [c_void_p, c_int]
        _lib.PdfToolsImage2PdfProfiles_Archive_SetConformance.restype = c_bool
        if not _lib.PdfToolsImage2PdfProfiles_Archive_SetConformance(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def alternate_text(self) -> StringList:
        """
        The alternate text describing the image

         
        The alternate text provides a meaningful description of the images.
        For example, "This color image shows a small sailing boat at sunset".
        This information can be used to read the document to the visually impaired.
         
        The list must contain a description for each page of the input image document.
        For the conversion of :class:`pdftools_sdk.image.single_page_document.SinglePageDocument` , a single description
        is sufficient. For :class:`pdftools_sdk.image.multi_page_document.MultiPageDocument` , multiple descriptions may be
        required.
         
        Alternate text is required for PDF/A level A conformance.
        It is not advisable to add "dummy" tagging solely for the purpose of achieving level A
        conformance. Instead, for scanned text documents, the Conversion Service can be used to
        recognize the characters in the documents (OCR) and tag the image with the recognized structure and text.
        For other types of images, such as photos, logos or graphics, alternate text descriptions
        should be written manually by a user.
         
        Default is empty list



        Returns:
            pdftools_sdk.string_list.StringList

        """
        from pdftools_sdk.string_list import StringList

        _lib.PdfToolsImage2PdfProfiles_Archive_GetAlternateText.argtypes = [c_void_p]
        _lib.PdfToolsImage2PdfProfiles_Archive_GetAlternateText.restype = c_void_p
        ret_val = _lib.PdfToolsImage2PdfProfiles_Archive_GetAlternateText(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return StringList._create_dynamic_type(ret_val)


    @alternate_text.setter
    def alternate_text(self, val: StringList) -> None:
        """
        The alternate text describing the image

         
        The alternate text provides a meaningful description of the images.
        For example, "This color image shows a small sailing boat at sunset".
        This information can be used to read the document to the visually impaired.
         
        The list must contain a description for each page of the input image document.
        For the conversion of :class:`pdftools_sdk.image.single_page_document.SinglePageDocument` , a single description
        is sufficient. For :class:`pdftools_sdk.image.multi_page_document.MultiPageDocument` , multiple descriptions may be
        required.
         
        Alternate text is required for PDF/A level A conformance.
        It is not advisable to add "dummy" tagging solely for the purpose of achieving level A
        conformance. Instead, for scanned text documents, the Conversion Service can be used to
        recognize the characters in the documents (OCR) and tag the image with the recognized structure and text.
        For other types of images, such as photos, logos or graphics, alternate text descriptions
        should be written manually by a user.
         
        Default is empty list



        Args:
            val (pdftools_sdk.string_list.StringList):
                property value

        """
        from pdftools_sdk.string_list import StringList

        if not isinstance(val, StringList):
            raise TypeError(f"Expected type {StringList.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsImage2PdfProfiles_Archive_SetAlternateText.argtypes = [c_void_p, c_void_p]
        _lib.PdfToolsImage2PdfProfiles_Archive_SetAlternateText.restype = c_bool
        if not _lib.PdfToolsImage2PdfProfiles_Archive_SetAlternateText(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def language(self) -> Optional[str]:
        """
        The language of the output PDF

         
        The language code that specifies the language of the PDF and specifically
        its :attr:`pdftools_sdk.image2_pdf.profiles.archive.Archive.alternate_text`  descriptions.
        Specifying the language is highly recommended for PDF/A level A conformance.
         
        The codes are defined in BCP 47 and ISO 3166:2013 and can
        be obtained from the Internet Engineering Task Force and
        the International Organization for Standardization.
         
        If no code is set, the language will be specified as
        unknown.
         
        Examples:
         
        - "en"
        - "en-US"
        - "de"
        - "de-CH"
        - "fr-FR"
        - "zxx" (for non linguistic content)
         
         
        Default is `None` (unknown)



        Returns:
            Optional[str]

        """
        _lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW.restype = c_size_t
        ret_val_size = _lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsImage2PdfProfiles_Archive_GetLanguageW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @language.setter
    def language(self, val: Optional[str]) -> None:
        """
        The language of the output PDF

         
        The language code that specifies the language of the PDF and specifically
        its :attr:`pdftools_sdk.image2_pdf.profiles.archive.Archive.alternate_text`  descriptions.
        Specifying the language is highly recommended for PDF/A level A conformance.
         
        The codes are defined in BCP 47 and ISO 3166:2013 and can
        be obtained from the Internet Engineering Task Force and
        the International Organization for Standardization.
         
        If no code is set, the language will be specified as
        unknown.
         
        Examples:
         
        - "en"
        - "en-US"
        - "de"
        - "de-CH"
        - "fr-FR"
        - "zxx" (for non linguistic content)
         
         
        Default is `None` (unknown)



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsImage2PdfProfiles_Archive_SetLanguageW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsImage2PdfProfiles_Archive_SetLanguageW.restype = c_bool
        if not _lib.PdfToolsImage2PdfProfiles_Archive_SetLanguageW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Archive._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Archive.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
