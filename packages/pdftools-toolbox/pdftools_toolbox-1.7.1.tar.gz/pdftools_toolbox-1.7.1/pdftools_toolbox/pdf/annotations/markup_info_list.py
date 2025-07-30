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
import pdftools_toolbox.pdf.annotations.markup_info

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.annotations.markup_info import MarkupInfo

else:
    MarkupInfo = "pdftools_toolbox.pdf.annotations.markup_info.MarkupInfo"


class MarkupInfoList(_NativeObject, list):
    """
    """
    def __len__(self) -> int:
        _lib.PtxPdfAnnots_MarkupInfoList_GetCount.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_MarkupInfoList_GetCount.restype = c_int
        ret_val = _lib.PtxPdfAnnots_MarkupInfoList_GetCount(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error()
        return ret_val

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in MarkupInfoList.")

    def __delitem__(self, index: int) -> None:
        if index < 0:  # Handle negative indexing
            index += len(self)
        self.remove(index)

    def remove(self, index: int) -> None:
        raise NotImplementedError("Removing elements is not supported in MarkupInfoList.")

    def extend(self, items: MarkupInfoList) -> None:
        if not isinstance(items, MarkupInfoList):
            raise TypeError(f"Expected type {MarkupInfoList.__name__}, but got {type(items).__name__}.")
        raise NotImplementedError("Extend method is not supported in MarkupInfoList.")

    def insert(self, index: int, value: Any) -> None:
        raise NotImplementedError("Insert method is not supported in MarkupInfoList.")

    def pop(self, index: int = -1) -> Any:
        raise NotImplementedError("Pop method is not supported in MarkupInfoList.")

    def copy(self) -> MarkupInfoList:
        raise NotImplementedError("Copy method is not supported in MarkupInfoList.")

    def sort(self, key=None, reverse=False) -> None:
        raise NotImplementedError("Sort method is not supported in MarkupInfoList.")

    def reverse(self) -> None:
        raise NotImplementedError("Reverse method is not supported in MarkupInfoList.")

    def __getitem__(self, index: Union[int, slice]) -> Union[Any, List[Any]]:
        from pdftools_toolbox.pdf.annotations.markup_info import MarkupInfo

        if isinstance(index, slice):
            raise NotImplementedError("Slicing is not implemented.")
        if not isinstance(index, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(index).__name__}.")

        if index < 0:  # Handle negative indexing
            index += len(self)

        _lib.PtxPdfAnnots_MarkupInfoList_Get.argtypes = [c_void_p, c_int]
        _lib.PtxPdfAnnots_MarkupInfoList_Get.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_MarkupInfoList_Get(self._handle, index)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return MarkupInfo._create_dynamic_type(ret_val)

    def __setitem__(self, index: int, value: Any) -> None:
        raise NotImplementedError("Setting elements is not supported in MarkupInfoList.")

    def append(self, value: MarkupInfo) -> None:
        raise NotImplementedError("Append method is not supported in MarkupInfoList.")

    def index(self, value: MarkupInfo, start: int = 0, stop: Optional[int] = None) -> int:
        from pdftools_toolbox.pdf.annotations.markup_info import MarkupInfo

        if not isinstance(value, MarkupInfo):
            raise TypeError(f"Expected type {MarkupInfo.__name__}, but got {type(value).__name__}.")
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
        return MarkupInfoList._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = MarkupInfoList.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
