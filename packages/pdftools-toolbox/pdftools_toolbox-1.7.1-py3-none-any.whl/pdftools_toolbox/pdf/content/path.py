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
from collections.abc import Iterable

import pdftools_toolbox.internal
import pdftools_toolbox.pdf.content.subpath

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.content.subpath import Subpath

else:
    Subpath = "pdftools_toolbox.pdf.content.subpath.Subpath"


class Path(_NativeObject, Iterable):
    """
    Paths define shapes, trajectories, and regions of all sorts.

    A path is made up of one or more disconnected subpaths, each comprising a sequence of connected segments.
    The topology of the path is unrestricted: it can be concave or convex, can contain multiple subpaths representing disjoint areas, and can intersect itself in arbitrary ways.


    """
    def __init__(self):
        """


        """
        _lib.PtxPdfContent_Path_New.argtypes = []
        _lib.PtxPdfContent_Path_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Path_New()
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def __iter__(self) -> PathIterator:
        _lib.PtxPdfContent_Path_GetIterator.argtypes = [c_void_p]
        _lib.PtxPdfContent_Path_GetIterator.restype = c_void_p
        iterator_handle = _lib.PtxPdfContent_Path_GetIterator(self._handle)
        if iterator_handle is None:
            _NativeBase._throw_last_error(False)
        return Path.PathIterator(iterator_handle)

    class PathIterator(_NativeObject):
        def __iter__(self) -> Path.PathIterator:
            return self

        def __enter__(self) -> Path.PathIterator:
            return self

        def __exit__(self, exc_type, exc_value, traceback) -> None:
            self.__del__()

        def __init__(self, iterator_handle: c_void_p) -> None:
            super()._initialize(iterator_handle)
            self._current: Optional[Subpath] = None

        def __next__(self) -> Subpath:
            _lib.PtxPdfContent_PathIterator_MoveNext.argtypes = [c_void_p]
            _lib.PtxPdfContent_PathIterator_MoveNext.restype = c_bool
            ret_val = _lib.PtxPdfContent_PathIterator_MoveNext(self._handle)
            if not ret_val:
                raise StopIteration
            self._current = self._get_value()
            return self._current

        def _get_value(self) -> Subpath:
            from pdftools_toolbox.pdf.content.subpath import Subpath

            _lib.PtxPdfContent_PathIterator_GetValue.argtypes = [c_void_p]
            _lib.PtxPdfContent_PathIterator_GetValue.restype = c_void_p
            ret_val = _lib.PtxPdfContent_PathIterator_GetValue(self._handle)
            if ret_val is None:
                _NativeBase._throw_last_error(False)
            return Subpath._create_dynamic_type(ret_val)


    @staticmethod
    def _create_dynamic_type(handle):
        return Path._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Path.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
