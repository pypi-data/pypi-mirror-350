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
    from pdftools_toolbox.pdf.content.paint import Paint
    from pdftools_toolbox.pdf.content.inside_rule import InsideRule

else:
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    InsideRule = "pdftools_toolbox.pdf.content.inside_rule.InsideRule"


class Fill(_NativeObject):
    """
    """
    def __init__(self, paint: Paint):
        """

        Args:
            paint (pdftools_toolbox.pdf.content.paint.Paint): 


        Raises:
            ValueError:
                if the document associated with the `paint` argument has already been closed


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(paint, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(paint).__name__}.")

        _lib.PtxPdfContent_Fill_New.argtypes = [c_void_p]
        _lib.PtxPdfContent_Fill_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Fill_New(paint._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    @property
    def paint(self) -> Paint:
        """

        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.fill.Fill`  object has already been closed


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfContent_Fill_GetPaint.argtypes = [c_void_p]
        _lib.PtxPdfContent_Fill_GetPaint.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Fill_GetPaint(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)


    @paint.setter
    def paint(self, val: Paint) -> None:
        """

        Args:
            val (pdftools_toolbox.pdf.content.paint.Paint):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.fill.Fill`  object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the document associated with the given :class:`pdftools_toolbox.pdf.content.paint.Paint`  object has already been closed

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.paint.Paint`  object is associated with a different document


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(val, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Fill_SetPaint.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_Fill_SetPaint.restype = c_bool
        if not _lib.PtxPdfContent_Fill_SetPaint(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def inside_rule(self) -> InsideRule:
        """

        Returns:
            pdftools_toolbox.pdf.content.inside_rule.InsideRule

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.fill.Fill`  object has already been closed


        """
        from pdftools_toolbox.pdf.content.inside_rule import InsideRule

        _lib.PtxPdfContent_Fill_GetInsideRule.argtypes = [c_void_p]
        _lib.PtxPdfContent_Fill_GetInsideRule.restype = c_int
        ret_val = _lib.PtxPdfContent_Fill_GetInsideRule(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return InsideRule(ret_val)



    @inside_rule.setter
    def inside_rule(self, val: InsideRule) -> None:
        """

        Args:
            val (pdftools_toolbox.pdf.content.inside_rule.InsideRule):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.fill.Fill`  object has already been closed

            OperationError:
                if the document is read-only


        """
        from pdftools_toolbox.pdf.content.inside_rule import InsideRule

        if not isinstance(val, InsideRule):
            raise TypeError(f"Expected type {InsideRule.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Fill_SetInsideRule.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_Fill_SetInsideRule.restype = c_bool
        if not _lib.PtxPdfContent_Fill_SetInsideRule(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Fill._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Fill.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
