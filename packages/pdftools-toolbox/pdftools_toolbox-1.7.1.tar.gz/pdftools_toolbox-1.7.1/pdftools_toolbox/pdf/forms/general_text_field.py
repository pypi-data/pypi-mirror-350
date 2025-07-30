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


class GeneralTextField(pdftools_toolbox.pdf.forms.text_field.TextField):
    """
    A general text field


    """
    @staticmethod
    def create(target_document: Document) -> GeneralTextField:
        """
        Create a general text form field

        The returned form field object is not yet used, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated



        Returns:
            pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField: 
                the newly created general text field



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

        _lib.PtxPdfForms_GeneralTextField_Create.argtypes = [c_void_p]
        _lib.PtxPdfForms_GeneralTextField_Create.restype = c_void_p
        ret_val = _lib.PtxPdfForms_GeneralTextField_Create(target_document._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return GeneralTextField._create_dynamic_type(ret_val)



    @property
    def max_length(self) -> Optional[int]:
        """
        The maximal text length

        When setting this property to a non-null value, the length of this field's text is truncated.



        Returns:
            Optional[int]

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_GeneralTextField_GetMaxLength.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PtxPdfForms_GeneralTextField_GetMaxLength.restype = c_bool
        ret_val = c_int()
        if not _lib.PtxPdfForms_GeneralTextField_GetMaxLength(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error()
            return None
        return ret_val.value



    @max_length.setter
    def max_length(self, val: Optional[int]) -> None:
        """
        The maximal text length

        When setting this property to a non-null value, the length of this field's text is truncated.



        Args:
            val (Optional[int]):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field has widgets

            ValueError:
                if the given value is not `None` and is smaller than *0*


        """
        if val is not None and not isinstance(val, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfForms_GeneralTextField_SetMaxLength.argtypes = [c_void_p, POINTER(c_int)]
        _lib.PtxPdfForms_GeneralTextField_SetMaxLength.restype = c_bool
        if not _lib.PtxPdfForms_GeneralTextField_SetMaxLength(self._handle, byref(c_int(val)) if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def multiline(self) -> bool:
        """
        Flags this text field as multi-line



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_GeneralTextField_GetMultiline.argtypes = [c_void_p]
        _lib.PtxPdfForms_GeneralTextField_GetMultiline.restype = c_bool
        ret_val = _lib.PtxPdfForms_GeneralTextField_GetMultiline(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @multiline.setter
    def multiline(self, val: bool) -> None:
        """
        Flags this text field as multi-line



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field has widgets


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_GeneralTextField_SetMultiline.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_GeneralTextField_SetMultiline.restype = c_bool
        if not _lib.PtxPdfForms_GeneralTextField_SetMultiline(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def password(self) -> bool:
        """
        Flags this text field as a password entry field



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_GeneralTextField_GetPassword.argtypes = [c_void_p]
        _lib.PtxPdfForms_GeneralTextField_GetPassword.restype = c_bool
        ret_val = _lib.PtxPdfForms_GeneralTextField_GetPassword(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @password.setter
    def password(self, val: bool) -> None:
        """
        Flags this text field as a password entry field



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            StateError:
                if the form field has widgets


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfForms_GeneralTextField_SetPassword.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_GeneralTextField_SetPassword.restype = c_bool
        if not _lib.PtxPdfForms_GeneralTextField_SetPassword(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def do_not_spell_check(self) -> bool:
        """
        Flags this text field for prevention from spell checking



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_GeneralTextField_GetDoNotSpellCheck.argtypes = [c_void_p]
        _lib.PtxPdfForms_GeneralTextField_GetDoNotSpellCheck.restype = c_bool
        ret_val = _lib.PtxPdfForms_GeneralTextField_GetDoNotSpellCheck(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @do_not_spell_check.setter
    def do_not_spell_check(self, val: bool) -> None:
        """
        Flags this text field for prevention from spell checking



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
        _lib.PtxPdfForms_GeneralTextField_SetDoNotSpellCheck.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_GeneralTextField_SetDoNotSpellCheck.restype = c_bool
        if not _lib.PtxPdfForms_GeneralTextField_SetDoNotSpellCheck(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def do_not_scroll(self) -> bool:
        """
        Flags this text field non scrollable



        Returns:
            bool

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfForms_GeneralTextField_GetDoNotScroll.argtypes = [c_void_p]
        _lib.PtxPdfForms_GeneralTextField_GetDoNotScroll.restype = c_bool
        ret_val = _lib.PtxPdfForms_GeneralTextField_GetDoNotScroll(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @do_not_scroll.setter
    def do_not_scroll(self, val: bool) -> None:
        """
        Flags this text field non scrollable



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
        _lib.PtxPdfForms_GeneralTextField_SetDoNotScroll.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfForms_GeneralTextField_SetDoNotScroll.restype = c_bool
        if not _lib.PtxPdfForms_GeneralTextField_SetDoNotScroll(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return GeneralTextField._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = GeneralTextField.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
