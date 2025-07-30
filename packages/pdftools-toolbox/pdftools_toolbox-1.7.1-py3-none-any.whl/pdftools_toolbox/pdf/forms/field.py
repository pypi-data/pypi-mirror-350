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
import pdftools_toolbox.pdf.forms.field_node

if TYPE_CHECKING:
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.forms.widget import Widget
    from pdftools_toolbox.pdf.forms.widget_list import WidgetList

else:
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Widget = "pdftools_toolbox.pdf.forms.widget.Widget"
    WidgetList = "pdftools_toolbox.pdf.forms.widget_list.WidgetList"


class Field(pdftools_toolbox.pdf.forms.field_node.FieldNode, ABC):
    """
    A form field


    """
    def add_new_widget(self, bounding_box: Rectangle) -> Widget:
        """
        Create a new widget and add to the form field

        This method creates a widget for the form field.
        The widget is automatically added to the field's widgets, but not to any page.
        This method does not work for radio button form fields;
        Use :meth:`pdftools_toolbox.pdf.forms.radio_button.RadioButton.add_new_widget` .



        Args:
            boundingBox (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                The widget's target rectangle on the page



        Returns:
            pdftools_toolbox.pdf.forms.widget.Widget: 
                the newly created form field widget



        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only

            OperationError:
                if the form field is of type :class:`pdftools_toolbox.pdf.forms.radio_button_group.RadioButtonGroup` 


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.pdf.forms.widget import Widget

        if not isinstance(bounding_box, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(bounding_box).__name__}.")

        _lib.PtxPdfForms_Field_AddNewWidget.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfForms_Field_AddNewWidget.restype = c_void_p
        ret_val = _lib.PtxPdfForms_Field_AddNewWidget(self._handle, bounding_box)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Widget._create_dynamic_type(ret_val)



    @property
    def widgets(self) -> WidgetList:
        """
        This form field's widget annotations



        Returns:
            pdftools_toolbox.pdf.forms.widget_list.WidgetList

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.widget_list import WidgetList

        _lib.PtxPdfForms_Field_GetWidgets.argtypes = [c_void_p]
        _lib.PtxPdfForms_Field_GetWidgets.restype = c_void_p
        ret_val = _lib.PtxPdfForms_Field_GetWidgets(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return WidgetList._create_dynamic_type(ret_val)


    @property
    def read_only(self) -> bool:
        """
        Flags this field as read-only



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_Field_GetReadOnly.argtypes = [c_void_p]
        _lib.PtxPdfForms_Field_GetReadOnly.restype = c_bool
        ret_val = _lib.PtxPdfForms_Field_GetReadOnly(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @read_only.setter
    def read_only(self, val: bool) -> None:
        """
        Flags this field as read-only



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_Field_SetReadOnly.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_Field_SetReadOnly.restype = c_bool
        if not _lib.PtxPdfForms_Field_SetReadOnly(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def required(self) -> bool:
        """
        Flags this field as mandatory



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_Field_GetRequired.argtypes = [c_void_p]
        _lib.PtxPdfForms_Field_GetRequired.restype = c_bool
        ret_val = _lib.PtxPdfForms_Field_GetRequired(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @required.setter
    def required(self, val: bool) -> None:
        """
        Flags this field as mandatory



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_Field_SetRequired.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_Field_SetRequired.restype = c_bool
        if not _lib.PtxPdfForms_Field_SetRequired(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def do_not_export(self) -> bool:
        """
        Tells whether this field is exported



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_Field_GetDoNotExport.argtypes = [c_void_p]
        _lib.PtxPdfForms_Field_GetDoNotExport.restype = c_bool
        ret_val = _lib.PtxPdfForms_Field_GetDoNotExport(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @do_not_export.setter
    def do_not_export(self, val: bool) -> None:
        """
        Tells whether this field is exported



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_Field_SetDoNotExport.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_Field_SetDoNotExport.restype = c_bool
        if not _lib.PtxPdfForms_Field_SetDoNotExport(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfForms_Field_GetType.argtypes = [c_void_p]
        _lib.PtxPdfForms_Field_GetType.restype = c_int

        obj_type = _lib.PtxPdfForms_Field_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return Field._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.forms.text_field import TextField 
            return TextField._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.forms.general_text_field import GeneralTextField 
            return GeneralTextField._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.forms.comb_text_field import CombTextField 
            return CombTextField._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.forms.push_button import PushButton 
            return PushButton._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.forms.check_box import CheckBox 
            return CheckBox._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.forms.radio_button_group import RadioButtonGroup 
            return RadioButtonGroup._from_handle(handle)
        elif obj_type == 7:
            from pdftools_toolbox.pdf.forms.choice_field import ChoiceField 
            return ChoiceField._from_handle(handle)
        elif obj_type == 8:
            from pdftools_toolbox.pdf.forms.list_box import ListBox 
            return ListBox._from_handle(handle)
        elif obj_type == 9:
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
        instance = Field.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
