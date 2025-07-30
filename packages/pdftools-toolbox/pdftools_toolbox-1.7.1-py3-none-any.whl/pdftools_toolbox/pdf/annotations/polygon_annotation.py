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
    from pdftools_toolbox.pdf.content.path import Path
    from pdftools_toolbox.pdf.content.stroke import Stroke
    from pdftools_toolbox.pdf.content.paint import Paint

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Path = "pdftools_toolbox.pdf.content.path.Path"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"


class PolygonAnnotation(pdftools_toolbox.pdf.annotations.drawing_annotation.DrawingAnnotation):
    """
    A polygon annotation


    """
    @staticmethod
    def create(target_document: Document, path: Path, stroke: Optional[Stroke], fill: Optional[Paint]) -> PolygonAnnotation:
        """
        Create a polygon annotation.

        The returned polygon annotation is not yet part of any page.
        It can be added to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated.

            path (pdftools_toolbox.pdf.content.path.Path): 
                The path of the polygon.

            stroke (Optional[pdftools_toolbox.pdf.content.stroke.Stroke]): 
                The stroking parameters used for stroking the polygon.
                The stroking paint is used as the annotation's main paint.
                If `None` then the polygon is not filled.

            fill (Optional[pdftools_toolbox.pdf.content.paint.Paint]): 
                The paint used for filling the polygon.
                If `None` then the polygon is not filled.



        Returns:
            pdftools_toolbox.pdf.annotations.polygon_annotation.PolygonAnnotation: 
                The newly created polygon annotation.



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `path` argument has not been constructed with a :class:`pdftools_toolbox.pdf.content.path_generator.PathGenerator` 

            ValueError:
                if the `targetDocument`'s conformance is not PDF 2.0 and the `path` argument contains curve-to operations

            ValueError:
                if the `path` argument contains close-subpath or rectangle operations

            pdftools_toolbox.unsupported_feature_error.UnsupportedFeatureError:
                if the `targetDocument`'s conformance is PDF 2.0 and the `path` argument contains curve-to operations

            ValueError:
                if the `stroke` and `fill` arguments are both `None`

            ValueError:
                if the `stroke` argument is not associated with `targetDocument`

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

            ValueError:
                if the `fill` has a :attr:`pdftools_toolbox.pdf.content.paint.Paint.color_space`  other than a device color space

            ValueError:
                if the `fill` has a non-`None`:attr:`pdftools_toolbox.pdf.content.paint.Paint.transparency`  with :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 

            ValueError:
                if the `fill` argument is not associated with the `targetDocument`

            pdftools_toolbox.conformance_error.ConformanceError:
                if the explicitly requested PDF conformance is smaller than PDF 1.5


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.pdf.content.path import Path
        from pdftools_toolbox.pdf.content.stroke import Stroke
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(path, Path):
            raise TypeError(f"Expected type {Path.__name__}, but got {type(path).__name__}.")
        if stroke is not None and not isinstance(stroke, Stroke):
            raise TypeError(f"Expected type {Stroke.__name__} or None, but got {type(stroke).__name__}.")
        if fill is not None and not isinstance(fill, Paint):
            raise TypeError(f"Expected type {Paint.__name__} or None, but got {type(fill).__name__}.")

        _lib.PtxPdfAnnots_PolygonAnnotation_Create.argtypes = [c_void_p, c_void_p, c_void_p, c_void_p]
        _lib.PtxPdfAnnots_PolygonAnnotation_Create.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_PolygonAnnotation_Create(target_document._handle, path._handle, stroke._handle if stroke is not None else None, fill._handle if fill is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return PolygonAnnotation._create_dynamic_type(ret_val)



    @property
    def fill(self) -> Paint:
        """
        The filling paint



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfAnnots_PolygonAnnotation_GetFill.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_PolygonAnnotation_GetFill.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_PolygonAnnotation_GetFill(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return PolygonAnnotation._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = PolygonAnnotation.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
