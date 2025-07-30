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
import pdftools_toolbox.pdf.annotations.drawing_annotation

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.point import Point
    from pdftools_toolbox.pdf.content.stroke import Stroke
    from pdftools_toolbox.pdf.annotations.line_ending import LineEnding
    from pdftools_toolbox.pdf.content.paint import Paint

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Point = "pdftools_toolbox.geometry.real.point.Point"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"
    LineEnding = "pdftools_toolbox.pdf.annotations.line_ending.LineEnding"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"


class LineAnnotation(pdftools_toolbox.pdf.annotations.drawing_annotation.DrawingAnnotation):
    """
    A line annotation

    An annotation that draws a line on a page.


    """
    @staticmethod
    def create(target_document: Document, start: Point, end: Point, stroke: Stroke) -> Optional[LineAnnotation]:
        """
        Create a line annotation.

        The returned line annotation is not yet part of any page.
        It can be added to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated.

            start (pdftools_toolbox.geometry.real.point.Point): 
                The line's start point.

            end (pdftools_toolbox.geometry.real.point.Point): 
                The line's end point.

            stroke (pdftools_toolbox.pdf.content.stroke.Stroke): 
                The stroking parameters used for stroking the line.
                The stroking paint is used as the annotation's main paint.



        Returns:
            Optional[pdftools_toolbox.pdf.annotations.line_annotation.LineAnnotation]: 
                The newly created line annotation.



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `stroke` argument is not associated with the `targetDocument`

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  has a :attr:`pdftools_toolbox.pdf.content.paint.Paint.color_space`  other than a device color space

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  has a non-`None`:attr:`pdftools_toolbox.pdf.content.paint.Paint.transparency`  with :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 

            ValueError:
                if the `stroke` argument's :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.line_cap_style`  is other than :attr:`pdftools_toolbox.pdf.content.line_cap_style.LineCapStyle.BUTT` 

            ValueError:
                if the `stroke` argument's :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.line_join_style`  is other than :attr:`pdftools_toolbox.pdf.content.line_join_style.LineJoinStyle.MITER` 

            ValueError:
                if the `stroke` argument's :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.miter_limit`  is other than 10

            ValueError:
                if the `stroke` argument's :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.dash_phase`  is other than 0


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.point import Point
        from pdftools_toolbox.pdf.content.stroke import Stroke

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(start, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(start).__name__}.")
        if not isinstance(end, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(end).__name__}.")
        if not isinstance(stroke, Stroke):
            raise TypeError(f"Expected type {Stroke.__name__}, but got {type(stroke).__name__}.")

        _lib.PtxPdfAnnots_LineAnnotation_Create.argtypes = [c_void_p, POINTER(Point), POINTER(Point), c_void_p]
        _lib.PtxPdfAnnots_LineAnnotation_Create.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_LineAnnotation_Create(target_document._handle, start, end, stroke._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return LineAnnotation._create_dynamic_type(ret_val)



    @property
    def start(self) -> Point:
        """
        The line's starting point



        Returns:
            pdftools_toolbox.geometry.real.point.Point

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        _lib.PtxPdfAnnots_LineAnnotation_GetStart.argtypes = [c_void_p, POINTER(Point)]
        _lib.PtxPdfAnnots_LineAnnotation_GetStart.restype = c_bool
        ret_val = Point()
        if not _lib.PtxPdfAnnots_LineAnnotation_GetStart(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def end(self) -> Point:
        """
        The line's ending point



        Returns:
            pdftools_toolbox.geometry.real.point.Point

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        _lib.PtxPdfAnnots_LineAnnotation_GetEnd.argtypes = [c_void_p, POINTER(Point)]
        _lib.PtxPdfAnnots_LineAnnotation_GetEnd.restype = c_bool
        ret_val = Point()
        if not _lib.PtxPdfAnnots_LineAnnotation_GetEnd(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def start_style(self) -> LineEnding:
        """
        The starting point's style



        Returns:
            pdftools_toolbox.pdf.annotations.line_ending.LineEnding

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.annotations.line_ending import LineEnding

        _lib.PtxPdfAnnots_LineAnnotation_GetStartStyle.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_LineAnnotation_GetStartStyle.restype = c_int
        ret_val = _lib.PtxPdfAnnots_LineAnnotation_GetStartStyle(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return LineEnding(ret_val)



    @property
    def end_style(self) -> LineEnding:
        """
        The ending point's style



        Returns:
            pdftools_toolbox.pdf.annotations.line_ending.LineEnding

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.annotations.line_ending import LineEnding

        _lib.PtxPdfAnnots_LineAnnotation_GetEndStyle.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_LineAnnotation_GetEndStyle.restype = c_int
        ret_val = _lib.PtxPdfAnnots_LineAnnotation_GetEndStyle(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return LineEnding(ret_val)



    @property
    def line_ending_fill(self) -> Paint:
        """
        The line ending filling paint

        This paint applies to both the starting end the ending point.



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfAnnots_LineAnnotation_GetLineEndingFill.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_LineAnnotation_GetLineEndingFill.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_LineAnnotation_GetLineEndingFill(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return LineAnnotation._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = LineAnnotation.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
