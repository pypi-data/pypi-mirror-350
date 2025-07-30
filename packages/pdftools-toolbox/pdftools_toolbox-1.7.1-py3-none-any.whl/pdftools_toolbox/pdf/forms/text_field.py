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
    from pdftools_toolbox.geometry.horizontal_alignment import HorizontalAlignment

else:
    HorizontalAlignment = "pdftools_toolbox.geometry.horizontal_alignment.HorizontalAlignment"


class TextField(pdftools_toolbox.pdf.forms.field.Field, ABC):
    """
    A text field


    """
    @property
    def text(self) -> Optional[str]:
        """
        This field's text



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_TextField_GetTextW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_TextField_GetTextW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_TextField_GetTextW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_TextField_GetTextW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @text.setter
    def text(self, val: Optional[str]) -> None:
        """
        This field's text



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                the form field is marked as read-only

            StateError:
                if the form field has widgets

            ValueError:
                the string length of the given value exceeds the text field's :attr:`pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField.max_length` 


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_TextField_SetTextW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_TextField_SetTextW.restype = c_bool
        if not _lib.PtxPdfForms_TextField_SetTextW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def alignment(self) -> HorizontalAlignment:
        """
        The text alignment



        Returns:
            pdftools_toolbox.geometry.horizontal_alignment.HorizontalAlignment

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.geometry.horizontal_alignment import HorizontalAlignment

        _lib.PtxPdfForms_TextField_GetAlignment.argtypes = [c_void_p]
        _lib.PtxPdfForms_TextField_GetAlignment.restype = c_int
        ret_val = _lib.PtxPdfForms_TextField_GetAlignment(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return HorizontalAlignment(ret_val)



    @alignment.setter
    def alignment(self, val: HorizontalAlignment) -> None:
        """
        The text alignment



        Args:
            val (pdftools_toolbox.geometry.horizontal_alignment.HorizontalAlignment):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field has widgets


        """
        from pdftools_toolbox.geometry.horizontal_alignment import HorizontalAlignment

        if not isinstance(val, HorizontalAlignment):
            raise TypeError(f"Expected type {HorizontalAlignment.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_TextField_SetAlignment.argtypes = [c_void_p, c_int]
        _lib.PtxPdfForms_TextField_SetAlignment.restype = c_bool
        if not _lib.PtxPdfForms_TextField_SetAlignment(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def font_size(self) -> Optional[float]:
        """
        The font size

        If `None` then the font size is chosen automatically by the PDF viewer.



        Returns:
            Optional[float]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_TextField_GetFontSize.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PtxPdfForms_TextField_GetFontSize.restype = c_bool
        ret_val = c_double()
        if not _lib.PtxPdfForms_TextField_GetFontSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @font_size.setter
    def font_size(self, val: Optional[float]) -> None:
        """
        The font size

        If `None` then the font size is chosen automatically by the PDF viewer.



        Args:
            val (Optional[float]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field has widgets

            ValueError:
                if the given value is smaller than *0.0*


        """
        if val is not None and not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_TextField_SetFontSize.argtypes = [c_void_p, POINTER(c_double)]
        _lib.PtxPdfForms_TextField_SetFontSize.restype = c_bool
        if not _lib.PtxPdfForms_TextField_SetFontSize(self._handle, byref(c_double(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfForms_TextField_GetType.argtypes = [c_void_p]
        _lib.PtxPdfForms_TextField_GetType.restype = c_int

        obj_type = _lib.PtxPdfForms_TextField_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return TextField._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.forms.general_text_field import GeneralTextField 
            return GeneralTextField._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.forms.comb_text_field import CombTextField 
            return CombTextField._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = TextField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
