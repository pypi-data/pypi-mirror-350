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
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.size import Size
    from pdftools_toolbox.pdf.page import Page
    from pdftools_toolbox.pdf.page_copy_options import PageCopyOptions
    from pdftools_toolbox.pdf.content.content import Content

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Size = "pdftools_toolbox.geometry.real.size.Size"
    Page = "pdftools_toolbox.pdf.page.Page"
    PageCopyOptions = "pdftools_toolbox.pdf.page_copy_options.PageCopyOptions"
    Content = "pdftools_toolbox.pdf.content.content.Content"


class Group(_NativeObject):
    """
    """
    @staticmethod
    def create(target_document: Document, size: Size) -> Group:
        """
        Create an empty group object.

        The returned group object is not yet used on any page, but it is associated with the given target document.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            size (pdftools_toolbox.geometry.real.size.Size): 
                the size of the group



        Returns:
            pdftools_toolbox.pdf.content.group.Group: 
                the newly created group object



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.size import Size

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(size, Size):
            raise TypeError(f"Expected type {Size.__name__}, but got {type(size).__name__}.")

        _lib.PtxPdfContent_Group_Create.argtypes = [c_void_p, POINTER(Size)]
        _lib.PtxPdfContent_Group_Create.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Group_Create(target_document._handle, size)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Group._create_dynamic_type(ret_val)


    @staticmethod
    def copy_from_page(target_document: Document, page: Page, options: Optional[PageCopyOptions]) -> Group:
        """
        Create a group object from a page.

         
        From a given page in an input document, create a group object in the given target document.
        The returned object is associated with the target document but not yet part of it.
         
        A group that contains interactive elements can be painted once only.
        Interactive elements are annotations, group fields, outlines or logical structure information.
        If a group needs to be painted multiple times,
        interactive elements can be flattened or the group can be copied multiple times from the page.
         
        There are some interactive elements such as form fields or text annotations that cannot be rotated.
        So if you plan to rotate the group, it is recommended to flatten form fields and annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            page (pdftools_toolbox.pdf.page.Page): 
                a page of a different document

            options (Optional[pdftools_toolbox.pdf.page_copy_options.PageCopyOptions]): 
                the copy options



        Returns:
            pdftools_toolbox.pdf.content.group.Group: 
                the copied group, associated with the current document.



        Raises:
            OSError:
                Error reading from the input document or writing to the output document

            pdftools_toolbox.corrupt_error.CorruptError:
                The input document is corrupt

            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            pdftools_toolbox.conformance_error.ConformanceError:
                The explicitly requested conformance level is PDF/A Level A
                (:attr:`pdftools_toolbox.pdf.conformance.Conformance.PDFA1A` , :attr:`pdftools_toolbox.pdf.conformance.Conformance.PDFA2A` ,
                or :attr:`pdftools_toolbox.pdf.conformance.Conformance.PDFA3A` )
                and the copy option :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.copy_logical_structure`  is not set.

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `page` object is not associated with an input document

            ValueError:
                if the document associated with the `page` object has already been closed

            ValueError:
                if the argument `options` has :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.form_fields`  set to :attr:`pdftools_toolbox.pdf.forms.form_field_copy_strategy.FormFieldCopyStrategy.COPY` 
                and the `targetDocument` contains form fields that have either been copied explicitly
                with :meth:`pdftools_toolbox.pdf.forms.field_node.FieldNode.copy`  or created with :meth:`pdftools_toolbox.pdf.forms.check_box.CheckBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.create` , :meth:`pdftools_toolbox.pdf.forms.comb_text_field.CombTextField.create` ,
                :meth:`pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField.create` , :meth:`pdftools_toolbox.pdf.forms.list_box.ListBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.radio_button_group.RadioButtonGroup.create` , or :meth:`pdftools_toolbox.pdf.forms.sub_form.SubForm.create` .

            ValueError:
                if the argument `options` has :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.unsigned_signatures`  set to :attr:`pdftools_toolbox.pdf.copy_strategy.CopyStrategy.COPY` 
                and the `targetDocument` contains form fields that have either been copied explicitly
                with :meth:`pdftools_toolbox.pdf.forms.field_node.FieldNode.copy`  or created with :meth:`pdftools_toolbox.pdf.forms.check_box.CheckBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.combo_box.ComboBox.create` , :meth:`pdftools_toolbox.pdf.forms.comb_text_field.CombTextField.create` ,
                :meth:`pdftools_toolbox.pdf.forms.general_text_field.GeneralTextField.create` , :meth:`pdftools_toolbox.pdf.forms.list_box.ListBox.create` ,
                :meth:`pdftools_toolbox.pdf.forms.radio_button_group.RadioButtonGroup.create` , or :meth:`pdftools_toolbox.pdf.forms.sub_form.SubForm.create` .

            ValueError:
                if `options` has :attr:`pdftools_toolbox.pdf.page_copy_options.PageCopyOptions.copy_outline_items`  set to `True`
                and the `targetDocument` contains outline items that have been copied explicitly
                with :meth:`pdftools_toolbox.pdf.navigation.outline_item.OutlineItem.copy` .


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.page import Page
        from pdftools_toolbox.pdf.page_copy_options import PageCopyOptions

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(page, Page):
            raise TypeError(f"Expected type {Page.__name__}, but got {type(page).__name__}.")
        if options is not None and not isinstance(options, PageCopyOptions):
            raise TypeError(f"Expected type {PageCopyOptions.__name__} or None, but got {type(options).__name__}.")

        _lib.PtxPdfContent_Group_CopyFromPage.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PtxPdfContent_Group_CopyFromPage.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Group_CopyFromPage(target_document._handle, page._handle, options._handle if options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Group._create_dynamic_type(ret_val)



    @property
    def size(self) -> Size:
        """
        The size of the group.



        Returns:
            pdftools_toolbox.geometry.real.size.Size

        Raises:
            StateError:
                if the group has already been closed


        """
        from pdftools_toolbox.geometry.real.size import Size

        _lib.PtxPdfContent_Group_GetSize.argtypes = [c_void_p, POINTER(Size)]
        _lib.PtxPdfContent_Group_GetSize.restype = c_bool
        ret_val = Size()
        if not _lib.PtxPdfContent_Group_GetSize(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def content(self) -> Content:
        """
        the group content.

        If the group is writable, the content object can be used to apply new content on the group.



        Returns:
            pdftools_toolbox.pdf.content.content.Content

        Raises:
            StateError:
                if the group has already been closed


        """
        from pdftools_toolbox.pdf.content.content import Content

        _lib.PtxPdfContent_Group_GetContent.argtypes = [c_void_p]
        _lib.PtxPdfContent_Group_GetContent.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Group_GetContent(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Content._create_dynamic_type(ret_val)


    @property
    def isolated(self) -> bool:
        """
        the transparency isolation behavior



        Returns:
            bool

        Raises:
            StateError:
                if the group has already been closed


        """
        _lib.PtxPdfContent_Group_GetIsolated.argtypes = [c_void_p]
        _lib.PtxPdfContent_Group_GetIsolated.restype = c_bool
        ret_val = _lib.PtxPdfContent_Group_GetIsolated(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @isolated.setter
    def isolated(self, val: bool) -> None:
        """
        the transparency isolation behavior



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the group has already been closed

            StateError:
                if the group has already been painted

            OperationError:
                The document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Group_SetIsolated.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfContent_Group_SetIsolated.restype = c_bool
        if not _lib.PtxPdfContent_Group_SetIsolated(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def knockout(self) -> bool:
        """
        the transparency knockout behavior



        Returns:
            bool

        Raises:
            StateError:
                if the group has already been closed


        """
        _lib.PtxPdfContent_Group_GetKnockout.argtypes = [c_void_p]
        _lib.PtxPdfContent_Group_GetKnockout.restype = c_bool
        ret_val = _lib.PtxPdfContent_Group_GetKnockout(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @knockout.setter
    def knockout(self, val: bool) -> None:
        """
        the transparency knockout behavior



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                if the group has already been closed

            StateError:
                if the group has already been painted

            OperationError:
                The document is read-only


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Group_SetKnockout.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfContent_Group_SetKnockout.restype = c_bool
        if not _lib.PtxPdfContent_Group_SetKnockout(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Group._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Group.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
