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
import pdftools_toolbox.pdf.forms.text_field

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document

else:
    Document = "pdftools_toolbox.pdf.document.Document"


class CombTextField(pdftools_toolbox.pdf.forms.text_field.TextField):
    """
    A fixed pitch text field

    In a comb text field, the :attr:`pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField.max_length`  must be defined.
    The glyphs displayed are placed in :attr:`pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField.max_length`  equally spaced cells.


    """
    @staticmethod
    def create(target_document: Document, max_length: int) -> CombTextField:
        """
        Create a comb text form field

        The returned form field object is not yet used, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            maxLength (int): 
                the maximal character length for this field



        Returns:
            pdftools_toolbox.pdf.forms.comb_text_field.CombTextField: 
                the newly created comb text field



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

            ValueError:
                if `maxLength` is smaller than 0


        """
        from pdftools_toolbox.pdf.document import Document

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(max_length, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(max_length).__name__}.")

        _lib.PtxPdfForms_CombTextField_Create.argtypes = [c_void_p, c_int]
        _lib.PtxPdfForms_CombTextField_Create.restype = c_void_p
        ret_val = _lib.PtxPdfForms_CombTextField_Create(target_document._handle, max_length)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return CombTextField._create_dynamic_type(ret_val)



    @property
    def max_length(self) -> int:
        """
        The maximal text length

        When setting this property, the length of this field's text is truncated to the given value.



        Returns:
            int

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_CombTextField_GetMaxLength.argtypes = [c_void_p]
        _lib.PtxPdfForms_CombTextField_GetMaxLength.restype = c_int
        ret_val = _lib.PtxPdfForms_CombTextField_GetMaxLength(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @max_length.setter
    def max_length(self, val: int) -> None:
        """
        The maximal text length

        When setting this property, the length of this field's text is truncated to the given value.



        Args:
            val (int):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field has widgets

            ValueError:
                if the given value is smaller than *0*


        """
        if not isinstance(val, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_CombTextField_SetMaxLength.argtypes = [c_void_p, c_int]
        _lib.PtxPdfForms_CombTextField_SetMaxLength.restype = c_bool
        if not _lib.PtxPdfForms_CombTextField_SetMaxLength(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return CombTextField._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = CombTextField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
