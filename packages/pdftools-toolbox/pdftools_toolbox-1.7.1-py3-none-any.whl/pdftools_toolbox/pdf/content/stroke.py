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
    from pdftools_toolbox.pdf.content.line_cap_style import LineCapStyle
    from pdftools_toolbox.pdf.content.line_join_style import LineJoinStyle

else:
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    LineCapStyle = "pdftools_toolbox.pdf.content.line_cap_style.LineCapStyle"
    LineJoinStyle = "pdftools_toolbox.pdf.content.line_join_style.LineJoinStyle"


class Stroke(_NativeObject):
    """
    """
    def __init__(self, paint: Paint, line_width: float):
        """

        Args:
            paint (pdftools_toolbox.pdf.content.paint.Paint): 
            lineWidth (float): 


        Raises:
            ValueError:
                if the document associated with the `paint` argument has already been closed


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(paint, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(paint).__name__}.")
        if not isinstance(line_width, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(line_width).__name__}.")

        _lib.PtxPdfContent_Stroke_New.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_Stroke_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Stroke_New(paint._handle, line_width)
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
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfContent_Stroke_GetPaint.argtypes = [c_void_p]
        _lib.PtxPdfContent_Stroke_GetPaint.restype = c_void_p
        ret_val = _lib.PtxPdfContent_Stroke_GetPaint(self._handle)
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
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.paint.Paint`  object has already been closed

            ValueError:
                if the given :class:`pdftools_toolbox.pdf.content.paint.Paint`  object is associated with a different document


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(val, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Stroke_SetPaint.argtypes = [c_void_p, c_void_p]
        _lib.PtxPdfContent_Stroke_SetPaint.restype = c_bool
        if not _lib.PtxPdfContent_Stroke_SetPaint(self._handle, val._handle):
            _NativeBase._throw_last_error(False)

    @property
    def line_width(self) -> float:
        """

        Returns:
            float

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed


        """
        _lib.PtxPdfContent_Stroke_GetLineWidth.argtypes = [c_void_p]
        _lib.PtxPdfContent_Stroke_GetLineWidth.restype = c_double
        ret_val = _lib.PtxPdfContent_Stroke_GetLineWidth(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @line_width.setter
    def line_width(self, val: float) -> None:
        """

        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Stroke_SetLineWidth.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_Stroke_SetLineWidth.restype = c_bool
        if not _lib.PtxPdfContent_Stroke_SetLineWidth(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def line_cap_style(self) -> LineCapStyle:
        """

        Returns:
            pdftools_toolbox.pdf.content.line_cap_style.LineCapStyle

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed


        """
        from pdftools_toolbox.pdf.content.line_cap_style import LineCapStyle

        _lib.PtxPdfContent_Stroke_GetLineCapStyle.argtypes = [c_void_p]
        _lib.PtxPdfContent_Stroke_GetLineCapStyle.restype = c_int
        ret_val = _lib.PtxPdfContent_Stroke_GetLineCapStyle(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return LineCapStyle(ret_val)



    @line_cap_style.setter
    def line_cap_style(self, val: LineCapStyle) -> None:
        """

        Args:
            val (pdftools_toolbox.pdf.content.line_cap_style.LineCapStyle):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            OperationError:
                if the document is read-only


        """
        from pdftools_toolbox.pdf.content.line_cap_style import LineCapStyle

        if not isinstance(val, LineCapStyle):
            raise TypeError(f"Expected type {LineCapStyle.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Stroke_SetLineCapStyle.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_Stroke_SetLineCapStyle.restype = c_bool
        if not _lib.PtxPdfContent_Stroke_SetLineCapStyle(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def line_join_style(self) -> LineJoinStyle:
        """

        Returns:
            pdftools_toolbox.pdf.content.line_join_style.LineJoinStyle

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed


        """
        from pdftools_toolbox.pdf.content.line_join_style import LineJoinStyle

        _lib.PtxPdfContent_Stroke_GetLineJoinStyle.argtypes = [c_void_p]
        _lib.PtxPdfContent_Stroke_GetLineJoinStyle.restype = c_int
        ret_val = _lib.PtxPdfContent_Stroke_GetLineJoinStyle(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return LineJoinStyle(ret_val)



    @line_join_style.setter
    def line_join_style(self, val: LineJoinStyle) -> None:
        """

        Args:
            val (pdftools_toolbox.pdf.content.line_join_style.LineJoinStyle):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            OperationError:
                if the document is read-only


        """
        from pdftools_toolbox.pdf.content.line_join_style import LineJoinStyle

        if not isinstance(val, LineJoinStyle):
            raise TypeError(f"Expected type {LineJoinStyle.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Stroke_SetLineJoinStyle.argtypes = [c_void_p, c_int]
        _lib.PtxPdfContent_Stroke_SetLineJoinStyle.restype = c_bool
        if not _lib.PtxPdfContent_Stroke_SetLineJoinStyle(self._handle, c_int(val.value)):
            _NativeBase._throw_last_error(False)

    @property
    def dash_array(self) -> List[float]:
        """

        Returns:
            List[float]

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed


        """
        _lib.PtxPdfContent_Stroke_GetDashArray.argtypes = [c_void_p, POINTER(c_double), c_size_t]
        _lib.PtxPdfContent_Stroke_GetDashArray.restype = c_size_t
        ret_val_size = _lib.PtxPdfContent_Stroke_GetDashArray(self._handle, None, 0)
        if ret_val_size == -1:
            _NativeBase._throw_last_error(False)
        ret_val = (c_double * ret_val_size)()
        _lib.PtxPdfContent_Stroke_GetDashArray(self._handle, ret_val, c_size_t(ret_val_size))
        return list(ret_val)


    @dash_array.setter
    def dash_array(self, val: List[float]) -> None:
        """

        Args:
            val (List[float]):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, list):
            raise TypeError(f"Expected type {list.__name__}, but got {type(val).__name__}.")
        if not all(isinstance(c, Number) for c in val):
            raise TypeError(f"All elements in {val} must be {Number}")
        _lib.PtxPdfContent_Stroke_SetDashArray.argtypes = [c_void_p, POINTER(c_double), c_size_t]
        _lib.PtxPdfContent_Stroke_SetDashArray.restype = c_bool
        if not _lib.PtxPdfContent_Stroke_SetDashArray(self._handle, (c_double * len(val))(*val), len(val)):
            _NativeBase._throw_last_error(False)

    @property
    def dash_phase(self) -> float:
        """

        Returns:
            float

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed


        """
        _lib.PtxPdfContent_Stroke_GetDashPhase.argtypes = [c_void_p]
        _lib.PtxPdfContent_Stroke_GetDashPhase.restype = c_double
        ret_val = _lib.PtxPdfContent_Stroke_GetDashPhase(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @dash_phase.setter
    def dash_phase(self, val: float) -> None:
        """

        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Stroke_SetDashPhase.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_Stroke_SetDashPhase.restype = c_bool
        if not _lib.PtxPdfContent_Stroke_SetDashPhase(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def miter_limit(self) -> float:
        """

        Returns:
            float

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed


        """
        _lib.PtxPdfContent_Stroke_GetMiterLimit.argtypes = [c_void_p]
        _lib.PtxPdfContent_Stroke_GetMiterLimit.restype = c_double
        ret_val = _lib.PtxPdfContent_Stroke_GetMiterLimit(self._handle)
        if ret_val == -1.0:
            _NativeBase._throw_last_error()
        return ret_val



    @miter_limit.setter
    def miter_limit(self, val: float) -> None:
        """

        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the document associated with the :class:`pdftools_toolbox.pdf.content.stroke.Stroke`  object has already been closed

            OperationError:
                if the document is read-only


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfContent_Stroke_SetMiterLimit.argtypes = [c_void_p, c_double]
        _lib.PtxPdfContent_Stroke_SetMiterLimit.restype = c_bool
        if not _lib.PtxPdfContent_Stroke_SetMiterLimit(self._handle, val):
            _NativeBase._throw_last_error(False)


    @staticmethod
    def _create_dynamic_type(handle):
        return Stroke._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = Stroke.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
