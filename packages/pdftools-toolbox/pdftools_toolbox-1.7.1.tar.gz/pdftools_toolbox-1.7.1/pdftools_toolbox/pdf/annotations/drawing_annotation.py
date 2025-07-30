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
import pdftools_toolbox.pdf.annotations.markup_annotation

if TYPE_CHECKING:
    from pdftools_toolbox.pdf.content.paint import Paint
    from pdftools_toolbox.pdf.annotations.popup import Popup

else:
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    Popup = "pdftools_toolbox.pdf.annotations.popup.Popup"


class DrawingAnnotation(pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation):
    """
    A drawing annotation

    An annotation used to draws something on a page.


    """
    @property
    def paint(self) -> Paint:
        """
        The paint for line stroking and for the popup



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt and the annotation's paint cannot be read


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfAnnots_DrawingAnnotation_GetPaint.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_DrawingAnnotation_GetPaint.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_DrawingAnnotation_GetPaint(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)


    @property
    def popup(self) -> Optional[Popup]:
        """
        The pop-up



        Returns:
            Optional[pdftools_toolbox.pdf.annotations.popup.Popup]

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.annotations.popup import Popup

        _lib.PtxPdfAnnots_DrawingAnnotation_GetPopup.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_DrawingAnnotation_GetPopup.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_DrawingAnnotation_GetPopup(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Popup._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        _lib.PtxPdfAnnots_DrawingAnnotation_GetType.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_DrawingAnnotation_GetType.restype = c_int

        obj_type = _lib.PtxPdfAnnots_DrawingAnnotation_GetType(handle)
        # Create and return the object based on the type
        if obj_type == 0:
            return DrawingAnnotation._from_handle(handle)
        elif obj_type == 1:
            from pdftools_toolbox.pdf.annotations.line_annotation import LineAnnotation 
            return LineAnnotation._from_handle(handle)
        elif obj_type == 2:
            from pdftools_toolbox.pdf.annotations.ink_annotation import InkAnnotation 
            return InkAnnotation._from_handle(handle)
        elif obj_type == 3:
            from pdftools_toolbox.pdf.annotations.poly_line_annotation import PolyLineAnnotation 
            return PolyLineAnnotation._from_handle(handle)
        elif obj_type == 4:
            from pdftools_toolbox.pdf.annotations.polygon_annotation import PolygonAnnotation 
            return PolygonAnnotation._from_handle(handle)
        elif obj_type == 5:
            from pdftools_toolbox.pdf.annotations.rectangle_annotation import RectangleAnnotation 
            return RectangleAnnotation._from_handle(handle)
        elif obj_type == 6:
            from pdftools_toolbox.pdf.annotations.ellipse_annotation import EllipseAnnotation 
            return EllipseAnnotation._from_handle(handle)
        else:
            return None


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = DrawingAnnotation.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
