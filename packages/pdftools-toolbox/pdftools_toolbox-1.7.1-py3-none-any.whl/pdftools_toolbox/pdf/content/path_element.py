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
import pdftools_toolbox.pdf.content.content_element

if TYPE_CHECKING:
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.content.path import Path
    from pdftools_toolbox.pdf.content.stroke import Stroke
    from pdftools_toolbox.pdf.content.fill import Fill

else:
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Path = "pdftools_toolbox.pdf.content.path.Path"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"
    Fill = "pdftools_toolbox.pdf.content.fill.Fill"


class PathElement(pdftools_toolbox.pdf.content.content_element.ContentElement):
    """
    """
    @property
    def alignment_box(self) -> Rectangle:
        """
        the box for alignment

        This is a rectangle that may not encompass all parts of an element, but is usefull for alignment.



        Returns:
            pdftools_toolbox.geometry.real.rectangle.Rectangle

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.geometry.real.rectangle import Rectangle

        _lib.PtxPdfContent_PathElement_GetAlignmentBox.argtypes = [c_void_p, POINTER(Rectangle)]
        _lib.PtxPdfContent_PathElement_GetAlignmentBox.restype = c_bool
        ret_val = Rectangle()
        if not _lib.PtxPdfContent_PathElement_GetAlignmentBox(self._handle, byref(ret_val)):
            _NativeBase._throw_last_error(False)
        return ret_val


    @property
    def path(self) -> Path:
        """
        This path element's path object.



        Returns:
            pdftools_toolbox.pdf.content.path.Path

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.path import Path

        _lib.PtxPdfContent_PathElement_GetPath.argtypes = [c_void_p]
        _lib.PtxPdfContent_PathElement_GetPath.restype = c_void_p
        ret_val = _lib.PtxPdfContent_PathElement_GetPath(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Path._create_dynamic_type(ret_val)


    @property
    def stroke(self) -> Optional[Stroke]:
        """
        This path element's parameters for stroking the path or `None` if the path is not stroked.



        Returns:
            Optional[pdftools_toolbox.pdf.content.stroke.Stroke]

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.stroke import Stroke

        _lib.PtxPdfContent_PathElement_GetStroke.argtypes = [c_void_p]
        _lib.PtxPdfContent_PathElement_GetStroke.restype = c_void_p
        ret_val = _lib.PtxPdfContent_PathElement_GetStroke(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Stroke._create_dynamic_type(ret_val)


    @property
    def fill(self) -> Optional[Fill]:
        """
        This path element's parameters for filling the path or `None` if the path is not filled.



        Returns:
            Optional[pdftools_toolbox.pdf.content.fill.Fill]

        Raises:
            StateError:
                the object has already been closed


        """
        from pdftools_toolbox.pdf.content.fill import Fill

        _lib.PtxPdfContent_PathElement_GetFill.argtypes = [c_void_p]
        _lib.PtxPdfContent_PathElement_GetFill.restype = c_void_p
        ret_val = _lib.PtxPdfContent_PathElement_GetFill(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Fill._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return PathElement._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = PathElement.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
