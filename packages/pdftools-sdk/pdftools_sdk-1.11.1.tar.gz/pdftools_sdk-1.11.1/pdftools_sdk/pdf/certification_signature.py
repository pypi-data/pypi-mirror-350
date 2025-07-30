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
import pdftools_sdk.pdf.signature

if TYPE_CHECKING:
    from pdftools_sdk.pdf.mdp_permissions import MdpPermissions

else:
    MdpPermissions = "pdftools_sdk.pdf.mdp_permissions.MdpPermissions"


class CertificationSignature(pdftools_sdk.pdf.signature.Signature):
    """
    A document certification (MDP) signature that certifies the document

    These signatures are also called Document Modification Detection and Prevention (MDP) signatures.
    This type of signature enables the detection of rejected changes specified by the author.


    """
    @property
    def permissions(self) -> MdpPermissions:
        """
        The access permissions granted for this document

        Note that for encrypted PDF documents, the restrictions defined by this `CertificationSignature` are in addition
        to the document's :attr:`pdftools_sdk.pdf.document.Document.permissions` .



        Returns:
            pdftools_sdk.pdf.mdp_permissions.MdpPermissions

        Raises:
            StateError:
                If the object has already been closed


        """
        from pdftools_sdk.pdf.mdp_permissions import MdpPermissions

        _lib.PdfToolsPdf_CertificationSignature_GetPermissions.argtypes = [c_void_p]
        _lib.PdfToolsPdf_CertificationSignature_GetPermissions.restype = c_int
        ret_val = _lib.PdfToolsPdf_CertificationSignature_GetPermissions(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return MdpPermissions(ret_val)




    @staticmethod
    def _create_dynamic_type(handle):
        return CertificationSignature._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = CertificationSignature.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
