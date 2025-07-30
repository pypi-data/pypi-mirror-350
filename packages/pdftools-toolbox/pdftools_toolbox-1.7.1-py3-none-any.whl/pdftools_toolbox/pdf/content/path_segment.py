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
import pdftools_toolbox.internal
import pdftools_toolbox.geometry.real.point

class PathSegment(Structure):
    """

    Attributes:
        end_point (pdftools_toolbox.geometry.real.point.Point):
            The start point of the segment corresponds to the end point of the previous segment.

        segment_type (c_int):
            Defines the type of this path segment.

        control_point1 (pdftools_toolbox.geometry.real.point.Point):
            Only valid if the :attr:`pdftools_toolbox.pdf.content.path_segment.PathSegment.end_point`  is set to :attr:`pdftools_toolbox.pdf.content.path_segment_type.PathSegmentType.CUBIC` 

        control_point2 (pdftools_toolbox.geometry.real.point.Point):
            Only valid if the :attr:`pdftools_toolbox.pdf.content.path_segment.PathSegment.end_point`  is set to :attr:`pdftools_toolbox.pdf.content.path_segment_type.PathSegmentType.CUBIC` 


    """
    _fields_ = [
        ("end_point", pdftools_toolbox.geometry.real.point.Point),
        ("segment_type", c_int),
        ("control_point1", pdftools_toolbox.geometry.real.point.Point),
        ("control_point2", pdftools_toolbox.geometry.real.point.Point),
    ]
