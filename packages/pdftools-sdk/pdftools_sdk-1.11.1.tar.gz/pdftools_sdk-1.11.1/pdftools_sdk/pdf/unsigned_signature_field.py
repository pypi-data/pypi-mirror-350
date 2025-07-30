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
import pdftools_sdk.pdf.signature_field

class UnsignedSignatureField(pdftools_sdk.pdf.signature_field.SignatureField):
    """
    An unsigned signature field

    An unsigned signature field that can be signed.
    The purpose of the signature field is to indicate that the document should be signed and to 
    define the page and position where the visual appearance of the signature should be placed.
    This is especially useful for forms and contracts that have dedicated spaces for signatures.


    """
    @staticmethod
    def _create_dynamic_type(handle):
        return UnsignedSignatureField._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = UnsignedSignatureField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
