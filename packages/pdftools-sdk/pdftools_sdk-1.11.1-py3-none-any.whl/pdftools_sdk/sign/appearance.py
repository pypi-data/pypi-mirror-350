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
    from pdftools_sdk.geometry.units.size import Size
    from pdftools_sdk.sign.custom_text_variable_map import CustomTextVariableMap

else:
    Size = "pdftools_sdk.geometry.units.size.Size"
    CustomTextVariableMap = "pdftools_sdk.sign.custom_text_variable_map.CustomTextVariableMap"


class Appearance(_NativeObject):
    """
    The visual appearance of signatures

     
    A signature may have a visual appearance on a page of the document.
    The visual appearance is optional and has no effect on the validity of the signature.
    Because of this and because a visual appearance may cover important content of the page,
    it is recommended to create invisible signatures by default.
     
    Typically, a visual appearance is created for forms with a dedicated area reserved for the appearance.
    Other transaction documents, e.g. invoices, correspondence, or bank statements, are usually signed without a visual appearance.
     
    The appearance can be positioned on a page using :attr:`pdftools_sdk.sign.appearance.Appearance.page_number` , :attr:`pdftools_sdk.sign.appearance.Appearance.top` , :attr:`pdftools_sdk.sign.appearance.Appearance.right` ,
    :attr:`pdftools_sdk.sign.appearance.Appearance.bottom` , and :attr:`pdftools_sdk.sign.appearance.Appearance.left` .
    It is recommended to set either :attr:`pdftools_sdk.sign.appearance.Appearance.top`  or :attr:`pdftools_sdk.sign.appearance.Appearance.bottom`  and :attr:`pdftools_sdk.sign.appearance.Appearance.right`  or :attr:`pdftools_sdk.sign.appearance.Appearance.left` .
    If all are `None`, the default is to position the appearance in the lower right corner with `12 pt`
    (`1/6 inch` or `4.2 mm`) distance to the bottom and right edge of the page,
    i.e. `Bottom = 12` and `Right = 12`.


    """
    @staticmethod
    def create_from_json(stream: io.IOBase) -> Appearance:
        """
        Create an appearance with the content loaded from a JSON file

        The format of the JSON file is described in the user manual.



        Args:
            stream (io.IOBase): 
                The JSON file defining the content



        Returns:
            pdftools_sdk.sign.appearance.Appearance: 


        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                The file is not a valid JSON file.

            pdftools_sdk.not_found_error.NotFoundError:
                An image or font referenced in the JSON was not found.

            pdftools_sdk.generic_error.GenericError:
                The JSON file is not a valid appearance content specification.

            pdftools_sdk.processing_error.ProcessingError:
                Could not process content of the JSON.


        """
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")

        _lib.PdfToolsSign_Appearance_CreateFromJson.argtypes = [POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsSign_Appearance_CreateFromJson.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Appearance_CreateFromJson(_StreamDescriptor(stream))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Appearance._create_dynamic_type(ret_val)


    @staticmethod
    def create_from_xml(stream: io.IOBase) -> Appearance:
        """
        Create an appearance with the content loaded from an XML file

        The format of the XML file is described in the user manual.



        Args:
            stream (io.IOBase): 
                The XML file defining the content



        Returns:
            pdftools_sdk.sign.appearance.Appearance: 


        Raises:
            pdftools_sdk.corrupt_error.CorruptError:
                The file is not a valid XML file.

            pdftools_sdk.not_found_error.NotFoundError:
                An image or font referenced in the XML was not found.

            pdftools_sdk.generic_error.GenericError:
                The XML file is not a valid appearance content specification.

            pdftools_sdk.processing_error.ProcessingError:
                Could not process content of the XML.


        """
        if not isinstance(stream, io.IOBase):
            raise TypeError(f"Expected type {io.IOBase.__name__}, but got {type(stream).__name__}.")

        _lib.PdfToolsSign_Appearance_CreateFromXml.argtypes = [POINTER(pdftools_sdk.internal.streams._StreamDescriptor)]
        _lib.PdfToolsSign_Appearance_CreateFromXml.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Appearance_CreateFromXml(_StreamDescriptor(stream))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Appearance._create_dynamic_type(ret_val)


    @staticmethod
    def create_field_bounding_box(size: Size) -> Appearance:
        """
        Create the bounding box for an unsigned signature field

        Unsigned signature fields can define a rectangle on a page.
        When the field is signed, the signer creates a visual appearance within that rectangle.



        Args:
            size (pdftools_sdk.geometry.units.size.Size): 
                The size of the rectangle



        Returns:
            pdftools_sdk.sign.appearance.Appearance: 


        """
        from pdftools_sdk.geometry.units.size import Size

        if not isinstance(size, Size):
            raise TypeError(f"Expected type {Size.__name__}, but got {type(size).__name__}.")

        _lib.PdfToolsSign_Appearance_CreateFieldBoundingBox.argtypes = [POINTER(Size)]
        _lib.PdfToolsSign_Appearance_CreateFieldBoundingBox.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Appearance_CreateFieldBoundingBox(size)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Appearance._create_dynamic_type(ret_val)



    @property
    def page_number(self) -> Optional[int]:
        """
        The number of the page where the appearance is positioned

         
        Page number must be in the range from `1` to :attr:`pdftools_sdk.pdf.document.Document.page_count` .
         
        If `None`, the appearance is positioned on the last page.
         
        Default is `None`



        Returns:
            Optional[int]

        """
        _lib.PdfToolsSign_Appearance_GetPageNumber.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsSign_Appearance_GetPageNumber.restype = c_bool
        ret_val = c_int()
        if not _lib.PdfToolsSign_Appearance_GetPageNumber(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @page_number.setter
    def page_number(self, val: Optional[int]) -> None:
        """
        The number of the page where the appearance is positioned

         
        Page number must be in the range from `1` to :attr:`pdftools_sdk.pdf.document.Document.page_count` .
         
        If `None`, the appearance is positioned on the last page.
         
        Default is `None`



        Args:
            val (Optional[int]):
                property value

        """
        if val is not None and not isinstance(val, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_Appearance_SetPageNumber.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PdfToolsSign_Appearance_SetPageNumber.restype = c_bool
        if not _lib.PdfToolsSign_Appearance_SetPageNumber(self._handle, byref(c_int(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def top(self) -> Optional[float]:
        """
        Distance to top of page

         
        This property specifies the distance between appearance's top edge and the top of the page.
         
        If `None`, the distance to the top is unspecified.
         
        Default is `None`



        Returns:
            Optional[float]

        """
        _lib.PdfToolsSign_Appearance_GetTop.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_GetTop.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsSign_Appearance_GetTop(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @top.setter
    def top(self, val: Optional[float]) -> None:
        """
        Distance to top of page

         
        This property specifies the distance between appearance's top edge and the top of the page.
         
        If `None`, the distance to the top is unspecified.
         
        Default is `None`



        Args:
            val (Optional[float]):
                property value

        Raises:
            ValueError:
                If the given value is negative


        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_Appearance_SetTop.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_SetTop.restype = c_bool
        if not _lib.PdfToolsSign_Appearance_SetTop(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def right(self) -> Optional[float]:
        """
        Distance to right of page

         
        This property specifies the distance between appearance's right edge and the right of the page.
         
        If `None`, the distance to the right is unspecified.
         
        Default is `None`



        Returns:
            Optional[float]

        """
        _lib.PdfToolsSign_Appearance_GetRight.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_GetRight.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsSign_Appearance_GetRight(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @right.setter
    def right(self, val: Optional[float]) -> None:
        """
        Distance to right of page

         
        This property specifies the distance between appearance's right edge and the right of the page.
         
        If `None`, the distance to the right is unspecified.
         
        Default is `None`



        Args:
            val (Optional[float]):
                property value

        Raises:
            ValueError:
                If the given value is negative


        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_Appearance_SetRight.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_SetRight.restype = c_bool
        if not _lib.PdfToolsSign_Appearance_SetRight(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def bottom(self) -> Optional[float]:
        """
        Distance to bottom of page

         
        This property specifies the distance between appearance's bottom edge and the bottom of the page.
         
        If `None`, the distance to the bottom is unspecified.
         
        Default is `None`



        Returns:
            Optional[float]

        """
        _lib.PdfToolsSign_Appearance_GetBottom.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_GetBottom.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsSign_Appearance_GetBottom(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @bottom.setter
    def bottom(self, val: Optional[float]) -> None:
        """
        Distance to bottom of page

         
        This property specifies the distance between appearance's bottom edge and the bottom of the page.
         
        If `None`, the distance to the bottom is unspecified.
         
        Default is `None`



        Args:
            val (Optional[float]):
                property value

        Raises:
            ValueError:
                If the given value is negative


        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_Appearance_SetBottom.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_SetBottom.restype = c_bool
        if not _lib.PdfToolsSign_Appearance_SetBottom(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def left(self) -> Optional[float]:
        """
        Distance to left of page

         
        This property specifies the distance between appearance's left edge and the left of the page.
         
        If `None`, the distance to the left is unspecified.
         
        Default is `None`



        Returns:
            Optional[float]

        """
        _lib.PdfToolsSign_Appearance_GetLeft.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_GetLeft.restype = c_bool
        ret_val = c_double()
        if not _lib.PdfToolsSign_Appearance_GetLeft(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @left.setter
    def left(self, val: Optional[float]) -> None:
        """
        Distance to left of page

         
        This property specifies the distance between appearance's left edge and the left of the page.
         
        If `None`, the distance to the left is unspecified.
         
        Default is `None`



        Args:
            val (Optional[float]):
                property value

        Raises:
            ValueError:
                If the given value is negative


        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsSign_Appearance_SetLeft.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PdfToolsSign_Appearance_SetLeft.restype = c_bool
        if not _lib.PdfToolsSign_Appearance_SetLeft(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def custom_text_variables(self) -> CustomTextVariableMap:
        """
        Maps the name of a custom text variable to its value.
        These variables can parametrize the content of the text element in the appearance configuration XML and Json files.
        They are used by setting "[custom:‹key›]".



        Returns:
            pdftools_sdk.sign.custom_text_variable_map.CustomTextVariableMap

        """
        from pdftools_sdk.sign.custom_text_variable_map import CustomTextVariableMap

        _lib.PdfToolsSign_Appearance_GetCustomTextVariables.argtypes = [c_void_p]
        _lib.PdfToolsSign_Appearance_GetCustomTextVariables.restype = c_void_p
        ret_val = _lib.PdfToolsSign_Appearance_GetCustomTextVariables(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return CustomTextVariableMap._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return Appearance._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Appearance.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
