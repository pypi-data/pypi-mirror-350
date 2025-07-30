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
    from pdftools_toolbox.pdf.navigation.destination import Destination
    from pdftools_toolbox.pdf.navigation.outline_copy_options import OutlineCopyOptions
    from pdftools_toolbox.pdf.navigation.outline_item_list import OutlineItemList

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Destination = "pdftools_toolbox.pdf.navigation.destination.Destination"
    OutlineCopyOptions = "pdftools_toolbox.pdf.navigation.outline_copy_options.OutlineCopyOptions"
    OutlineItemList = "pdftools_toolbox.pdf.navigation.outline_item_list.OutlineItemList"


class OutlineItem(_NativeObject):
    """
    An outline item represents an entry in the outline tree of the document.
    It is also known as "Bookmark".


    """
    @staticmethod
    def create(target_document: Document, title: str, destination: Optional[Destination]) -> OutlineItem:
        """
        Create a new outline item (bookmark).

        The returned outline item is not yet part of the outline item tree, but it is associated with the given target document.
        It can be inserted at any position in the tree.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated

            title (str): 
                The title of the newly created outline item.

            destination (Optional[pdftools_toolbox.pdf.navigation.destination.Destination]): 
                The destination that this outline item refers to or
                `None` if the item has no destination.



        Returns:
            pdftools_toolbox.pdf.navigation.outline_item.OutlineItem: 
                The newly created outline item.



        Raises:
            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the document associated with the `destination` argument has already been closed

            ValueError:
                if the `destination` argument belongs to a different document


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.navigation.destination import Destination

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(title, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(title).__name__}.")
        if destination is not None and not isinstance(destination, Destination):
            raise TypeError(f"Expected type {Destination.__name__} or None, but got {type(destination).__name__}.")

        _lib.PtxPdfNav_OutlineItem_CreateW.argtypes = [c_void_p, c_wchar_p, c_void_p]
        _lib.PtxPdfNav_OutlineItem_CreateW.restype = c_void_p
        ret_val = _lib.PtxPdfNav_OutlineItem_CreateW(target_document._handle, _string_to_utf16(title), destination._handle if destination is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return OutlineItem._create_dynamic_type(ret_val)


    @staticmethod
    def copy(target_document: Document, outline_item: OutlineItem, options: Optional[OutlineCopyOptions]) -> OutlineItem:
        """
        Copy an outline item

        Copy an outline item object including all descendants from an input document to the given `targetDocument`.
        The returned object is associated with the given target document but not yet part of it.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                the output document with which the returned object is associated

            outlineItem (pdftools_toolbox.pdf.navigation.outline_item.OutlineItem): 
                An outline item of a different document

            options (Optional[pdftools_toolbox.pdf.navigation.outline_copy_options.OutlineCopyOptions]): 
                The options used to copy the item



        Returns:
            pdftools_toolbox.pdf.navigation.outline_item.OutlineItem: 
                The copied outline item, associated with the current document.



        Raises:
            pdftools_toolbox.conformance_error.ConformanceError:
                The conformance level of the source document is not compatible
                with the conformance level of the target document.

            ValueError:
                if the `targetDocument` argument is `None`

            ValueError:
                if the `targetDocument` argument has already been closed

            ValueError:
                if the `targetDocument` argument is read-only

            ValueError:
                if the `outlineItem` argument is not associated with an input document

            ValueError:
                the target document contains implicitly copied outline items

            ValueError:
                the `outlineItem` argument is `None`

            ValueError:
                the `outlineItem` argument is not associated with an input document

            OSError:
                Error reading from the source document or writing to the target document


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.navigation.outline_copy_options import OutlineCopyOptions

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(outline_item, OutlineItem):
            raise TypeError(f"Expected type {OutlineItem.__name__}, but got {type(outline_item).__name__}.")
        if options is not None and not isinstance(options, OutlineCopyOptions):
            raise TypeError(f"Expected type {OutlineCopyOptions.__name__} or None, but got {type(options).__name__}.")

        _lib.PtxPdfNav_OutlineItem_Copy.argtypes = [c_void_p, c_void_p, c_void_p]
        _lib.PtxPdfNav_OutlineItem_Copy.restype = c_void_p
        ret_val = _lib.PtxPdfNav_OutlineItem_Copy(target_document._handle, outline_item._handle, options._handle if options is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return OutlineItem._create_dynamic_type(ret_val)



    @property
    def title(self) -> str:
        """
        The title of the outline item.



        Returns:
            str

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_OutlineItem_GetTitleW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfNav_OutlineItem_GetTitleW.restype = c_size_t
        ret_val_size = _lib.PtxPdfNav_OutlineItem_GetTitleW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfNav_OutlineItem_GetTitleW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @title.setter
    def title(self, val: str) -> None:
        """
        The title of the outline item.



        Args:
            val (str):
                property value

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.

            OperationError:
                the object is not associated to an output document.


        """
        if not isinstance(val, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_OutlineItem_SetTitleW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfNav_OutlineItem_SetTitleW.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItem_SetTitleW(self._handle, _string_to_utf16(val)):
            _NativeBase._throw_last_error(False)

    @property
    def bold(self) -> bool:
        """
        If `True`, the outline item is displayed in bold font.



        Returns:
            bool

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_OutlineItem_GetBold.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineItem_GetBold.restype = c_bool
        ret_val = _lib.PtxPdfNav_OutlineItem_GetBold(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @bold.setter
    def bold(self, val: bool) -> None:
        """
        If `True`, the outline item is displayed in bold font.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.

            OperationError:
                the object is not associated to an output document.


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_OutlineItem_SetBold.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_OutlineItem_SetBold.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItem_SetBold(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def italic(self) -> bool:
        """
        If `True`, the outline item is displayed in italic font.



        Returns:
            bool

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_OutlineItem_GetItalic.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineItem_GetItalic.restype = c_bool
        ret_val = _lib.PtxPdfNav_OutlineItem_GetItalic(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @italic.setter
    def italic(self, val: bool) -> None:
        """
        If `True`, the outline item is displayed in italic font.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.

            OperationError:
                the object is not associated to an output document.


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_OutlineItem_SetItalic.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_OutlineItem_SetItalic.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItem_SetItalic(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def destination(self) -> Optional[Destination]:
        """
        The destination of the outline item.



        Returns:
            Optional[pdftools_toolbox.pdf.navigation.destination.Destination]

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.

            OperationError:
                the object is not associated to an input document.


        """
        from pdftools_toolbox.pdf.navigation.destination import Destination

        _lib.PtxPdfNav_OutlineItem_GetDestination.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineItem_GetDestination.restype = c_void_p
        ret_val = _lib.PtxPdfNav_OutlineItem_GetDestination(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Destination._create_dynamic_type(ret_val)


    @destination.setter
    def destination(self, val: Optional[Destination]) -> None:
        """
        The destination of the outline item.



        Args:
            val (Optional[pdftools_toolbox.pdf.navigation.destination.Destination]):
                property value

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.

            OperationError:
                the object is not associated to an output document.


        """
        from pdftools_toolbox.pdf.navigation.destination import Destination

        if val is not None and not isinstance(val, Destination):
            raise TypeError(f"Expected type {Destination.__name__} or None, but got {type(val).__name__}.")
        _lib.PtxPdfNav_OutlineItem_SetDestination.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfNav_OutlineItem_SetDestination.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItem_SetDestination(self._handle, val._handle if val is not None else None):
            _NativeBase._throw_last_error(False)

    @property
    def is_open(self) -> bool:
        """
         
        - If `True`, the item is expanded.
        - If `False`, the item is collapsed.
         
        This is property is only meaningful if the item has child items.



        Returns:
            bool

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        _lib.PtxPdfNav_OutlineItem_IsOpen.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineItem_IsOpen.restype = c_bool
        ret_val = _lib.PtxPdfNav_OutlineItem_IsOpen(self._handle)
        if not ret_val:
            _NativeBase._throw_last_error()
        return ret_val



    @is_open.setter
    def is_open(self, val: bool) -> None:
        """
         
        - If `True`, the item is expanded.
        - If `False`, the item is collapsed.
         
        This is property is only meaningful if the item has child items.



        Args:
            val (bool):
                property value

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.

            OperationError:
                the object is not associated to an output document.


        """
        if not isinstance(val, bool):
            raise TypeError(f"Expected type {bool.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfNav_OutlineItem_IsOpen.argtypes = [c_void_p, c_bool]
        _lib.PtxPdfNav_OutlineItem_IsOpen.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItem_IsOpen(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def children(self) -> OutlineItemList:
        """
        The child items of this outline item.



        Returns:
            pdftools_toolbox.pdf.navigation.outline_item_list.OutlineItemList

        Raises:
            StateError:
                the object has already been closed.

            StateError:
                the associated document has already been closed.


        """
        from pdftools_toolbox.pdf.navigation.outline_item_list import OutlineItemList

        _lib.PtxPdfNav_OutlineItem_GetChildren.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineItem_GetChildren.restype = c_void_p
        ret_val = _lib.PtxPdfNav_OutlineItem_GetChildren(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return OutlineItemList._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return OutlineItem._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = OutlineItem.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
