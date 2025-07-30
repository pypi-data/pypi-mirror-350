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

class Quadrilateral(Structure):
    """
    A quadrilateral is a polygon with four sides and four corners.
    When associated with text, the horizontal text writing direction goes from :attr:`pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral.bottom_left`  to :attr:`pdftools_toolbox.geometry.real.quadrilateral.Quadrilateral.bottom_left` .



    Attributes:
        bottom_left (pdftools_toolbox.geometry.real.point.Point):
        bottom_right (pdftools_toolbox.geometry.real.point.Point):
        top_right (pdftools_toolbox.geometry.real.point.Point):
        top_left (pdftools_toolbox.geometry.real.point.Point):

    """
    _fields_ = [
        ("bottom_left", pdftools_toolbox.geometry.real.point.Point),
        ("bottom_right", pdftools_toolbox.geometry.real.point.Point),
        ("top_right", pdftools_toolbox.geometry.real.point.Point),
        ("top_left", pdftools_toolbox.geometry.real.point.Point),
    ]
