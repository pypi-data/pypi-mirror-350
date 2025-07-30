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
    from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy
    from pdftools_sdk.document_assembly.removal_strategy import RemovalStrategy
    from pdftools_sdk.document_assembly.name_conflict_resolution import NameConflictResolution
    from pdftools_sdk.document_assembly.named_destination_copy_strategy import NamedDestinationCopyStrategy
    from pdftools_sdk.document_assembly.page_rotation import PageRotation

else:
    CopyStrategy = "pdftools_sdk.document_assembly.copy_strategy.CopyStrategy"
    RemovalStrategy = "pdftools_sdk.document_assembly.removal_strategy.RemovalStrategy"
    NameConflictResolution = "pdftools_sdk.document_assembly.name_conflict_resolution.NameConflictResolution"
    NamedDestinationCopyStrategy = "pdftools_sdk.document_assembly.named_destination_copy_strategy.NamedDestinationCopyStrategy"
    PageRotation = "pdftools_sdk.document_assembly.page_rotation.PageRotation"


class PageCopyOptions(_NativeObject):
    """
    This class determines whether and how different PDF elements are copied.


    """
    def __init__(self):
        """


        """
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_New.argtypes = []
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_New.restype = c_void_p
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def links(self) -> CopyStrategy:
        """
        Copy strategy for links.

         
        Specifies how links (document internal and external links) are treated
        when copying a page.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Returns:
            pdftools_sdk.document_assembly.copy_strategy.CopyStrategy

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetLinks.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetLinks.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetLinks(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return CopyStrategy(ret_val)



    @links.setter
    def links(self, val: CopyStrategy) -> None:
        """
        Copy strategy for links.

         
        Specifies how links (document internal and external links) are treated
        when copying a page.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Args:
            val (pdftools_sdk.document_assembly.copy_strategy.CopyStrategy):
                property value

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        if not isinstance(val, CopyStrategy):
            raise TypeError(f"Expected type {CopyStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetLinks.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetLinks.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetLinks(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def form_fields(self) -> CopyStrategy:
        """
        Copy strategy for form fields.

         
        Specifies how form fields are treated when copying a page.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Returns:
            pdftools_sdk.document_assembly.copy_strategy.CopyStrategy

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFields.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFields.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFields(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return CopyStrategy(ret_val)



    @form_fields.setter
    def form_fields(self, val: CopyStrategy) -> None:
        """
        Copy strategy for form fields.

         
        Specifies how form fields are treated when copying a page.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Args:
            val (pdftools_sdk.document_assembly.copy_strategy.CopyStrategy):
                property value

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        if not isinstance(val, CopyStrategy):
            raise TypeError(f"Expected type {CopyStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFields.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFields.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFields(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def signed_signatures(self) -> RemovalStrategy:
        """
        Removal strategy for signed signature fields.

         
        Signed digital signatures are always invalidated when copying a page
        and therefore have to be removed.
        This property specifies, whether the visual representation of the signature
        is preserved.
         
        Default value: :attr:`pdftools_sdk.document_assembly.removal_strategy.RemovalStrategy.REMOVE` 



        Returns:
            pdftools_sdk.document_assembly.removal_strategy.RemovalStrategy

        """
        from pdftools_sdk.document_assembly.removal_strategy import RemovalStrategy

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetSignedSignatures.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetSignedSignatures.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetSignedSignatures(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return RemovalStrategy(ret_val)



    @signed_signatures.setter
    def signed_signatures(self, val: RemovalStrategy) -> None:
        """
        Removal strategy for signed signature fields.

         
        Signed digital signatures are always invalidated when copying a page
        and therefore have to be removed.
        This property specifies, whether the visual representation of the signature
        is preserved.
         
        Default value: :attr:`pdftools_sdk.document_assembly.removal_strategy.RemovalStrategy.REMOVE` 



        Args:
            val (pdftools_sdk.document_assembly.removal_strategy.RemovalStrategy):
                property value

        """
        from pdftools_sdk.document_assembly.removal_strategy import RemovalStrategy

        if not isinstance(val, RemovalStrategy):
            raise TypeError(f"Expected type {RemovalStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetSignedSignatures.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetSignedSignatures.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetSignedSignatures(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def unsigned_signatures(self) -> CopyStrategy:
        """
        Copy strategy for unsigned signature fields.

         
        Specifies how signature fields are treated, that are not yet signed.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Returns:
            pdftools_sdk.document_assembly.copy_strategy.CopyStrategy

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetUnsignedSignatures.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetUnsignedSignatures.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetUnsignedSignatures(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return CopyStrategy(ret_val)



    @unsigned_signatures.setter
    def unsigned_signatures(self, val: CopyStrategy) -> None:
        """
        Copy strategy for unsigned signature fields.

         
        Specifies how signature fields are treated, that are not yet signed.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Args:
            val (pdftools_sdk.document_assembly.copy_strategy.CopyStrategy):
                property value

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        if not isinstance(val, CopyStrategy):
            raise TypeError(f"Expected type {CopyStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetUnsignedSignatures.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetUnsignedSignatures.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetUnsignedSignatures(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def annotations(self) -> CopyStrategy:
        """
        Copy strategy for annotations.

         
        Specifies how interactive annotations (like sticky notes or text highlights)
        are treated when copying a page.
        This does not include links, form fields and signature fields which
        are not considered annotations in this product.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Returns:
            pdftools_sdk.document_assembly.copy_strategy.CopyStrategy

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetAnnotations.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetAnnotations.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetAnnotations(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return CopyStrategy(ret_val)



    @annotations.setter
    def annotations(self, val: CopyStrategy) -> None:
        """
        Copy strategy for annotations.

         
        Specifies how interactive annotations (like sticky notes or text highlights)
        are treated when copying a page.
        This does not include links, form fields and signature fields which
        are not considered annotations in this product.
         
        Default value: :attr:`pdftools_sdk.document_assembly.copy_strategy.CopyStrategy.COPY` 



        Args:
            val (pdftools_sdk.document_assembly.copy_strategy.CopyStrategy):
                property value

        """
        from pdftools_sdk.document_assembly.copy_strategy import CopyStrategy

        if not isinstance(val, CopyStrategy):
            raise TypeError(f"Expected type {CopyStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetAnnotations.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetAnnotations.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetAnnotations(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def copy_outline_items(self) -> bool:
        """
        Copy outline items (bookmarks).

         
        Specifies whether outline items (also known as bookmarks) pointing to the copied page
        should be copied to the target document automatically.
         
        Default value: `True`



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyOutlineItems.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyOutlineItems.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyOutlineItems(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_outline_items.setter
    def copy_outline_items(self, val: bool) -> None:
        """
        Copy outline items (bookmarks).

         
        Specifies whether outline items (also known as bookmarks) pointing to the copied page
        should be copied to the target document automatically.
         
        Default value: `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyOutlineItems.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyOutlineItems.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyOutlineItems(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def copy_associated_files(self) -> bool:
        """
        Copy associated files.

         
        Specifies whether embedded files associated with a page or any of its
        subobjects are also copied when copying the page.
         
        Default value: `True`



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyAssociatedFiles.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyAssociatedFiles.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyAssociatedFiles(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_associated_files.setter
    def copy_associated_files(self, val: bool) -> None:
        """
        Copy associated files.

         
        Specifies whether embedded files associated with a page or any of its
        subobjects are also copied when copying the page.
         
        Default value: `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyAssociatedFiles.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyAssociatedFiles.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyAssociatedFiles(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def copy_logical_structure(self) -> bool:
        """
        Copy the logical structure and tagging information.

         
        Specifies whether the logical structure and tagging information associated
        with a page or its content is also copied when copying the page.
         
        This is required if the target document conformance is PDF/A Level a.
         
        Default value: `True`



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyLogicalStructure.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyLogicalStructure.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetCopyLogicalStructure(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @copy_logical_structure.setter
    def copy_logical_structure(self, val: bool) -> None:
        """
        Copy the logical structure and tagging information.

         
        Specifies whether the logical structure and tagging information associated
        with a page or its content is also copied when copying the page.
         
        This is required if the target document conformance is PDF/A Level a.
         
        Default value: `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyLogicalStructure.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyLogicalStructure.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetCopyLogicalStructure(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def form_field_conflict_resolution(self) -> NameConflictResolution:
        """
        Resolution of conflicting form field names.

         
        Form field of different files can have the same name (identifier).
        This property specifies how name conflicts are resolved,
        when copying pages from multiple source files.
         
        Default value: :attr:`pdftools_sdk.document_assembly.name_conflict_resolution.NameConflictResolution.MERGE` 



        Returns:
            pdftools_sdk.document_assembly.name_conflict_resolution.NameConflictResolution

        """
        from pdftools_sdk.document_assembly.name_conflict_resolution import NameConflictResolution

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFieldConflictResolution.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFieldConflictResolution.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetFormFieldConflictResolution(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return NameConflictResolution(ret_val)



    @form_field_conflict_resolution.setter
    def form_field_conflict_resolution(self, val: NameConflictResolution) -> None:
        """
        Resolution of conflicting form field names.

         
        Form field of different files can have the same name (identifier).
        This property specifies how name conflicts are resolved,
        when copying pages from multiple source files.
         
        Default value: :attr:`pdftools_sdk.document_assembly.name_conflict_resolution.NameConflictResolution.MERGE` 



        Args:
            val (pdftools_sdk.document_assembly.name_conflict_resolution.NameConflictResolution):
                property value

        """
        from pdftools_sdk.document_assembly.name_conflict_resolution import NameConflictResolution

        if not isinstance(val, NameConflictResolution):
            raise TypeError(f"Expected type {NameConflictResolution.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFieldConflictResolution.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFieldConflictResolution.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetFormFieldConflictResolution(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def named_destinations(self) -> NamedDestinationCopyStrategy:
        """
        Copy strategy for named destinations

         
        Specify whether named destinations are resolved when copying a page.
         
        Default value: :attr:`pdftools_sdk.document_assembly.named_destination_copy_strategy.NamedDestinationCopyStrategy.COPY` 



        Returns:
            pdftools_sdk.document_assembly.named_destination_copy_strategy.NamedDestinationCopyStrategy

        """
        from pdftools_sdk.document_assembly.named_destination_copy_strategy import NamedDestinationCopyStrategy

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetNamedDestinations.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetNamedDestinations.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetNamedDestinations(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return NamedDestinationCopyStrategy(ret_val)



    @named_destinations.setter
    def named_destinations(self, val: NamedDestinationCopyStrategy) -> None:
        """
        Copy strategy for named destinations

         
        Specify whether named destinations are resolved when copying a page.
         
        Default value: :attr:`pdftools_sdk.document_assembly.named_destination_copy_strategy.NamedDestinationCopyStrategy.COPY` 



        Args:
            val (pdftools_sdk.document_assembly.named_destination_copy_strategy.NamedDestinationCopyStrategy):
                property value

        """
        from pdftools_sdk.document_assembly.named_destination_copy_strategy import NamedDestinationCopyStrategy

        if not isinstance(val, NamedDestinationCopyStrategy):
            raise TypeError(f"Expected type {NamedDestinationCopyStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetNamedDestinations.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetNamedDestinations.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetNamedDestinations(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def optimize_resources(self) -> bool:
        """
        Find and merge redundant resources.

         
        Find and merge redundant resources such as fonts and images.
        This can lead to much smaller files, especially when copying
        pages from multiple similar source files.
        However, it also results in longer processing time.
         
        Default value: `True`



        Returns:
            bool

        """
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetOptimizeResources.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetOptimizeResources.restype = c_bool
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetOptimizeResources(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @optimize_resources.setter
    def optimize_resources(self, val: bool) -> None:
        """
        Find and merge redundant resources.

         
        Find and merge redundant resources such as fonts and images.
        This can lead to much smaller files, especially when copying
        pages from multiple similar source files.
        However, it also results in longer processing time.
         
        Default value: `True`



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetOptimizeResources.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetOptimizeResources.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetOptimizeResources(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def page_rotation(self) -> PageRotation:
        """
        Specify how page(s) should be rotated.

         
         
        Default is :attr:`pdftools_sdk.document_assembly.page_rotation.PageRotation.NOROTATION` 



        Returns:
            pdftools_sdk.document_assembly.page_rotation.PageRotation

        """
        from pdftools_sdk.document_assembly.page_rotation import PageRotation

        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetPageRotation.argtypes = [c_void_p]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetPageRotation.restype = c_int
        ret_val = _lib.PdfToolsDocumentAssembly_PageCopyOptions_GetPageRotation(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return PageRotation(ret_val)



    @page_rotation.setter
    def page_rotation(self, val: PageRotation) -> None:
        """
        Specify how page(s) should be rotated.

         
         
        Default is :attr:`pdftools_sdk.document_assembly.page_rotation.PageRotation.NOROTATION` 



        Args:
            val (pdftools_sdk.document_assembly.page_rotation.PageRotation):
                property value

        """
        from pdftools_sdk.document_assembly.page_rotation import PageRotation

        if not isinstance(val, PageRotation):
            raise TypeError(f"Expected type {PageRotation.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetPageRotation.argtypes = [c_void_p, c_int]
        _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetPageRotation.restype = c_bool
        if not _lib.PdfToolsDocumentAssembly_PageCopyOptions_SetPageRotation(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return PageCopyOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = PageCopyOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
