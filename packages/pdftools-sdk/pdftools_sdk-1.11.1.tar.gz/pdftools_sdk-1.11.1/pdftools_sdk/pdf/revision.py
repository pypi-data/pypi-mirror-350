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

class Revision(_NativeObject):
    """
    The document revision

    An incremental update to a PDF creates a new revision.
    A revision is defined by the update itself and all updates that came before, including the initial document.
    An update can introduce changes to the document (visible or invisible), it can sign the current revision, or it can do both.
    But an update can only ever hold one valid signature.


    """
    def write(self, stream: io.IOBase) -> None:
        """
        Write the contents of the document revision to a stream



        Args:
            stream (io.IOBase): 
                The stream to which the revision is written.




        Raises:
            OSError:
                Unable to write to the stream.


        """
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")

        _lib.PdfToolsPdf_Revision_Write.argtypes = [c_void_p, POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsPdf_Revision_Write.restype = c_bool
        if not _lib.PdfToolsPdf_Revision_Write(self._handle, _StreamDescriptor(stream)):
            _NativeBase._throw_last_error(False)



    @property
    def is_latest(self) -> bool:
        """
        Whether this is the latest document revision



        Returns:
            bool

        """
        _lib.PdfToolsPdf_Revision_IsLatest.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Revision_IsLatest.restype = c_bool
        ret_val = _lib.PdfToolsPdf_Revision_IsLatest(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @property
    def has_non_signing_updates(self) -> bool:
        """
        Whether the revision contains a non-signing update.

        Returns `True` if any update leading up to this revision does not contain a signature.
        Returns `False` if every update that leads up to this revision contains a signature.



        Returns:
            bool

        """
        _lib.PdfToolsPdf_Revision_GetHasNonSigningUpdates.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Revision_GetHasNonSigningUpdates.restype = c_bool
        ret_val = _lib.PdfToolsPdf_Revision_GetHasNonSigningUpdates(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        return Revision._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Revision.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
