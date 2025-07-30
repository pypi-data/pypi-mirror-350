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
    from pdftools_sdk.optimization.removal_strategy import RemovalStrategy
    from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy

else:
    RemovalStrategy = "pdftools_sdk.optimization.removal_strategy.RemovalStrategy"
    ConversionStrategy = "pdftools_sdk.optimization.conversion_strategy.ConversionStrategy"


class RemovalOptions(_NativeObject):
    """
    The parameters defining the optional data to remove or flatten

     
    Removal options specify the PDF data structures to copy or remove,
    e.g. article threads, metadata, or alternate images.
     
    In addition, the visual appearances of signatures, annotations, form fields,
    and links can be flattened.
     
    Flattening means, that the appearance of such a data structure is drawn as
    non-editable graphic onto the page; for visual appearances of signatures,
    flattening has a slightly different meaning
    (see property :attr:`pdftools_sdk.optimization.removal_options.RemovalOptions.remove_signature_appearances` ).


    """
    @property
    def remove_alternate_images(self) -> bool:
        """
        Whether to remove additional or alternative versions of images

        Default is `False` except in the profile :class:`pdftools_sdk.optimization.profiles.print.Print` .



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveAlternateImages.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveAlternateImages.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemoveAlternateImages(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_alternate_images.setter
    def remove_alternate_images(self, val: bool) -> None:
        """
        Whether to remove additional or alternative versions of images

        Default is `False` except in the profile :class:`pdftools_sdk.optimization.profiles.print.Print` .



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveAlternateImages.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveAlternateImages.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemoveAlternateImages(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_article_threads(self) -> bool:
        """
        Whether to remove the sequential flows (threads) of articles

        Default is `True` except in the profile :class:`pdftools_sdk.optimization.profiles.archive.Archive` .



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveArticleThreads.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveArticleThreads.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemoveArticleThreads(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_article_threads.setter
    def remove_article_threads(self, val: bool) -> None:
        """
        Whether to remove the sequential flows (threads) of articles

        Default is `True` except in the profile :class:`pdftools_sdk.optimization.profiles.archive.Archive` .



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveArticleThreads.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveArticleThreads.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemoveArticleThreads(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_metadata(self) -> bool:
        """
        Whether to remove document's XMP metadata

        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: `False`
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: `False`
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: `False`
         



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveMetadata.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveMetadata.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemoveMetadata(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_metadata.setter
    def remove_metadata(self, val: bool) -> None:
        """
        Whether to remove document's XMP metadata

        Default:
         
        - :class:`pdftools_sdk.optimization.profiles.web.Web`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.print.Print`  profile: `False`
        - :class:`pdftools_sdk.optimization.profiles.archive.Archive`  profile: `False`
        - :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize`  profile: `True`
        - :class:`pdftools_sdk.optimization.profiles.mrc.Mrc`  profile: `False`
         



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveMetadata.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveMetadata.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemoveMetadata(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_output_intents(self) -> bool:
        """
        Whether to remove all output intents

         
        Output intents provide a means for matching the color characteristics
        of PDF page content with those of a target output device or
        production environment in which the document will be printed.
         
        Default is `False` except in the profile :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize` .



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveOutputIntents.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveOutputIntents.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemoveOutputIntents(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_output_intents.setter
    def remove_output_intents(self, val: bool) -> None:
        """
        Whether to remove all output intents

         
        Output intents provide a means for matching the color characteristics
        of PDF page content with those of a target output device or
        production environment in which the document will be printed.
         
        Default is `False` except in the profile :class:`pdftools_sdk.optimization.profiles.minimal_file_size.MinimalFileSize` .



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveOutputIntents.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveOutputIntents.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemoveOutputIntents(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_piece_info(self) -> bool:
        """
        Whether to remove the piece-info dictionary (private PDF processor data)

         
        The removal of this proprietary application data has no effect on the document's
        visual appearance.
         
        Default is `True` except in the profile :class:`pdftools_sdk.optimization.profiles.archive.Archive` .



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_RemovalOptions_GetRemovePieceInfo.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemovePieceInfo.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemovePieceInfo(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_piece_info.setter
    def remove_piece_info(self, val: bool) -> None:
        """
        Whether to remove the piece-info dictionary (private PDF processor data)

         
        The removal of this proprietary application data has no effect on the document's
        visual appearance.
         
        Default is `True` except in the profile :class:`pdftools_sdk.optimization.profiles.archive.Archive` .



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemovePieceInfo.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemovePieceInfo.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemovePieceInfo(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_structure_tree(self) -> bool:
        """
        Whether to remove the data describing the logical structure of a PDF

         
        The logical structure of the document is a description of the content of its pages.
        It consists of a fine granular hierarchical tagging that distinguishes between the actual content and artifacts (such as page numbers, layout artifacts, etc.).
        The tagging provides a meaningful description, for example "This is a header", "This color image shows a small sailing boat at sunset", etc.
        This information can be used e.g. to read the document to the visually impaired.
         
        Default is `True` except in the profile :class:`pdftools_sdk.optimization.profiles.archive.Archive` .



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveStructureTree.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveStructureTree.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemoveStructureTree(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_structure_tree.setter
    def remove_structure_tree(self, val: bool) -> None:
        """
        Whether to remove the data describing the logical structure of a PDF

         
        The logical structure of the document is a description of the content of its pages.
        It consists of a fine granular hierarchical tagging that distinguishes between the actual content and artifacts (such as page numbers, layout artifacts, etc.).
        The tagging provides a meaningful description, for example "This is a header", "This color image shows a small sailing boat at sunset", etc.
        This information can be used e.g. to read the document to the visually impaired.
         
        Default is `True` except in the profile :class:`pdftools_sdk.optimization.profiles.archive.Archive` .



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveStructureTree.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveStructureTree.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemoveStructureTree(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_thumbnails(self) -> bool:
        """
        Whether to remove thumbnail images which represent the PDF pages in miniature form

        Default is `True` in all profiles.



        Returns:
            bool

        """
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveThumbnails.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveThumbnails.restype = c_bool
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemoveThumbnails(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @remove_thumbnails.setter
    def remove_thumbnails(self, val: bool) -> None:
        """
        Whether to remove thumbnail images which represent the PDF pages in miniature form

        Default is `True` in all profiles.



        Args:
            val (bool):
                property value

        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveThumbnails.argtypes = [c_void_p, c_bool]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveThumbnails.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemoveThumbnails(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def remove_signature_appearances(self) -> RemovalStrategy:
        """
        Whether to remove or flatten signature appearances

         
        A signature in a PDF consist of two parts:
         
         
        - *(a)* The invisible digital signature in the PDF.
        - *(b)* The visual appearance that was attributed to the signature.
         
         
        Part (a) can be used by a viewing application, to verify that the PDF
        has not changed since it has been signed and report this to the user.
         
        During optimizing, the PDF is altered and hence its digital signature
        (a) is broken and must be removed.
         
         
        - :attr:`pdftools_sdk.optimization.removal_strategy.RemovalStrategy.FLATTEN` : (a) is removed and (b) is drawn as non-editable graphic onto the page.
          Within the context of signatures this is called "flattening".
        - :attr:`pdftools_sdk.optimization.removal_strategy.RemovalStrategy.REMOVE` : (a) and (b) are removed.
         
         
        Default is :attr:`pdftools_sdk.optimization.removal_strategy.RemovalStrategy.FLATTEN`  in all profiles.



        Returns:
            pdftools_sdk.optimization.removal_strategy.RemovalStrategy

        """
        from pdftools_sdk.optimization.removal_strategy import RemovalStrategy

        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveSignatureAppearances.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetRemoveSignatureAppearances.restype = c_int
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetRemoveSignatureAppearances(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return RemovalStrategy(ret_val)



    @remove_signature_appearances.setter
    def remove_signature_appearances(self, val: RemovalStrategy) -> None:
        """
        Whether to remove or flatten signature appearances

         
        A signature in a PDF consist of two parts:
         
         
        - *(a)* The invisible digital signature in the PDF.
        - *(b)* The visual appearance that was attributed to the signature.
         
         
        Part (a) can be used by a viewing application, to verify that the PDF
        has not changed since it has been signed and report this to the user.
         
        During optimizing, the PDF is altered and hence its digital signature
        (a) is broken and must be removed.
         
         
        - :attr:`pdftools_sdk.optimization.removal_strategy.RemovalStrategy.FLATTEN` : (a) is removed and (b) is drawn as non-editable graphic onto the page.
          Within the context of signatures this is called "flattening".
        - :attr:`pdftools_sdk.optimization.removal_strategy.RemovalStrategy.REMOVE` : (a) and (b) are removed.
         
         
        Default is :attr:`pdftools_sdk.optimization.removal_strategy.RemovalStrategy.FLATTEN`  in all profiles.



        Args:
            val (pdftools_sdk.optimization.removal_strategy.RemovalStrategy):
                property value

        """
        from pdftools_sdk.optimization.removal_strategy import RemovalStrategy

        if not isinstance(val, RemovalStrategy):
            raise TypeError(f"Expected type {RemovalStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveSignatureAppearances.argtypes = [c_void_p, c_int]
        _lib.PdfToolsOptimization_RemovalOptions_SetRemoveSignatureAppearances.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetRemoveSignatureAppearances(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def annotations(self) -> ConversionStrategy:
        """
        The conversion strategy for annotations

         
        The conversion strategy for annotations.
         
        Annotations in PDF are interactive elements on the pages, such as:
         
        - Sticky notes
        - Free text annotations
        - Line, square, circle, and polygon annotations
        - Highlight, underline and strikeout annotations
        - Stamp annotations
        - Ink annotations
        - File attachment annotation
        - Sound and movie annotations
        - 3D annotations
         
         
        Note that this does not include form fields (see :attr:`pdftools_sdk.optimization.removal_options.RemovalOptions.form_fields` ) and links (see :attr:`pdftools_sdk.optimization.removal_options.RemovalOptions.links` ).
         
        Default is :attr:`pdftools_sdk.optimization.conversion_strategy.ConversionStrategy.COPY`  in all profiles.



        Returns:
            pdftools_sdk.optimization.conversion_strategy.ConversionStrategy

        """
        from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy

        _lib.PdfToolsOptimization_RemovalOptions_GetAnnotations.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetAnnotations.restype = c_int
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetAnnotations(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ConversionStrategy(ret_val)



    @annotations.setter
    def annotations(self, val: ConversionStrategy) -> None:
        """
        The conversion strategy for annotations

         
        The conversion strategy for annotations.
         
        Annotations in PDF are interactive elements on the pages, such as:
         
        - Sticky notes
        - Free text annotations
        - Line, square, circle, and polygon annotations
        - Highlight, underline and strikeout annotations
        - Stamp annotations
        - Ink annotations
        - File attachment annotation
        - Sound and movie annotations
        - 3D annotations
         
         
        Note that this does not include form fields (see :attr:`pdftools_sdk.optimization.removal_options.RemovalOptions.form_fields` ) and links (see :attr:`pdftools_sdk.optimization.removal_options.RemovalOptions.links` ).
         
        Default is :attr:`pdftools_sdk.optimization.conversion_strategy.ConversionStrategy.COPY`  in all profiles.



        Args:
            val (pdftools_sdk.optimization.conversion_strategy.ConversionStrategy):
                property value

        """
        from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy

        if not isinstance(val, ConversionStrategy):
            raise TypeError(f"Expected type {ConversionStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetAnnotations.argtypes = [c_void_p, c_int]
        _lib.PdfToolsOptimization_RemovalOptions_SetAnnotations.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetAnnotations(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def form_fields(self) -> ConversionStrategy:
        """
        The conversion strategy for interactive forms

        Default is :attr:`pdftools_sdk.optimization.conversion_strategy.ConversionStrategy.COPY`  in all profiles.



        Returns:
            pdftools_sdk.optimization.conversion_strategy.ConversionStrategy

        """
        from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy

        _lib.PdfToolsOptimization_RemovalOptions_GetFormFields.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetFormFields.restype = c_int
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetFormFields(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ConversionStrategy(ret_val)



    @form_fields.setter
    def form_fields(self, val: ConversionStrategy) -> None:
        """
        The conversion strategy for interactive forms

        Default is :attr:`pdftools_sdk.optimization.conversion_strategy.ConversionStrategy.COPY`  in all profiles.



        Args:
            val (pdftools_sdk.optimization.conversion_strategy.ConversionStrategy):
                property value

        """
        from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy

        if not isinstance(val, ConversionStrategy):
            raise TypeError(f"Expected type {ConversionStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetFormFields.argtypes = [c_void_p, c_int]
        _lib.PdfToolsOptimization_RemovalOptions_SetFormFields.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetFormFields(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def links(self) -> ConversionStrategy:
        """
        The conversion strategy for links

        Default is :attr:`pdftools_sdk.optimization.conversion_strategy.ConversionStrategy.COPY`  in all profiles.



        Returns:
            pdftools_sdk.optimization.conversion_strategy.ConversionStrategy

        """
        from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy

        _lib.PdfToolsOptimization_RemovalOptions_GetLinks.argtypes = [c_void_p]
        _lib.PdfToolsOptimization_RemovalOptions_GetLinks.restype = c_int
        ret_val = _lib.PdfToolsOptimization_RemovalOptions_GetLinks(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ConversionStrategy(ret_val)



    @links.setter
    def links(self, val: ConversionStrategy) -> None:
        """
        The conversion strategy for links

        Default is :attr:`pdftools_sdk.optimization.conversion_strategy.ConversionStrategy.COPY`  in all profiles.



        Args:
            val (pdftools_sdk.optimization.conversion_strategy.ConversionStrategy):
                property value

        """
        from pdftools_sdk.optimization.conversion_strategy import ConversionStrategy

        if not isinstance(val, ConversionStrategy):
            raise TypeError(f"Expected type {ConversionStrategy.__name__}, but got {type(val).__name__}.")
        _lib.PdfToolsOptimization_RemovalOptions_SetLinks.argtypes = [c_void_p, c_int]
        _lib.PdfToolsOptimization_RemovalOptions_SetLinks.restype = c_bool
        if not _lib.PdfToolsOptimization_RemovalOptions_SetLinks(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return RemovalOptions._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = RemovalOptions.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
