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
    from pdftools_sdk.pdf.permission import Permission

else:
    Permission = "pdftools_sdk.pdf.permission.Permission"


class Encryption(_NativeObject):
    """
    The parameters to encrypt PDF documents

     
    PDF document can be encrypted to protect content from unauthorized access.
    The encryption process applies encryption to all streams (e.g. images) and strings, but not to other items in the PDF document.
    This means the structure of the PDF document is accessible, but the content of its pages is encrypted.
     
    The standard security handler allows access permissions and up to two passwords to be specified for a document:
    A user password (see :attr:`pdftools_sdk.pdf.encryption.Encryption.user_password` ) and an owner password (see :attr:`pdftools_sdk.pdf.encryption.Encryption.owner_password` ).
     
    The following list shows the four possible combinations of passwords and how an application processing such a PDF document behaves:
     
     
    - *No user password, no owner password (no encryption):*
      Everyone can read, i.e. no password required to open the document.
      Everyone can change security settings.
    - *No user password, owner password:*
      Everyone can read, i.e. no password required to open the document.
      Access permissions are restricted (unless the owner password is provided).
      Owner password required to change security settings.
    - *User password, no owner password:*
      User password required to read.
      All access permissions are granted.
    - *User password, owner password:*
      User or owner password required to read.
      Access permissions are restricted (unless the owner password is provided).
      Owner password required to change security settings.
     
     
    Since encryption is not allowed by the PDF/A ISO standards, PDF/A documents must not be encrypted.


    """
    def __init__(self, user_password: Optional[str], owner_password: Optional[str], permissions: Permission):
        """

        Args:
            userPassword (Optional[str]): 
                Set the user password of the output document (see :attr:`pdftools_sdk.pdf.encryption.Encryption.user_password` ).
                If `None` or empty, no user password is set.

            ownerPassword (Optional[str]): 
                Set the owner password and permissions of the output document (see :attr:`pdftools_sdk.pdf.encryption.Encryption.owner_password` ).
                If `None` or empty, no owner password is set.

            permissions (pdftools_sdk.pdf.permission.Permission): 
                The permissions to be set on the PDF document.
                If no owner password is set, the permissions must not be restricted, i.e. the `permissions` must be `All`.



        """
        from pdftools_sdk.pdf.permission import Permission

        if user_password is not None and not isinstance(user_password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(user_password).__name__}.")
        if owner_password is not None and not isinstance(owner_password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(owner_password).__name__}.")
        if not isinstance(permissions, Permission):
            raise TypeError(f"Expected type {Permission.__name__}, but got {type(permissions).__name__}.")

        _lib.PdfToolsPdf_Encryption_NewW.argtypes = [c_wchar_p, c_wchar_p, c_int]
        _lib.PdfToolsPdf_Encryption_NewW.restype = c_void_p
        ret_val = _lib.PdfToolsPdf_Encryption_NewW(_string_to_utf16(user_password), _string_to_utf16(owner_password), c_int(permissions.value))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def set_permissions(self, owner_password: str, permissions: Permission) -> None:
        """
        Set the owner password and access permissions.

        Only the given permissions are granted when opening the document.
        To the owner of the document, all permissions are granted.
        For this, the document must be opened by specifying the owner password (see :attr:`pdftools_sdk.pdf.encryption.Encryption.owner_password` ).



        Args:
            ownerPassword (str): 
                The owner password to be set on the PDF document (see :attr:`pdftools_sdk.pdf.encryption.Encryption.owner_password` ).

            permissions (pdftools_sdk.pdf.permission.Permission): 
                The permissions to be set on the PDF document.




        Raises:
            ValueError:
                If restricted `permissions` (i.e. not `All`) are specified without `ownerPassword`.


        """
        from pdftools_sdk.pdf.permission import Permission

        if not isinstance(owner_password, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(owner_password).__name__}.")
        if not isinstance(permissions, Permission):
            raise TypeError(f"Expected type {Permission.__name__}, but got {type(permissions).__name__}.")

        _lib.PdfToolsPdf_Encryption_SetPermissionsW.argtypes = [c_void_p, c_wchar_p, c_int]
        _lib.PdfToolsPdf_Encryption_SetPermissionsW.restype = c_bool
        if not _lib.PdfToolsPdf_Encryption_SetPermissionsW(self._handle, _string_to_utf16(owner_password), c_int(permissions.value)):
            _NativeBase._throw_last_error(False)



    @property
    def user_password(self) -> Optional[str]:
        """
        The user password

         
        This password protects the document against unauthorized opening and reading.
         
        If a PDF document is protected by a user password, it cannot be opened without a password.
        The user or, if set, owner password must be provided to open and read the document.
         
        If a document is not protected by a user password, it can be opened by without a password, even if an owner password is set.
         
        If the password contains characters that are not in the Windows ANSI encoding (Windows Code Page 1252),
        the output document's compliance level is automatically upgraded to PDF version 1.7.
        This is because older PDF versions do not support Unicode passwords.



        Returns:
            Optional[str]

        """
        _lib.PdfToolsPdf_Encryption_GetUserPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Encryption_GetUserPasswordW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Encryption_GetUserPasswordW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Encryption_GetUserPasswordW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @user_password.setter
    def user_password(self, val: Optional[str]) -> None:
        """
        The user password

         
        This password protects the document against unauthorized opening and reading.
         
        If a PDF document is protected by a user password, it cannot be opened without a password.
        The user or, if set, owner password must be provided to open and read the document.
         
        If a document is not protected by a user password, it can be opened by without a password, even if an owner password is set.
         
        If the password contains characters that are not in the Windows ANSI encoding (Windows Code Page 1252),
        the output document's compliance level is automatically upgraded to PDF version 1.7.
        This is because older PDF versions do not support Unicode passwords.



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PdfToolsPdf_Encryption_SetUserPasswordW.argtypes = [c_void_p, c_wchar_p]
        _lib.PdfToolsPdf_Encryption_SetUserPasswordW.restype = c_bool
        if not _lib.PdfToolsPdf_Encryption_SetUserPasswordW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def owner_password(self) -> Optional[str]:
        """
        The owner password

         
        This password is sometimes also referred to as the author’s password.
        This password grants full access to the document.
        Not only can the document be opened and read, it also allows the document's security settings, access permissions, and passwords to be changed.
         
        If the password contains characters that are not in the Windows ANSI encoding (Windows Code Page 1252),
        the output document's compliance level is automatically upgraded to PDF version 1.7.
        This is because older PDF versions do not support Unicode passwords.



        Returns:
            Optional[str]

        """
        _lib.PdfToolsPdf_Encryption_GetOwnerPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PdfToolsPdf_Encryption_GetOwnerPasswordW.restype = c_size_t
        ret_val_size = _lib.PdfToolsPdf_Encryption_GetOwnerPasswordW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PdfToolsPdf_Encryption_GetOwnerPasswordW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def permissions(self) -> Permission:
        """
        The access permissions granted when opening the document

         
        The operations granted in a PDF document are controlled using permission flags.
        In order to set permission flags, the PDF document must be encrypted and have an owner password.
         
        The restricted permissions apply whenever the document is opened with a password other than the owner password.
        The owner password is required to initially set or later change the permission flags.
         
        When opening an encrypted document, the access permissions for the document can be read using :attr:`pdftools_sdk.pdf.document.Document.permissions` .
        Note that the permissions might be different from the "Document Restrictions Summary" displayed in Adobe Acrobat.



        Returns:
            pdftools_sdk.pdf.permission.Permission

        """
        from pdftools_sdk.pdf.permission import Permission

        _lib.PdfToolsPdf_Encryption_GetPermissions.argtypes = [c_void_p]
        _lib.PdfToolsPdf_Encryption_GetPermissions.restype = c_int
        ret_val = _lib.PdfToolsPdf_Encryption_GetPermissions(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Permission(ret_val)




    @staticmethod
    def _create_dynamic_type(handle):
        return Encryption._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Encryption.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
