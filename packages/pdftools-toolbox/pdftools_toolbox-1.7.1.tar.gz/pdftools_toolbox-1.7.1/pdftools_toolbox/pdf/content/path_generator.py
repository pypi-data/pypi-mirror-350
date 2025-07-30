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
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.content.path import Path

else:
    Point = "pdftools_toolbox.geometry.real.point.Point"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Path = "pdftools_toolbox.pdf.content.path.Path"


class PathGenerator(_NativeObject):
    """
    """
    def __init__(self, path: Path):
        """
        Create a new path generator for appending to a path.



        Args:
            path (pdftools_toolbox.pdf.content.path.Path): 
                the path object



        """
        from pdftools_toolbox.pdf.content.path import Path

        if not isinstance(path, Path):
            raise TypeError(f"Expected type {Path.__name__}, but got {type(path).__name__}.")

        _lib.PtxPdfContent_PathGenerator_New.argtypes = [c_void_p]
        _lib.PtxPdfContent_PathGenerator_New.restype = c_void_p
        ret_val = _lib.PtxPdfContent_PathGenerator_New(path._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        super()._initialize(ret_val)


    def move_to(self, target: Point) -> None:
        """
        Move the current position.

        Begin a new subpath by moving the current point to the specified coordinates,
        omitting any connecting line segment.
        If the previous path construction operator in the current path was also MoveTo,
        the new MoveTo overrides it;
        no vestige of the previous MoveTo operation remains in the path.



        Args:
            target (pdftools_toolbox.geometry.real.point.Point): 
                the target coordinates




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(target, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(target).__name__}.")

        _lib.PtxPdfContent_PathGenerator_MoveTo.argtypes = [c_void_p, POINTER(Point)]
        _lib.PtxPdfContent_PathGenerator_MoveTo.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_MoveTo(self._handle, target):
            _NativeBase._throw_last_error(False)


    def line_to(self, target: Point) -> None:
        """
        Draw a line.

        Append a straight line segment from the current point to the target coordinates.
        The current position is changed to the target position.



        Args:
            target (pdftools_toolbox.geometry.real.point.Point): 
                the target coordinates




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(target, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(target).__name__}.")

        _lib.PtxPdfContent_PathGenerator_LineTo.argtypes = [c_void_p, POINTER(Point)]
        _lib.PtxPdfContent_PathGenerator_LineTo.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_LineTo(self._handle, target):
            _NativeBase._throw_last_error(False)


    def bezier_to(self, control_point1: Point, control_point2: Point, target: Point) -> None:
        """
        Draw a bezier curve.

         
        Append a cubic Bézier curve to the current path.
        The curve extends from the current point to the `target` position,
        using `controlPoint1` and `controlPoint2` as the Bézier control points.
         
        The current position is changed to the target position.



        Args:
            controlPoint1 (pdftools_toolbox.geometry.real.point.Point): 
                the first bezier control point

            controlPoint2 (pdftools_toolbox.geometry.real.point.Point): 
                the second bezier control point

            target (pdftools_toolbox.geometry.real.point.Point): 
                the target coordinates




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(control_point1, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(control_point1).__name__}.")
        if not isinstance(control_point2, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(control_point2).__name__}.")
        if not isinstance(target, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(target).__name__}.")

        _lib.PtxPdfContent_PathGenerator_BezierTo.argtypes = [c_void_p, POINTER(Point), POINTER(Point), POINTER(Point)]
        _lib.PtxPdfContent_PathGenerator_BezierTo.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_BezierTo(self._handle, control_point1, control_point2, target):
            _NativeBase._throw_last_error(False)


    def close_subpath(self) -> None:
        """
        Close the current subpath.

        Close the current subpath by appending a straight line segment from the
        current point to the starting point of the subpath.
        This operator terminates the current subpath;
        appending another segment to the current path will begin a new subpath,
        even if the new segment begins at the endpoint reached by the closeSubpath() operation.
        If the current subpath has already been closed, CloseSubpath() does nothing.





        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        _lib.PtxPdfContent_PathGenerator_CloseSubpath.argtypes = [c_void_p]
        _lib.PtxPdfContent_PathGenerator_CloseSubpath.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_CloseSubpath(self._handle):
            _NativeBase._throw_last_error(False)


    def add_rectangle(self, rectangle: Rectangle) -> None:
        """
        Append a rectangle to the current path as a complete subpath.



        Args:
            rectangle (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the rectangle to be added to the path




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(rectangle, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(rectangle).__name__}.")

        _lib.PtxPdfContent_PathGenerator_AddRectangle.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfContent_PathGenerator_AddRectangle.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_AddRectangle(self._handle, rectangle):
            _NativeBase._throw_last_error(False)


    def add_circle(self, center: Point, radius: float) -> None:
        """
        Append a circle to the current path as a complete subpath.



        Args:
            center (pdftools_toolbox.geometry.real.point.Point): 
                the center of the circle

            radius (float): 
                the radius of the circle




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.point import Point

        if not isinstance(center, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(center).__name__}.")
        if not isinstance(radius, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(radius).__name__}.")

        _lib.PtxPdfContent_PathGenerator_AddCircle.argtypes = [c_void_p, POINTER(Point), c_double]
        _lib.PtxPdfContent_PathGenerator_AddCircle.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_AddCircle(self._handle, center, radius):
            _NativeBase._throw_last_error(False)


    def add_ellipse(self, rectangle: Rectangle) -> None:
        """
        Add an ellipse to the current path as a complete subpath.



        Args:
            rectangle (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the surrounding rectangle of the ellipse




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(rectangle, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(rectangle).__name__}.")

        _lib.PtxPdfContent_PathGenerator_AddEllipse.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfContent_PathGenerator_AddEllipse.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_AddEllipse(self._handle, rectangle):
            _NativeBase._throw_last_error(False)


    def add_arc(self, rectangle: Rectangle, alpha1: float, alpha2: float) -> None:
        """
        Add an elliptical arc to the current path.



        Args:
            rectangle (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the surrounding rectangle of the ellipse

            alpha1 (float): 
                the angle between the x-axis and the begin of the arc

            alpha2 (float): 
                the angle between the x-axis and the end of the arc




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(rectangle, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(rectangle).__name__}.")
        if not isinstance(alpha1, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(alpha1).__name__}.")
        if not isinstance(alpha2, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(alpha2).__name__}.")

        _lib.PtxPdfContent_PathGenerator_AddArc.argtypes = [c_void_p, POINTER(Rectangle), c_double, c_double]
        _lib.PtxPdfContent_PathGenerator_AddArc.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_AddArc(self._handle, rectangle, alpha1, alpha2):
            _NativeBase._throw_last_error(False)


    def add_pie(self, rectangle: Rectangle, alpha1: float, alpha2: float) -> None:
        """
        Add an elliptical piece of pie to the current path as a complete subpath.



        Args:
            rectangle (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                the surrounding rectangle of the ellipse

            alpha1 (float): 
                the angle between the x-axis and the begin of the arc

            alpha2 (float): 
                the angle between the x-axis and the end of the arc




        Raises:
            StateError:
                if the object has already been closed

            StateError:
                if the path object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        if not isinstance(rectangle, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(rectangle).__name__}.")
        if not isinstance(alpha1, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(alpha1).__name__}.")
        if not isinstance(alpha2, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(alpha2).__name__}.")

        _lib.PtxPdfContent_PathGenerator_AddPie.argtypes = [c_void_p, POINTER(Rectangle), c_double, c_double]
        _lib.PtxPdfContent_PathGenerator_AddPie.restype = c_bool
        if not _lib.PtxPdfContent_PathGenerator_AddPie(self._handle, rectangle, alpha1, alpha2):
            _NativeBase._throw_last_error(False)



    def __exit__(self, exc_type, exc_value, traceback):
        _lib.PtxPdfContent_PathGenerator_Close.argtypes = [c_void_p]
        _lib.PtxPdfContent_PathGenerator_Close.restype = c_bool
        if self._handle is not None:
            try:
                if not _lib.PtxPdfContent_PathGenerator_Close(self._handle):
                    super()._throw_last_error()
            finally:
                self._handle = None  # Invalidate the handle

    def __enter__(self):
        return self

    @staticmethod
    def _create_dynamic_type(handle):
        return PathGenerator._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = PathGenerator.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
