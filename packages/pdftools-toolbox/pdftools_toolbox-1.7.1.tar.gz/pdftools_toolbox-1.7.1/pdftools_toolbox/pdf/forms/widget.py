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

else:
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"


class Widget(_NativeObject):
    """
    A form field widget


    """
    @property
    def bounding_box(self) -> Rectangle:
        """
        The location on the page



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfForms_Widget_GetBoundingBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfForms_Widget_GetBoundingBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfForms_Widget_GetBoundingBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def hidden(self) -> bool:
        """
        The widget's visibility

        If `True` then the widget is present, but is invisible and not available for user interaction.
        Depending on the :attr:`pdftools_toolbox.pdf.forms.widget.Widget.no_print`  property it will, however, still be visible when printing.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_Widget_GetHidden.argtypes = [c_void_p]
        _lib.PtxPdfForms_Widget_GetHidden.restype = c_bool
        ret_val = _lib.PtxPdfForms_Widget_GetHidden(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @hidden.setter
    def hidden(self, val: bool) -> None:
        """
        The widget's visibility

        If `True` then the widget is present, but is invisible and not available for user interaction.
        Depending on the :attr:`pdftools_toolbox.pdf.forms.widget.Widget.no_print`  property it will, however, still be visible when printing.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_Widget_SetHidden.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_Widget_SetHidden.restype = c_bool
        if not _lib.PtxPdfForms_Widget_SetHidden(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def locked(self) -> bool:
        """
        Whether the widget can be modified

        This does not restrict modification of the widget's content.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_Widget_GetLocked.argtypes = [c_void_p]
        _lib.PtxPdfForms_Widget_GetLocked.restype = c_bool
        ret_val = _lib.PtxPdfForms_Widget_GetLocked(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @locked.setter
    def locked(self, val: bool) -> None:
        """
        Whether the widget can be modified

        This does not restrict modification of the widget's content.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_Widget_SetLocked.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_Widget_SetLocked.restype = c_bool
        if not _lib.PtxPdfForms_Widget_SetLocked(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def no_print(self) -> bool:
        """
        The widget's visibility when printing

        If `True` then the widget is not present in a print output of the document.



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_Widget_GetNoPrint.argtypes = [c_void_p]
        _lib.PtxPdfForms_Widget_GetNoPrint.restype = c_bool
        ret_val = _lib.PtxPdfForms_Widget_GetNoPrint(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        return Widget._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Widget.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
