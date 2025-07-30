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

else:
    Document = "pdftools_toolbox.pdf.document.Document"


class CheckBox(pdftools_toolbox.pdf.forms.field.Field):
    """
    A check box field


    """
    @staticmethod
    def create(target_document: Document) -> CheckBox:
        """
        Create a check box form field

        The returned form field object is not yet used, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated



        Returns:
            pdftools_toolbox.pdf.forms.check_box.CheckBox: 
                the newly created check box field



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

        _lib.PtxPdfForms_CheckBox_Create.argtypes = [c_void_p]
        _lib.PtxPdfForms_CheckBox_Create.restype = c_void_p
        ret_val = _lib.PtxPdfForms_CheckBox_Create(target_document._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return CheckBox._create_dynamic_type(ret_val)



    @property
    def checked_export_name(self) -> Optional[str]:
        """
        The name of the checked ('on') state used when exporting



        Returns:
            Optional[str]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_CheckBox_GetCheckedExportNameW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_CheckBox_GetCheckedExportNameW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_CheckBox_GetCheckedExportNameW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error()
            return None
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_CheckBox_GetCheckedExportNameW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def checked(self) -> bool:
        """
        The state of the check box



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_CheckBox_GetChecked.argtypes = [c_void_p]
        _lib.PtxPdfForms_CheckBox_GetChecked.restype = c_bool
        ret_val = _lib.PtxPdfForms_CheckBox_GetChecked(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @checked.setter
    def checked(self, val: bool) -> None:
        """
        The state of the check box



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field is marked as read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_CheckBox_SetChecked.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_CheckBox_SetChecked.restype = c_bool
        if not _lib.PtxPdfForms_CheckBox_SetChecked(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return CheckBox._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = CheckBox.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
