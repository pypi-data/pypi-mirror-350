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
import pdftools_toolbox.pdf.page

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.pdf.page_copy_options import PageCopyOptions
    from pdftools_toolbox.pdf.page import Page

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    PageCopyOptions = "pdftools_toolbox.pdf.page_copy_options.PageCopyOptions"
    Page = "pdftools_toolbox.pdf.page.Page"


class PageList(_NativeObject, list):
    """
    """
    @staticmethod
    def copy(target_document: Document, page_list: PageList, options: Optional[PageCopyOptions]) -> PageList:
        """
        Copy a page list

        Copy pages from an input document to the given `targetDocument`.
        The returned list is associated with the given target document but not yet part of it.
        It can be appended to the document's page list.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            pageList (pdftools_toolbox.pdf.page_list.PageList): 
                a page list of a different document

            options (Optional[pdftools_toolbox.pdf.page_copy_options.PageCopyOptions]): 
                the copy options



        Returns:
            pdftools_toolbox.pdf.page_list.PageList: 
                the copied page list, associated with the target document.



        Raises:
            OSError:
                Error reading from the source document or writing to the target document

            pdftools_toolbox.corrupt_error.CorruptError:
                The source document is corrupt

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
                if the `pageList` object is not associated with an input document

            ValueError:
                if the document associated with `pageList` has already been closed

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
        from pdftools_toolbox.pdf.page_copy_options import PageCopyOptions

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(page_list, PageList):
            raise TypeError(f"Expected type {PageList.__name__}, but got {type(page_list).__name__}.")
        if options is not None and not isinstance(options, PageCopyOptions):
            raise TypeError(f"Expected type {PageCopyOptions.__name__} or None, but got {type(options).__name__}.")

        _lib.PtxPdf_PageList_Copy.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PtxPdf_PageList_Copy.restype = c_void_p
        ret_val = _lib.PtxPdf_PageList_Copy(target_document._handle, page_list._handle, options._handle if options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PageList._create_dynamic_type(ret_val)



    def __len__(self) -> int:
        _lib.PtxPdf_PageList_GetCount.argtypes = [c_void_p]
        _lib.PtxPdf_PageList_GetCount.restype = c_int
        ret_val = _lib.PtxPdf_PageList_GetCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in PageList.")

    def __delitem__(self, index: int) -> None:
        if index < 0:  # Handle negative indexing
            index += len(self)
        self.remove(index)

    def remove(self, index: int) -> None:
        raise NotImplementedError("Removing elements is not supported in PageList.")

    def extend(self, items: PageList) -> None:
        if not isinstance(items, PageList):
            raise TypeError(f"Expected type {PageList.__name__}, but got {type(items).__name__}.")
        _lib.PtxPdf_PageList_AddRange.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_PageList_AddRange.restype = c_bool
        ret_val = _lib.PtxPdf_PageList_AddRange(self._handle, items._handle)
        if not ret_val:
            _NativeBase._throw_last_error(False)

    def _get_slice(self, slice_obj: slice) -> PageList:
        start = slice_obj.start or 0
        end = slice_obj.stop or len(self)
        step = slice_obj.step or 1

        if step != 1:  # Check if the step is not equal to 1
            raise ValueError("Slicing with a step different from 1 is not supported.")

        _lib.PtxPdf_PageList_GetRange.argtypes = [c_void_p, c_int, c_int]
        _lib.PtxPdf_PageList_GetRange.restype = c_void_p
        ret_val = _lib.PtxPdf_PageList_GetRange(self._handle, start, end - start)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PageList._create_dynamic_type(ret_val)

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError("Insert method is not supported in PageList.")

    def pop(self, index: int = -1) -> Any:
        raise NotImplementedError("Pop method is not supported in PageList.")

    def sort(self, key=None, reverse=False) -> None:
        raise NotImplementedError("Sort method is not supported in PageList.")

    def reverse(self) -> None:
        raise NotImplementedError("Reverse method is not supported in PageList.")

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        from pdftools_toolbox.pdf.page import Page

        if isinstance(index, slice):
            return self._get_slice(index)
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PtxPdf_PageList_Get.argtypes = [c_void_p, c_int]
        _lib.PtxPdf_PageList_Get.restype = c_void_p
        ret_val = _lib.PtxPdf_PageList_Get(self._handle, index)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Page._create_dynamic_type(ret_val)

    def __setitem__(self, index: int, value: Any) -> None:
        raise NotImplementedError("Setting elements is not supported in PageList.")

    def append(self, value: Page) -> None:
        from pdftools_toolbox.pdf.page import Page

        if not isinstance(value, Page):
            raise TypeError(f"Expected type {Page.__name__}, but got {type(value).__name__}.")

        _lib.PtxPdf_PageList_Add.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdf_PageList_Add.restype = c_bool
        ret_val = _lib.PtxPdf_PageList_Add(self._handle, value._handle)
        if not ret_val:
            _NativeBase._throw_last_error(False)

    def index(self, value: Page, start: int = 0, stop: Optional[int] = None) -> int:
        from pdftools_toolbox.pdf.page import Page

        if not isinstance(value, Page):
            raise TypeError(f"Expected type {Page.__name__}, but got {type(value).__name__}.")
        if not isinstance(start, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(start).__name__}.")
        if stop is not None and not isinstance(stop, int):
            raise TypeError(f"Expected type {int.__name__} or None, but got {type(stop).__name__}.")

        length = len(self)
        if start < 0:
            start += length
        if stop is None:
            stop = length
        elif stop < 0:
            stop += length

        for i in range(max(start, 0), min(stop, length)):
            if self[i] == value:
                return i

        raise ValueError(f"{value} is not in the list.")


    def __iter__(self):
        self._iter_index = 0  # Initialize the index for iteration
        return self

    def __next__(self):
        if self._iter_index < len(self):  # Check if there are more items to iterate over
            item = self.__getitem__(self._iter_index)  # Get the item at the current index
            self._iter_index += 1  # Move to the next index
            return item
        else:
            raise StopIteration  # Signal that iteration is complete

    @staticmethod
    def _create_dynamic_type(handle):
        return PageList._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = PageList.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
