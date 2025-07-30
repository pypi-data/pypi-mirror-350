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

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document

else:
    Document = "pdftools_toolbox.pdf.document.Document"


class FieldNode(_NativeObject, ABC):
    """
    Base class for form fields and sub forms


    """
    @staticmethod
    def copy(target_document: Document, field_node: FieldNode) -> FieldNode:
        """
        Copy a form field node

        Copy a form field node object from an input document to the given `targetDocument`.
        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            fieldNode (pdftools_toolbox.pdf.forms.field_node.FieldNode): 
                a form field of a different document



        Returns:
            pdftools_toolbox.pdf.forms.field_node.FieldNode: 
                the copied form field, associated with the current document



        Raises:
            OSError:
                Error reading from the source document or writing to the target document

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                the `fieldNode` object is not associated with an input document

            ValueError:
                the target document contains form fields that have been implicitly copied by a call to
                :meth:`pdftools_toolbox.pdf.page.Page.copy`  with an argument `options` from `pdftools_toolbox.pdf.page.Page.copy` in which
                :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.form_fields`  was set to :attr:`pdftools_toolbox.pdf.forms.form_field_copy_strategy.FormFieldCopyStrategy.COPY` 

            ValueError:
                the target document contains unsigned signatures that have been implicitly copied by a call to
                :meth:`pdftools_toolbox.pdf.page.Page.copy`  with an argument `options` from `pdftools_toolbox.pdf.page.Page.copy` in which
                :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.unsigned_signatures`  was set to :attr:`pdftools_toolbox.pdf.copy_strategy.CopyStrategy.COPY` .

            ValueError:
                the document associated with the `fieldNode` object has been closed


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(field_node, FieldNode):
            raise TypeError(f"Expected type {FieldNode.__name__}, but got {type(field_node).__name__}.")

        _lib.PtxPdfForms_FieldNode_Copy.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfForms_FieldNode_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfForms_FieldNode_Copy(target_document._handle, field_node._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FieldNode._create_dynamic_type(ret_val)



    @property
    def display_name(self) -> Optional[str]:
        """
        User interface name

        The display name is not directly visible, but a PDF viewer can display this name, e.g., in a tool tip.



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_FieldNode_GetDisplayNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_FieldNode_GetDisplayNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_FieldNode_GetDisplayNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_FieldNode_GetDisplayNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @display_name.setter
    def display_name(self, val: Optional[str]) -> None:
        """
        User interface name

        The display name is not directly visible, but a PDF viewer can display this name, e.g., in a tool tip.



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_FieldNode_SetDisplayNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_FieldNode_SetDisplayNameW.restype = c_bool
        if not _lib.PtxPdfForms_FieldNode_SetDisplayNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def export_name(self) -> Optional[str]:
        """
        The name used when exporting



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_FieldNode_GetExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_FieldNode_GetExportNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_FieldNode_GetExportNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_FieldNode_GetExportNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @export_name.setter
    def export_name(self, val: Optional[str]) -> None:
        """
        The name used when exporting



        Args:
            val (Optional[str]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only


        """
        if val is not None and not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_FieldNode_SetExportNameW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_FieldNode_SetExportNameW.restype = c_bool
        if not _lib.PtxPdfForms_FieldNode_SetExportNameW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfForms_FieldNode_GetType.argtypes = [c_void_p]
        _lib.PtxPdfForms_FieldNode_GetType.restype = c_int

        obj_type = _lib.PtxPdfForms_FieldNode_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return FieldNode._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.forms.sub_form import SubForm 
            return SubForm._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.forms.field import Field 
            return Field._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.forms.text_field import TextField 
            return TextField._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.forms.general_text_field import GeneralTextField 
            return GeneralTextField._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.forms.comb_text_field import CombTextField 
            return CombTextField._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.forms.push_button import PushButton 
            return PushButton._from_handle(handle)
        elif obj_type == 7:
            from pdftools_toolbox.pdf.forms.check_box import CheckBox 
            return CheckBox._from_handle(handle)
        elif obj_type == 8:
            from pdftools_toolbox.pdf.forms.radio_button_group import RadioButtonGroup 
            return RadioButtonGroup._from_handle(handle)
        elif obj_type == 9:
            from pdftools_toolbox.pdf.forms.choice_field import ChoiceField 
            return ChoiceField._from_handle(handle)
        elif obj_type == 10:
            from pdftools_toolbox.pdf.forms.list_box import ListBox 
            return ListBox._from_handle(handle)
        elif obj_type == 11:
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
        instance = FieldNode.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
