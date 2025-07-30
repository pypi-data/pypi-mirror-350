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
import pdftools_toolbox.pdf.navigation.outline_item

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.navigation.outline_item import OutlineItem

else:
    OutlineItem = "pdftools_toolbox.pdf.navigation.outline_item.OutlineItem"


class OutlineItemList(_NativeObject, list):
    """
    """
    def __len__(self) -> int:
        _lib.PtxPdfNav_OutlineItemList_GetCount.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineItemList_GetCount.restype = c_int
        ret_val = _lib.PtxPdfNav_OutlineItemList_GetCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val

    def clear(self) -> None:
        _lib.PtxPdfNav_OutlineItemList_Clear.argtypes = [c_void_p]
        _lib.PtxPdfNav_OutlineItemList_Clear.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItemList_Clear(self._handle):
            _NativeBase._throw_last_error(False)

    def __delitem__(self, index: int) -> None:
        if index < 0:  # Handle negative indexing
            index += len(self)
        self.remove(index)

    def remove(self, index: int) -> None:
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        _lib.PtxPdfNav_OutlineItemList_Remove.argtypes = [c_void_p, c_int]
        _lib.PtxPdfNav_OutlineItemList_Remove.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItemList_Remove(self._handle, index):
            _NativeBase._throw_last_error(False)

    def extend(self, items: OutlineItemList) -> None:
        if not isinstance(items, OutlineItemList):
            raise TypeError(f"Expected type {OutlineItemList.__name__}, but got {type(items).__name__}.")
        for item in items:
            self.append(item)

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError("Insert method is not supported in OutlineItemList.")

    def pop(self, index: int = -1) -> Any:
        raise NotImplementedError("Pop method is not supported in OutlineItemList.")

    def copy(self) -> OutlineItemList:
        raise NotImplementedError("Copy method is not supported in OutlineItemList.")

    def sort(self, key=None, reverse=False) -> None:
        raise NotImplementedError("Sort method is not supported in OutlineItemList.")

    def reverse(self) -> None:
        raise NotImplementedError("Reverse method is not supported in OutlineItemList.")

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        from pdftools_toolbox.pdf.navigation.outline_item import OutlineItem

        if isinstance(index, slice):
            raise NotImplementedError("Slicing is not implemented.")
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PtxPdfNav_OutlineItemList_Get.argtypes = [c_void_p, c_int]
        _lib.PtxPdfNav_OutlineItemList_Get.restype = c_void_p
        ret_val = _lib.PtxPdfNav_OutlineItemList_Get(self._handle, index)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return OutlineItem._create_dynamic_type(ret_val)

    def __setitem__(self, index: int, value: Any) -> None:
        from pdftools_toolbox.pdf.navigation.outline_item import OutlineItem

        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")
        if not isinstance(value, OutlineItem):
            raise TypeError(f"Expected type {OutlineItem.__name__}, but got {type(value).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PtxPdfNav_OutlineItemList_Set.argtypes = [c_void_p, c_int, c_void_p]
        _lib.PtxPdfNav_OutlineItemList_Set.restype = c_bool
        if not _lib.PtxPdfNav_OutlineItemList_Set(self._handle, index, value._handle):
            _NativeBase._throw_last_error(False)

    def append(self, value: OutlineItem) -> None:
        from pdftools_toolbox.pdf.navigation.outline_item import OutlineItem

        if not isinstance(value, OutlineItem):
            raise TypeError(f"Expected type {OutlineItem.__name__}, but got {type(value).__name__}.")

        _lib.PtxPdfNav_OutlineItemList_Add.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfNav_OutlineItemList_Add.restype = c_bool
        ret_val = _lib.PtxPdfNav_OutlineItemList_Add(self._handle, value._handle)
        if not ret_val:
            _NativeBase._throw_last_error(False)

    def index(self, value: OutlineItem, start: int = 0, stop: Optional[int] = None) -> int:
        from pdftools_toolbox.pdf.navigation.outline_item import OutlineItem

        if not isinstance(value, OutlineItem):
            raise TypeError(f"Expected type {OutlineItem.__name__}, but got {type(value).__name__}.")
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
        return OutlineItemList._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = OutlineItemList.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
