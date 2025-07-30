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
    from pdftools_sdk.sys.date import _Date

else:
    _Date = "pdftools_sdk.sys.date._Date"


class Metadata(_NativeObject):
    """
     
    Represents the metadata of a document or an object in a document.
     
    For document level metadata,
    all changes are reflected in both,
    XMP metadata and document info dictionary depending on the conformance
    of the document.


    """
    @property
    def title(self) -> Optional[str]:
        """
        The title of the document or resource.

        This property corresponds to the "dc:title" entry
        in the XMP metadata and to the "Title" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PdfToolsPdf_Metadata_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Metadata_GetTitleW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Metadata_GetTitleW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Metadata_GetTitleW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def author(self) -> Optional[str]:
        """
        The name of the person who created the document or resource.

        This property corresponds to the "dc:creator" entry
        in the XMP metadata and to the "Author" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PdfToolsPdf_Metadata_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Metadata_GetAuthorW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Metadata_GetAuthorW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Metadata_GetAuthorW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def subject(self) -> Optional[str]:
        """
        The subject of the document or resource.

        This property corresponds to the "dc:description" entry
        in the XMP metadata and to the "Subject" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PdfToolsPdf_Metadata_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Metadata_GetSubjectW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Metadata_GetSubjectW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Metadata_GetSubjectW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def keywords(self) -> Optional[str]:
        """
        Keywords associated with the document or resource.

         
        Keywords can be separated by:
         
        - carriage return / line feed
        - comma
        - semicolon
        - tab
        - double space
         
         
        This property corresponds to the "pdf:Keywords" entry
        in the XMP metadata and to the "Keywords" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PdfToolsPdf_Metadata_GetKeywordsW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Metadata_GetKeywordsW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Metadata_GetKeywordsW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Metadata_GetKeywordsW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def creator(self) -> Optional[str]:
        """
        The original application that created the document.

         
        The name of the first known tool used to create the document or resource.
         
        This property corresponds to the "xmp:CreatorTool" entry
        in the XMP metadata and to the "Creator" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PdfToolsPdf_Metadata_GetCreatorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Metadata_GetCreatorW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Metadata_GetCreatorW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Metadata_GetCreatorW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def producer(self) -> Optional[str]:
        """
        The application that created the PDF

         
        If the document was converted to PDF from another format,
        the name of the PDF processor that converted it to PDF.
         
        This property corresponds to the "pdf:Producer" entry
        in the XMP metadata and to the "Producer" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        _lib.PdfToolsPdf_Metadata_GetProducerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Metadata_GetProducerW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Metadata_GetProducerW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Metadata_GetProducerW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def creation_date(self) -> Optional[datetime]:
        """
        The date and time the document or resource was originally created.

        This property corresponds to the "xmp:CreateDate" entry
        in the XMP metadata and to the "CreationDate" entry in
        the document information dictionary.



        Returns:
            Optional[datetime]

        Raises:
            StateError:
                if the metadata have already been closed


        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsPdf_Metadata_GetCreationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsPdf_Metadata_GetCreationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsPdf_Metadata_GetCreationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @property
    def modification_date(self) -> Optional[datetime]:
        """
        The date and time the document or resource was most recently modified.

        This property corresponds to the "xmp:ModifyDate" entry
        in the XMP metadata and to the "ModDate" entry in
        the document information dictionary.



        Returns:
            Optional[datetime]

        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                The date is corrupt.

            StateError:
                if the metadata have already been closed


        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsPdf_Metadata_GetModificationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsPdf_Metadata_GetModificationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsPdf_Metadata_GetModificationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()



    @staticmethod
    def _create_dynamic_type(handle):
        return Metadata._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Metadata.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
