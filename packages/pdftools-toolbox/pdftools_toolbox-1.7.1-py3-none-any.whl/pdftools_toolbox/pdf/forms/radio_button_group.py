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
import pdftools_toolbox.pdf.forms.field

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.forms.radio_button import RadioButton
    from pdftools_toolbox.pdf.forms.radio_button_list import RadioButtonList

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    RadioButton = "pdftools_toolbox.pdf.forms.radio_button.RadioButton"
    RadioButtonList = "pdftools_toolbox.pdf.forms.radio_button_list.RadioButtonList"


class RadioButtonGroup(pdftools_toolbox.pdf.forms.field.Field):
    """
    A radio button field


    """
    @staticmethod
    def create(target_document: Document) -> RadioButtonGroup:
        """
        Create a radio button form field

        The returned form field object is not yet used, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated



        Returns:
            pdftools_toolbox.pdf.forms.radio_button_group.RadioButtonGroup: 
                the newly created radio button field



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                the target document contains form fields that have been implicitly copied by a call to
                :meth:`pdftools_toolbox.pdf.page.Page.copy`  with an argument `options` from `pdftools_toolbox.pdf.page.Page.copy` in which
                :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.form_fields`  was set to :attr:`pdftools_toolbox.pdf.forms.form_field_copy_strategy.FormFieldCopyStrategy.COPY` 

            ValueError:
                the target document contains unsigned signatures that have been implicitly copied by a call to
                :meth:`pdftools_toolbox.pdf.page.Page.copy`  with an argument `options` from `pdftools_toolbox.pdf.page.Page.copy` in which
                :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.unsigned_signatures`  was set to :attr:`pdftools_toolbox.pdf.copy_strategy.CopyStrategy.COPY` .


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")

        _lib.PtxPdfForms_RadioButtonGroup_Create.argtypes = [c_void_p]
        _lib.PtxPdfForms_RadioButtonGroup_Create.restype = c_void_p
        ret_val = _lib.PtxPdfForms_RadioButtonGroup_Create(target_document._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return RadioButtonGroup._create_dynamic_type(ret_val)


    def add_new_button(self, export_name: Optional[str]) -> RadioButton:
        """
        Create a radio button

        The created radio button is automatically added to this radio button field's :attr:`pdftools_toolbox.pdf.forms.radio_button_group.RadioButtonGroup.buttons` .



        Args:
            exportName (Optional[str]): 
                the radio button's export name



        Returns:
            pdftools_toolbox.pdf.forms.radio_button.RadioButton: 
                the newly created radio button



        Raises:
            StateError:
                if the document has already been closed

            OperationError:
                if the document is read-only


        """
        from pdftools_toolbox.pdf.forms.radio_button import RadioButton

        if export_name is not None and not isinstance(export_name, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(export_name).__name__}.")

        _lib.PtxPdfForms_RadioButtonGroup_AddNewButtonW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_RadioButtonGroup_AddNewButtonW.restype = c_void_p
        ret_val = _lib.PtxPdfForms_RadioButtonGroup_AddNewButtonW(self._handle, _string_to_utf16(export_name))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return RadioButton._create_dynamic_type(ret_val)



    @property
    def buttons(self) -> RadioButtonList:
        """
        This field's buttons



        Returns:
            pdftools_toolbox.pdf.forms.radio_button_list.RadioButtonList

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.radio_button_list import RadioButtonList

        _lib.PtxPdfForms_RadioButtonGroup_GetButtons.argtypes = [c_void_p]
        _lib.PtxPdfForms_RadioButtonGroup_GetButtons.restype = c_void_p
        ret_val = _lib.PtxPdfForms_RadioButtonGroup_GetButtons(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return RadioButtonList._create_dynamic_type(ret_val)


    @property
    def chosen_button(self) -> Optional[RadioButton]:
        """
        This field's selected button

        if `None` is set, then no button is chosen.



        Returns:
            Optional[pdftools_toolbox.pdf.forms.radio_button.RadioButton]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.radio_button import RadioButton

        _lib.PtxPdfForms_RadioButtonGroup_GetChosenButton.argtypes = [c_void_p]
        _lib.PtxPdfForms_RadioButtonGroup_GetChosenButton.restype = c_void_p
        ret_val = _lib.PtxPdfForms_RadioButtonGroup_GetChosenButton(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return RadioButton._create_dynamic_type(ret_val)


    @chosen_button.setter
    def chosen_button(self, val: Optional[RadioButton]) -> None:
        """
        This field's selected button

        if `None` is set, then no button is chosen.



        Args:
            val (Optional[pdftools_toolbox.pdf.forms.radio_button.RadioButton]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the provided radio button object does not belong to the radio button field

            StateError:
                if the given :class:`pdftools_toolbox.pdf.forms.radio_button.RadioButton`  object is `None` and the radio button group does not support toggling to off

            StateError:
                if the form field is marked as read-only


        """
        from pdftools_toolbox.pdf.forms.radio_button import RadioButton

        if val is not None and not isinstance(val, RadioButton):
            raise TypeError(f"Expected type {RadioButton.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_RadioButtonGroup_SetChosenButton.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfForms_RadioButtonGroup_SetChosenButton.restype = c_bool
        if not _lib.PtxPdfForms_RadioButtonGroup_SetChosenButton(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return RadioButtonGroup._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = RadioButtonGroup.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
