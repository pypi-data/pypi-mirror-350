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
    from pdftools_toolbox.geometry.real.point import Point
    from pdftools_toolbox.pdf.content.paint import Paint
    from pdftools_toolbox.pdf.annotations.popup import Popup

else:
    Document = "pdftools_toolbox.pdf.document.Document"
    Point = "pdftools_toolbox.geometry.real.point.Point"
    Paint = "pdftools_toolbox.pdf.content.paint.Paint"
    Popup = "pdftools_toolbox.pdf.annotations.popup.Popup"


class StickyNote(pdftools_toolbox.pdf.annotations.markup_annotation.MarkupAnnotation):
    """
    A sticky note annotation


    """
    @staticmethod
    def create(target_document: Document, top_left: Point, content: Optional[str], paint: Paint) -> StickyNote:
        """
        Create a sticky note annotation.

        The returned sticky note annotation is not yet part of any page.
        It can be added to a page's list of annotations.



        Args:
            targetDocument (pdftools_toolbox.pdf.document.Document): 
                The output document with which the returned object is associated

            topLeft (pdftools_toolbox.geometry.real.point.Point): 
                The location of the annotation's upper left corner on the page

            content (Optional[str]): 
                The text content

            paint (pdftools_toolbox.pdf.content.paint.Paint): 
                The paint for the sticky note icon.



        Returns:
            pdftools_toolbox.pdf.annotations.sticky_note.StickyNote: 
                The newly created sticky note annotation



        Raises:
            ValueError:
                if the `targetDocument` has already been closed

            ValueError:
                if the `targetDocument` is read-only

            ValueError:
                if the color space of the `paint` argument is not a device color space

            ValueError:
                if the `paint` has a non-`None`:attr:`pdftools_toolbox.pdf.content.paint.Paint.transparency`  with :attr:`pdftools_toolbox.pdf.content.transparency.Transparency.blend_mode`  other than :attr:`pdftools_toolbox.pdf.content.blend_mode.BlendMode.NORMAL` 

            ValueError:
                if the `paint` argument is not associated with the `targetDocument`


        """
        from pdftools_toolbox.pdf.document import Document
        from pdftools_toolbox.geometry.real.point import Point
        from pdftools_toolbox.pdf.content.paint import Paint

        if not isinstance(target_document, Document):
            raise TypeError(f"Expected type {Document.__name__}, but got {type(target_document).__name__}.")
        if not isinstance(top_left, Point):
            raise TypeError(f"Expected type {Point.__name__}, but got {type(top_left).__name__}.")
        if content is not None and not isinstance(content, str):
            raise TypeError(f"Expected type {str.__name__} or None, but got {type(content).__name__}.")
        if not isinstance(paint, Paint):
            raise TypeError(f"Expected type {Paint.__name__}, but got {type(paint).__name__}.")

        _lib.PtxPdfAnnots_StickyNote_CreateW.argtypes = [c_void_p, POINTER(Point), c_wchar_p, c_void_p]
        _lib.PtxPdfAnnots_StickyNote_CreateW.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_StickyNote_CreateW(target_document._handle, top_left, _string_to_utf16(content), paint._handle)
        if ret_val is None:
            _NativeBase._throw_last_error(False)
        return StickyNote._create_dynamic_type(ret_val)



    @property
    def paint(self) -> Paint:
        """
        The paint for the icon and the popup



        Returns:
            pdftools_toolbox.pdf.content.paint.Paint

        Raises:
            StateError:
                if the object has already been closed

            pdftools_toolbox.corrupt_error.CorruptError:
                if the PDF is corrupt and the annotation's paint cannot be read


        """
        from pdftools_toolbox.pdf.content.paint import Paint

        _lib.PtxPdfAnnots_StickyNote_GetPaint.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_StickyNote_GetPaint.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_StickyNote_GetPaint(self._handle)
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

        _lib.PtxPdfAnnots_StickyNote_GetPopup.argtypes = [c_void_p]
        _lib.PtxPdfAnnots_StickyNote_GetPopup.restype = c_void_p
        ret_val = _lib.PtxPdfAnnots_StickyNote_GetPopup(self._handle)
        if ret_val is None:
            _NativeBase._throw_last_error()
            return None
        return Popup._create_dynamic_type(ret_val)



    @staticmethod
    def _create_dynamic_type(handle):
        return StickyNote._from_handle(handle)


    @classmethod
    def _from_handle(cls, handle):
        """
        Internal factory method for constructing an instance using an internal handle.
        This method creates an instance of the class by bypassing the public constructor.
        """
        instance = StickyNote.__new__(cls)  # Bypass __init__
        instance._initialize(handle)
        return instance

    def _initialize(self, handle):
        super()._initialize(handle)
