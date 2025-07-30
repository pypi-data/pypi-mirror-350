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
    from pdftools_toolbox.pdf.forms.choice_item_list import ChoiceItemList

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    ChoiceItemList = "pdftools_toolbox.pdf.forms.choice_item_list.ChoiceItemList"


class ListBox(pdftools_toolbox.pdf.forms.choice_field.ChoiceField):
    """
    A list box field


    """
    @staticmethod
    def create(target_document: Document) -> ListBox:
        """
        Create a list box form field

        The returned form field object is not yet used, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated



        Returns:
            pdftools_toolbox.pdf.forms.list_box.ListBox: 
                the newly created list box field



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

        _lib.PtxPdfForms_ListBox_Create.argtypes = [c_void_p]
        _lib.PtxPdfForms_ListBox_Create.restype = c_void_p
        ret_val = _lib.PtxPdfForms_ListBox_Create(target_document._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ListBox._create_dynamic_type(ret_val)



    @property
    def allow_multi_select(self) -> bool:
        """
        Allow multiple items to be selected



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_ListBox_GetAllowMultiSelect.argtypes = [c_void_p]
        _lib.PtxPdfForms_ListBox_GetAllowMultiSelect.restype = c_bool
        ret_val = _lib.PtxPdfForms_ListBox_GetAllowMultiSelect(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @allow_multi_select.setter
    def allow_multi_select(self, val: bool) -> None:
        """
        Allow multiple items to be selected



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
        _lib.PtxPdfForms_ListBox_SetAllowMultiSelect.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_ListBox_SetAllowMultiSelect.restype = c_bool
        if not _lib.PtxPdfForms_ListBox_SetAllowMultiSelect(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def chosen_items(self) -> ChoiceItemList:
        """
        The selected choice items

         
        Adding to this list results in an error:
         
        - *IllegalState*
          - if the list has already been closed
          - if the choice field is marked a read-only
          - if this list is not empty and the list box field is not marked as multi-select
          - if the choice field has widgets
        - *UnsupportedOperation* if the document is read-only
        - *IllegalArgument*
          - if the given choice item is `None`
          - if the given choice item has already been closed
          - if the given choice item is already present in this list
          - if the given choice item does not belong to the list box field's choice items
         
         
        Removing items or clearing the list results in an *IllegalState* error if the form field is marked as read-only, or if it has widgets.



        Returns:
            pdftools_toolbox.pdf.forms.choice_item_list.ChoiceItemList

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.forms.choice_item_list import ChoiceItemList

        _lib.PtxPdfForms_ListBox_GetChosenItems.argtypes = [c_void_p]
        _lib.PtxPdfForms_ListBox_GetChosenItems.restype = c_void_p
        ret_val = _lib.PtxPdfForms_ListBox_GetChosenItems(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return ChoiceItemList._create_dynamic_type(ret_val)


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
        _lib.PtxPdfForms_ListBox_GetFontSize.argtypes = [c_void_p]
        _lib.PtxPdfForms_ListBox_GetFontSize.restype = c_double
        ret_val = _lib.PtxPdfForms_ListBox_GetFontSize(self._handle)
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
        _lib.PtxPdfForms_ListBox_SetFontSize.argtypes = [c_void_p, c_double]
        _lib.PtxPdfForms_ListBox_SetFontSize.restype = c_bool
        if not _lib.PtxPdfForms_ListBox_SetFontSize(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return ListBox._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = ListBox.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
