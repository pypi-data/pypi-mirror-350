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


class MetadataSettings(_NativeObject):
    """
    It allows you to set and update individual metadata properties.
    Any metadata properties that have been explicitly set are included in the output document.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsPdf_MetadataSettings_New.argtypes = []
        _lib.PdfToolsPdf_MetadataSettings_New.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_MetadataSettings_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


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
                If the metadata settings have already been closed


        """
        _lib.PdfToolsPdf_MetadataSettings_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_MetadataSettings_GetTitleW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_MetadataSettings_GetTitleW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_MetadataSettings_GetTitleW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @title.setter
    def title(self, val: Optional[str]) -> None:
        """
        The title of the document or resource.

        This property corresponds to the "dc:title" entry
        in the XMP metadata and to the "Title" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetTitleW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsPdf_MetadataSettings_SetTitleW.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetTitleW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

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
                If the metadata settings have already been closed


        """
        _lib.PdfToolsPdf_MetadataSettings_GetAuthorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_MetadataSettings_GetAuthorW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_MetadataSettings_GetAuthorW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_MetadataSettings_GetAuthorW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @author.setter
    def author(self, val: Optional[str]) -> None:
        """
        The name of the person who created the document or resource.

        This property corresponds to the "dc:creator" entry
        in the XMP metadata and to the "Author" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetAuthorW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsPdf_MetadataSettings_SetAuthorW.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetAuthorW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

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
                If the metadata settings have already been closed


        """
        _lib.PdfToolsPdf_MetadataSettings_GetSubjectW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_MetadataSettings_GetSubjectW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_MetadataSettings_GetSubjectW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_MetadataSettings_GetSubjectW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @subject.setter
    def subject(self, val: Optional[str]) -> None:
        """
        The subject of the document or resource.

        This property corresponds to the "dc:description" entry
        in the XMP metadata and to the "Subject" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetSubjectW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsPdf_MetadataSettings_SetSubjectW.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetSubjectW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

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
                If the metadata settings have already been closed


        """
        _lib.PdfToolsPdf_MetadataSettings_GetKeywordsW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_MetadataSettings_GetKeywordsW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_MetadataSettings_GetKeywordsW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_MetadataSettings_GetKeywordsW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @keywords.setter
    def keywords(self, val: Optional[str]) -> None:
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



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetKeywordsW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsPdf_MetadataSettings_SetKeywordsW.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetKeywordsW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

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
                If the metadata settings have already been closed


        """
        _lib.PdfToolsPdf_MetadataSettings_GetCreatorW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_MetadataSettings_GetCreatorW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_MetadataSettings_GetCreatorW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_MetadataSettings_GetCreatorW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @creator.setter
    def creator(self, val: Optional[str]) -> None:
        """
        The original application that created the document.

         
        The name of the first known tool used to create the document or resource.
         
        This property corresponds to the "xmp:CreatorTool" entry
        in the XMP metadata and to the "Creator" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetCreatorW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsPdf_MetadataSettings_SetCreatorW.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetCreatorW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def producer(self) -> Optional[str]:
        """
        The application that created the PDF

         
        If the document has been converted to PDF from another format,
        the name of the PDF processor that converted the document to PDF.
         
        This property corresponds to the "pdf:Producer" entry
        in the XMP metadata and to the "Producer" entry in
        the document information dictionary.



        Returns:
            Optional[str]

        Raises:
            StateError:
                If the metadata settings have already been closed


        """
        _lib.PdfToolsPdf_MetadataSettings_GetProducerW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_MetadataSettings_GetProducerW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_MetadataSettings_GetProducerW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_MetadataSettings_GetProducerW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @producer.setter
    def producer(self, val: Optional[str]) -> None:
        """
        The application that created the PDF

         
        If the document has been converted to PDF from another format,
        the name of the PDF processor that converted the document to PDF.
         
        This property corresponds to the "pdf:Producer" entry
        in the XMP metadata and to the "Producer" entry in
        the document information dictionary.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetProducerW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsPdf_MetadataSettings_SetProducerW.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetProducerW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

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
                If the metadata settings have already been closed


        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsPdf_MetadataSettings_GetCreationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsPdf_MetadataSettings_GetCreationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsPdf_MetadataSettings_GetCreationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @creation_date.setter
    def creation_date(self, val: Optional[datetime]) -> None:
        """
        The date and time the document or resource was originally created.

        This property corresponds to the "xmp:CreateDate" entry
        in the XMP metadata and to the "CreationDate" entry in
        the document information dictionary.



        Args:
            val (Optional[datetime]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed

            ValueError:
                The date is invalid.


        """
        from pdftools_sdk.sys.date import _Date

        if val is not None and not isinstance(val, datetime):
            raise TypeError(f"Expected type {datetime.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetCreationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsPdf_MetadataSettings_SetCreationDate.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetCreationDate(self._handle, _Date._from_datetime(val)):
            _NativeBase._throw_last_error(False)

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
            StateError:
                If the metadata settings have already been closed


        """
        from pdftools_sdk.sys.date import _Date

        _lib.PdfToolsPdf_MetadataSettings_GetModificationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsPdf_MetadataSettings_GetModificationDate.restype = c_bool
        ret_val = _Date()
        if not _lib.PdfToolsPdf_MetadataSettings_GetModificationDate(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val._to_datetime()


    @modification_date.setter
    def modification_date(self, val: Optional[datetime]) -> None:
        """
        The date and time the document or resource was most recently modified.

        This property corresponds to the "xmp:ModifyDate" entry
        in the XMP metadata and to the "ModDate" entry in
        the document information dictionary.



        Args:
            val (Optional[datetime]):
                property value

        Raises:
            StateError:
                If the metadata settings have already been closed

            ValueError:
                The date is invalid.


        """
        from pdftools_sdk.sys.date import _Date

        if val is not None and not isinstance(val, datetime):
            raise TypeError(f"Expected type {datetime.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_MetadataSettings_SetModificationDate.argtypes = [c_void_p, POINTER(_Date)]
        _lib.PdfToolsPdf_MetadataSettings_SetModificationDate.restype = c_bool
        if not _lib.PdfToolsPdf_MetadataSettings_SetModificationDate(self._handle, _Date._from_datetime(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return MetadataSettings._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = MetadataSettings.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
