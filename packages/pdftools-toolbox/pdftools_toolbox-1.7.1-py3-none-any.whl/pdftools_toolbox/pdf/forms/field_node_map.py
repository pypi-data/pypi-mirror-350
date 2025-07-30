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
import pdftools_toolbox.pdf.forms.field_node

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.forms.field_node import FieldNode

else:
    FieldNode = "pdftools_toolbox.pdf.forms.field_node.FieldNode"


class FieldNodeMap(_NativeObject, dict):
    """
    """
    def lookup(self, identifier_path: Optional[str]) -> FieldNode:
        """
        Access a form field by path

        Lookup the form field node given by the identifier path.



        Args:
            identifierPath (Optional[str]): 
                the identifier path in which sub forms must be delimited by full stops '.'



        Returns:
            pdftools_toolbox.pdf.forms.field_node.FieldNode: 
                the resulting form field node.



        Raises:
            StateError:
                if the document has already been closed

            pdftools_toolbox.not_found_error.NotFoundError:
                if no form field with this identifier exists


        """
        from pdftools_toolbox.pdf.forms.field_node import FieldNode

        if identifier_path is not None and not isinstance(identifier_path, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(identifier_path).__name__}.")

        _lib.PtxPdfForms_FieldNodeMap_LookupW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_FieldNodeMap_LookupW.restype = c_void_p
        ret_val = _lib.PtxPdfForms_FieldNodeMap_LookupW(self._handle, _string_to_utf16(identifier_path))
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FieldNode._create_dynamic_type(ret_val)



    def __len__(self) -> int:
        _lib.PtxPdfForms_FieldNodeMap_GetCount.argtypes = [c_void_p]
        _lib.PtxPdfForms_FieldNodeMap_GetCount.restype = c_int
        ret_val = _lib.PtxPdfForms_FieldNodeMap_GetCount(self._handle)
        if ret_val < 0:
            _NativeBase._throw_last_error(False)
        return ret_val

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError("Deleting elements is not supported in FieldNodeMap.")

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in FieldNodeMap.")
    def _get(self, key: str) -> int:
        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")

        _lib.PtxPdfForms_FieldNodeMap_GetW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfForms_FieldNodeMap_GetW.restype = c_int
        ret_val = _lib.PtxPdfForms_FieldNodeMap_GetW(self._handle, _string_to_utf16(key))
        if ret_val == -1 and _NativeBase._last_error_code() != 5:
            _NativeBase._throw_last_error()
        return ret_val

    def _get_key(self, it: int) -> str:
        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PtxPdfForms_FieldNodeMap_GetKeyW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfForms_FieldNodeMap_GetKeyW.restype = c_size_t
        ret_val_size = _lib.PtxPdfForms_FieldNodeMap_GetKeyW(self._handle, it, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfForms_FieldNodeMap_GetKeyW(self._handle, it, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)

    def pop(self, key, default=None):
        raise NotImplementedError("Pop method is not supported in FieldNodeMap.")

    def popitem(self):
        raise NotImplementedError("Popitem method is not supported in FieldNodeMap.")

    def update(self, *args, **kwargs):
        raise NotImplementedError("Update method is not supported in FieldNodeMap.")

    def setdefault(self, key, default=None):
        raise NotImplementedError("Setdefault method is not supported in FieldNodeMap.")
    def __missing__(self, key):
        raise NotImplementedError("Missing is not supported in FieldNodeMap.")

    def __getitem__(self, key: str) -> FieldNode:
        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")

        it = self._get(key)
        if it == -1:
            raise KeyError(f"Key {key} not found!")
        return self._get_value(it)

    def __setitem__(self, key: str, value: FieldNode) -> None:
        from pdftools_toolbox.pdf.forms.field_node import FieldNode

        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")
        if not isinstance(value, FieldNode):
            raise TypeError(f"Expected type {FieldNode.__name__}, but got {type(value).__name__}.")

        _lib.PtxPdfForms_FieldNodeMap_SetW.argtypes = [c_void_p, c_wchar_p, c_void_p]
        _lib.PtxPdfForms_FieldNodeMap_SetW.restype = c_bool
        if not _lib.PtxPdfForms_FieldNodeMap_SetW(self._handle, _string_to_utf16(key), value._handle):
            _NativeBase._throw_last_error(False)

    def _get_value(self, it: int) -> FieldNode:
        from pdftools_toolbox.pdf.forms.field_node import FieldNode

        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PtxPdfForms_FieldNodeMap_GetValue.argtypes = [c_void_p, c_int]
        _lib.PtxPdfForms_FieldNodeMap_GetValue.restype = c_void_p
        ret_val = _lib.PtxPdfForms_FieldNodeMap_GetValue(self._handle, it)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FieldNode._create_dynamic_type(ret_val)


    # Iterable implementation
    def __iter__(self) -> Iterator[str]:
        return FieldNodeMap._FieldNodeMapKeyIterator(self)

    def keys(self) -> Iterator[str]:
        return iter(self)

    def _get_begin(self) -> int:
        _lib.PtxPdfForms_FieldNodeMap_GetBegin.argtypes = [c_void_p]
        _lib.PtxPdfForms_FieldNodeMap_GetBegin.restype = c_int
        ret_val = _lib.PtxPdfForms_FieldNodeMap_GetBegin(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def _get_end(self) -> int:
        _lib.PtxPdfForms_FieldNodeMap_GetEnd.argtypes = [c_void_p]
        _lib.PtxPdfForms_FieldNodeMap_GetEnd.restype = c_int
        ret_val = _lib.PtxPdfForms_FieldNodeMap_GetEnd(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def _get_next(self, it: int) -> int:
        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PtxPdfForms_FieldNodeMap_GetNext.argtypes = [c_void_p, c_int]
        _lib.PtxPdfForms_FieldNodeMap_GetNext.restype = c_int
        ret_val = _lib.PtxPdfForms_FieldNodeMap_GetNext(self._handle, it)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def items(self) -> Iterator[Tuple[str, FieldNode]]:
        return FieldNodeMap._FieldNodeMapKeyValueIterator(self)

    def values(self) -> Iterator[FieldNode]:
        return FieldNodeMap._FieldNodeMapValueIterator(self)


    class _FieldNodeMapKeyIterator:
        def __init__(self, map_instance: FieldNodeMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> FieldNodeMap._FieldNodeMapKeyIterator:
            return self

        def __next__(self) -> str:
            if self._current == self._end:
                raise StopIteration
            if self._current == -1:
                self._current = self._map_instance._get_begin()
            else:
                self._current = self._map_instance._get_next(self._current)
            if self._current == self._end:
                raise StopIteration
            return self._map_instance._get_key(self._current)

    class _FieldNodeMapValueIterator:
        def __init__(self, map_instance: FieldNodeMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> FieldNodeMap._FieldNodeMapValueIterator:
            return self

        def __next__(self):
            if self._current == self._end:
                raise StopIteration
            if self._current == -1:
                self._current = self._map_instance._get_begin()
            else:
                self._current = self._map_instance._get_next(self._current)
            if self._current == self._end:
                raise StopIteration
            return self._map_instance._get_value(self._current)

    class _FieldNodeMapKeyValueIterator:
        def __init__(self, map_instance: FieldNodeMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> FieldNodeMap._FieldNodeMapKeyValueIterator:
            return self

        def __next__(self):
            if self._current == self._end:
                raise StopIteration
            if self._current == -1:
                self._current = self._map_instance._get_begin()
            else:
                self._current = self._map_instance._get_next(self._current)
            if self._current == self._end:
                raise StopIteration
            return self._map_instance._get_key(self._current), self._map_instance._get_value(self._current)

    @staticmethod
    def _create_dynamic_type(handle):
        return FieldNodeMap._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = FieldNodeMap.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
