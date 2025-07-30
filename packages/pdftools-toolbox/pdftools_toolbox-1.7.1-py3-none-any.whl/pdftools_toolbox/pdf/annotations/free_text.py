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
    from pdftools_toolbox.pdf.document import Document
    from pdftools_toolbox.geometry.real.rectangle import Rectangle
    from pdftools_toolbox.pdf.content.paint import Paint
    from pdftools_toolbox.pdf.content.stroke import Stroke
    from pdftools_toolbox.geometry.horizontal_alignment import HorizontalAlignment

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Rectangle = "pdftools_toolbox.geometry.real.rectangle.Rectangle"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    Stroke = "pdftools_toolbox.pdf.content.stroke.Stroke"
    HorizontalAlignment = "pdftools_toolbox.geometry.horizontal_alignment.HorizontalAlignment"


class FreeText(pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation):
    """
    An annotation that displays text

    For a free-text annotation, the annotation's content is used as text to be displayed as the annotation's visual manifestation on the page.


    """
    @staticmethod
    def create(target_document: Document, bounding_box: Rectangle, content: Optional[str], paint: Optional[Paint], stroke: Optional[Stroke] = None) -> FreeText:
        """
        Create a free-text annotation.

        The returned free-text annotation is not yet part of any page.
        It can be added to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated.

            boundingBox (pdftools_toolbox.geometry.real.rectangle.Rectangle): 
                The location on the page.

            content (Optional[str]): 
                The text content.

            paint (Optional[pdftools_toolbox.pdf.content.paint.Paint]): 
                This paint used for the background of the free text annotation.
                If `None`, the background is transparent.

            stroke (Optional[pdftools_toolbox.pdf.content.stroke.Stroke]): 
                The stroking parameters used for stroking the rectangle.
                The stroking paint is used as the annotation's main paint.



        Returns:
            pdftools_toolbox.pdf.annotations.free_text.FreeText: 
                The newly created free text annotation.



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the `paint` has a :attr:`pdftools_toolbox.pdf.content.paint.Paint.color_space`  other than a device color space

            ValueError:
                if the `paint` has a non-`None`:attr:`pdftools_toolbox.pdf.content.paint.Paint.transparency`  with :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 

            ValueError:
                if the `paint` argument is not associated with the `targetDocument`

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  has a :attr:`pdftools_toolbox.pdf.content.paint.Paint.color_space`  other than a device color space

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.paint`  has a non-`None`:attr:`pdftools_toolbox.pdf.content.paint.Paint.transparency`  with :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.line_cap_style`  is other than :attr:`pdftools_toolbox.pdf.content.line_cap_style.LineCapStyle.BUTT` 

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.line_join_style`  is other than :attr:`pdftools_toolbox.pdf.content.line_join_style.LineJoinStyle.MITER` 

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.miter_limit`  is other than 10

            ValueError:
                if the `stroke`'s :attr:`pdftools_toolbox.pdf.content.stroke.Stroke.dash_phase`  is other than 0


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.rectangle import Rectangle
        from pdftools_toolbox.pdf.content.paint import Paint
        from pdftools_toolbox.pdf.content.stroke import Stroke

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(bounding_box, Rectangle):
            raise TypeError(f"Expected type {Rectangle.__name__}, but got {type(bounding_box).__name__}.")
        if content is not None and not isinstance(content, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(content).__name__}.")
        if paint is not None and not isinstance(paint, Paint):
            raise TypeError(f"Expected type {Paint.__name__} or None, but got {type(paint).__name__}.")
        if stroke is not None and not isinstance(stroke, Stroke):
            raise TypeError(f"Expected type {Stroke.__name__} or None, but got {type(stroke).__name__}.")

        _lib.PtxPdfAnnots_FreeText_CreateW.argtypes = [c_void_p, POINTER(Rectangle), c_wchar_p, c_void_p, c_void_p]
        _lib.PtxPdfAnnots_FreeText_CreateW.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_FreeText_CreateW(target_document._handle, bounding_box, _string_to_utf16(content), paint._handle if paint is not None else None, stroke._handle if stroke is not None else None)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return FreeText._create_dynamic_type(ret_val)



    @property
    def font_size(self) -> float:
        """
        The font size

         
        Default value: 12.
         
        Note: the font size has no effect when rich text is used



        Returns:
            float

        Raises:
            StateError:
                if the object has already been closed


        """
        _lib.PtxPdfAnnots_FreeText_GetFontSize.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_FreeText_GetFontSize.restype = c_double
        ret_val = _lib.PtxPdfAnnots_FreeText_GetFontSize(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return ret_val



    @font_size.setter
    def font_size(self, val: float) -> None:
        """
        The font size

         
        Default value: 12.
         
        Note: the font size has no effect when rich text is used



        Args:
            val (float):
                property value

        Raises:
            StateError:
                if the object has already been closed

            OperationError:
                if the document is read-only

            ValueError:
                if the given value is smaller than *0.0*


        """
        if not isinstance(val, Number):
            raise TypeError(f"Expected type {Number.__name__}, but got {type(val).__name__}.")
        _lib.PtxPdfAnnots_FreeText_SetFontSize.argtypes = [c_void_p, c_double]
        _lib.PtxPdfAnnots_FreeText_SetFontSize.restype = c_bool
        if not _lib.PtxPdfAnnots_FreeText_SetFontSize(self._handle, val):
            _NativeBase._throw_last_error(False)

    @property
    def alignment(self) -> HorizontalAlignment:
        """
        The text alignment



        Returns:
            pdftools_toolbox.geometry.horizontal_alignment.HorizontalAlignment

        Raises:
            StateError:
                if the object has already been closed


        """
        from pdftools_toolbox.geometry.horizontal_alignment import HorizontalAlignment

        _lib.PtxPdfAnnots_FreeText_GetAlignment.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_FreeText_GetAlignment.restype = c_int
        ret_val = _lib.PtxPdfAnnots_FreeText_GetAlignment(self._handle)
        if ret_val == 0:
            _NativeBase._throw_last_error()
        return HorizontalAlignment(ret_val)



    @property
    def paint(self) -> Paint:
        """
        The paint for the text background and the popup



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt and the annotation's paint cannot be read


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfAnnots_FreeText_GetPaint.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_FreeText_GetPaint.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_FreeText_GetPaint(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return Paint._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return FreeText._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = FreeText.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
