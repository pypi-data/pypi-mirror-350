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
import pdftools_toolbox.pdf.forms.choice_field

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.forms.choice_item import ChoiceItem

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    ChoiceItem = "pdftools_toolbox.pdf.forms.choice_item.ChoiceItem"


class ComboBox(pdftools_toolbox.pdf.forms.choice_field.ChoiceField):
    """
    A combo box field


    """
    @staticmethod
    def create(target_document: Document) -> ComboBox:
        """
        Create a combo box form field

        The returned form field object is not yet used, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated



        Returns:
            pdftools_toolbox.pdf.forms.combo_box.ComboBox: 
                the newly created combo box field



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

        _lib.PtxPdfForms_ComboBox_Create.argtypes = [c_void_p]
        _lib.PtxPdfForms_ComboBox_Create.restype = c_void_p
        ret_val = _lib.PtxPdfForms_ComboBox_Create(target_document._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ComboBox._create_dynamic_type(ret_val)



    @property
    def can_edit(self) -> bool:
        """
        Has an editable item



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_ComboBox_GetCanEdit.argtypes = [c_void_p]
        _lib.PtxPdfForms_ComboBox_GetCanEdit.restype = c_bool
        ret_val = _lib.PtxPdfForms_ComboBox_GetCanEdit(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @can_edit.setter
    def can_edit(self, val: bool) -> None:
        """
        Has an editable item



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
        _lib.PtxPdfForms_ComboBox_SetCanEdit.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_ComboBox_SetCanEdit.restype = c_bool
        if not _lib.PtxPdfForms_ComboBox_SetCanEdit(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def chosen_item(self) -> Optional[ChoiceItem]:
        """
        The selected combo box item

        If this property is `None` then the :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.editable_item_name`  is the selected value.
        Setting this property automatically sets :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.editable_item_name`  to `None`.



        Returns:
            Optional[pdftools_toolbox.pdf.forms.choice_item.ChoiceItem]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.choice_item import ChoiceItem

        _lib.PtxPdfForms_ComboBox_GetChosenItem.argtypes = [c_void_p]
        _lib.PtxPdfForms_ComboBox_GetChosenItem.restype = c_void_p
        ret_val = _lib.PtxPdfForms_ComboBox_GetChosenItem(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return ChoiceItem._create_dynamic_type(ret_val)


    @chosen_item.setter
    def chosen_item(self, val: Optional[ChoiceItem]) -> None:
        """
        The selected combo box item

        If this property is `None` then the :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.editable_item_name`  is the selected value.
        Setting this property automatically sets :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.editable_item_name`  to `None`.



        Args:
            val (Optional[pdftools_toolbox.pdf.forms.choice_item.ChoiceItem]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the provided choice item object does not belong to the combo box field

            StateError:
                if the form field is marked as read-only

            StateError:
                if the form field has widgets


        """
        from pdftools_toolbox.pdf.forms.choice_item import ChoiceItem

        if val is not None and not isinstance(val, ChoiceItem):
            raise TypeError(f"Expected type {ChoiceItem.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_ComboBox_SetChosenItem.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfForms_ComboBox_SetChosenItem.restype = c_bool
        if not _lib.PtxPdfForms_ComboBox_SetChosenItem(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def editable_item_name(self) -> Optional[str]:
        """
        The name of the editable item

        This property is `None` if any of the combo box items is selected, i.e., if :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.chosen_item`  is not `None`.
        Setting this property automatically sets :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.chosen_item`  to `None`.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_ComboBox_GetEditableItemNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_ComboBox_GetEditableItemNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_ComboBox_GetEditableItemNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_ComboBox_GetEditableItemNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @editable_item_name.setter
    def editable_item_name(self, val: Optional[str]) -> None:
        """
        The name of the editable item

        This property is `None` if any of the combo box items is selected, i.e., if :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.chosen_item`  is not `None`.
        Setting this property automatically sets :attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.chosen_item`  to `None`.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field has no editable item (:attr:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.can_edit`  property is `False`)

            StateError:
                if the form field is marked as read-only

            StateError:
                if the form field has widgets


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_ComboBox_SetEditableItemNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_ComboBox_SetEditableItemNameW.restype = c_bool
        if not _lib.PtxPdfForms_ComboBox_SetEditableItemNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def font_size(self) -> float:
        """
        The font size

        If 0.0 is set, then the font size is chosen automatically by the PDF processor.



        Returns:
            float

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_ComboBox_GetFontSize.argtypes = [c_void_p]
        _lib.PtxPdfForms_ComboBox_GetFontSize.restype = c_double
        ret_val = _lib.PtxPdfForms_ComboBox_GetFontSize(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @font_size.setter
    def font_size(self, val: float) -> None:
        """
        The font size

        If 0.0 is set, then the font size is chosen automatically by the PDF processor.



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the given value is smaller than *0.0*


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_ComboBox_SetFontSize.argtypes = [c_void_p, c_double]
        _lib.PtxPdfForms_ComboBox_SetFontSize.restype = c_bool
        if not _lib.PtxPdfForms_ComboBox_SetFontSize(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ComboBox._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ComboBox.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
