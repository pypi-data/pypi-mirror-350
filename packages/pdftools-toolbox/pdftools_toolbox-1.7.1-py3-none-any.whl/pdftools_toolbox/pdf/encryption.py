from __future__ import annotations
import io
from typing import List, Iterator, Tuple, Optional, Any, TYPE_CHECKING, Callable
from ctypes import *
from datetime import datetime
from numbers import Number
from pdftools_toolbox.internal import _lib
from pdftools_toolbox.internal.utils import _string_to_utf16, _utf16_to_string
from pdftools_toolbox.internal.streams import _StreamDescriptor, _NativeStream
from pdftools_toolbox.internal.native_base import _NativeBase
from pdftools_toolbox.internal.native_object import _NativeObject

import pdftools_toolbox.internal

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.permission import Permission

else:
    Permission = "pdftools_toolbox.pdf.permission.Permission"


class Encryption(_NativeObject):
    """
    The password and permissions that should be applied to a document, when it is 
    created using the :meth:`pdftools_toolbox.pdf.document.Document.create`  or :meth:`pdftools_toolbox.pdf.document.Document.create_with_fdf` 
    methods.
    The encryption algorithm (e.g., MD4, AES) will be the highest level of encryption that is
    supported for the document :attr:`pdftools_toolbox.pdf.document.Document.conformance` .
    Note that encryption is not permitted for any PDF/A level :attr:`pdftools_toolbox.pdf.document.Document.conformance` .


    """
    def __init__(self, user_password: Optional[str], owner_password: Optional[str], permissions: Permission):
        """
        The :attr:`pdftools_toolbox.pdf.encryption.Encryption.user_password`  may be used to open the document with the 
        permissions defined by the :attr:`pdftools_toolbox.pdf.encryption.Encryption.permissions`  parameter.
        The :attr:`pdftools_toolbox.pdf.encryption.Encryption.owner_password`  may be used to open the document with no 
        access restrictions.
        The :attr:`pdftools_toolbox.pdf.encryption.Encryption.permissions`  may be `None` (all permissions), or  
        a concatenation of the allowed :class:`pdftools_toolbox.pdf.permission.Permission`  values.



        Args:
            userPassword (Optional[str]): 
            ownerPassword (Optional[str]): 
            permissions (pdftools_toolbox.pdf.permission.Permission): 


        """
        from pdftools_toolbox.pdf.permission import Permission

        if user_password is not None and not isinstance(user_password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(user_password).__name__}.")
        if owner_password is not None and not isinstance(owner_password, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(owner_password).__name__}.")
        if not isinstance(permissions, Permission):
            raise TypeError(f"Expected type {Permission.__name__}, but got {type(permissions).__name__}.")

        _lib.PtxPdf_Encryption_NewW.argtypes = [c_wchar_p, c_wchar_p, c_int]
        _lib.PtxPdf_Encryption_NewW.restype = c_void_p
        ret_val = _lib.PtxPdf_Encryption_NewW(_string_to_utf16(user_password), _string_to_utf16(owner_password), c_int(permissions.value))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def user_password(self) -> Optional[str]:
        """
        The user password opens the document with the permissions defined 
        by the :attr:`pdftools_toolbox.pdf.encryption.Encryption.permissions`  parameter.



        Returns:
            Optional[str]

        """
        _lib.PtxPdf_Encryption_GetUserPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Encryption_GetUserPasswordW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Encryption_GetUserPasswordW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Encryption_GetUserPasswordW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @user_password.setter
    def user_password(self, val: Optional[str]) -> None:
        """
        The user password opens the document with the permissions defined 
        by the :attr:`pdftools_toolbox.pdf.encryption.Encryption.permissions`  parameter.



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Encryption_SetUserPasswordW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Encryption_SetUserPasswordW.restype = c_bool
        if not _lib.PtxPdf_Encryption_SetUserPasswordW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def owner_password(self) -> Optional[str]:
        """
        The owner password opens the document with no access restrictions.



        Returns:
            Optional[str]

        """
        _lib.PtxPdf_Encryption_GetOwnerPasswordW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdf_Encryption_GetOwnerPasswordW.restype = c_size_t
        ret_val_size = _lib.PtxPdf_Encryption_GetOwnerPasswordW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdf_Encryption_GetOwnerPasswordW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @owner_password.setter
    def owner_password(self, val: Optional[str]) -> None:
        """
        The owner password opens the document with no access restrictions.



        Args:
            val (Optional[str]):
                property value

        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdf_Encryption_SetOwnerPasswordW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdf_Encryption_SetOwnerPasswordW.restype = c_bool
        if not _lib.PtxPdf_Encryption_SetOwnerPasswordW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def permissions(self) -> Permission:
        """
        The permissions that will be granted to a user who opens the document 
        using the :attr:`pdftools_toolbox.pdf.encryption.Encryption.user_password` . 
        The value is either null (all permissions), or a concatenation  
        of the allowed :class:`pdftools_toolbox.pdf.permission.Permission`  values.



        Returns:
            pdftools_toolbox.pdf.permission.Permission

        """
        from pdftools_toolbox.pdf.permission import Permission

        _lib.PtxPdf_Encryption_GetPermissions.argtypes = [c_void_p]
        _lib.PtxPdf_Encryption_GetPermissions.restype = c_int
        ret_val = _lib.PtxPdf_Encryption_GetPermissions(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return Permission(ret_val)



    @permissions.setter
    def permissions(self, val: Permission) -> None:
        """
        The permissions that will be granted to a user who opens the document 
        using the :attr:`pdftools_toolbox.pdf.encryption.Encryption.user_password` . 
        The value is either null (all permissions), or a concatenation  
        of the allowed :class:`pdftools_toolbox.pdf.permission.Permission`  values.



        Args:
            val (pdftools_toolbox.pdf.permission.Permission):
                property value

        """
        from pdftools_toolbox.pdf.permission import Permission

        if not isinstance(val, Permission):
            raise TypeError(f"Expected type {Permission.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdf_Encryption_SetPermissions.argtypes = [c_void_p, c_int]
        _lib.PtxPdf_Encryption_SetPermissions.restype = c_bool
        if not _lib.PtxPdf_Encryption_SetPermissions(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


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
