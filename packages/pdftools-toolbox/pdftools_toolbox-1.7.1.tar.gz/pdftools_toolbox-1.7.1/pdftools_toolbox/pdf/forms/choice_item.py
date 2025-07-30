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

class ChoiceItem(_NativeObject):
    """
    An item in a list box field or combo box field


    """
    @property
    def display_name(self) -> Optional[str]:
        """
        Displayed name

        This is the name of the item as displayed in a PDF viewer.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_ChoiceItem_GetDisplayNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_ChoiceItem_GetDisplayNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_ChoiceItem_GetDisplayNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_ChoiceItem_GetDisplayNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @display_name.setter
    def display_name(self, val: Optional[str]) -> None:
        """
        Displayed name

        This is the name of the item as displayed in a PDF viewer.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the owning choice field's document is read-only

            StateError:
                if the owning choice field has widgets


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_ChoiceItem_SetDisplayNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_ChoiceItem_SetDisplayNameW.restype = c_bool
        if not _lib.PtxPdfForms_ChoiceItem_SetDisplayNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def export_name(self) -> Optional[str]:
        """
        Export name

        This is the name of the item used when exporting.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_ChoiceItem_GetExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_ChoiceItem_GetExportNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_ChoiceItem_GetExportNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_ChoiceItem_GetExportNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @export_name.setter
    def export_name(self, val: Optional[str]) -> None:
        """
        Export name

        This is the name of the item used when exporting.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the owning choice field's document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_ChoiceItem_SetExportNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_ChoiceItem_SetExportNameW.restype = c_bool
        if not _lib.PtxPdfForms_ChoiceItem_SetExportNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ChoiceItem._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ChoiceItem.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
