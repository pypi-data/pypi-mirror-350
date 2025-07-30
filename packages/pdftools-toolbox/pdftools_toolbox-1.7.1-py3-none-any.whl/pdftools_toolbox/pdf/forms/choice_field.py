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
from abc import ABC

import pdftools_toolbox.internal
import pdftools_toolbox.pdf.forms.field

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.forms.choice_item import ChoiceItem
    from pdftools_toolbox.pdf.forms.choice_item_list import ChoiceItemList

else:
    ChoiceItem = "pdftools_toolbox.pdf.forms.choice_item.ChoiceItem"
    ChoiceItemList = "pdftools_toolbox.pdf.forms.choice_item_list.ChoiceItemList"


class ChoiceField(pdftools_toolbox.pdf.forms.field.Field, ABC):
    """
    A choice field


    """
    def add_new_item(self, display_name: Optional[str]) -> ChoiceItem:
        """
        Creates a new choice item.
        The item is automatically added to the choice field's :attr:`pdftools_toolbox.pdf.forms.choice_field.ChoiceField.items` .



        Args:
            displayName (Optional[str]): 
                this item's display name



        Returns:
            pdftools_toolbox.pdf.forms.choice_item.ChoiceItem: 
                the newly created choice item



        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the form field has widgets

            OperationError:
                the document is read-only


        """
        from pdftools_toolbox.pdf.forms.choice_item import ChoiceItem

        if display_name is not None and not isinstance(display_name, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(display_name).__name__}.")

        _lib.PtxPdfForms_ChoiceField_AddNewItemW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_ChoiceField_AddNewItemW.restype = c_void_p
        ret_val = _lib.PtxPdfForms_ChoiceField_AddNewItemW(self._handle, _string_to_utf16(display_name))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ChoiceItem._create_dynamic_type(ret_val)



    @property
    def items(self) -> ChoiceItemList:
        """
        The list of choice items

        Adding or removing items or clearing the list is not supported.



        Returns:
            pdftools_toolbox.pdf.forms.choice_item_list.ChoiceItemList

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.choice_item_list import ChoiceItemList

        _lib.PtxPdfForms_ChoiceField_GetItems.argtypes = [c_void_p]
        _lib.PtxPdfForms_ChoiceField_GetItems.restype = c_void_p
        ret_val = _lib.PtxPdfForms_ChoiceField_GetItems(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ChoiceItemList._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfForms_ChoiceField_GetType.argtypes = [c_void_p]
        _lib.PtxPdfForms_ChoiceField_GetType.restype = c_int

        obj_type = _lib.PtxPdfForms_ChoiceField_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return ChoiceField._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.forms.list_box import ListBox 
            return ListBox._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.forms.combo_box import ComboBox 
            return ComboBox._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ChoiceField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
