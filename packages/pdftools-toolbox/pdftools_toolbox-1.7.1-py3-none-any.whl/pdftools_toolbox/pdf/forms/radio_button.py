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
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.forms.widget import Widget
    from pdftools_toolbox.pdf.forms.widget_list import WidgetList

else:
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Widget = "pdftools_toolbox.pdf.forms.widget.Widget"
    WidgetList = "pdftools_toolbox.pdf.forms.widget_list.WidgetList"


class RadioButton(_NativeObject):
    """
    A button in a radio button group


    """
    def add_new_widget(self, bounding_box: Rectangle) -> Widget:
        """
        Create radio button widget

        This method creates a widget for the radio button.
        The widget is automatically added to the button's widgets and to the radio button form field's widgets, but not to any page.



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


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.pdf.forms.widget import Widget

        if not isinstance(bounding_box, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(bounding_box).__name__}.")

        _lib.PtxPdfForms_RadioButton_AddNewWidget.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfForms_RadioButton_AddNewWidget.restype = c_void_p
        ret_val = _lib.PtxPdfForms_RadioButton_AddNewWidget(self._handle, bounding_box)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Widget._create_dynamic_type(ret_val)



    @property
    def export_name(self) -> Optional[str]:
        """
        The button's name used when exporting



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_RadioButton_GetExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_RadioButton_GetExportNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_RadioButton_GetExportNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_RadioButton_GetExportNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def widgets(self) -> WidgetList:
        """
        The button's widget annotations



        Returns:
            pdftools_toolbox.pdf.forms.widget_list.WidgetList

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.widget_list import WidgetList

        _lib.PtxPdfForms_RadioButton_GetWidgets.argtypes = [c_void_p]
        _lib.PtxPdfForms_RadioButton_GetWidgets.restype = c_void_p
        ret_val = _lib.PtxPdfForms_RadioButton_GetWidgets(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return WidgetList._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return RadioButton._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = RadioButton.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
