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
    from pdftools_toolbox.geometry.real.point import Point

else:
    Point = "pdftools_toolbox.geometry.real.point.Point"


class Glyph(_NativeObject):
    """
    """
    @property
    def text(self) -> str:
        """
        glyph text

        This is the glyph's associated text.



        Returns:
            str

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_Glyph_GetTextW.argtypes = [c_void_p, POINTER(c_wchar), c_size_t]
        _lib.PtxPdfContent_Glyph_GetTextW.restype = c_size_t
        ret_val_size = _lib.PtxPdfContent_Glyph_GetTextW(self._handle, None, 0)
        if ret_val_size == 0:
            _NativeBase._throw_last_error(False)
        ret_val = create_unicode_buffer(ret_val_size)
        _lib.PtxPdfContent_Glyph_GetTextW(self._handle, ret_val, c_size_t(ret_val_size))
        return _utf16_to_string(ret_val, ret_val_size)


    @property
    def position(self) -> Point:
        """
        glyph position

         
        This is the position of the glyph within its :class:`pdftools_toolbox.pdf.content.text_fragment.TextFragment` .
        To find the point on the page this position has to be transformed with
        :attr:`pdftools_toolbox.pdf.content.text_fragment.TextFragment.transform` .
         
        The extent of the glyph with respect to its position depends on the text
        fragment's :attr:`pdftools_toolbox.pdf.content.text_fragment.TextFragment.writing_mode` .
        In :attr:`pdftools_toolbox.pdf.content.writing_mode.WritingMode.HORIZONTAL`  writing mode,
        the glyph's position is at the left of the glyph on the height of the base line.
        In :attr:`pdftools_toolbox.pdf.content.writing_mode.WritingMode.VERTICAL`  writing mode,
        the glyph's position is at the middle of the glyph's horizontal extent,
        vertically at the top.



        Returns:
            pdftools_toolbox.geometry.real.point.Point

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        _lib.PtxPdfContent_Glyph_GetPosition.argtypes = [c_void_p, POINTER(Point)]
        _lib.PtxPdfContent_Glyph_GetPosition.restype = c_bool
        ret_val = Point()
        if not _lib.PtxPdfContent_Glyph_GetPosition(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def width(self) -> float:
        """
        glyph width

        This is the width of the glyph.



        Returns:
            float

        Raises:
            StateError:
                the object has already been closed


        """
        _lib.PtxPdfContent_Glyph_GetWidth.argtypes = [c_void_p]
        _lib.PtxPdfContent_Glyph_GetWidth.restype = c_double
        ret_val = _lib.PtxPdfContent_Glyph_GetWidth(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val




    @staticmethod
    def _create_dynamic_type(handle):
        return Glyph._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Glyph.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
