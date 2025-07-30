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

class RoleMap(_NativeObject, dict):
    """
    A dictionary that maps the names of structure types used in the document to
    their approximate equivalents in the set of standard structure types. Allowed values from the PDF standard are:
    Document, Part, Sect, Art, Div, H1, H2, H3, H4, H5, H6, P, L, LI, Lbl, LBody, Table, TR, TH,
    TD, THead, TBody, TFoot, Span, Quote, Note, Reference, Figure, Caption, Artifact, Form, Field,
    Link, Code, Annot, Ruby, Warichu, TOC, TOCI, Index and BibEntry.


    """
    def __len__(self) -> int:
        _lib.PtxPdfStructure_RoleMap_GetCount.argtypes = [c_void_p]
        _lib.PtxPdfStructure_RoleMap_GetCount.restype = c_int
        ret_val = _lib.PtxPdfStructure_RoleMap_GetCount(self._handle)
        if ret_val < 0:
            _NativeBase._throw_last_error(False)
        return ret_val

    def __delitem__(self, key: str) -> None:
        raise NotImplementedError("Deleting elements is not supported in RoleMap.")

    def clear(self) -> None:
        raise NotImplementedError("Clear method is not supported in RoleMap.")
    def _get(self, key: str) -> int:
        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")

        _lib.PtxPdfStructure_RoleMap_GetW.argtypes = [c_void_p, c_wchar_p]
        _lib.PtxPdfStructure_RoleMap_GetW.restype = c_int
        ret_val = _lib.PtxPdfStructure_RoleMap_GetW(self._handle, _string_to_utf16(key))
        if ret_val == -1 and _NativeBase._last_error_code() != 5:
            _NativeBase._throw_last_error()
        return ret_val

    def _get_key(self, it: int) -> str:
        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PtxPdfStructure_RoleMap_GetKeyW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfStructure_RoleMap_GetKeyW.restype = c_size_t
        ret_val_size = _lib.PtxPdfStructure_RoleMap_GetKeyW(self._handle, it, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfStructure_RoleMap_GetKeyW(self._handle, it, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)

    def pop(self, key, default=None):
        raise NotImplementedError("Pop method is not supported in RoleMap.")

    def popitem(self):
        raise NotImplementedError("Popitem method is not supported in RoleMap.")

    def update(self, *args, **kwargs):
        raise NotImplementedError("Update method is not supported in RoleMap.")

    def setdefault(self, key, default=None):
        raise NotImplementedError("Setdefault method is not supported in RoleMap.")
    def __missing__(self, key):
        raise NotImplementedError("Missing is not supported in RoleMap.")

    def __getitem__(self, key: str) -> str:
        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")

        it = self._get(key)
        if it == -1:
            raise KeyError(f"Key {key} not found!")
        return self._get_value(it)

    def __setitem__(self, key: str, value: str) -> None:

        if not isinstance(key, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(key).__name__}.")
        if not isinstance(value, str):
            raise TypeError(f"Expected type {str.__name__}, but got {type(value).__name__}.")

        _lib.PtxPdfStructure_RoleMap_SetW.argtypes = [c_void_p, c_wchar_p, c_wchar_p]
        _lib.PtxPdfStructure_RoleMap_SetW.restype = c_bool
        if not _lib.PtxPdfStructure_RoleMap_SetW(self._handle, _string_to_utf16(key), _string_to_utf16(value)):
            _NativeBase._throw_last_error(False)


    def _get_value(self, it: int) -> str:

        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PtxPdfStructure_RoleMap_GetValueW.argtypes = [c_void_p, c_int, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfStructure_RoleMap_GetValueW.restype = c_size_t
        ret_val_size = _lib.PtxPdfStructure_RoleMap_GetValueW(self._handle, it, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfStructure_RoleMap_GetValueW(self._handle, it, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    # Iterable implementation
    def __iter__(self) -> Iterator[str]:
        return RoleMap._RoleMapKeyIterator(self)

    def keys(self) -> Iterator[str]:
        return iter(self)

    def _get_begin(self) -> int:
        _lib.PtxPdfStructure_RoleMap_GetBegin.argtypes = [c_void_p]
        _lib.PtxPdfStructure_RoleMap_GetBegin.restype = c_int
        ret_val = _lib.PtxPdfStructure_RoleMap_GetBegin(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def _get_end(self) -> int:
        _lib.PtxPdfStructure_RoleMap_GetEnd.argtypes = [c_void_p]
        _lib.PtxPdfStructure_RoleMap_GetEnd.restype = c_int
        ret_val = _lib.PtxPdfStructure_RoleMap_GetEnd(self._handle)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def _get_next(self, it: int) -> int:
        if not isinstance(it, int):
            raise TypeError(f"Expected type {int.__name__}, but got {type(it).__name__}.")

        _lib.PtxPdfStructure_RoleMap_GetNext.argtypes = [c_void_p, c_int]
        _lib.PtxPdfStructure_RoleMap_GetNext.restype = c_int
        ret_val = _lib.PtxPdfStructure_RoleMap_GetNext(self._handle, it)
        if ret_val == -1:
            _NativeBase._throw_last_error(False)
        return ret_val

    def items(self) -> Iterator[Tuple[str, str]]:
        return RoleMap._RoleMapKeyValueIterator(self)

    def values(self) -> Iterator[str]:
        return RoleMap._RoleMapValueIterator(self)


    class _RoleMapKeyIterator:
        def __init__(self, map_instance: RoleMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> RoleMap._RoleMapKeyIterator:
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

    class _RoleMapValueIterator:
        def __init__(self, map_instance: RoleMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> RoleMap._RoleMapValueIterator:
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

    class _RoleMapKeyValueIterator:
        def __init__(self, map_instance: RoleMap):
            self._map_instance = map_instance
            self._current = -1
            self._end = self._map_instance._get_end()

        def __iter__(self) -> RoleMap._RoleMapKeyValueIterator:
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
        return RoleMap._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = RoleMap.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
